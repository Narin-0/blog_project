class AuthStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print(f"Пользователь {request.user.username} авторизован.")
        else:
            print("Анонимный пользователь.")
        
        response = self.get_response(request)
        return response