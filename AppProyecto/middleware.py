from django.shortcuts import redirect

class SessionRequiredMiddleware:
    """
    Middleware que obliga a tener la sesión iniciada
    para acceder a cualquier URL protegida.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Rutas públicas (no requieren inicio de sesión)
        rutas_publicas = [
            "",
            "/login",
            "/recuperar-contrasena",
            "/restablecer/",
            "/static/",
        ]

        path = request.path.lower()

        # Permitir rutas públicas
        if any(path.startswith(r) for r in rutas_publicas):
            return self.get_response(request)

        # Verificar si el usuario tiene sesión
        if not request.session.get("usuario_id"):
            return redirect("inicio")  # Nombre de URL del login

        # Si tiene sesión → continuar
        return self.get_response(request)
