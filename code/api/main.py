import socketserver
import http.server
import json
from urllib.parse import urlsplit

from providers import auth_provider
from processors import notification_processor
from helpers import validator
from controllers import (
    WarehousesController,
    LocationsController,
    TransfersController,
    ItemsController,
    Item_linesController,
    Item_groupsController,
    Item_typesController,
    InventoriesController,
    SuppliersController,
    OrdersController,
    ClientsController,
    ShipmentsController
)
from services import transfer_service

CONTROLLERS = {
    "warehouses": WarehousesController,
    "locations": LocationsController,
    "transfers": TransfersController,
    "items": ItemsController,
    "item_lines": Item_linesController,
    "item_groups": Item_groupsController,
    "item_types": Item_typesController,
    "inventories": InventoriesController,
    "suppliers": SuppliersController,
    "orders": OrdersController,
    "clients": ClientsController,
    "shipments": ShipmentsController
}

class ApiRequestHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, status_code, data=None):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode())

    def validate_request(self, required_method: str):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)

        if user is None:
            self.send_json(401)
            return None, None

        path_parts = urlsplit(self.path).path.strip("/").split("/")
        if len(path_parts) >= 3 and path_parts[:2] == ["api", "v1"]:
            resource_paths = path_parts[2:]
            if not resource_paths or not resource_paths[0]:
                self.send_json(404)
                return None, None
            # Check direct of de user rechten heeft voor dit specifieke pad en methode
            if not auth_provider.has_access(user, resource_paths, required_method):
                self.send_json(403)
                return None, None
            return resource_paths, user

        self.send_json(404)
        return None, None

    def dispatch_request(self, method: str, paths: list[str], user=None):
        method = method.upper()
        if method not in {"GET", "POST", "PUT", "DELETE"}:
            return 405, None
        if not paths:
            return 404, None

        resource = paths[0]
        controller = CONTROLLERS.get(resource)
        if controller is None:
            return 404, None

        if method == "DELETE" and len(paths) == 1:
            return 405, None
        if method == "DELETE" and resource == "inventories":
            return 404, None

        if method == "PUT" and resource == "transfers" and len(paths) == 3 and paths[2] == "commit":
            try:
                transfer_id = int(paths[1])
            except ValueError:
                return 400, {"error": "ID must be an integer"}
            return transfer_service.handle_transfer_commit(self, transfer_id), None

        functions = getattr(controller, f"{method}_FUNCTIONS", {})
        selected_function = None
        for route, function in functions.items():
            if isinstance(route, str):
                route = (route, "id") if method == "DELETE" else (route,)
            if len(route) != len(paths):
                continue
            matches = all(
                expected == actual or expected == "id"
                for expected, actual in zip(route, paths)
            )
            if matches:
                selected_function = function
                break
        if selected_function is None:
            return 404, None

        resource_id = None
        if len(paths) > 1:
            try:
                resource_id = int(paths[1])
            except ValueError:
                return 400, {"error": "ID must be an integer"}

        if method == "GET":
            result = selected_function(resource_id)
            return (404, None) if result is None else (200, result)

        if method in {"POST", "PUT"}:
            try:
                payload = self.read_json_body()
            except (json.JSONDecodeError, UnicodeDecodeError):
                return 400, {"error": "Invalid JSON format"}

            if method == "POST" or len(paths) == 2:
                is_valid, error_message = validator.validate_request_body(resource, payload)
                if not is_valid:
                    return 400, {"error": error_message}

            if method == "POST":
                selected_function(payload)
                return 201, None

            selected_function(resource_id, payload)
            return 200, None

        selected_function(resource_id)
        return 200, None

    def _handle_api_method(self, method: str):
        try:
            paths, user = self.validate_request(method.lower())
            if paths is None:
                return
            status_code, body = self.dispatch_request(method, paths, user)
            self.send_json(status_code, body)
        except Exception:
            self.send_json(500)

    def do_GET(self):
        self._handle_api_method("GET")

    def do_POST(self):
        self._handle_api_method("POST")

    def do_PUT(self):
        self._handle_api_method("PUT")

    def do_DELETE(self):
        self._handle_api_method("DELETE")


