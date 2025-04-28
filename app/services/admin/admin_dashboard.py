from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import House, Admin, SuccessReport
from app.models import Invitation  # if you're tracking visit requests

def get_dashboard_data(admin_id: int, db: Session):
    house_ids = db.query(House.house_id).filter(House.assigned_for == admin_id).subquery()
    pending_reports = db.query(Invitation).filter(Invitation.house_id.in_(house_ids), Invitation.status == "seen").count() or 0
    total_houses = db.query(House).filter(House.assigned_for == admin_id).count() or 0
    pending_visits = db.query(Invitation).filter(Invitation.house_id.in_(house_ids), Invitation.status == "not seen").count() or 0
    transactions = db.query(SuccessReport).filter(SuccessReport.admin_id == admin_id).all() or []
    total_revenue = sum([float(t.price) for t in transactions]) if transactions else 0.0
    success_rate = f"{round(len(transactions) / total_houses * 100, 2) if total_houses else 0}%" if transactions else "0%"

    recent_transactions = [
        {
            "house": t.house_name,
            "amount": float(t.price),
            "date": t.date.strftime("%Y-%m-%d"),
            "type": t.type
        } for t in sorted(transactions, key=lambda x: x.date, reverse=True)[:5]
    ] if transactions else []

    return {
        "totalRevenue": f"${total_revenue:,.0f}" if total_revenue else "$0",
        "pendingReports": pending_reports,
        "totalHouses": total_houses,
        "pendingVisits": pending_visits,
        "successRate": success_rate,
        "recentTransactions": recent_transactions
    }
