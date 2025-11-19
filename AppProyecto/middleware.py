from django.shortcuts import redirect

class SessionRequiredMiddleware:
    """
    Middleware que obliga a tener la sesión iniciada
    para acceder a cualquier URL protegida.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Rutas públicas (no requieren inicio de sesión)
        # Verificar exactamente la ruta raíz
        if path == "/" or path == "":
            return self.get_response(request)
        
        # Verificar rutas públicas específicas (con y sin barra final)
        rutas_publicas = [
            "/login",
            "/recuperar-contrasena",
        ]
        
        # Normalizar path para comparación (sin barra final)
        path_normalizado = path.rstrip('/')
        
        # Verificar si la ruta es una ruta pública exacta
        if path_normalizado in rutas_publicas or path in rutas_publicas:
            return self.get_response(request)
        
        # Permitir rutas de restablecimiento de contraseña (con token)
        if path.startswith("/restablecer-contrasena/"):
            return self.get_response(request)
        
        # Permitir archivos estáticos y media
        if path.startswith("/static/") or path.startswith("/media/"):
            return self.get_response(request)

        # Verificar si el usuario tiene sesión (usando 'user_id' que es lo que se guarda en login_views.py)
        # Asegurarse de que la sesión esté activa
        if not hasattr(request, 'session'):
            return redirect("login")
        
        user_id = request.session.get("user_id")
        if not user_id:
            # Redirigir al login si no está autenticado
            return redirect("login")

        # Si tiene sesión → continuar
        return self.get_response(request)
