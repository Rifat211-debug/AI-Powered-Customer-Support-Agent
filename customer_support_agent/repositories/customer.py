from sqlalchemy.orm import Session
from customer_support_agent.models import Customer


class CustomersRepository:
    def create_or_get(self, db: Session, email: str, name: str | None = None,
                      company: str | None = None) -> Customer:
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer is not None:
            changed = False
            if not customer.name and name:
                customer.name = name
                changed = True
            if not customer.company and company:
                customer.company = company  
                changed = True
            if changed:
                db.commit()
                db.refresh(customer)
                return customer

        customer = Customer(email = email, name = name, company = company)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get_by_id(self, db: Session, customer_id: int) -> Customer | None:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_email(self, db: Session, customer_email: str) -> Customer | None:
        return db.query(Customer).filter(Customer.email == customer_email).first()

