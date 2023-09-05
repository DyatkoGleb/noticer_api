from fastapi.responses import JSONResponse

class ErrorResponse:
    def __init__(self, error: str):
        self.success = False
        self.error = error

    def get(self):
        response_data = {"success": self.success, "error": self.error}
        return JSONResponse(content=response_data, status_code=400)