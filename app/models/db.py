from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# User Table
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_no = Column(String(20), nullable=False, unique=True)  
    password = Column(String(255), nullable=False)
    invitation_code = Column(String(255), unique=True)
    invited_by = Column(Integer, ForeignKey('user.user_id'), nullable=True)

    houses = relationship("House", back_populates="owner_user")
    invitations = relationship("Invitation", back_populates="invited_user", cascade="all, delete")
    inviter = relationship("User", remote_side=[user_id], back_populates="invitees")
    invitees = relationship("User", back_populates="inviter")

# Admin Table
class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_no = Column(String(20), nullable=False, unique=True)  
    id_front = Column(String(255), nullable=False)
    id_back = Column(String(255), nullable=False)
    invitation_code = Column(String(255), unique=True)
    admin_type = Column(Enum('super-admin', 'admin', name="admin_type_enum"), nullable=False)
    houses = relationship("House", back_populates="assigned_admin")
    success_reports = relationship("SuccessReport", back_populates="admin")
    failure_reports = relationship("FailureReport", back_populates="admin")
    invitations = relationship("Invitation", back_populates="inviting_admin", cascade="all, delete")

# Area Table
class Area(Base):
    __tablename__ = 'area'

    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


# House Table
class House(Base):
    __tablename__ = 'house'

    house_id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Enum('sell', 'rent', name="category_enum"), nullable=False)
    location = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    condition = Column(Enum('fairly used', 'newly built', 'old and renovated', name="condition_enum"), nullable=True)
    bedroom = Column(Integer, nullable=False)
    toilets = Column(Integer, nullable=False)
    listed_by = Column(Enum('agent', 'owner', name="listed_by_enum"), nullable=True, server_default='owner')
    property_type = Column(Enum('apartment', 'condominium', name="property_type_enum"), nullable=False)
    furnish_status = Column(Enum('furnished', 'semi furnished', 'unfurnished', name="furnish_status_enum"), nullable=False)
    bathroom = Column(Integer, nullable=False)
    facility = Column(Text, nullable=True)  
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    negotiability = Column(Enum('open to negotiation', 'not', name="negotiability_enum"), nullable=False)  
    parking_space = Column(Boolean, nullable=False, default=False)
    assigned_for = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    owner = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    status = Column(Enum('pending', 'available', 'rented', 'sold', name="status_enum"), nullable=False, default='pending')
    photo = Column(Text, nullable=True)
    video = Column(String(255), nullable=True)
    posted_by = Column(Integer, ForeignKey('broker.broker_id'), nullable=True)

    assigned_admin = relationship("Admin", back_populates="houses")
    owner_user = relationship("User", back_populates="houses")
    broker = relationship("Broker", back_populates="houses")
    success_reports = relationship("SuccessReport", back_populates="house")
    failure_reports = relationship("FailureReport", back_populates="house")

# Broker Table
class Broker(Base):
    __tablename__ = 'broker'

    broker_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)  
    houses = relationship("House", back_populates="broker")

# Success Report Table
class SuccessReport(Base):
    __tablename__ = 'success_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    house_id = Column(Integer, ForeignKey('house.house_id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum('rent', 'sell', name="report_type_enum"), nullable=False)
    commission = Column(Numeric(10, 2), nullable=False)
    transaction_photo = Column(String(255), nullable=False)

    admin = relationship("Admin", back_populates="success_reports")
    house = relationship("House", back_populates="success_reports")

# Failure Report Table
class FailureReport(Base):
    __tablename__ = 'failure_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    house_id = Column(Integer, ForeignKey('house.house_id'), nullable=False)
    reason = Column(Text, nullable=False)

    admin = relationship("Admin", back_populates="failure_reports")
    house = relationship("House", back_populates="failure_reports")

# Invitation Table
class Invitation(Base):
    __tablename__ = 'invitation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('seen', 'not seen', name="invitation_status_enum"), nullable=False, default='not seen')
    visited_date = Column(DateTime, nullable=True)

    invited_user = relationship("User", back_populates="invitations")
    inviting_admin = relationship("Admin", back_populates="invitations")

# Admin Location Table
class AdminLocation(Base):
    __tablename__ = 'admin_location'  # Fixed table name format

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    area_code = Column(Integer, ForeignKey('area.code'), nullable=False)

   
