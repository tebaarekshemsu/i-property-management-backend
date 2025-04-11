from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Boolean, Numeric, Text, DateTime, ARRAY
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

DATABASE_URL = "postgresql://neondb_owner:npg_lQWvnz7Bm8Pq@ep-purple-hill-a2toa720-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User Table
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_no = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    invitation_code = Column(String, unique=True)
    invited_by = Column(String, nullable=True)

    houses = relationship("House", back_populates="owner_user")
    invitations = relationship("Invitation", back_populates="invited_user")

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
    password = Column(String(255), nullable=False)

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
    image_urls = Column(ARRAY(Text), nullable=True)
    video = Column(String(255), nullable=True)
    posted_by = Column(Integer, ForeignKey('broker.broker_id'), nullable=True)

    assigned_admin = relationship("Admin", back_populates="houses")
    owner_user = relationship("User", back_populates="houses")
    broker = relationship("Broker", back_populates="houses")
    success_reports = relationship("SuccessReport", back_populates="house")
    failure_reports = relationship("FailureReport", back_populates="house")
    vip_status = relationship("VIPStatus", uselist=False, back_populates="house", cascade="all, delete")

# VIP Status Table
class VIPStatus(Base):
    __tablename__ = 'vip_status'

    vip_id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey('house.house_id', ondelete="CASCADE"), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    house = relationship("House", back_populates="vip_status")

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
    request_date = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(Enum('seen', 'not seen', name="invitation_status_enum"), nullable=False, default='not seen')
    visited_date = Column(DateTime, nullable=True)

    invited_user = relationship("User", back_populates="invitations")
    inviting_admin = relationship("Admin", back_populates="invitations")

# Admin Location Table
class AdminLocation(Base):
    __tablename__ = 'admin_location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False)
    area_code = Column(Integer, ForeignKey('area.code'), nullable=False, default=0)

# Create all tables
Base.metadata.create_all(bind=engine)

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
