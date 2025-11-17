from AppProyecto.models import Trabajador, Genero
from django.shortcuts import render, redirect, get_object_or_404
from AppProyecto.services.trabajador_service import TrabajadorService
from django.core.paginator import Paginator
from django.db import IntegrityError

def validar_telefono(telefono):
    """Valida el formato básico del teléfono."""
    if not telefono.isdigit() or len(telefono) < 8:
        raise ValueError('El teléfono debe contener solo números y mínimo 8 dígitos')

def listar_trabajadores(request):
    trabajadores_list = Trabajador.objects.all().order_by('nombre')
    paginator = Paginator(trabajadores_list, 5)
    page_number = request.GET.get('page')
    trabajadores_page = paginator.get_page(page_number)
    return render(request, 'trabajadores/lista.html', {'trabajadores': trabajadores_page})

def crear_trabajador(request):
    context = {
        'generos': Genero.objects.all(),
    }
    
    if request.method == "POST":
        try:
            # Obtener y limpiar datos del formulario
            data = {
                "rut": request.POST.get("rut", "").strip(),
                "nombre": request.POST.get("nombre", "").strip(),
                "genero_id": request.POST.get("genero"),
                "direccion": request.POST.get("direccion", "").strip(),
                "telefono": request.POST.get("telefono", "").strip(),
            }
            context['values'] = data  # Mantener los datos en caso de error

            # Validaciones de campos vacíos
            if not data["rut"]:
                raise ValueError("El RUT es requerido")
            if not data["nombre"]:
                raise ValueError("El nombre es requerido")
            if not data["genero_id"]:
                raise ValueError("El género es requerido")
            if not data["telefono"]:
                raise ValueError("El teléfono es requerido")    
            if not data["direccion"]:
                raise ValueError("La dirección es requerida")

            # Validaciones de longitud
            if len(data["nombre"]) > 100:
                raise ValueError("El nombre no puede exceder los 100 caracteres")
            if len(data["direccion"]) > 200:
                raise ValueError("La dirección no puede exceder los 200 caracteres")

            # Validar formato de teléfono
            validar_telefono(data["telefono"])

            # Crear trabajador
            TrabajadorService.crear_trabajador_usuario(data)
            return redirect('listar_trabajadores')

        except ValueError as e:
            context['error'] = str(e)
            return render(request, "trabajadores/formulario.html", context)
        except IntegrityError:
            context['error'] = "Ya existe un trabajador con ese RUT"
            return render(request, "trabajadores/formulario.html", context)
        except Exception as e:
            context['error'] = f"Ocurrió un error inesperado: {str(e)}"
            return render(request, "trabajadores/formulario.html", context)

    return render(request, "trabajadores/formulario.html", context)

def actualizar_trabajador(request, rut):
    trabajador = get_object_or_404(Trabajador, rut=rut)
    context = {
        'trabajador': trabajador,
        'generos': Genero.objects.all()
    }
    
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.POST.get('nombre', '').strip(),
                'genero_id': request.POST.get('genero'),
                'direccion': request.POST.get('direccion', '').strip(),
                'telefono': request.POST.get('telefono', '').strip(),
            }
            context['values'] = data

            # Validaciones de campos vacíos
            if not data['nombre']:
                raise ValueError("El nombre es requerido")
            if not data['genero_id']:
                raise ValueError("El género es requerido")
            if not data['direccion']:
                raise ValueError("La dirección es requerida")
            if not data['telefono']:
                raise ValueError("El teléfono es requerido")

            # Validaciones de longitud
            if len(data['nombre']) > 100:
                raise ValueError("El nombre no puede exceder los 100 caracteres")
            if len(data['direccion']) > 200:
                raise ValueError("La dirección no puede exceder los 200 caracteres")

            # Validar formato de teléfono
            validar_telefono(data['telefono'])

            TrabajadorService.actualizar_trabajador(rut, data)
            return redirect('listar_trabajadores')

        except ValueError as e:
            context['error'] = str(e)
            return render(request, 'trabajadores/formulario.html', context)
        except Exception as e:
            context['error'] = f"Error al actualizar el trabajador: {str(e)}"
            return render(request, 'trabajadores/formulario.html', context)

    return render(request, 'trabajadores/formulario.html', context)

def eliminar_trabajador(request, rut):
    trabajador = TrabajadorService.obtener_trabajador(rut)
    if request.method == 'POST':
        TrabajadorService.eliminar_trabajador(rut)
        return redirect('listar_trabajadores')
    return render(request, 'trabajadores/eliminar.html', {'trabajador': trabajador})




def trabajadores_por_genero_view(request):
    """
    Vista que pasa los datos del servicio al template HTML.
    """
    datos = TrabajadorService.listar_trabajadores_por_genero()
    return render(request, "ProcidimientosAlmacenados/trabajadores_por_genero.html.html", {"datos": datos})