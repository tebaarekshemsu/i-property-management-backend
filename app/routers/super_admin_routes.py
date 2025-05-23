from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse # Import JSONResponse
from app.services.super_admin import dashboard_service, admin_service

router = APIRouter(prefix='/super_admin', tags=['super_admin'])


@router.get('/location')
def get_all_area():
    """
    Get all areas.
    """
    # Assuming dashboard_service.get_all_location() directly returns a list of dictionaries
    # or handles the (response, status) tuple internally.
    # If it returns (response_dict, status_code), you'll need to adjust.
    locations = admin_service.get_all_locations()
    return JSONResponse(content=locations, status_code=status.HTTP_200_OK)


@router.get('/get_admins')
def get_all_admins():
    """
    Get all admins.
    """
    # admin_service.get_all_admins() should call the handler's get_all_admins()
    # which now returns a list of dicts directly (as adjusted in the handler).
    admins = admin_service.get_all_admins()
    return JSONResponse(content=admins, status_code=status.HTTP_200_OK)


@router.post("/add_admin")
async def add_admin(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_no: str = Form(...),
    password: str = Form(...),
    invitation_code: str = Form(...),
    admin_type: str = Form("admin"),
    area_codes: str = Form("[]"),
    id_front: Optional[UploadFile] = File(None),
    id_back: Optional[UploadFile] = File(None),
):
    """
    Add a new admin with optional ID images.
    """
    try:
        # Combine first and last name
        name = f"{first_name} {last_name}"
        
        response = await admin_service.add_admin(
            name=name,  # Pass the combined name
            phone_no=phone_no,
            password=password,
            invitation_code=invitation_code,
            admin_type=admin_type,
            area_codes=area_codes,
            id_front=id_front,
            id_back=id_back
        )
        return response

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Unexpected error in route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")



@router.post('/delete-admin-location') # Renamed to be more specific
def delete_admin_location(admin_data: dict):
    """
    Delete an admin's location assignment.
    """
    admin_id = admin_data.get("admin_id")
    area_code = admin_data.get("area_code")

    if not admin_id or not area_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing admin_id or area_code")

    # Assuming admin_update_service.delete_admin_location also returns (response_dict, status_code)
    response_content, status_code = admin_update_service.delete_admin_location(admin_id, area_code)

    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=response_content.get("error", "Failed to delete admin location"))

    return JSONResponse(content=response_content, status_code=status_code)


@router.delete('/admin/{admin_id}')
def delete_admin(admin_id: int):
    """
    Delete an admin by ID.
    """
    # admin_service.delete_admin() is expected to return (response_dict, status_code)
    response_content, status_code = admin_service.delete_admin(admin_id)

    if status_code >= 400:
        raise HTTPException(status_code=status_code, detail=response_content.get("error", "Failed to delete admin"))

    return JSONResponse(content=response_content, status_code=status_code)