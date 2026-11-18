class UserView:
    def show_message(message: str, status: int, success: bool = False) -> dict:
        return {
            "success": success,
            "message": message
        }, status