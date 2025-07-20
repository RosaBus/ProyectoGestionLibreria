import sys
from PySide6.QtWidgets import QApplication
from src.servicio.libro import LibroServicio

app = QApplication ()
Ui_vtnLibro = LibroServicio()
Ui_vtnLibro.show()
sys.exit(app.exec())