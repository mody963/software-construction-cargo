SCHEMAS = {
    "warehouses": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "code": {"type": "string"},
            "name": {"type": "string"},
            "address": {"type": "string"},
            "city": {"type": "string"},
            "zip_code": {"type": "string"},
            "province": {"type": "string"},
            "country": {"type": "string"},
            "contact_name": {"type": ["string", "null"]},
            "contact_phone": {"type": ["string", "null"]},
            "contact_email": {"type": ["string", "null"]},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "code", "name", "address", "city", "country"],
        "additionalProperties": True # True gelaten mocht er een onverwacht extra veld in de data zitten
    },

    "locations": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "warehouse_id": {"type": "integer"},
            "code": {"type": "string"},
            "name": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "warehouse_id", "code", "name"],
        "additionalProperties": True
    },

    "clients": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "address": {"type": "string"},
            "city": {"type": "string"},
            "zip_code": {"type": "string"},
            "province": {"type": "string"},
            "country": {"type": "string"},
            "contact_name": {"type": ["string", "null"]},
            "contact_phone": {"type": ["string", "null"]},
            "contact_email": {"type": ["string", "null"]},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "name", "address", "city", "country"],
        "additionalProperties": True
    },

    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "code": {"type": "string"}, # In de documentatie heet de resource 'code', in het model 'name'
            "description": {"type": "string"},
            "barcode": {"type": "string"},
            "model_number": {"type": "string"},
            "commodity_code": {"type": ["string", "integer"]}, 
            "unit_weight": {"type": "number"}, # Number is voor floats/decimals
            "item_line_id": {"type": "integer"},
            "item_group_id": {"type": "integer"},
            "item_type_id": {"type": "integer"},
            "min_purchase_qty": {"type": "integer"},
            "case_size": {"type": "integer"},
            "packaging_type": {"type": "string"},
            "order_multiple": {"type": "integer"},
            "supplier_id": {"type": "integer"},
            "supplier_sku": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "description", "item_line_id", "item_group_id", "item_type_id", "supplier_id"],
        "additionalProperties": True 
    },

    "item_lines": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "name", "description"],
        "additionalProperties": True
    },

    "item_groups": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "name", "description"],
        "additionalProperties": True
    },

    "item_types": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "name", "description"],
        "additionalProperties": True
    },

    "inventories": {
        "type": "object",
        "properties": {
            "item_id": {"type": "integer"},
            "location_id": {"type": "integer"},
            "quantity_on_hand": {"type": "integer"},
            "quantity_expected": {"type": "integer"},
            "quantity_ordered": {"type": "integer"},
            "quantity_allocated": {"type": "integer"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["item_id", "location_id", "quantity_on_hand"],
        "additionalProperties": True
    },

    "suppliers": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "code": {"type": "string"},
            "name": {"type": "string"},
            "address": {"type": "string"},
            "city": {"type": "string"},
            "zip_code": {"type": "string"},
            "province": {"type": "string"},
            "country": {"type": "string"},
            "contact_name": {"type": ["string", "null"]},
            "phone_number": {"type": ["string", "null"]},
            "reference": {"type": ["string", "null"]},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        },
        "required": ["id", "code", "name", "address", "city", "country"],
        "additionalProperties": True
    },

    "orders": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "client_id": {"type": "integer"},
            "order_date": {"type": "string"},
            "request_date": {"type": "string"},
            "reference": {"type": "string"},
            "customer_po_number": {"type": "string"},
            "order_status": {"type": "string"},
            "shipping_notes": {"type": ["string", "null"]},
            "warehouse_id": {"type": "integer"},
            "ship_to_client_id": {"type": "integer"},
            "bill_to_client_id": {"type": "integer"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"},
                        "amount": {"type": "integer"}
                    },
                    "required": ["item_id", "amount"]
                }
            }
        },
        "required": ["id", "client_id", "order_status", "warehouse_id"],
        "additionalProperties": True
    },

    "shipments": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "reference": {"type": "string"},
            "order_id": {"type": "integer"},
            "shipment_date": {"type": "string"},
            "shipment_type": {"type": "string"},
            "shipment_status": {"type": "string"},
            "carrier_name": {"type": "string"},
            "shipping_method": {"type": "string"},
            "payment_type": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"},
                        "amount": {"type": "integer"}
                    },
                    "required": ["item_id", "amount"]
                }
            }
        },
        "required": ["id", "reference", "order_id", "shipment_status"],
        "additionalProperties": True
    },

    "transfers": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "reference": {"type": "string"},
            "transfer_from": {"type": "integer"},
            "transfer_to": {"type": "integer"},
            "transfer_status": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"},
                        "amount": {"type": "integer"}
                    },
                    "required": ["item_id", "amount"]
                }
            }
        },
        "required": ["id", "reference", "transfer_status"],
        "additionalProperties": True
    }
}
