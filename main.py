import sys

# Comentário aleatório

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMdiArea
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import (QPushButton, QLineEdit)
from PyQt5 import (QtWidgets, QtGui)

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Pathfinder 2E Combat Tracker')
        self.setCentralWidget(QMdiArea())
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self.setGeometry(300, 300, 450, 600)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction(QIcon(), 'Load')
        self.menu.addAction(QIcon(), 'Save')
        self.menu.addAction(QIcon(), 'About')
        self.menu.addAction(QIcon(), '&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)

        cond = QtWidgets.QAction('Condition', tools)
        folderOpen = QtWidgets.QAction(QtGui.QIcon("add_pack.ico"), "Open Folder", tools)
#        txt = QtWidgets.QAction(QLineEdit('Aqui', tools))
        tools.addAction(cond)
        tools.addAction(folderOpen)
        tools.addAction('Add Char', self.close,)
        tools.addAction('Add Monster', self.close)
        tools.addAction('Remove Char', self.close)
        tools.addAction('Reorder Init', self.close)
        tools.addAction('Exit', self.close)
        charBtn = QPushButton('CharBTN', self)
        charBtn.setToolTip('Add char')
        charBtn.move(0, 53)


    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())