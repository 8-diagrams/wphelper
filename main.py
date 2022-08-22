#!venv/bin/python3

import sys
import PySide2

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

import mylog

logger = mylog.logger

from mainwin import MainWindow
#from basic_ui.user_interface.main_window import MainWindow

import functools


if '__main__' == __name__:
     
    app = QApplication(sys.argv)
    #dir(PySide2)
    
    clipboard = app.clipboard()
    
    main_window = MainWindow()

    # make click board
    clipboard.dataChanged.connect( functools.partial(main_window.hkClipboard, clipboard=clipboard) )

    main_window.window.show()

    ret = app.exec_()
    sys.exit(ret)
