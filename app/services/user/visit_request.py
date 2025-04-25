from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Invitation, House, Admin
from fastapi import HTTPException

def save_visit_request(data: dict, user_id: int, db: Session):
    try:
        # Validate incoming data
        house_id = data.get('house_id')
        request_date = data.get('request_date')

        if not house_id:
            raise HTTPException(status_code=400, detail="House ID is required.")
        if not request_date:
            raise HTTPException(status_code=400, detail="Request date is required.")

        # Create the invitation
        invitation = Invitation(
            user_id=user_id,  # Use the user_id from the token
            house_id=house_id,
            request_date=request_date
        )

        db.add(invitation)
        db.commit()
        db.refresh(invitation)

        return {"message": "Visit request saved successfully", "request_id": invitation.id}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while saving the visit request: {str(e)}")