class InvalidRequest(Exception):
    pass


class ToolError(Exception):
    def __init__(self, code=500, message="Tool failed", data=None):
        super().__init__(message)
        self.code = code
        self.data = data or {}
