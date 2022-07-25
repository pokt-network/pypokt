class PortalRPCError(RuntimeError):
    def __init__(self, code, message):
        msg = "The following error was returned from the Portal:\n Code: {} – Message: {}".format(
            code, message
        )
        super().__init__(msg)


class PoktRPCError(RuntimeError):
    def __init__(self, code, message):
        msg = (
            "The following RPC error was encountered:\n Code: {} – Message: {}".format(
                code, message
            )
        )
        super().__init__(msg)
