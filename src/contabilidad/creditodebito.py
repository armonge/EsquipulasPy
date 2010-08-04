'''
Created on 04/08/2010

@author: marcos
'''
from PyQt4.QtCore import pyqtSlot, SIGNAL, QModelIndex, Qt, QTimer, \
    SLOT, QDateTime

from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QDataWidgetMapper, \
    QDialog, QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
     QLineEdit,QMessageBox

from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery

from ui.UI_creditodebito import Ui_frmCreditoDebito
from utility.base import Base
from decimal import Decimal

class frmCreditoDebito( Ui_frmCreditoDebito, QMainWindow,Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """


    def __init__( self, user, parent ):
        