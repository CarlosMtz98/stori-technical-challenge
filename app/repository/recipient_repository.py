from app.models.recipient import Recipient
from app.repository.repository_interface import IRepository
from app.utils.validators.validate_email import is_valid_email


class RecipientRepository(IRepository):
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Recipient).all()

    def get_by_id(self, id):
        return self.session.query(Recipient).get(id)

    def get_by_email(self, email):
        return self.session.query(Recipient).filter(Recipient.email == email).first()

    def create(self, recipient):
        if recipient and is_valid_email(recipient.email) and not self.get_by_email(recipient.email):
            self.session.add(recipient)
            self.session.commit()

    def update(self, item):
        if self.get_by_id(item.id):
            self.session.merge(item)
            self.session.commit()

    def delete(self, id):
        recipient = self.get_by_id(id)
        if recipient:
            self.session.delete(recipient)
            self.session.commit()
