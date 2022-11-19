import sqlite3
import sys

from PyQt5 import uic
from PyQt5.Qt import *

DB_NAME = 'coffee.sqlite'


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect(DB_NAME)
        self.button_add.clicked.connect(self.add_row)
        self.button_edit.clicked.connect(self.edit_row)
        self.button_update.clicked.connect(self.update)
        self.showw()

    def showw(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName(DB_NAME)
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        view = self.tableView
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('Espresso')
        model.select()
        self.model = model

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)

    def add_row(self):
        inputDialog = Dialog()
        rez = inputDialog.exec()
        if not rez:
            msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return
        try:
            ID = inputDialog.id.text()
            title_variety = inputDialog.title.text()
            degree_of_roasting = inputDialog.roasting.text()
            ground_or_grains = inputDialog.grains_or_not.text()
            description = inputDialog.disc.text()
            price = inputDialog.price.text()
            packing_volume = inputDialog.V.text()

            r = self.model.record()
            r.setValue("ID", ID)
            r.setValue("title_variety", title_variety)
            r.setValue("degree_of_roasting", degree_of_roasting)
            r.setValue("ground_or_grains", ground_or_grains)
            r.setValue("description", description)
            r.setValue("price", price)
            r.setValue("packing_volume", packing_volume)
            self.model.insertRecord(-1, r)
            self.model.select()
        except:
            pass

    def edit_row(self):
        self.s = Edit_dialog()
        self.s.show()

    def update(self):
        self.showw()


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление строки')

        self.id = QLineEdit()
        self.title = QLineEdit()
        self.roasting = QLineEdit()
        self.grains_or_not = QLineEdit()
        self.disc = QLineEdit()
        self.price = QLineEdit()
        self.V = QLineEdit()

        try:
            form_layout = QFormLayout()
            form_layout.addRow('ID:', self.id)
            form_layout.addRow('title_variety:', self.title)
            form_layout.addRow('degree_of_roasting:', self.roasting)
            form_layout.addRow('ground_or_grains:', self.grains_or_not)
            form_layout.addRow('description:', self.disc)
            form_layout.addRow('price:', self.price)
            form_layout.addRow('packing_volume:', self.V)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QVBoxLayout()
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)
            self.setLayout(main_layout)
        except:
            pass


class Edit_dialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect(DB_NAME)
        self.button_commit.clicked.connect(self.upd)

    def upd(self):
        try:
            self.ID = int(self.id_edit.text())
            self.title = self.title_variety.text()
            self.roasting = self.degree_of_roasting.text()
            self.grains_or_not = self.ground_or_grains.text()
            self.disc = self.description.text()
            self.price = int(self.price.text())
            self.V = int(self.packing_volume.text())
        except:
            pass

        try:
            cur = self.con.cursor()
            cort = (self.title, self.roasting, self.grains_or_not,
                    self.disc, self.price, self.V, self.ID)
            cur.execute(f'UPDATE Espresso SET title_variety=?, degree_of_roasting=?,'
                        f'ground_or_grains=?, description=?,'
                        f'price=?, packing_volume=? WHERE ID=?', cort)
            self.con.commit()
            self.con.close()
        except:
            pass

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
