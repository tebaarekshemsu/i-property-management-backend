from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Invitation, House, Admin
from fastapi import HTTPException

def save_visit_request(visit_data: dict, user_id: int, db: Session):
    """
    Save a visit request for a house.
    """
    house_id = visit_data.get("house_id")
    house = db.query(House).filter(House.house_id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    invitation = Invitation(
        user_id=user_id,
        house_id=house_id,
        status="not seen"
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return {"success": True, "message": "Visit request saved successfully", "invitation": invitation}