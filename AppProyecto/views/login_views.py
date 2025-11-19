from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from AppProyecto.models import Usuario


def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')

        # Validar que ambos campos están presentes
        if not nombre_usuario or not contrasena:
            error_message = "Por favor, ingrese su nombre de usuario y contraseña."
            return render(request, 'login.html', {'error': error_message})

        # Obtener el usuario por nombre de usuario
        try:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
        except Usuario.DoesNotExist:
            error_message = "Credenciales inválidas."
            return render(request, 'login.html', {'error': error_message})

        # Verificar la contraseña
        if check_password(contrasena, usuario.contrasena):
            # Almacenar información del usuario en la sesión
            request.session['user_id'] = usuario.id_usuario
            request.session.save()  # Asegurar que la sesión se guarde
            
            # Redirigir al home después de validar el login
            return redirect('home')  # Asegúrate de que 'home' esté definido en tus URLs
        else:
            error_message = "Credenciales inválidas."
            return render(request, 'login.html', {'error': error_message})

    return render(request, 'login.html')
