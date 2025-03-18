from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Invitation

app = Flask(__name__)  # Fixed the app name

def save_visit_request(data):
    print('hello')
    print(data)
    with app.app_context():  # Activate the application context
        db: Session = SessionLocal()
        try:
            invitation = Invitation(
                user_id=data['user_id'],
                admin_id=data['admin_id'],
                request_date=data.get('request_date')  # Use get() to handle optional fields
            )
            db.add(invitation)
            db.commit()
            return jsonify({"message": "Visit request saved successfully", "request_id": invitation.id}), 201
        except Exception as e:
            db.rollback()
            print(str(e))
            return jsonify({"message": str(e)}), 400
        finally:
            db.close()


