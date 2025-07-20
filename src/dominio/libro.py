# Integrantes del Grupo#1 : Joselyne Paulette Játiva Vera
#                           Joselin Mariuxi Rodriguez Saldaña
#                           Jemina Victoria Suárez Veintimilla
#                           Rosa Angelica Bustamante Moreira

from src.dominio.producto import Producto

class Libro(Producto):
    """
    Esta clase representa un libro. Hereda de Producto y le agregamos detalles propios,
    como el autor, la edición y el ISBN
    """
    def __init__(self, codigo, nombre, precio, cantidad, autor, edicion, Isbn):
        """
        Constructor de la clase Libro.

        Args:
            codigo  Código único del libro.
            nombre (str): Nombre del libro.
            precio (float): Precio unitario del libro.
            cantidad (int): Cantidad disponible en inventario.
            autor (str): Autor del libro.
            edicion (str): Edición del libro.
            isbn : ISBN del libro.
        """
        super().__init__(codigo, nombre, precio, cantidad)
        self._autor = autor
        self._edicion = edicion
        self._isbn = Isbn

    # Getters y setters como propiedades
    @property
    def autor(self):
        """Getter para el autor del libro."""
        return self._autor

    @autor.setter
    def autor(self, nuevo_autor):
        """Setter para el autor del libro."""
        self._autor = nuevo_autor

    @property
    def edicion(self):
        """Getter para la edición del libro."""
        return self._edicion

    @edicion.setter
    def edicion(self, nueva_edicion):
        """Setter para la edición del libro."""
        self._edicion = nueva_edicion

    @property
    def Isbn(self):
        """Getter para el ISBN del libro."""
        return self._isbn

    @Isbn.setter
    def Isbn(self, nuevo_isbn):
        """Setter para el ISBN del libro."""
        self._isbn = nuevo_isbn


