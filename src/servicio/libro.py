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
    #INICIALIZACION DE LOS METODOS LLAMO TODOS LOS METODOS
    def __init__(self):
        super(LibroServicio, self).__init__()
        self.ui= Ui_vtnLibro()
        self.ui.setupUi(self)
        self.ui.btnNuevo.clicked.connect(self.nuevo)
        self.ui.btnLimpiar.clicked.connect(self.limpiar)
        self.ui.btnBorrar.clicked.connect(self.borrar)
        self.ui.btnActualizar.clicked.connect(self.actualizar)
        self.ui.btnLibrobuscar.clicked.connect(self.buscarLibro)
        self.ui.txtCodigo.setValidator(QIntValidator())
        self.ui.txtPrecio.setValidator(QDoubleValidator())
        self.ui.txtCantidad.setValidator(QIntValidator())
        self.ui.txtIsbn.setValidator(QIntValidator())


    def nuevo(self):
        if (self.ui.txtCodigo.text() == "" or self.ui.txtNombre.text() == ""
                or self.ui.txtPrecio.text() == "" or self.ui.txtCantidad.text() == ""
                or self.ui.txtAutor.text() == "" or len(self.ui.txtIsbn.text()) < 10
                or self.ui.txtIsbn == "" or self.ui.txtEdicion.text() == ""):
            QMessageBox.warning(self, 'Advertencia',
                            "COMPLETAR DATOS")  # MENSAJE DE ADVERTENCIA POR CONSOLA self significa se levante al frente de ventana principal
        # QMessageBox.critical(self,'Titulo Ventana','Mensaje') #

        else:

            precio_str = self.ui.txtPrecio.text().replace(',', '.')
            try:
                precio = float(precio_str)
            except ValueError:
                QMessageBox.critical(self, 'ERROR', "El precio debe ser un número válido (ej. 10.50).")
                return
            libro = Libro(codigo=self.ui.txtCodigo.text(),
                          nombre=self.ui.txtNombre.text(),
                          precio= precio,
                          cantidad=self.ui.txtCantidad.text(),
                          autor=self.ui.txtAutor.text(),
                          edicion =self.ui.txtEdicion.text(),
                          Isbn = self.ui.txtIsbn.text(),)

            if LibroDao.insertar_libro(libro) == -1:
                QMessageBox.critical(self, 'ERROR', "ERROR AL GRABAR")
            else:
                self.ui.statusbar.showMessage("Se Guardo correctamente", 3000)
                self.limpiar()


    def actualizar(self):
        if (self.ui.txtCodigo.text() == "" or self.ui.txtNombre.text() == ""
                or self.ui.txtPrecio.text() == "" or self.ui.txtCantidad.text() == ""
                or self.ui.txtAutor.text() == "" or len(self.ui.txtIsbn.text()) < 10 or self.ui.txtIsbn.text()==""
                or self.ui.txtEdicion.text() == ""):
            QMessageBox.warning(self, 'Advertencia',
                            "COMPLETAR DATOS")  # MENSAJE DE ADVERTENCIA POR CONSOLA self significa se levante al frente de ventana principal

        else:

            precio_str = self.ui.txtPrecio.text().replace(',', '.')
            try:
                precio = float(precio_str)
            except ValueError:
                QMessageBox.critical(self, 'ERROR', "El precio debe ser un número válido (ej. 10.50).")
                return

            libro = Libro(codigo=self.ui.txtCodigo.text(),
                          nombre=self.ui.txtNombre.text(),
                          precio=precio,
                          cantidad=self.ui.txtCantidad.text(),
                          autor=self.ui.txtAutor.text(),
                          edicion =self.ui.txtEdicion.text(),
                          Isbn = self.ui.txtIsbn.text(),
                          )

            if LibroDao.actualizar_libro(libro) == -1:
                QMessageBox.critical(self, 'ERROR', "ERROR AL GRABAR")
            else:
                self.ui.statusbar.showMessage("Se Guardo correctamente", 3000)
                self.limpiar()

    def borrar(self):

        if QMessageBox.question(self, "Confirmacion", "Desea borrar el registro") == QMessageBox.Yes:
            retorno = LibroDao.eliminar_libro(self.ui.txtCodigo.text())
            if retorno != -1:
                self.ui.statusbar.showMessage("Registro Eliminado con éxito", 3000)
                self.limpiar()
            else:
                QMessageBox.critical(self, "Error", "No se pudo Eliminar")

    def limpiar(self):
        self.ui.txtCodigo.setText("")
        self.ui.txtNombre.setText("")
        self.ui.txtPrecio.setText("")
        self.ui.txtCantidad.setText("")
        self.ui.txtAutor.setText("")
        self.ui.txtEdicion.setText("")
        self.ui.txtIsbn.setText("")

    def buscarLibro (self):

        if len(self.ui.txtCodigo.text()) < 10:
            QMessageBox.warning(self,'Advertencia',"COMPLETAR DATOS" ) #MENSAJE DE ADVERTENCIA POR CONSOLA self significa se levante al frente de ventana principal
            #QMessageBox.critical(self,'Titulo Ventana','Mensaje') #
        else:
            libros = LibroDao.seleccionar_libro(self.ui.txtCodigo.text())
            if libros :
                self.ui.txtNombre.setText(libros.nombre)
                self.ui.txtPrecio.setText(str(libros.precio))
                self.ui.txtCantidad.setText(str(libros.cantidad))
                self.ui.txtAutor.setText(libros.autor)
                self.ui.txtEdicion.setText(libros.edicion)
                self.ui.txtIsbn.setText(str(libros.Isbn))

            else:
                QMessageBox.warning(self,"Advertencia","No se encontro el Libro que Buscaba")








