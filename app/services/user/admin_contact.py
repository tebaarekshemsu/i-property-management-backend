from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from app.models import Area,AdminLocation,Admin

from app.database import SessionLocal


def search_admins_by_area_name(
    area_name: str = Query(..., description="Area name to search for"),
    db= SessionLocal()
):
    
    print(area_name)
    # Find areas matching the search term
    areas = db.query(Area).filter(
        func.lower(Area.name).contains(func.lower(area_name))
    ).all()
    
    if not areas:
        return {"admins": []}
    
    area_codes = [area.code for area in areas]
    
    # Find all admin_ids that are assigned to these areas
    admin_ids = db.query(AdminLocation.admin_id).filter(
        AdminLocation.area_code.in_(area_codes)
    ).distinct().all()
    
    # Extract the admin_ids from the result
    admin_ids = [admin_id[0] for admin_id in admin_ids]
    
    if not admin_ids:
        return {"admins": []}
    
    # Get admin details
    admins_query = db.query(Admin).filter(Admin.admin_id.in_(admin_ids)).all()
    
    # For each admin, get all their areas
    result_admins = []
    for admin in admins_query:
        # Get all area codes for this admin
        admin_area_codes = db.query(AdminLocation.area_code).filter(
            AdminLocation.admin_id == admin.admin_id
        ).all()
        admin_area_codes = [code[0] for code in admin_area_codes]
        
        # Get area names
        area_names = db.query(Area.name).filter(
            Area.code.in_(admin_area_codes)
        ).all()
        area_names = [name[0] for name in area_names]
        
        # Create admin response with areas
        admin_response = {
            "admin_id": admin.admin_id,
            "name": admin.name,
            "phone_no": admin.phone_no,
            "admin_type": admin.admin_type,
            "areas": area_names
        }
        result_admins.append(admin_response)
    
    return {"admins": result_admins}

