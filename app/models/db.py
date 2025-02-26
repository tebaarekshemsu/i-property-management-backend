from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# User Table
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_no = Column(Integer, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    invitation_code = Column(String(255), unique=True)
    invited_by = Column(String(255), nullable=True)

    houses = relationship("House", back_populates="owner_user")
    invitations = relationship("Invitation", back_populates="invited_user")


# Admin Table
class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_no = Column(Integer, nullable=False, unique=True)
    id_front = Column(String(255), nullable=False)
    id_back = Column(String(255), nullable=False)
    area_code = Column(Integer, ForeignKey('area.code'), nullable=False)
    invitation_code = Column(String(255), unique=True)
    admin_type = Column(Enum('super-admin', 'admin'), nullable=False)

    area = relationship("Area", back_populates="admins")
    houses = relationship("House", back_populates="assigned_admin")
    success_reports = relationship("SuccessReport", back_populates="admin")
    failure_reports = relationship("FailureReport", back_populates="admin")
    invitations = relationship("Invitation", back_populates="inviting_admin")


# Area Table
class Area(Base):
    __tablename__ = 'area'

    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    admins = relationship("Admin", back_populates="area")


# House Table
class House(Base):
    __tablename__ = 'house'

    house_id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Enum('sell', 'rent'), nullable=False)
    location = Column(String(255), nullable=False)  # Assuming location is a sub-city
    address = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    condition = Column(Enum('fairly used', 'newly built', 'old and renovated'), nullable=True)
    bedroom = Column(Integer, nullable=False)
    toilets = Column(Integer, nullable=False)
    listed_by = Column(Enum('agent', 'owner'), nullable=True, default='owner')
    property_type = Column(Enum('apartment', 'condominium'), nullable=False)
    furnish_status = Column(Enum('furnished', 'semi furnished', 'unfurnished'), nullable=False)
    bathroom = Column(Integer, nullable=False)
    facility = Column(String(255), nullable=True)  # Comma-separated facilities
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    negotiability = Column(Enum('open to n', 'not'), nullable=False)
    parking_space = Column(Boolean, nullable=False, default=False)
    assigned_for = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    owner = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    status = Column(Enum('pending', 'available', 'rented', 'sold'), nullable=False, default='pending')
    photo = Column(Text, nullable=True)  # Comma-separated file paths
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
    phone_number = Column(Integer, nullable=False, unique=True)

    houses = relationship("House", back_populates="broker")


# Success Report Table
class SuccessReport(Base):
    __tablename__ = 'success_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    house_id = Column(Integer, ForeignKey('house.house_id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum('rent', 'sell'), nullable=False)
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
    status = Column(Enum('seen', 'not seen'), nullable=False, default='not seen')
    visited_date = Column(DateTime, nullable=True)

    invited_user = relationship("User", back_populates="invitations")
    inviting_admin = relationship("Admin", back_populates="invitations")
