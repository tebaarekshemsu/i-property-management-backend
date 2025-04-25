from app.models.db import Invitation
from fastapi import HTTPException
from app.database import SessionLocal

def get_visit_requests(user_id: int):
    db = SessionLocal()
    print("Fetching visit requests for user ID:", user_id)
    try:
        # Fetch visit requests for the given user_id
        visit_requests = db.query(Invitation).filter(Invitation.user_id == user_id).all()

        if not visit_requests:
            return []

        return [
            {
                "id": invitation.id,
                "house_id": invitation.house_id,
                "request_date": invitation.request_date.strftime("%Y-%m-%d"),
                "status": invitation.status,
            }
            for invitation in visit_requests
        ]
    except Exception as e:
        print(f"Error fetching visit requests: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch visit requests")
    finally:
        db.close()