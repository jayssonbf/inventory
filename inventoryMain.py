from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_screen.ui", self)
        self.searchButton.clicked.connect(self.gotoProductScreen)

    def gotoProductScreen(self):
        print(f'Current Index: {widget.currentIndex() + 1}')
        widget.setCurrentIndex(widget.currentIndex()+1)

class ProductScreen(QMainWindow):
    def __init__(self):
        super(ProductScreen, self).__init__()
        uic.loadUi('product_screen.ui', self)
        self.backLink.clicked.connect(lambda: gotoMain(self))
        self.addProduct.clicked.connect(lambda: gotoAddProduct(self))

        def gotoMain(self):
            print(f'Current Index: {widget.currentIndex()-1}')
            widget.setCurrentIndex(widget.currentIndex() - 1)


        def gotoAddProduct(self):
            print(f'Current Index: {widget.currentIndex() + 1}')
            widget.setCurrentIndex(widget.currentIndex() + 1)


class AddScreen(QMainWindow):
    def __init__(self):
        super(AddScreen, self).__init__()
        uic.loadUi('add_screen.ui', self)
        self.goBack.clicked.connect(self.gotoMain)

    def gotoMain(self):
        print(f'Current Index: {widget.currentIndex() - 2}')
        widget.setCurrentIndex(widget.currentIndex() - 2)


#window
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
productscreen = ProductScreen()
addscreen = AddScreen()

widget.addWidget(mainwindow)
widget.addWidget(productscreen)
widget.addWidget(addscreen)

widget.setWindowTitle('Inventory Management System')
widget.setFixedHeight(600)
widget.setFixedWidth(840)
#widget.setStyleSheet('background: #FFFFFF;')
widget.show()

sys.exit(app.exec_())

