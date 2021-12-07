import sqlite3
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QComboBox
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QStandardItem


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self.data = data

    def rowCount(self, parent=None):
        return self.data.shape[0]

    def columnCount(self, parent=None):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        return None


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     applicant = sqlite3.connect("gsz.db")
#     df = pd.read_sql_query("SELECT * FROM applicants", applicant)
#     df = df.drop(["num_courses_taken"], axis=1)
#     model = pandasModel(df)
#     view = QTableView()
#     view.setModel(model)
#     view.resize(800, 600)
#     view.show()
#     print(model.rowCount())
#     print(model.columnCount())
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    applicant = sqlite3.connect("gsz.db")
    df = pd.read_sql_query("SELECT * FROM applicants", applicant)
    df = df.drop(["num_courses_taken"], axis=1)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    for row in range(model.rowCount()):
        c = QComboBox()
        c.addItems(
            [
                "approve",
                "deny",
            ]
        )
        i = view.model().index(row, 7)
        view.setIndexWidget(i, c)
    view.resize(800, 600)
    view.show()
    print(model.rowCount())
    print(model.columnCount())
    sys.exit(app.exec_())
