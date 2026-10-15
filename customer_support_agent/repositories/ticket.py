from sqlalchemy import func
from sqlalchemy.orm import Session
from customer_support_agent.models import Customer, Ticket


class TicketsRepository:
    def create(self, db: Session, customer_id: int | None, subject: str,
               description: str, priority: str = "medium",
               status: str = "open") -> Ticket:
        ticket = Ticket(customer_id=customer_id, subject=subject,
                                description=description, priority=priority, status=status)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    def list(self, db: Session, limit: int = 100) -> list[dict]:
        rows = (db.query(Ticket, Customer.email.label("customer_email"),
                        Customer.name.label("customer_name"),
                        Customer.company.label("customer_company"))
                        .outerjoin(Customer, Customer.id == Ticket.customer_id)
                        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
                        .limit(limit).all())
        result = []

        for ticket, email, name, company in rows:
            result.append({
                "id": ticket.id, "customer_id": ticket.customer_id,
                "subject": ticket.subject, "description": ticket.description,
                "status": ticket.status, "priority": ticket.priority,
                "created_at": ticket.created_at, "updated_at": ticket.updated_at,
                "customer_email": email, "customer_name": name,
                "customer_company": company,
            }) 
        return result

    def get_by_id(self, db: Session, ticket_id: int) -> dict | None:
        row = (db.query(Ticket, Customer.email.label("customer_email"),
                        Customer.name.label("customer_name"),
                        Customer.company.label("customer_company"))
                        .outerjoin(Customer, Customer.id == Ticket.customer_id)
                        .filter(ticket_id == Ticket.id).first())

        if row is None:
            return None

        ticket, email, name, company = row

        return {
            "id": ticket.id, "customer_id": ticket.customer_id,
            "subject": ticket.subject, "description": ticket.description,
            "status": ticket.status, "priority": ticket.priority,
            "created_at": ticket.created_at, "updated_at": ticket.updated_at,
            "customer_email": email, "customer_name": name,
            "customer_company": company
        } 

    def set_status(self, db: Session, ticket_id: int, status: str) -> Ticket | None:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket is None:
            return None

        ticket.status = status
        db.commit()
        db.refresh(ticket)
        return ticket

    def count_for_customer(self, db: Session, customer_email: str) -> int:
        count = (db.query(func.count(Ticket.id))
                 .join(Customer, Customer.id == Ticket.customer_id)
                 .filter(Customer.email == customer_email, Ticket.status == "open")
                 .scaler())

        return int(count or 0)   
