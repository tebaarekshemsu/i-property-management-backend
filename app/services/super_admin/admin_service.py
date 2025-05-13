from app.models import Admin ,AdminLocation
from app.database import SessionLocal

def get_all_admins():
    db = SessionLocal()
    try:
        return db.query(Admin).all()
    finally:
        db.close()

def add_admin(admin_data):
    db = SessionLocal()
    try:
        area_codes = admin_data.pop("area_codes", []) 
        new_admin = Admin(**admin_data)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f'Admin added successfully with ID: {new_admin.admin_id}') 
        for x in area_codes:
            new_admin_location=AdminLocation(admin_id=new_admin.admin_id,area_code=x)
            db.add(new_admin_location)
        db.commit()

        return {"message": "Admin added successfully with the area code"}
    finally:
        db.close()

def delete_admin(admin_id):
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
        if not admin:
            return {"error": "Admin not found"}
        
        db.delete(admin)
        db.commit()
        return {"message": "Admin deleted successfully"}
    finally:
        db.close()