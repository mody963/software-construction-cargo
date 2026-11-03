from main import ApiRequestHandler


def handle_delete_version_1(self, paths, user):
    # Issue #39 oplossen: Als er geen ID is meegegeven (padlengte 1), is het een collectie
    if len(paths) == 1:
        return int(405)  # 405 Method Not Allowed

    resource = paths[0]

    # Inventories mogen niet verwijderd worden via ID
    if resource == "inventories":
        return int(404)

    delete_action = ApiRequestHandler.DELETE_FUNCTIONS.get(resource)
    if delete_action is None:
        return int(404)

    try:
        resource_id = int(paths[1])
    except ValueError:
        # 500-crash voorkomen bij string ID's
        return int(400)

    # Voer de verwijder-actie en save() uit
    delete_action(resource_id)
    return int(200)
