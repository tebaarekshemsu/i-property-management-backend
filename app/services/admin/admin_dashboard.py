from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import House, Admin, SuccessReport
from app.models import Invitation  # if you're tracking visit requests

def get_dashboard_data(admin_id: int, db: Session):
    total_users = db.query(func.count(Admin.admin_id)).scalar()
    total_houses = db.query(House).filter(House.assigned_for == admin_id).count()
    pending_visits = db.query(Invitation).filter(Invitation.admin_id == admin_id, Invitation.status == "not seen").count()
    transactions = db.query(SuccessReport).filter(SuccessReport.admin_id == admin_id).all()
    total_revenue = sum([float(t.price) for t in transactions])
    success_rate = f"{round(len(transactions) / total_houses * 100, 2) if total_houses else 0}%"

    recent_transactions = [
        {
            "house": t.house_name,
            "amount": float(t.price),
            "date": t.date.strftime("%Y-%m-%d"),
            "type": t.type
        } for t in sorted(transactions, key=lambda x: x.date, reverse=True)[:5]
    ]

    return {
        "totalRevenue": f"${total_revenue:,.0f}",
        "totalUsers": total_users,
        "totalHouses": total_houses,
        "pendingVisits": pending_visits,
        "successRate": success_rate,
        "recentTransactions": recent_transactions
    }
