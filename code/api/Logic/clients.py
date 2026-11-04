
from Logic.GenericRepository import GenericRepository
from models.client import Client


CLIENTS = []

class Clients(GenericRepository[Client]):
# Wanneer je een nieuwe klasse maakt die eigenschappen overerft van een andere klasse,
# overschrijft de __init__ van de nieuwe klasse (de child class) standaard die van de parent class.
# Met super().__init__() zorg je ervoor dat de variabelen en instellingen van de parent class toch netjes worden klaargezet en uitgevoerd


    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "client.json",
            model=Client,
            key_fields=("id",),
            debug=is_debug
        )

    def get_clients(self):
        return [vars(client).copy() for client in self.get_all()]

    def get_client(self, client_id):
        client = self.get_by_id(client_id)

        if client is None:
            return None

        return vars(client).copy()

    def add_client(self, client):
        client["created_at"] = self.get_timestamp()
        client["updated_at"] = self.get_timestamp()

        new_client = Client(**client)
        self.insert(new_client)

    def update_client(self, client_id, client):
        existing_client = self.get_by_id(client_id)

        if existing_client is None:
            return

        client["id"] = client_id
        client["created_at"] = existing_client.created_at
        client["updated_at"] = self.get_timestamp()

        updated_client = Client(**client)
        self.update(client_id, item=updated_client)

    def remove_client(self, client_id):
        self.delete(client_id)
