from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QMenu, QMenuBar, QAction, QFileDialog, QVBoxLayout, QWidget, QPlainTextEdit, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import QEvent, Qt
import sys
import scanner
import Parser
from scanner import Scanner
from Parser import Parser


archivo_seleccionado=''

class ventanaGrafica(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.setWindowTitle('Proyecto 2')
        self.setGeometry(100, 100, 800, 800)

        # Agregar widgets y configuraciones adicionales para la interfaz de usuario
        self.iniciarUI()
        QApplication.instance().installEventFilter(self)  #Se inicializa la instancia para el cursor X y Y
    
    #Parametros de la interfaz grafica
    def iniciarUI(self):
        #Area de editor de texto
        self.cajaTexto = QPlainTextEdit(self)
        self.cajaTexto.setFont(QFont("Candara", 12))
        self.cajaTexto.setStyleSheet('''
            QPlainTextEdit {
                background-color: #252526;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
        ''')
        self.setCentralWidget(self.cajaTexto)
        
        #Label del cursor en X y Y
        self.label_posicion = QLabel(self)
        self.label_posicion.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_posicion.setStyleSheet('font-size: 12px; font-family: Arial; color: gray;')
        self.statusBar().addPermanentWidget(self.label_posicion)
        self.label_posicion.setText('Posición: (0,0)')
        

        # Area de visualización de sentencias
        self.visorTraductor = QTextEdit(self)
        self.visorTraductor.setReadOnly(True)
        self.widgetTraductor = QDockWidget("Sentencias para MongoDB", self)
        self.widgetTraductor.setStyleSheet('''
            QDockWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
        ''')
        self.widgetTraductor.setWidget(self.visorTraductor)
        self.addDockWidget(2, self.widgetTraductor)

        # Agregar tabla de tokens
        self.tablaTokens = QTableWidget(self)
        self.tablaTokens.setStyleSheet('''
            QDockWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
        ''')
        self.tablaTokens.setColumnCount(4)
        self.tablaTokens.setHorizontalHeaderLabels(['No.', 'Tipo', 'Linea', 'Lexema'])
        self.widgetTokens = QDockWidget("Tokens", self)
        self.widgetTokens.setStyleSheet('''
            QDockWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
        ''')
        self.widgetTokens.setWidget(self.tablaTokens)
        self.addDockWidget(2, self.widgetTokens)

        # Area de errores
        self.tablaErrores = QTableWidget(self)
        self.tablaErrores.setColumnCount(5)
        self.tablaErrores.setHorizontalHeaderLabels(['Tipo', 'Linea', 'Columna', 'Token', 'Descripcion'])
        self.widgetErrores = QDockWidget("Errores", self)
        self.widgetErrores.setStyleSheet('''
            QDockWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
        ''')
        self.widgetErrores.setWidget(self.tablaErrores)
        self.addDockWidget(2, self.widgetErrores)

        # Menu Archivo
        self.menuArchivo = QMenu("Archivo", self)
        self.menuArchivo.setStyleSheet('''
    QMenu {
        background-color: #2F2F2F;
        color: #F8F8F8;
    }
    QMenu::item {
        padding: 2px 20px 2px 20px;
    }
    QMenu::item:selected {
        background-color: #3E3E3E;
    }
''')
        self.menuAnalisis = QMenu("Análisis", self)
        self.menuAnalisis.setStyleSheet('''
    QMenu {
        background-color: #2F2F2F;
        color: #F8F8F8;
    }
    QMenu::item {
        padding: 2px 20px 2px 20px;
    }
    QMenu::item:selected {
        background-color: #3E3E3E;
    }
''')
        self.menuVer = QMenu("Ver", self)
        self.menuVer.setStyleSheet('''
    QMenu {
        background-color: #2F2F2F;
        color: #F8F8F8;
    }
    QMenu::item {
        padding: 2px 20px 2px 20px;
    }
    QMenu::item:selected {
        background-color: #3E3E3E;
    }
''')

        #Menu para Archivo
        self.accionNuevo = QAction("Nuevo", self)
        self.accionAbrir = QAction("Abrir", self)
        self.accionGuardar = QAction("Guardar", self)
        self.accionGuardarComo = QAction("Guardar como", self)
        self.accionSalir = QAction("Salir", self)

        self.menuArchivo.addAction(self.accionNuevo)
        self.menuArchivo.addAction(self.accionAbrir)
        self.menuArchivo.addAction(self.accionGuardar)
        self.menuArchivo.addAction(self.accionGuardarComo)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.accionSalir)

        #Menu para Analisis
        self.accionAnalizar = QAction("Generar sentencias MongoDB", self)
        self.menuAnalisis.addAction(self.accionAnalizar)

        #Menu para Ver
        self.accionVerTokens = QAction("Tokens", self)
        self.menuVer.addAction(self.accionVerTokens)

        # Se añaden los menus a la barra de Menus
        self.barraMenu = QMenuBar(self)
        self.barraMenu.addMenu(self.menuArchivo)
        self.barraMenu.addMenu(self.menuAnalisis)
        self.barraMenu.addMenu(self.menuVer)
        self.setMenuBar(self.barraMenu)

        #Se realizan las acciones de las funciones
        self.accionAbrir.triggered.connect(self.abrirArchivo)
        self.accionGuardar.triggered.connect(self.guardarArchivo)
        self.accionGuardarComo.triggered.connect(self.guardarArchivoComo)
        self.accionNuevo.triggered.connect(self.nuevoArchivo)
        self.accionSalir.triggered.connect(self.close)
        self.accionAnalizar.triggered.connect(self.analizar)
        self.accionVerTokens.triggered.connect(self.mostrarTokens)

    def actualizar_posicion(self, event):
        if event.type() == QEvent.MouseMove:
            cursor = QCursor()
            pos = cursor.pos()
            if self.rect().contains(self.mapFromGlobal(pos)):
                x = pos.x() - self.geometry().x()
                y = pos.y() - self.geometry().y()
                self.label_posicion.setText(f'Posición: ({x},{y})')

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if self.rect().contains(self.mapFromGlobal(event.pos())):
                self.actualizar_posicion(event)
        return super().eventFilter(source, event)
    
    def nuevoArchivo(self):
        if self.cajaTexto.document().isModified():
            pass 

        self.cajaTexto.clear()

    def abrirArchivo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.cajaTexto.setPlainText(file.read())
                global archivo_seleccionado 
                archivo_seleccionado = file_name #Se guardar el directorio exacto del archivo

    def guardarArchivo(self):
        global archivo_seleccionado
        if not self.cajaTexto.document().isModified():
            return
        if archivo_seleccionado:
            with open(archivo_seleccionado, 'w', encoding='utf-8') as file:
                file.write(self.cajaTexto.toPlainText())

    def guardarArchivoComo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.cajaTexto.toPlainText())

    def analizar(self):
        input_str = self.cajaTexto.toPlainText()
        scanner_instance = scanner.Scanner(input_str)
        tokens = scanner_instance.initToken()  # Obtener los tokens
        parser = Parser(tokens)  # Crear una instancia del analizador con los tokens

        try:
            result = parser.parse()
            print(result)

            expresionesMongo = []
            for i in result:
                if i[0] == "CREAR_DB":
                    expresionesMongo.append(f"use('{i[1]}')")
                    print("CREAR_DB:", i[1])
                elif i[0] == "ELIMINAR_DB":
                    expresionesMongo.append(f"db.dropDatabase('{i[1]}')")
                    print("ELIMINAR_DB")
                elif i[0] == "CREAR_COLECCION":
                    expresionesMongo.append(f"db.createCollection('{i[1]}')")
                    print("CREAR_COLECCION:", i[1])
                elif i[0] == "ELIMINAR_COLECCION":
                    expresionesMongo.append(f"db.{i[1]}.drop()")
                elif i[0] == "INSERTAR_UNICO":
                    expresionesMongo.append(f"db.{i[1]}.insertOne({i[2]})")
                elif i[0] == "ACTUALIZAR_UNICO":
                    expresionesMongo.append(f"db.{i[1]}.updateOne({i[2]}, {i[3]})")
                elif i[0] == "ELIMINAR_UNICO":
                    expresionesMongo.append(f"db.{i[1]}.deleteOne({i[2]})")
                elif i[0] == "BUSCAR_TODO":
                    expresionesMongo.append(f"db.{i[1]}.find()")
                elif i[0] == "BUSCAR_UNICO":
                    expresionesMongo.append(f"db.{i[1]}.findOne()")

            self.visorTraductor.setPlainText("\n".join(expresionesMongo))
            self.mostrarTokens(parser.tokens)
            self.tablaTokens.update()
        except Exception as e:
            self.actualizarTablaError(f"Error inesperado: {str(e)}")
            self.tablaErrores.update()
        print("Resultados:", result)

    def actualizarTablaError(self, error_msg):
        self.tablaErrores.setRowCount(1)
        self.tablaErrores.setItem(0, 0, QTableWidgetItem("Error"))
        self.tablaErrores.setItem(0, 1, QTableWidgetItem("-"))
        self.tablaErrores.setItem(0, 2, QTableWidgetItem("-"))
        self.tablaErrores.setItem(0, 3, QTableWidgetItem("-"))
        self.tablaErrores.setItem(0, 4, QTableWidgetItem(error_msg))

    def mostrarTokens(self, tokens):
        scanner = Scanner(self.cajaTexto.toPlainText())
        tokens = scanner.initToken()
        print("Tokens:", tokens)  # Imprime la variable tokens aquí para ver su valor
        
        if isinstance(tokens, list):
            self.tablaTokens.setRowCount(len(tokens))
            for i, token in enumerate(tokens):
                self.tablaTokens.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.tablaTokens.setItem(i, 1, QTableWidgetItem(token[0]))
                self.tablaTokens.setItem(i, 2, QTableWidgetItem(str(token[2])))
                self.tablaTokens.setItem(i, 3, QTableWidgetItem(token[1]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = ventanaGrafica()
    main_win.show()
    sys.exit(app.exec_())