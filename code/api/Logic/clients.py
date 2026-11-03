import json

from Logic.base import Base
from Logic.GenericRepository import GenericRepository

CLIENTS = []

class Clients(Base):

    def __init__(self, data, file_path, is_debug=False):
        self.repository = GenericRepository(
            file_path,
            data,
            key_fields=("id",),
            debug=is_debug
        )

    def get_clients(self):
        return self.repository.get_all()

    def get_client(self, client_id):
        return self.repository.get_by_id(client_id)

    def add_client(self, client):
        client["created_at"] = self.get_timestamp()
        client["updated_at"] = self.get_timestamp()
        self.repository.insert(client)

    def update_client(self, client_id, client):
        client["updated_at"] = self.get_timestamp()

        self.repository.update(client_id, item=client)

    def remove_client(self, client_id):
        self.repository.delete(client_id)

    def save(self):
        self.repository.save()