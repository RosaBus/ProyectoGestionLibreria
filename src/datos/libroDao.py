
from src.datos.conexiones import Conexiones
from src.dominio.libro import Libro # Asumiendo que la clase 'Libro' está definida en otro lugar

class LibroDao:
    """
    Objeto de Acceso a Datos (DAO) para la entidad Libro.
    Gestiona las operaciones de base de datos para los libros, incluyendo
    inserción, selección, actualización y eliminación.
    """

    # Consultas SQL utilizadas para las operaciones de base de datos
    _INSERT = ("INSERT INTO Libro(Codigo, Nombre, Precio, Cantidad, Autor, Edicion, Isbn) values "
               "(?, ?, ?, ?, ?, ?, ?)")
    _ERROR = -1  # Código de error estándar devuelto por los métodos
    _SELECT = ("select Codigo, Nombre, Precio, Cantidad, Autor, Edicion, Isbn from Libro "
               "where Codigo = ?")
    _UPDATE = ("update Libro set Nombre=?, Precio=?, Cantidad=?, "
               "Autor=?, Edicion=?, Isbn=? where Codigo=?")
    _DELETE = "delete from Libro where Codigo = ?"

    @classmethod
    def insertar_libro(cls, libro: Libro) -> int:
        """
        Inserta un nuevo registro de libro en la base de datos.

        Args:
            libro (Libro): El objeto Libro que contiene los detalles del libro
                           (codigo, nombre, precio, cantidad, autor, edicion, Isbn).

        Returns:
            int: El número de filas insertadas (normalmente 1 si tiene éxito),
                 o _ERROR (-1) si ocurre una excepción.
        """
        try:
            # Utiliza un gestor de contexto para el cursor de la base de datos,
            # asegurando que se cierre correctamente.
            with Conexiones.obtenerCursor() as cursor:
                datos = (libro.codigo, libro.nombre, libro.precio, libro.cantidad,
                         libro.autor, libro.edicion, libro.Isbn)
                retorno = cursor.execute(cls._INSERT, datos)
                # rowcount devuelve el número de filas afectadas por la declaración DML.
                return retorno.rowcount
        except Exception as e:
            # Imprime la excepción para fines de depuración. En un sistema de producción,
            # considera usar un framework de logging adecuado.
            print(f"Error al insertar libro: {e}")
            return cls._ERROR

    @classmethod
    def seleccionar_libro(cls, codigo: str) -> Libro | None:
        """
        Selecciona un único registro de libro de la base de datos basándose en su código.

        Args:
            codigo (str): El código único del libro a recuperar.

        Returns:
            Libro: Un objeto Libro poblado con los datos recuperados si se encuentra.
            None: Si el libro no se encuentra o si ocurre un error.
        """
        try:
            with Conexiones.obtenerCursor() as cursor:
                datos = (codigo,)
                # fetchone() recupera una sola fila de datos.
                retorno = cursor.execute(cls._SELECT, datos).fetchone()

                if retorno: # Verifica si se encontró un registro
                    # Desempaqueta la tupla devuelta por fetchone() en un objeto Libro.
                    libro = Libro(
                        codigo=retorno[0],
                        nombre=retorno[1],
                        precio=retorno[2],
                        cantidad=retorno[3],
                        autor=retorno[4],
                        edicion=retorno[5],
                        Isbn=retorno[6],
                    )
                    return libro
                else:
                    return None # No se encontró ningún libro con el código dado

        except Exception as e:
            print(f"Error al seleccionar libro: {e}")
            # Para operaciones SELECT, el rollback no suele ser estrictamente necesario
            # a menos que las operaciones del cursor afecten de alguna manera el estado de la transacción.
            # Sin embargo, no hace daño. Asumiendo que Conexiones maneja el commit/rollback
            # correctamente para su cursor.
            if hasattr(cursor, 'rollback'): # Llama a rollback de forma segura si está disponible
                 cursor.rollback()
            return None

    @classmethod
    def actualizar_libro(cls, libro: Libro) -> int:
        """
        Actualiza un registro de libro existente en la base de datos.

        Args:
            libro (Libro): El objeto Libro que contiene los detalles actualizados.
                           El atributo 'codigo' se utiliza para identificar el libro.

        Returns:
            int: El número de filas actualizadas (normalmente 1 si tiene éxito),
                 o _ERROR (-1) si ocurre una excepción.
        """
        try:
            # Conversión explícita a float e int para mayor robustez, asumiendo que estos tipos
            # son esperados por la columna de la base de datos.
            precio = float(libro.precio)
            cantidad = int(libro.cantidad)

            with Conexiones.obtenerCursor() as cursor:
                datos = (
                    libro.nombre, precio, cantidad, libro.autor,
                    libro.edicion, libro.Isbn, libro.codigo
                )
                retorno = cursor.execute(cls._UPDATE, datos)
                return retorno.rowcount
        except Exception as e:
            print(f"Error al actualizar libro: {e}")
            return cls._ERROR

    @classmethod
    def eliminar_libro(cls, codigo: str) -> int:
        """
        Elimina un registro de libro de la base de datos basándose en su código.

        Args:
            codigo (str): El código único del libro a eliminar.

        Returns:
            int: El número de filas eliminadas (normalmente 1 si tiene éxito),
                 o _ERROR (-1) si ocurre una excepción.
        """
        try:
            with Conexiones.obtenerCursor() as cursor:
                # Asegura que el código se trate como una cadena para el parámetro de la consulta.
                # Dependiendo de tu controlador de DB, la conversión explícita podría ser crucial o redundante.
                datos = (str(codigo),)
                # print(f"Intentando eliminar libro con código: {codigo} (Tipo: {type(codigo)})") # Para depuración
                retorno = cursor.execute(cls._DELETE, datos)
                return retorno.rowcount

        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            # print(f"Tipo de error: {type(e)}") # Para depuración
            # Asegura que se llame a rollback si el cursor es parte de un contexto transaccional.
            if hasattr(cursor, 'rollback'):
                cursor.rollback()
            return cls._ERROR

