# from sqlalchemy import Column, Integer, String, Enum
# from app.models.db import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     phone_no = Column(String, unique=True, index=True)
#     password = Column(String, nullable=False)
#     invitation_code = Column(String, unique=True)
#     invited_by = Column(Integer, nullable=True)

# class Admin(Base):
#     __tablename__ = "admins"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     phone_no = Column(String, unique=True, index=True)
#     password = Column(String, nullable=False)
#     id_front = Column(String, nullable=False)
#     id_back = Column(String, nullable=False)
#     invitation_code = Column(String, unique=True)
#     admin_type = Column(Enum('super-admin', 'admin', name="admin_type_enum"), nullable=False)
