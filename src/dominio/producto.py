# Integrantes del Grupo#1 : Joselyne Paulette Játiva Vera
#                           Joselin Mariuxi Rodriguez Saldaña
#                           Jemina Victoria Suárez Veintimilla
#                           Rosa Angelica Bustamante Moreira

class Producto:
    """
    Esta clase representa un producto general de la librería. La usamos como base
    para crear otros productos más específicos.
    """
    def __init__(self, codigo, nombre, precio, cantidad):
        """
        Aquí estamos definiendo el constructor de la clase Producto. Es decir,
        cuando se crea un nuevo producto, le doy su código, nombre, precio y cantidad.

        Args:
            codigo (str): Código único del producto.
            nombre (str): Nombre del producto.
            precio (float): Precio unitario del producto.
            cantidad (int): Cantidad disponible en inventario.
        """
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._cantidad = cantidad

    # Getters y setters como propiedades
    @property
    def codigo(self):
        """Getter para el código del producto."""
        return self._codigo

    @codigo.setter
    def codigo(self, nuevo_codigo):
        """Setter para el código del producto."""
        self._codigo = nuevo_codigo

    @property
    def nombre(self):
        """Getter para el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Setter para el nombre del producto."""
        self._nombre = nuevo_nombre

    @property
    def precio(self):
        """Getter para el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        """Setter para el precio del producto."""
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            print("El precio no puede ser negativo.")

    @property
    def cantidad(self):
        """Getter para la cantidad en inventario del producto."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        """Setter para la cantidad en inventario del producto."""
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            print("La cantidad no puede ser negativa.")

