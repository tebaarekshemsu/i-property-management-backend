from sqlalchemy.orm import Session
from app.models import User, Invitation
from fastapi import HTTPException

def fetch_visit_requests(current_user: User, db: Session):
    """
    Get all visit requests for the current user.
    """
    requests = db.query(Invitation).filter(Invitation.user_id == current_user.user_id).all()
    return [
        {
            "id": request.id,
            "house_id": request.house_id,
            "request_date": request.request_date,
            "visited_date": request.visited_date,
            "status": request.status
        }
        for request in requests
    ]