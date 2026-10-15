from sqlalchemy.orm import Session
from customer_support_agent.models import Customer, Draft, Ticket


class DraftsRepository:
    def create(self, db: Session, ticket_id: int, content: str,
               context_used: str | None = None,
               status: str = "pending") -> Draft:
        draft = Draft(ticket_id = ticket_id, content = content, context_used = context_used,
                      status = status)
        db.add(draft)
        db.commit()
        db.refresh(draft)
        return draft

    def get_latest_for_ticket(self, db: Session, ticket_id : int) -> Draft | None:
        return (db.query(Draft).filter(Draft.ticket_id == ticket_id).
                order_by(Draft.created_at.desc(), Draft.id.desc()).first())

    def get_by_id(self, db: Session, draft_id: int) -> Draft | None:
        return db.query(Draft).filter(Draft.id == draft_id).first()

    def update(self, db: Session, draft_id: int, content: str | None = None,
               status: str | None = None) -> Draft | None:
        draft = db.query(Draft).filter(Draft.id == draft_id).first()
        if draft is None:
            return None

        if content is not None:
            draft.content = content
        if status is not None:
            draft.status = status
        db.commit()
        db.refresh(draft)
        return draft  

    def get_ticket_and_customer_by_draft(self, db: Session, draft_id: int) -> dict | None:
        row = (db.query(
            Draft.id.label("draft_id"),
            Draft.ticket_id.label("ticket_id"),
            Draft.content.label("draft_content"),
            Draft.status.label("draft_status"),
            Ticket.subject.label("subject"),
            Ticket.description.label("description"),
            Ticket.status.label("ticket_status"),
            Customer.id.label("customer_id"),
            Customer.email.label("customer_email"),
            Customer.name.label("customer_name"),
            Customer.company.label("customer_company"),
        )
        .join(Ticket, Ticket.id == Draft.ticket_id)
        .join(Customer, Customer.id == Ticket.customer_id)
        .filter(Draft.id == draft_id).first())
        
        return dict(row._mapping) if row is not None else None      
