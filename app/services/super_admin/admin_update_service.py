from app.models import AdminLocation
from app.database import SessionLocal


def delete_admin_location(admin_id,area_code):
    db = SessionLocal()
    try:
        area = db.query(AdminLocation).filter(AdminLocation.admin_id == admin_id,AdminLocation.area_code == area_code).first()
        if not area:
            return {"error": "area not found"}
        
        db.delete(area)
        db.commit()
        return {"message": "area deleted successfully"}
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