if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), ApiRequestHandler) as httpd:
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()

# def handle_delete_version_1(self, paths, user):
    #     if paths[0] == "warehouses":
    #         warehouse_id = int(paths[1])
    #         data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
    #         data_provider.fetch_warehouse_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "locations":
    #         location_id = int(paths[1])
    #         data_provider.fetch_location_pool().remove_location(location_id)
    #         data_provider.fetch_location_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "transfers":
    #         transfer_id = int(paths[1])
    #         data_provider.fetch_transfer_pool().remove_transfer(transfer_id)
    #         data_provider.fetch_transfer_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "items":
    #         item_id = int(paths[1])
    #         data_provider.fetch_item_pool().remove_item(item_id)
    #         data_provider.fetch_item_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "item_lines":
    #         item_line_id = int(paths[1])
    #         data_provider.fetch_item_line_pool().remove_item_line(item_line_id)
    #         data_provider.fetch_item_line_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "item_groups":
    #         item_group_id = int(paths[1])
    #         data_provider.fetch_item_group_pool().remove_item_group(item_group_id)
    #         data_provider.fetch_item_group_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "item_types":
    #         item_type_id = int(paths[1])
    #         data_provider.fetch_item_type_pool().remove_item_type(item_type_id)
    #         data_provider.fetch_item_type_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "inventories":
    #         self.send_response(404)
    #         self.end_headers()
    #     elif paths[0] == "suppliers":
    #         supplier_id = int(paths[1])
    #         data_provider.fetch_supplier_pool().remove_supplier(supplier_id)
    #         data_provider.fetch_supplier_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "orders":
    #         order_id = int(paths[1])
    #         data_provider.fetch_order_pool().remove_order(order_id)
    #         data_provider.fetch_order_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "clients":
    #         client_id = int(paths[1])
    #         data_provider.fetch_client_pool().remove_client(client_id)
    #         data_provider.fetch_client_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     elif paths[0] == "shipments":
    #         shipment_id = int(paths[1])
    #         data_provider.fetch_shipment_pool().remove_shipment(shipment_id)
    #         data_provider.fetch_shipment_pool().save()
    #         self.send_response(200)
    #         self.end_headers()
    #     else:
    #         self.send_response(404)
    #         self.end_headers()

    # alle losse functions die er zijn om zo de elif  evt weg te kunne halen.

    # def handle_get_version_2(self, paths: list[str], user: str |None):
    #     parts= len(paths)

    #     if paths[0] not in [resource.value for resource in AllResources]:
    #         self.send_response(404)
    #         self.end_headers()

    #     # losse kijk of de case groter is dan de algemene lengte die het kan hebben mbv de enum
    #     resource = next((resource for resource in AllResources if resource.path == paths[0]),None)
    #     if resource is None or parts > resource.max_path_length:
    #         self.send_response(404)
    #         self.end_headers()
    #         return

    #     else:

    #         if parts > 1:
    #             try:
    #                 resource_id = int(paths[1])
    #             except ValueError:
    #                 self.send_response(400)
    #                 self.end_headers()
    #                 return

    #         if paths[0] == AllResources.WAREHOUSES.path:
    #             match parts:
    #                 case 1:
    #                     # uiteindelijk nog een statement maken om te kijken of het wel iets returned idd, zoniet dan andere statuscode (204
    #                     self.send_response_code(data_provider.fetch_warehouse_pool().get_warehouses())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_warehouse_pool().get_warehouse(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.LOCATIONS.path:
    #                         self.send_response_code(data_provider.fetch_location_pool().get_locations_in_warehouse(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.LOCATIONS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_location_pool().get_locations())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_location_pool().get_location(resource_id))

    #         elif paths[0] == AllResources.TRANSFERS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_transfer_pool().get_transfers())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_transfer_pool().get_transfer(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_transfer_pool().get_items_in_transfer(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.ITEMS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_item_pool().get_items())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_item_pool().get_item(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.INVENTORY.path:
    #                         self.send_response_code(data_provider.fetch_inventory_pool().get_inventories_for_item(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)
    #                 case 4:
    #                     if paths[2] == AllResources.INVENTORY.path and paths[3] == AllResources.TOTALS.path:
    #                         self.send_response_code(data_provider.fetch_inventory_pool().get_inventory_totals_for_item(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.ITEM_LINES.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_item_line_pool().get_item_lines())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_item_line_pool().get_item_line(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_item_pool().get_items_for_item_line(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.ITEM_GROUPS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_item_group_pool().get_item_groups())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_item_group_pool().get_item_group(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_item_pool().get_items_for_item_group(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.ITEM_TYPES.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_item_type_pool().get_item_types())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_item_type_pool().get_item_type(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_item_pool().get_items_for_item_type(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.INVENTORIES.value:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_inventory_pool().get_inventories())
    #                 case 2:
    #                     # Inventory rows are keyed on a composite (item_id, location_id)
    #                     # in the new schema, so a single surrogate id has no meaning.
    #                     self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.SUPPLIERS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_supplier_pool().get_suppliers())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_supplier_pool().get_supplier(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_item_pool().get_items_for_supplier(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.ORDERS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_order_pool().get_orders())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_order_pool().get_order(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_order_pool().get_items_in_order(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.CLIENTS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_client_pool().get_clients())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_client_pool().get_client(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ORDERS.path:
    #                         self.send_response_code(data_provider.fetch_order_pool().get_orders_for_client(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    #         elif paths[0] == AllResources.SHIPMENTS.path:
    #             match parts:
    #                 case 1:
    #                     self.send_response_code(data_provider.fetch_shipment_pool().get_shipments())
    #                 case 2:
    #                     self.send_response_code(data_provider.fetch_shipment_pool().get_shipment(resource_id))
    #                 case 3:
    #                     if paths[2] == AllResources.ORDERS.path:
    #                         self.send_response_code(data_provider.fetch_shipment_pool().get_order_ids_in_shipment(resource_id))
    #                     elif paths[2] == AllResources.ITEMS.path:
    #                         self.send_response_code(data_provider.fetch_shipment_pool().get_items_in_shipment(resource_id))
    #                     else:
    #                         self.send_response_code(data=[], status_code=404)

    # def handle_post_version_1(self, paths, user):
    #     if paths[0] == "warehouses":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_warehouse = json.loads(post_data.decode())
    #         data_provider.fetch_warehouse_pool().add_warehouse(new_warehouse)
    #         data_provider.fetch_warehouse_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "locations":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_location = json.loads(post_data.decode())
    #         data_provider.fetch_location_pool().add_location(new_location)
    #         data_provider.fetch_location_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "transfers":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_transfer = json.loads(post_data.decode())
    #         data_provider.fetch_transfer_pool().add_transfer(new_transfer)
    #         data_provider.fetch_transfer_pool().save()
    #         notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "items":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_item = json.loads(post_data.decode())
    #         data_provider.fetch_item_pool().add_item(new_item)
    #         data_provider.fetch_item_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "item_lines":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_item_line = json.loads(post_data.decode())
    #         data_provider.fetch_item_line_pool().add_item_line(new_item_line)
    #         data_provider.fetch_item_line_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "item_groups":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_item_group = json.loads(post_data.decode())
    #         data_provider.fetch_item_group_pool().add_item_group(new_item_group)
    #         data_provider.fetch_item_group_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "item_types":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_item_type = json.loads(post_data.decode())
    #         data_provider.fetch_item_type_pool().add_item_type(new_item_type)
    #         data_provider.fetch_item_type_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "inventories":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_inventory = json.loads(post_data.decode())
    #         data_provider.fetch_inventory_pool().add_inventory(new_inventory)
    #         data_provider.fetch_inventory_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "suppliers":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_supplier = json.loads(post_data.decode())
    #         data_provider.fetch_supplier_pool().add_supplier(new_supplier)
    #         data_provider.fetch_supplier_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "orders":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_order = json.loads(post_data.decode())
    #         data_provider.fetch_order_pool().add_order(new_order)
    #         data_provider.fetch_order_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "clients":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_client = json.loads(post_data.decode())
    #         data_provider.fetch_client_pool().add_client(new_client)
    #         data_provider.fetch_client_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     elif paths[0] == "shipments":
    #         content_length = int(self.headers["Content-Length"])
    #         post_data = self.rfile.read(content_length)
    #         new_shipment = json.loads(post_data.decode())
    #         data_provider.fetch_shipment_pool().add_shipment(new_shipment)
    #         data_provider.fetch_shipment_pool().save()
    #         self.send_response(201)
    #         self.end_headers()
    #     else:
    #         self.send_response(404)
    #         self.end_headers()