# --- Ejemplo de Uso ---
if __name__ == '__main__':
    # Este bloque demuestra cómo podrías usar la clase LibroDao.
    # Asegúrate de que tus clases 'Conexiones' y 'Libro' estén configuradas
    # y accesibles correctamente para que este ejemplo se ejecute.

    # Ejemplo: Intentando eliminar un libro
    print("--- Probando eliminar_libro ---")
    codigo_libro_a_eliminar = '0000000003'
    filas_eliminadas = LibroDao.eliminar_libro(codigo_libro_a_eliminar)

    if filas_eliminadas == LibroDao._ERROR:
        print(f"Ocurrió un error al intentar eliminar el libro con código '{codigo_libro_a_eliminar}'.")
    elif filas_eliminadas == 0:
        print(f"No se encontró el libro con código '{codigo_libro_a_eliminar}' para eliminar.")
    else:
        print(f"Libro con código '{codigo_libro_a_eliminar}' eliminado exitosamente. Filas afectadas: {filas_eliminadas}")

    print("\n--- Probando insertar_libro (Necesita un objeto Libro) ---")
    # Para probar la inserción, primero necesitarías crear un objeto Libro.
    # from src.dominio.libro import Libro # Asegúrate de que Libro esté importado
    # nuevo_libro = Libro(
    #     codigo='0000000004',
    #     nombre='El Gran Gatsby',
    #     precio=15.99,
    #     cantidad=10,
    #     autor='F. Scott Fitzgerald',
    #     edicion='Primera',
    #     Isbn='978-0743273565'
    # )
    # filas_insertadas = LibroDao.insertar_libro(nuevo_libro)
    # if filas_insertadas == LibroDao._ERROR:
    #     print("Error al insertar el nuevo libro.")
    # else:
    #     print(f"Libro '{nuevo_libro.nombre}' insertado exitosamente. Filas afectadas: {filas_insertadas}")

    print("\n--- Probando seleccionar_libro ---")
    # libro_encontrado = LibroDao.seleccionar_libro('0000000001') # Asumiendo que este código existe
    # if libro_encontrado:
    #     print(f"Libro encontrado: {libro_encontrado.nombre} por {libro_encontrado.autor}, Precio: {libro_encontrado.precio}")
    # else:
    #     print("Libro no encontrado o error al seleccionar.")

    print("\n--- Probando actualizar_libro ---")
    # Si recuperaste un libro y quieres actualizarlo:
    # libro_a_actualizar = LibroDao.seleccionar_libro('0000000001')
    # if libro_a_actualizar:
    #     libro_a_actualizar.precio = 18.50
    #     filas_actualizadas = LibroDao.actualizar_libro(libro_a_actualizar)
    #     if filas_actualizadas == LibroDao._ERROR:
    #         print("Error al actualizar el libro.")
    #     else:
    #         print(f"Libro '{libro_a_actualizar.nombre}' actualizado exitosamente. Filas afectadas: {filas_actualizadas}")
