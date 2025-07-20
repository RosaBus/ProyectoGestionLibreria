# Integrantes del Grupo#1 : Joselyne Paulette Játiva Vera
#                           Joselin Mariuxi Rodriguez Saldaña
#                           Jemina Victoria Suárez Veintimilla
#                           Rosa Angelica Bustamante Moreira

from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox
from src.dominio.libro import Libro
from src.datos.libroDao import LibroDao
from src.ui.vtnLibro import Ui_vtnLibro

class LibroServicio(QMainWindow):
    """
    Clase LibroServicio
    ===================

    Esta clase gestiona la lógica de negocio para la administración de libros
    en una interfaz de usuario PySide6. Hereda de QMainWindow para proporcionar
    una ventana principal con funcionalidades CRUD (Crear, Leer, Actualizar, Borrar)
    para los registros de libros.

    Utiliza la clase `Ui_vtnLibro` para la interfaz gráfica y `LibroDao`
    para interactuar con la capa de persistencia de datos.
    """
    def __init__(self):
        """
        Inicializa la ventana principal de LibroServicio, configura la interfaz
        de usuario, conecta las señales de los botones a sus métodos
        correspondientes y establece validadores de entrada para los campos de texto.
        """
        super(LibroServicio, self).__init__()
        self.ui = Ui_vtnLibro()
        self.ui.setupUi(self)

        # Conexión de los botones a sus métodos correspondientes
        self.ui.btnNuevo.clicked.connect(self.nuevo)
        self.ui.btnLimpiar.clicked.connect(self.limpiar)
        self.ui.btnBorrar.clicked.connect(self.borrar)
        self.ui.btnActualizar.clicked.connect(self.actualizar)
        self.ui.btnLibrobuscar.clicked.connect(self.buscarLibro)

        # Configuración de validadores para los campos de entrada
        # Asegura que 'txtCodigo' solo acepte enteros.
        self.ui.txtCodigo.setValidator(QIntValidator())
        # Asegura que 'txtPrecio' solo acepte números decimales.
        self.ui.txtPrecio.setValidator(QDoubleValidator())
        # Asegura que 'txtCantidad' solo acepte enteros.
        self.ui.txtCantidad.setValidator(QIntValidator())
        # Asegura que 'txtIsbn' solo acepte enteros.
        self.ui.txtIsbn.setValidator(QIntValidator())

    def nuevo(self):
        """
        Crea un nuevo registro de libro en la base de datos.

        Realiza las siguientes comprobaciones:
        1. Valida que todos los campos requeridos no estén vacíos.
        2. Valida que el campo 'ISBN' tenga al menos 10 caracteres.
        3. Convierte el precio a un formato de punto flotante, manejando
           comas como separador decimal si es necesario.

        En caso de éxito, muestra un mensaje en la barra de estado y limpia el formulario.
        En caso de error, muestra un mensaje de advertencia o error crítico.
        """
        # Valida que todos los campos obligatorios estén completos
        if (self.ui.txtCodigo.text() == "" or self.ui.txtNombre.text() == ""
                or self.ui.txtPrecio.text() == "" or self.ui.txtCantidad.text() == ""
                or self.ui.txtAutor.text() == "" or len(self.ui.txtIsbn.text()) < 10
                or self.ui.txtIsbn.text() == "" or self.ui.txtEdicion.text() == ""):
            QMessageBox.warning(self, 'Advertencia', "COMPLETAR DATOS PARA CONTINUAR")
            return # Salir de la función si los datos no están completos

        # Reemplaza la coma por un punto para asegurar la correcta conversión a float
        precio_str = self.ui.txtPrecio.text().replace(',', '.')
        try:
            precio = float(precio_str)
        except ValueError:
            QMessageBox.critical(self, 'ERROR', "El precio debe ser un número válido (ej. 10.50).")
            return

        # Crea un objeto Libro con los datos del formulario
        libro = Libro(codigo=self.ui.txtCodigo.text(),
                      nombre=self.ui.txtNombre.text(),
                      precio=precio,
                      cantidad=self.ui.txtCantidad.text(),
                      autor=self.ui.txtAutor.text(),
                      edicion=self.ui.txtEdicion.text(),
                      Isbn=self.ui.txtIsbn.text())

        # Intenta insertar el libro en la base de datos
        if LibroDao.insertar_libro(libro) == -1:
            QMessageBox.critical(self, 'ERROR', "ERROR AL GUARDAR, INTENTE OTRA VEZ")
        else:
            self.ui.statusbar.showMessage("OPERACIÓN NUEVO REALIZADA CON ÉXITO", 3000)
            self.limpiar()

    def actualizar(self):
        """
        Actualiza un registro de libro existente en la base de datos.

        Realiza las mismas validaciones de entrada que el metodo nuevo.
        En caso de éxito, muestra un mensaje en la barra de estado y limpia el formulario.
        En caso de error, muestra un mensaje de advertencia o error crítico.
        """
        # Valida que todos los campos obligatorios estén completos
        if (self.ui.txtCodigo.text() == "" or self.ui.txtNombre.text() == ""
                or self.ui.txtPrecio.text() == "" or self.ui.txtCantidad.text() == ""
                or self.ui.txtAutor.text() == "" or len(self.ui.txtIsbn.text()) < 10
                or self.ui.txtIsbn.text() == "" or self.ui.txtEdicion.text() == ""):
            QMessageBox.warning(self, 'Advertencia', "COMPLETAR LOS DATOS PARA CONTINUAR")
            return

        # Reemplaza la coma por un punto para asegurar la correcta conversión a float
        precio_str = self.ui.txtPrecio.text().replace(',', '.')
        try:
            precio = float(precio_str)
        except ValueError:
            QMessageBox.critical(self, 'ERROR', "El precio debe ser un número válido (ej. 10.50).")
            return

        # Crea un objeto Libro con los datos actualizados del formulario
        libro = Libro(codigo=self.ui.txtCodigo.text(),
                      nombre=self.ui.txtNombre.text(),
                      precio=precio,
                      cantidad=self.ui.txtCantidad.text(),
                      autor=self.ui.txtAutor.text(),
                      edicion=self.ui.txtEdicion.text(),
                      Isbn=self.ui.txtIsbn.text())

        # Intenta actualizar el libro en la base de datos
        if LibroDao.actualizar_libro(libro) == -1:
            QMessageBox.critical(self, 'ERROR', "ERROR AL GUARDAR, INTENTE OTRA VEZ")
        else:
            self.ui.statusbar.showMessage("LA OPERACIÓN ACTUALIZAR REALIZADA CON ÉXITO", 3000)
            self.limpiar()

    def borrar(self):
        """
        Elimina un registro de libro de la base de datos.

        Solicita confirmación al usuario antes de proceder con la eliminación.
        Utiliza el campo `txtCodigo` para identificar el libro a borrar.
        En caso de éxito, muestra un mensaje en la barra de estado y limpia el formulario.
        En caso de error, muestra un mensaje de error crítico.
        """
        if QMessageBox.question(self, "Confirmación", "¿DESEA ELIMINAR EL REGISTRO?") == QMessageBox.Yes:
            retorno = LibroDao.eliminar_libro(self.ui.txtCodigo.text())
            if retorno != -1:
                self.ui.statusbar.showMessage("OPERACIÓN ELIMINAR REALIZADA CON ÉXITO", 3000)
                self.limpiar()
            else:
                QMessageBox.critical(self, "Error", "FALLO AL ELIMINAR, REGISTRO NO EXISTE")

    def buscarLibro(self):
        """
        Busca un libro en la base de datos utilizando el código proporcionado.

        Requiere que el campo `txtCodigo` tenga al menos 10 caracteres para la búsqueda
        (asumiendo que 'codigo' puede ser un identificador largo como un ISBN).
        Si el libro es encontrado, los datos se cargan en los campos del formulario.
        Si no se encuentra, se muestra una advertencia.
        """
        if len(self.ui.txtCodigo.text()) < 10:
            QMessageBox.warning(self, 'Advertencia', "COMPLETAR EL CÓDIGO PARA BUSCAR")
        else:
            libros = LibroDao.seleccionar_libro(self.ui.txtCodigo.text())
            if libros:
                # Carga los datos del libro encontrado en los campos del formulario
                self.ui.txtNombre.setText(libros.nombre)
                self.ui.txtPrecio.setText(str(libros.precio))
                self.ui.txtCantidad.setText(str(libros.cantidad))
                self.ui.txtAutor.setText(libros.autor)
                self.ui.txtEdicion.setText(libros.edicion)
                self.ui.txtIsbn.setText(str(libros.Isbn))
            else:
                QMessageBox.warning(self, "Advertencia", "ERROR EN LA BÚSQUEDA, NO EXISTE EL LIBRO")

    def limpiar(self):
        """
        Limpia todos los campos de texto del formulario de la interfaz de usuario.
        """
        self.ui.txtCodigo.setText("")
        self.ui.txtNombre.setText("")
        self.ui.txtPrecio.setText("")
        self.ui.txtCantidad.setText("")
        self.ui.txtAutor.setText("")
        self.ui.txtEdicion.setText("")
        self.ui.txtIsbn.setText("")

