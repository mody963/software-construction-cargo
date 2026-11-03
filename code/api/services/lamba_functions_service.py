
from providers import data_provider

GET_FUNCTIONS = {
    # warehouses
    ("warehouses",): lambda resource_id: data_provider.fetch_warehouse_pool().get_warehouses(),
    ("warehouses", "id"): lambda resource_id: data_provider.fetch_warehouse_pool().get_warehouse(resource_id),
    ("warehouses", "id", "locations"): lambda resource_id: data_provider.fetch_location_pool().get_locations_in_warehouse(resource_id),

    # locations
    ("locations",): lambda resource_id: data_provider.fetch_location_pool().get_locations(),
    ("locations", "id"): lambda resource_id: data_provider.fetch_location_pool().get_location(resource_id),

    # transfers
    ("transfers",): lambda resource_id: data_provider.fetch_transfer_pool().get_transfers(),
    ("transfers", "id"): lambda resource_id: data_provider.fetch_transfer_pool().get_transfer(resource_id),
    ("transfers", "id", "items"): lambda resource_id: data_provider.fetch_transfer_pool().get_items_in_transfer(resource_id),

    # items
    ("items",): lambda resource_id: data_provider.fetch_item_pool().get_items(),
    ("items", "id"): lambda resource_id: data_provider.fetch_item_pool().get_item(resource_id),
    ("items", "id", "inventory"): lambda resource_id: data_provider.fetch_inventory_pool().get_inventories_for_item(resource_id),
    ("items", "id", "inventory", "totals"): lambda resource_id: data_provider.fetch_inventory_pool().get_inventory_totals_for_item(resource_id),

    # item_lines
    ("item_lines",): lambda resource_id: data_provider.fetch_item_line_pool().get_item_lines(),
    ("item_lines", "id"): lambda resource_id: data_provider.fetch_item_line_pool().get_item_line(resource_id),
    ("item_lines", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_line(resource_id),

    # item_groups
    ("item_groups",): lambda resource_id: data_provider.fetch_item_group_pool().get_item_groups(),
    ("item_groups", "id"): lambda resource_id: data_provider.fetch_item_group_pool().get_item_group(resource_id),
    ("item_groups", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_group(resource_id),

    # item_types
    ("item_types",): lambda resource_id: data_provider.fetch_item_type_pool().get_item_types(),
    ("item_types", "id"): lambda resource_id: data_provider.fetch_item_type_pool().get_item_type(resource_id),
    ("item_types", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_type(resource_id),

    # inventories
    ("inventories",): lambda resource_id: data_provider.fetch_inventory_pool().get_inventories(),

    # suppliers
    ("suppliers",): lambda resource_id: data_provider.fetch_supplier_pool().get_suppliers(),
    ("suppliers", "id"): lambda resource_id: data_provider.fetch_supplier_pool().get_supplier(resource_id),
    ("suppliers", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_supplier(resource_id),

    # orders
    ("orders",): lambda resource_id: data_provider.fetch_order_pool().get_orders(),
    ("orders", "id"): lambda resource_id: data_provider.fetch_order_pool().get_order(resource_id),
    ("orders", "id", "items"): lambda resource_id: data_provider.fetch_order_pool().get_items_in_order(resource_id),

    # clients
    ("clients",): lambda resource_id: data_provider.fetch_client_pool().get_clients(),
    ("clients", "id"): lambda resource_id: data_provider.fetch_client_pool().get_client(resource_id),
    ("clients", "id", "orders"): lambda resource_id: data_provider.fetch_order_pool().get_orders_for_client(resource_id),

    # shipments
    ("shipments",): lambda resource_id: data_provider.fetch_shipment_pool().get_shipments(),
    ("shipments", "id"): lambda resource_id: data_provider.fetch_shipment_pool().get_shipment(resource_id),
    ("shipments", "id", "orders"): lambda resource_id: data_provider.fetch_shipment_pool().get_order_ids_in_shipment(resource_id),
    ("shipments", "id", "items"): lambda resource_id: data_provider.fetch_shipment_pool().get_items_in_shipment(resource_id),
}
PUT_FUNCTIONS = {
    # warehouses
    ("warehouses", "id"): lambda resource_id, updated_warehouse: (
        data_provider.fetch_warehouse_pool().update_warehouse(
            resource_id, updated_warehouse
        ),
        data_provider.fetch_warehouse_pool().save()
    ),
    # locations
    ("locations", "id"): lambda resource_id, updated_locatioon: (
        data_provider.fetch_location_pool().update_location(
            resource_id, updated_locatioon
        ),
        data_provider.fetch_location_pool().save()
    ),
    # transfers
    ("transfers", "id"): lambda resource_id, updated_transfer: (
        data_provider.fetch_transfer_pool().update_transfer(
            resource_id, updated_transfer
        ),
        data_provider.fetch_transfer_pool().save()
    ),
    # items
    ("items", "id"): lambda resource_id, updated_item: (
        data_provider.fetch_item_pool().update_item(
            resource_id, updated_item
        ),
        data_provider.fetch_item_pool().save()
    ),
    # item_lines
    ("item_lines", "id"): lambda resource_id, updated_item_line: (
        data_provider.fetch_item_line_pool().update_item_line(
            resource_id, updated_item_line
        ),
        data_provider.fetch_item_line_pool().save()
    ),
    # item_groups
    ("item_groups", "id"): lambda resource_id, updated_item_group: (
        data_provider.fetch_item_group_pool().update_item_group(
            resource_id, updated_item_group
        ),
        data_provider.fetch_item_group_pool().save()
    ),
    # item_types
    ("item_types", "id"): lambda resource_id, updated_item_type: (
        data_provider.fetch_item_type_pool().update_item_type(
            resource_id, updated_item_type
        ),
        data_provider.fetch_item_type_pool().save()
    ),
    # suppliers
    ("suppliers", "id"): lambda resource_id, updated_supplier: (
        data_provider.fetch_supplier_pool().update_supplier(
            resource_id, updated_supplier
        ),
        data_provider.fetch_supplier_pool().save()
    ),
    # orders
    ("orders", "id"): lambda resource_id, updated_order: (
        data_provider.fetch_order_pool().update_order(
            resource_id, updated_order
        ),
        data_provider.fetch_order_pool().save()
    ),
    ("orders", "id", "items"): lambda resource_id, updated_item_in_order: (
        data_provider.fetch_order_pool().update_items_in_order(
            resource_id, updated_item_in_order
        ),
        data_provider.fetch_order_pool().save()
    ),
    # clients
    ("clients", "id"): lambda resource_id, updated_client: (
        data_provider.fetch_client_pool().update_client(
            resource_id, updated_client
        ),
        data_provider.fetch_client_pool().save()
    ),
    # shipments
    ("shipments", "id"): lambda resource_id, updated_shipment: (
        data_provider.fetch_shipment_pool().update_shipment(
            resource_id, updated_shipment
        ),
        data_provider.fetch_shipment_pool().save()
    ),
    ("shipments", "id", "orders"): lambda resource_id, updated_order_in_shipment: (
        data_provider.fetch_shipment_pool().update_orders_in_shipment(
            resource_id, updated_order_in_shipment
        ),
        data_provider.fetch_shipment_pool().save()
    ),
    ("shipments", "id", "items"): lambda resource_id, updated_item_in_shipment: (
        data_provider.fetch_shipment_pool().update_items_in_shipment(
            resource_id, updated_item_in_shipment
        ),
        data_provider.fetch_shipment_pool().save(),
        data_provider.fetch_inventory_pool().save()
    ),
}
POST_FUNCTIONS = {
    ("warehouses",): lambda resource: data_provider.fetch_warehouse_pool().add_warehouse(resource),
    ("locations",): lambda resource: data_provider.fetch_location_pool().add_location(resource),
    ("transfers",): lambda resource: data_provider.fetch_transfer_pool().add_transfer(resource),
    ("items",): lambda resource: data_provider.fetch_item_pool().add_item(resource),
    ("item_lines",): lambda resource: data_provider.fetch_item_line_pool().add_item_line(resource),
    ("item_groups",): lambda resource: data_provider.fetch_item_group_pool().add_item_group(resource),
    ("item_types",): lambda resource: data_provider.fetch_item_type_pool().add_item_type(resource),
    ("inventories",): lambda resource: data_provider.fetch_inventory_pool().add_inventory(resource),
    ("suppliers",): lambda resource: data_provider.fetch_supplier_pool().add_supplier(resource),
    ("orders",): lambda resource: data_provider.fetch_order_pool().add_order(resource),
    ("clients",): lambda resource: data_provider.fetch_client_pool().add_client(resource),
    ("shipments",): lambda resource: data_provider.fetch_shipment_pool().add_shipment(resource),
}
DELETE_FUNCTIONS = {

    "warehouses": lambda id: (data_provider.fetch_warehouse_pool().remove_warehouse(id), data_provider.fetch_warehouse_pool().save()),
    "locations": lambda id: (data_provider.fetch_location_pool().remove_location(id), data_provider.fetch_location_pool().save()),
    "transfers": lambda id: (data_provider.fetch_transfer_pool().remove_transfer(id), data_provider.fetch_transfer_pool().save()),
    "items": lambda id: (data_provider.fetch_item_pool().remove_item(id), data_provider.fetch_item_pool().save()),
    "item_lines": lambda id: (data_provider.fetch_item_line_pool().remove_item_line(id), data_provider.fetch_item_line_pool().save()),
    "item_groups": lambda id: (data_provider.fetch_item_group_pool().remove_item_group(id), data_provider.fetch_item_group_pool().save()),
    "item_types": lambda id: (data_provider.fetch_item_type_pool().remove_item_type(id), data_provider.fetch_item_type_pool().save()),
    "suppliers": lambda id: (data_provider.fetch_supplier_pool().remove_supplier(id), data_provider.fetch_supplier_pool().save()),
    "orders": lambda id: (data_provider.fetch_order_pool().remove_order(id), data_provider.fetch_order_pool().save()),
    "clients": lambda id: (data_provider.fetch_client_pool().remove_client(id), data_provider.fetch_client_pool().save()),
    "shipments": lambda id: (data_provider.fetch_shipment_pool().remove_shipment(id), data_provider.fetch_shipment_pool().save()),
}
