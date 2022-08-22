from argparse import _MutuallyExclusiveGroup
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtCore import QObject, Qt, QSize, QFile, Signal
from PySide2.QtGui import QFont, QIcon,QBrush, QColor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListView, QListWidget, QListWidgetItem, QHeaderView
from PySide2.QtWidgets import QStatusBar, QWidget,QTableWidgetItem
from PySide2.QtWidgets import QMessageBox, QFileDialog
from PySide2.QtCore import QSignalMapper

import re
import mylog 

GLogger = mylog.logger

class MainWindow(QObject):
    def __init__(self):
        #print ( "TEST 2" )
        super(MainWindow, self).__init__()
        self._window = None
        self.ui_setup()
        self.src_data_list = []
    
    @property
    def window(self):
        """MainWindow widget."""
        return self._window

    def ui_setup(self):
        """Initialize user interface of main window."""
        loader = QUiLoader()
        file = QFile('./main.ui')
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        status_bar = QStatusBar(self._window)
        self._window.setStatusBar(status_bar)
        #self._window.setWindowIcon(QIcon('./interface/media/bucketing_icon.jpeg'))
        self._window.setWindowTitle('wordpress发文助手')

    def hkClipboard(self, **kwargs):
        GLogger.info(" I want to window *****\n")
        clipboard = kwargs['clipboard']
        data = clipboard.mimeData()
        print("clipboard in window *****\n ")
        print(data.formats())
        print("clipboard in html *****\n ")

        if 'text/html' in data.formats():
            print ( data.html() )
            self._window.textEdit_toPub_Html.setHtml( data.html() )
        print("clipboard in text *****\n ")
        if 'text/plain' in data.formats():
            print ( data.text() )
            self._window.textEdit_toPub_src.setPlainText( data.text() )

