import sys
import pandas as pd
from zipfile import ZipFile   
from PyQt5 import QtCore, QtWidgets

Qt = QtCore.Qt

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QtCore.QVariant()



def get_data(zipPath, file_name):
    reader = pd.read_csv(ZipFile(zipPath).open(file_name), 
                        encoding="latin", 
                        chunksize=50*1024*1024, 
                        iterator=True,
                        low_memory=False
                        )
    return reader.get_chunk(5000) # or 10000


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QTableView()
    data_table = get_data(zipPath='E:/40/2.zip', file_name='2.csv')
    model = PandasModel(data_table)
    view.setModel(model)

    view.show()
    sys.exit(application.exec_())
