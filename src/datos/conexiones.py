import sys
import pyodbc as bd

class Conexiones:
    """
    Clase que gestiona la conexión a la base de datos y la obtención de un cursor.
    """
    # Parámetros de conexión a la base de datos
    _SERVIDOR = 'ALVAREZBUSTAMANTE\\SQL_BUSTAMANTE'  # Dirección del servidor de la base de datos
    _BBDD = 'Libreria'  # Nombre de la base de datos
    _USUARIO = 'sa'  # Usuario para la conexión a la base de datos
    _PASSWORD = '123456789'  # Contraseña del usuario
    _conexiones = None  # Almacena la instancia de la conexión a la base de datos
    _cursor = None  # Almacena la instancia del cursor de la base de datos

    @classmethod
    def obtenerConexion(cls):
        """
        Obtiene y retorna la conexión a la base de datos.
        Si la conexión no existe, la crea utilizando los parámetros definidos en la clase.
        En caso de error durante la conexión, imprime el error y termina la ejecución del programa.

        :return: La instancia de la conexión a la base de datos.
        :rtype: pyodbc.Connection
        """
        if cls._conexiones is None:
            try:
                # Intenta establecer la conexión a la base de datos
                cls._conexiones = bd.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                             cls._SERVIDOR + ';DATABASE=' + cls._BBDD + ';UID=' + cls._USUARIO + ';PWD=' + cls._PASSWORD
                                             + ';TrustServerCertificate=yes')
                # log.debug(f'Conexión exitosa: {cls._conexión}') # Línea para depuración (comentada)
                return cls._conexiones
            except Exception as e:
                # Captura y maneja cualquier excepción que ocurra durante la conexión
                # log.error(f'Ocurrió una excepción al obtener la conexión: {e}') # Línea para depuración (comentada)
                print(f"Error al conectar a la base de datos: {e}")
                sys.exit(1) # Termina el programa con un código de error
        else:
            # Si la conexión ya existe, la retorna
            return cls._conexiones

    @classmethod
    def obtenerCursor(cls):
        """
        Obtiene y retorna un cursor para ejecutar comandos SQL en la base de datos.
        Si el cursor no existe, lo crea a partir de la conexión existente (o la crea si no existe).
        En caso de error al obtener el cursor, imprime el error y termina la ejecución del programa.

        :return: La instancia del cursor de la base de datos.
        :rtype: pyodbc.Cursor
        """
        if cls._cursor is None:
            try:
                # Obtiene la conexión (la creará si no existe) y luego crea un cursor
                cls._cursor = cls.obtenerConexion().cursor()
                # log.debug(f'Se abrió correctamente el cursor: {cls._cursor}') # Línea para depuración (comentada)
                return cls._cursor
            except Exception as e:
                # Captura y maneja cualquier excepción que ocurra al obtener el cursor
                # log.error(f'Ocurrió una excepción al obtener el cursor: {e}') # Línea para depuración (comentada)
                print(f"Error al obtener el cursor de la base de datos: {e}")
                sys.exit(1) # Termina el programa con un código de error
        else:
            # Si el cursor ya existe, lo retorna
            return cls._cursor

if __name__ == '__main__':
    # Este bloque se ejecuta solo si el script se ejecuta directamente (no cuando se importa como módulo)
    print("Intentando obtener conexión a la base de datos...")
    conexion = Conexiones.obtenerConexion()
    print(f"Objeto de conexión: {conexion}")

    print("\nIntentando obtener cursor de la base de datos...")
    cursor = Conexiones.obtenerCursor()
    print(f"Objeto de cursor: {cursor}")
