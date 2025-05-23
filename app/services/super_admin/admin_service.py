from app.models import Admin, AdminLocation, Area
from app.database import SessionLocal
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.utils.password import hash_password
import os
import shutil
from uuid import uuid4



UPLOAD_DIR = "uploads/admin_ids"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def add_admin(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_no: str = Form(...),
    password: str = Form(...),
    invitation_code: str = Form(...),
    admin_type: str = Form("admin"),
    area_codes: str = Form(""),  # comma-separated string
    id_front: UploadFile = File(None),
    id_back: UploadFile = File(None),
):
    db = SessionLocal()
    try:
        # Save uploaded ID images
        def save_file(file: UploadFile):
            if file:
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid4()}{ext}"
                file_path = os.path.join(UPLOAD_DIR, filename)
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(file.file, f)
                return filename
            return "default_front.jpg" if file is id_front else "default_back.jpg"

        id_front_filename = save_file(id_front)
        id_back_filename = save_file(id_back)

        area_code_list = [code.strip() for code in area_codes.split(",") if code.strip().isdigit()]

        # Check duplicate phone number
        if db.query(Admin).filter(Admin.phone_no == phone_no).first():
            return JSONResponse(status_code=409, content={"error": "Admin with this phone number already exists."})

        # Hash the password before storing
        hashed_password = hash_password(password)

        new_admin = Admin(
            name=f"{first_name} {last_name}",  # Combine first and last name
            phone_no=phone_no,
            password=hashed_password,  # Use hashed password
            invitation_code=invitation_code,
            admin_type=admin_type,
            id_front=id_front_filename,
            id_back=id_back_filename
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        # Add AdminLocation entries
        for area_code in area_code_list:
            area_code_int = int(area_code)
            if not db.query(Area).filter(Area.code == area_code_int).first():
                db.rollback()
                return JSONResponse(status_code=404, content={"error": f"Area code {area_code} not found."})
            db.add(AdminLocation(admin_id=new_admin.admin_id, area_code=area_code_int))
        db.commit()

        return {"message": "Admin added successfully with area codes."}
    except Exception as e:
        db.rollback()
        print(f"Error in add_admin: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        db.close()

def get_all_admins():
    db = SessionLocal()
    try:
        admins_data = []
        admins = db.query(Admin).all() # Fetch all Admin objects
        for admin in admins:
            # For each admin, query their associated locations via AdminLocation table
            # and then get the names from the Area table.
            admin_locations = db.query(AdminLocation).filter(AdminLocation.admin_id == admin.admin_id).all()
            area_names = []
            for al in admin_locations:
                area = db.query(Area).filter(Area.code == al.area_code).first()
                if area:
                    area_names.append(area.name) # Collect the name of the area

            admins_data.append({
                "admin_id": admin.admin_id,
                "name": admin.name,
                "phone_no": admin.phone_no, # Ensure 'phone_no' is returned as per frontend expectation
                "area_codes": area_names, # Send the list of area names
            })
        return admins_data
    finally:
        db.close()


def delete_admin(admin_id):
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
        if not admin:
            return {"error": "Admin not found"}, 404 # HTTP 404 Not Found

        # Due to ForeignKey(..., ondelete="CASCADE") in AdminLocation,
        # related AdminLocation entries will be automatically deleted.
        db.delete(admin)
        db.commit()
        return {"message": "Admin deleted successfully"}, 200 # HTTP 200 OK
    except Exception as e:
        db.rollback()
        print(f"Error deleting admin: {e}")
        return {"error": f"Failed to delete admin: {str(e)}"}, 500
    finally:
        db.close()

# Handler for fetching all locations (areas)
def get_all_locations():
    db = SessionLocal()
    try:
        locations = db.query(Area).all()
        # Convert Area objects to dictionary for JSON serialization
        return [{"area_code": loc.code, "name": loc.name} for loc in locations]
    finally:
        db.close()