# def handle_put_version_2(self, paths, user):
#     if paths[0] == "warehouses":
#         warehouse_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_warehouse = json.loads(post_data.decode())
#         data_provider.fetch_warehouse_pool().update_warehouse(
#             warehouse_id, updated_warehouse
#         )
#         data_provider.fetch_warehouse_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "locations":
#         location_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_location = json.loads(post_data.decode())
#         data_provider.fetch_location_pool().update_location(
#             location_id, updated_location
#         )
#         data_provider.fetch_location_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "transfers":
#         parts = len(paths)
#         match parts:
#             case 2:
#                 transfer_id = int(paths[1])
#                 content_length = int(self.headers["Content-Length"])
#                 post_data = self.rfile.read(content_length)
#                 updated_transfer = json.loads(post_data.decode())
#                 data_provider.fetch_transfer_pool().update_transfer(
#                     transfer_id, updated_transfer
#                 )
#                 data_provider.fetch_transfer_pool().save()
#                 self.send_response(200)
#                 self.end_headers()
#             case 3:
#                 if paths[2] == "commit":
#                     transfer_id = int(paths[1])
#                     transfer = data_provider.fetch_transfer_pool().get_transfer(
#                         transfer_id
#                     )
#                     from_location_id = transfer["from_location_id"]
#                     to_location_id = transfer["to_location_id"]
#                     inventory_pool = data_provider.fetch_inventory_pool()
#                     for x in transfer["items"]:
#                         item_id = x["item_id"]
#                         amount = x["amount"]
#                         # decrease on-hand at the source location
#                         src = inventory_pool.get_inventory(
#                             item_id, from_location_id
#                         )
#                         if src is not None:
#                             src["quantity_on_hand"] -= amount
#                             inventory_pool.update_inventory(
#                                 item_id, from_location_id, src
#                             )
#                         # increase (or create) on-hand at the destination location
#                         dst = inventory_pool.get_inventory(item_id, to_location_id)
#                         if dst is not None:
#                             dst["quantity_on_hand"] += amount
#                             inventory_pool.update_inventory(
#                                 item_id, to_location_id, dst
#                             )
#                         else:
#                             inventory_pool.add_inventory(
#                                 {
#                                     "item_id": item_id,
#                                     "location_id": to_location_id,
#                                     "quantity_on_hand": amount,
#                                     "quantity_expected": 0,
#                                     "quantity_ordered": 0,
#                                     "quantity_allocated": 0,
#                                 }
#                             )
#                     transfer["transfer_status"] = "Processed"
#                     transfer.pop("items", None)
#                     data_provider.fetch_transfer_pool().update_transfer(
#                         transfer_id, transfer
#                     )
#                     notification_processor.push(
#                         f"Processed batch transfer with id:{transfer['id']}"
#                     )
#                     data_provider.fetch_transfer_pool().save()
#                     data_provider.fetch_inventory_pool().save()
#                     self.send_response(200)
#                     self.end_headers()
#                 else:
#                     self.send_response(404)
#                     self.end_headers()
#             case _:
#                 self.send_response(404)
#                 self.end_headers()
#     elif paths[0] == "items":
#         item_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_item = json.loads(post_data.decode())
#         data_provider.fetch_item_pool().update_item(item_id, updated_item)
#         data_provider.fetch_item_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "item_lines":
#         item_line_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_item_line = json.loads(post_data.decode())
#         data_provider.fetch_item_line_pool().update_item_line(
#             item_line_id, updated_item_line
#         )
#         data_provider.fetch_item_line_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "item_groups":
#         item_group_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_item_group = json.loads(post_data.decode())
#         data_provider.fetch_item_group_pool().update_item_group(
#             item_group_id, updated_item_group
#         )
#         data_provider.fetch_item_group_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "item_types":
#         item_type_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_item_type = json.loads(post_data.decode())
#         data_provider.fetch_item_type_pool().update_item_type(
#             item_type_id, updated_item_type
#         )
#         data_provider.fetch_item_type_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "inventories":
#         # Inventory rows are keyed on a composite (item_id, location_id); a
#         # single surrogate id is not meaningful in the new schema.
#         self.send_response(404)
#         self.end_headers()
#     elif paths[0] == "suppliers":
#         supplier_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_supplier = json.loads(post_data.decode())
#         data_provider.fetch_supplier_pool().update_supplier(
#             supplier_id, updated_supplier
#         )
#         data_provider.fetch_supplier_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "orders":
#         parts = len(paths)
#         match parts:
#             case 2:
#                 order_id = int(paths[1])
#                 content_length = int(self.headers["Content-Length"])
#                 post_data = self.rfile.read(content_length)
#                 updated_order = json.loads(post_data.decode())
#                 data_provider.fetch_order_pool().update_order(
#                     order_id, updated_order
#                 )
#                 data_provider.fetch_order_pool().save()
#                 self.send_response(200)
#                 self.end_headers()
#             case 3:
#                 if paths[2] == "items":
#                     order_id = int(paths[1])
#                     content_length = int(self.headers["Content-Length"])
#                     post_data = self.rfile.read(content_length)
#                     updated_items = json.loads(post_data.decode())
#                     data_provider.fetch_order_pool().update_items_in_order(
#                         order_id, updated_items
#                     )
#                     data_provider.fetch_order_pool().save()
#                     self.send_response(200)
#                     self.end_headers()
#                 else:
#                     self.send_response(404)
#                     self.end_headers()
#             case _:
#                 self.send_response(404)
#                 self.end_headers()
#     elif paths[0] == "clients":
#         client_id = int(paths[1])
#         content_length = int(self.headers["Content-Length"])
#         post_data = self.rfile.read(content_length)
#         updated_client = json.loads(post_data.decode())
#         data_provider.fetch_client_pool().update_client(client_id, updated_client)
#         data_provider.fetch_client_pool().save()
#         self.send_response(200)
#         self.end_headers()
#     elif paths[0] == "shipments":
#         parts = len(paths)
#         match parts:
#             case 2:
#                 shipment_id = int(paths[1])
#                 content_length = int(self.headers["Content-Length"])
#                 post_data = self.rfile.read(content_length)
#                 updated_shipment = json.loads(post_data.decode())
#                 data_provider.fetch_shipment_pool().update_shipment(
#                     shipment_id, updated_shipment
#                 )
#                 data_provider.fetch_shipment_pool().save()
#                 self.send_response(200)
#                 self.end_headers()
#             case 3:
#                 if paths[2] == "orders":
#                     shipment_id = int(paths[1])
#                     content_length = int(self.headers["Content-Length"])
#                     post_data = self.rfile.read(content_length)
#                     updated_orders = json.loads(post_data.decode())
#                     data_provider.fetch_shipment_pool().update_orders_in_shipment(
#                         shipment_id, updated_orders
#                     )
#                     data_provider.fetch_shipment_pool().save()
#                     self.send_response(200)
#                     self.end_headers()
#                 elif paths[2] == "items":
#                     shipment_id = int(paths[1])
#                     content_length = int(self.headers["Content-Length"])
#                     post_data = self.rfile.read(content_length)
#                     updated_items = json.loads(post_data.decode())
#                     data_provider.fetch_shipment_pool().update_items_in_shipment(
#                         shipment_id, updated_items
#                     )
#                     data_provider.fetch_shipment_pool().save()
#                     self.send_response(200)
#                     self.end_headers()
#                 else:
#                     self.send_response(404)
#                     self.end_headers()
#             case _:
#                 self.send_response(404)
#                 self.end_headers()
#     else:
#         self.send_response(404)
#         self.end_headers()
