from providers import data_provider

from processors import notification_processor

# apparte transfer comit functie
# deze transfer commit functie zorgt er voor dat als er een product van locatie veranderd dit overal juist wordt aan gepast
# zodat er geen fouten in de vooraad kunnen zijn


def handle_transfer_commit(self, transfer_id):
    transfer_pool = data_provider.fetch_transfer_pool()
    transfer = transfer_pool.get_transfer(transfer_id)

    if transfer is None:
        return int(404)

    from_location_id = transfer["from_location_id"]
    to_location_id = transfer["to_location_id"]
    inventory_pool = data_provider.fetch_inventory_pool()

    for item in transfer["items"]:
        item_id = item["item_id"]
        amount = item["amount"]

        src = inventory_pool.get_inventory(item_id, from_location_id)

        if src is not None:
            src["quantity_on_hand"] -= amount
            inventory_pool.update_inventory(
                item_id, from_location_id, src
            )

        dst = inventory_pool.get_inventory(item_id, to_location_id)

        if dst is not None:
            dst["quantity_on_hand"] += amount
            inventory_pool.update_inventory(
                item_id, to_location_id, dst
            )
        else:
            inventory_pool.add_inventory({
                "item_id": item_id,
                "location_id": to_location_id,
                "quantity_on_hand": amount,
                "quantity_expected": 0,
                "quantity_ordered": 0,
                "quantity_allocated": 0,
            })

    transfer["transfer_status"] = "Processed"
    transfer.pop("items", None)

    transfer_pool.update_transfer(transfer_id, transfer)

    notification_processor.push(
        f"Processed batch transfer with id:{transfer['id']}"
    )

    transfer_pool.save()
    inventory_pool.save()

    return int(200)
