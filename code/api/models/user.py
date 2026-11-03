class EndpointAccess:
    def __init__(
        self,
        get: bool,
        post: bool,
        put: bool,
        delete: bool
    ):
        self.get = get
        self.post = post
        self.put = put
        self.delete = delete


class User:
    def __init__(
        self,
        api_key: str,
        app: str,
        endpoint_access: dict[str, EndpointAccess]
    ):
        self.api_key = api_key
        self.app = app
        self.endpoint_access = endpoint_access

