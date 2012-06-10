import sys
from PyQt4.QtGui import QApplication, QWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

class ListWindow(QWidget):
    def __init__(self, parent=None):
        super(ListWindow, self).__init__(parent)
        self.listWidget = QListWidget()
        for i in range(1, 11):
            self.listWidget.addItem("Item {}".format(i))
	item1 = QListWidgetItem('Text', self.listWidget)	
	item1.setData(Qt.UserRole, 'chunk-124.xml.bz2')
	# self.listWidget.addItem(item1)
        self.listWidget.itemActivated.connect(self.printItemText)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.listWidget)
        self.setLayout(mainLayout)

    def printItemText(self, item):
        """These two are equivalent"""
	w = self.listWidget.currentItem()
	print(w.text())
        print(w.data(Qt.UserRole).toPyObject())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    listWindow = ListWindow()
    listWindow.show()
    app.exec_()
