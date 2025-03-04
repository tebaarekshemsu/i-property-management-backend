from fastapi import APIRouter
from app.services.super_admin import dashboard_service, admin_service,admin_update_service

router = APIRouter(prefix='/super_admin', tags=['super_admin'])

@router.get('/dashboard')
def dashboard():
    return dashboard_service.get_dashboard_data()

@router.get('/dashboard/area')
def get_all_area():
    return dashboard_service.get_all_location()

@router.get('/admins')
def get_all_admins():
    return admin_service.get_all_admins()

@router.post('/admin')
def add_admin(admin_data: dict):
    return admin_service.add_admin(admin_data)

@router.post('/admin/area-delete')
def delete_admin_location(admin_data: dict):
    admin_id = admin_data.get("admin_id")
    area_code = admin_data.get("area_code")

    if not admin_id or not area_code:
        return {"error": "Missing admin_id or area_code"}

    return admin_update_service.delete_admin_location(admin_id, area_code)


@router.delete('/admin/{admin_id}')
def delete_admin(admin_id: int):
    return admin_service.delete_admin(admin_id)

