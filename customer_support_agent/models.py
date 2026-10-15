from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from customer_support_agent.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key = True, autoincrement  =True)
    email = Column(String, unique = True, nullable = False)
    name = Column(String, nullable = True)
    company = Column(String, nullable = True)
    created_at = Column(DateTime, server_default = func.current_timestamp())

    tickets = relationship("Ticket", back_populates = "customer")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="open")
    priority = Column(String, nullable=False, default="medium")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    customer = relationship("Customer", back_populates="tickets")
    drafts = relationship("Draft", back_populates="ticket")


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    content = Column(Text, nullable=False)
    context_used = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.current_timestamp())

    ticket = relationship("Ticket", back_populates="drafts")
