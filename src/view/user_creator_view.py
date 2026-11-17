class UserCreatorView:
    def show_success_message() -> dict:
        return {
            "success": True,
            "message": "User created successfully"
        }, 201
    
    def show_error_message(message: str) -> dict:
        return {
            "success": False,
            "message": message
        }
