from AppProyecto.models import Trabajador
from django.db import connection

class TrabajadorRepository:

    @staticmethod
    def obtener_todos():
        return Trabajador.objects.all()

    @staticmethod
    def obtener_por_rut(rut):
        return Trabajador.objects.filter(rut=rut).first()

    @staticmethod
    def create_trabajador(data):

        trabajador = Trabajador.objects.create(**data)
        return trabajador

    @staticmethod
    def actualizar_trabajador(rut, data):
        trabajador = TrabajadorRepository.obtener_por_rut(rut)
        if trabajador:
            for key, value in data.items():
                setattr(trabajador, key, value)
            trabajador.save()
        return trabajador

    @staticmethod
    def eliminar_trabajador(rut):
        trabajador = TrabajadorRepository.obtener_por_rut(rut)
        if trabajador:
            trabajador.delete()


    @staticmethod
    def obtener_trabajadores_por_genero():
        """
        Llama al procedimiento almacenado ContarTrabajadoresPorGenero 
        y devuelve los resultados como una lista de diccionarios.
        """
        with connection.cursor() as cursor:
            cursor.callproc("sp_listar_trabajadores_por_genero")
            resultados = cursor.fetchall()
            columnas = [col[0] for col in cursor.description]
            return [dict(zip(columnas, fila)) for fila in resultados]
