from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
import sys
import scanner
import database


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_screen.ui", self)
        self.setWindowTitle("Inventory Management System")
        self.searchButton.clicked.connect(self.search)
        self.scanButton.clicked.connect(self.scanBarcode)
        self.clearButton.clicked.connect(self.clearInput)
        self.show()

    def search(self):
        batch_number = self.batchInput.text()
        product_id = self.productInput.text()
        prod_type = self.typeDropdown.currentText()

        # If all of the inputs are empty
        if not batch_number and not product_id and not prod_type:
            self.showBlankPopup()

        else:
            # Get data from inputs and check database
            data = ""
            if batch_number:
                data = database.get_product_from_batch(batch_number)
            elif product_id:
                data = database.get_product_from_id(product_id)
            elif prod_type:
                data = database.get_product_by_type(prod_type)

            # If a match is found in database, open Product Screen
            if data:
                self.gotoProductScreen(data)

            # If no match is found, ask the user to add the product
            else:
                self.showAddItemQuery()

    def scanBarcode(self):
        batch = scanner.scan_for_barcode()
        self.batchInput.setText(str(batch))

    def showBlankPopup(self):
        box = QMessageBox()
        box.setWindowTitle("Error!")
        box.setIcon(QMessageBox.Critical)
        box.setText("Please fill out one of the fields.")
        box.exec_()

    def gotoProductScreen(self, data):
        self.product_screen = ProductScreen(data)
        self.product_screen.show()
        self.close()

    def showAddItemQuery(self):
        box = QMessageBox()
        result = box.question(self, 'Not Found',
                              "No product with the entered "
                              "information has been found. Would "
                              "you like to add that item?",
                              box.Yes | box.No)
        if result == box.Yes:
            self.add_screen = AddScreen()
            self.add_screen.show()
            self.close()

    def clearInput(self):
        self.batchInput.clear()
        self.productInput.clear()


class ProductScreen(QDialog):
    def __init__(self, products):
        super(ProductScreen, self).__init__()
        uic.loadUi('product_screen.ui', self)
        self.setWindowTitle("Inventory Management System")
        self.products = products
        self.loadTable()
        self.backLink.clicked.connect(self.gotoMain)
        self.addProduct.clicked.connect(self.gotoAddProduct)
        self.show()

    def gotoMain(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def gotoAddProduct(self):
        self.add_screen = AddScreen()
        self.add_screen.show()
        self.close()

    def loadTable(self):
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setRowCount(20)
        # If provided data, populate the table
        if self.products:
            table_row = 0
            for product in self.products:
                for table_column, product_attribute in enumerate(product):
                    self.productTable.setItem(table_row, table_column,
                                              QtWidgets.QTableWidgetItem(
                                                  str(product[table_column])))
                table_row += 1


class AddScreen(QDialog):
    def __init__(self):
        super(AddScreen, self).__init__()
        uic.loadUi('add_screen.ui', self)
        self.setWindowTitle("Inventory Management System")
        self.goBack.clicked.connect(self.gotoMain)
        self.createButton.clicked.connect(self.createItem)
        self.cancelButton.clicked.connect(self.gotoMain)

    def gotoMain(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def createItem(self):
        name = self.nameInput.text()
        batch = self.batchInput.text()
        status = self.statusInput.text()
        type = self.type.currentText()
        quantity = self.quantityInput.text()
        date = self.dateInput.text()
        description = self.descriptionInput.toPlainText()

        # Ensure no input is blank
        if not (name and batch and status and type and quantity and date and
                description):
            self.showWarningMessage()

        else:
            database.add_product(name, type, int(batch), description,
                                 int(quantity), status, date)

            self.showSuccessMessage()
            self.gotoMain()

    def showWarningMessage(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Error!")
        box.setText("Please make sure all fields are entered.")
        box.exec_()

    def showSuccessMessage(self):
        box = QMessageBox()
        box.setWindowTitle("Success!")
        box.setText("Product successfully added to the inventory!")
        box.exec_()


# window
app = QApplication(sys.argv)
widget = MainWindow()

widget.setWindowTitle('Inventory Management System')
widget.setFixedHeight(600)
widget.setFixedWidth(840)
# widget.setStyleSheet('background: #FFFFFF;')
widget.show()

sys.exit(app.exec_())
