from app.repository.repository_interface import IRepository


class SqlAlchemyRepository(IRepository):
    
    def get_all(self):
        pass

    def get_by_id(self, id):
        pass

    def create(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, id):
        pass