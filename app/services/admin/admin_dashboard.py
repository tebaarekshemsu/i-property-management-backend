from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import House, Admin, SuccessReport, FailureReport
from app.models import Invitation  # if you're tracking visit requests
from fastapi import HTTPException
from datetime import datetime, timedelta

def get_dashboard_data(admin_id: int, db: Session):
    """
    Get dashboard data for the current admin.
    """
    houses = db.query(House).filter(House.assigned_for == admin_id).all()
    visit_requests = db.query(Invitation).filter(Invitation.house_id.in_(
        db.query(House.house_id).filter(House.assigned_for == admin_id)
    )).all()
    success_reports = db.query(SuccessReport).filter(SuccessReport.admin_id == admin_id).all()
    failure_reports = db.query(FailureReport).filter(FailureReport.admin_id == admin_id).all()

    total_revenue = sum(report.price for report in success_reports)
    pending_reports = len([report for report in success_reports if not report.transaction_photo])
    pending_visits = len([request for request in visit_requests if request.status == "pending"])
    total_reports = len(success_reports) + len(failure_reports)
    success_rate = (len(success_reports) / total_reports * 100) if total_reports > 0 else 0

    recent_transactions = db.query(SuccessReport, House).join(
        Invitation, SuccessReport.invitation_id == Invitation.id
    ).join(
        House, Invitation.house_id == House.house_id
    ).filter(
        SuccessReport.admin_id == admin_id
    ).order_by(
        SuccessReport.id.desc()
    ).limit(5).all()

    return {
        "totalRevenue": f"{total_revenue:,.2f}",
        "pendingReports": pending_reports,
        "totalHouses": len(houses),
        "pendingVisits": pending_visits,
        "successRate": f"{success_rate:.1f}",
        "recentTransactions": [
            {
                "id": report.id,
                "house": house.title,
                "amount": f"{report.price:,.2f}",
                "date": report.created_at.strftime("%Y-%m-%d") if hasattr(report, 'created_at') else datetime.now().strftime("%Y-%m-%d"),
                "type": report.type
            }
            for report, house in recent_transactions
        ],
        # "houses": [
        #     {
        #         "house_id": house.house_id,
        #         "category": house.category,
        #         "location": house.location,
        #         "address": house.address,
        #         "size": house.size,
        #         "condition": house.condition,
        #         "bedroom": house.bedroom,
        #         "toilets": house.toilets,
        #         "bathroom": house.bathroom,
        #         "property_type": house.property_type,
        #         "furnish_status": house.furnish_status,
        #         "facility": house.facility,
        #         "description": house.description,
        #         "price": house.price,
        #         "negotiability": house.negotiability,
        #         "parking_space": house.parking_space,
        #         "listed_by": house.listed_by,
        #         "status": house.status,
        #         "image_urls": house.image_urls,
        #         "video": house.video
        #     }
        #     for house in houses
        # ],
        # "visit_requests": [
        #     {
        #         "id": request.id,
        #         "user_id": request.user_id,
        #         "house_id": request.house_id,
        #         "request_date": request.request_date,
        #         "visited_date": request.visited_date,
        #         "status": request.status
        #     }
        #     for request in visit_requests
        # ],
        # "success_reports": [
        #     {
        #         "id": report.id,
        #         "invitation_id": report.invitation_id,
        #         "price": report.price,
        #         "type": report.type,
        #         "commission": report.commission,
        #         "transaction_photo": report.transaction_photo
        #     }
        #     for report in success_reports
        # ],
        # "failure_reports": [
        #     {
        #         "id": report.id,
        #         "invitation_id": report.invitation_id,
        #         "reason": report.reason
        #     }
        #     for report in failure_reports
        # ]
    }
