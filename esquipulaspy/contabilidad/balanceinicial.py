#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ${file}
#       
#       Copyright 2010 Luis Carlos Mejia Garcia<lcmejia19@gmail.com>
'''
Created on 23/11/2010

@author: Luis Carlos Mejia Garcia
'''
import logging

from PyQt4.QtGui import QHBoxLayout,QMainWindow, QSortFilterProxyModel, QTableView, QItemSelectionModel, \
QItemSelection, QDataWidgetMapper, QMessageBox, qApp,QPushButton,QSizePolicy,QIcon,QPixmap
from PyQt4.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import pyqtSlot, QDateTime, QTimer, Qt,QSize

from ui.Ui_operations import Ui_frmOperations
from utility.accountselector import AccountsSelectorModel, AccountsSelectorDelegate
from utility import constantes
from utility import user
from decimal import Decimal

IDDOCUMENTO, NDOCIMPRESO, FECHACREACION, CONCEPTO = range( 4 )

IDCUENTA, CODIGO, DESCRIPCION, MONTO, IDDOCUMENTOC = range( 5 )
class FrmBalanceInicial( QMainWindow, Ui_frmOperations ):
    def __init__( self, parent = None ):
        super( FrmBalanceInicial, self ).__init__( parent )
        self.setupUi( self )
        self.__status = False
        self.database = QSqlDatabase.database()
        self.user = user.LoggedUser
        
        

#        self.setMaximumSize(600,300)
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( "No se pudo abrir la base de datos" )

            self.editModel = BalanceInicialModel()
            self.editModel.insertRow( 1 )
            self.editModel.insertRow( 1 )
            self.editModel.lines[1].name= "CAPITAL"
            self.editModel.lines[1].code = "320 001 000 000 000"
            
            self.startUI()

            delegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT 
                c.idcuenta, 
                c.codigo, 
                c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            """ ) )

            self.dtPicker.setDateTime( QDateTime.currentDateTime() )
            self.dtPicker.setMaximumDateTime( QDateTime.currentDateTime() )
            self.dtPicker.setReadOnly(False)

            self.tableDetails.setModel( self.editModel )
            self.tableDetails.setColumnHidden( IDCUENTA, True )
            self.tableDetails.setColumnHidden( IDDOCUMENTOC, True )
            self.tableDetails.setItemDelegate( delegate )
            self.tableDetails.resizeColumnsToContents()
        except UserWarning as inst:
            self.status = False
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
            logging.error( unicode( inst ) )
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(), "Hubo un error al tratar de iniciar el Balance Inicial" )
            logging.critical( unicode( inst ) )

    def startUI(self):        
        self.buttonBox.accepted.connect( self.save )
        self.stackedWidget.setCurrentIndex(0)
        self.dtPicker.setAlignment(Qt.AlignHCenter)
        
    
        self.btnAdd = QPushButton(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setMaximumSize(QSize(22, 16777215))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/res/list-add.png"), QIcon.Normal, QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.clicked.connect(self.addRow)
        
        self.btnRemove = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemove.sizePolicy().hasHeightForWidth())
        self.btnRemove.setSizePolicy(sizePolicy)
        self.btnRemove.setMaximumSize(QSize(22, 16777215))
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/res/list-remove.png"), QIcon.Normal, QIcon.Off)
        self.btnRemove.setIcon(icon1)
        self.btnRemove.clicked.connect(self.removeRow)
        
        
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.dtPicker)
        self.horizontalLayout.addWidget(self.btnAdd)
        self.horizontalLayout.addWidget(self.btnRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.tableDetails)
        self.verticalLayout.addWidget(self.stackedWidget)
    
        self.tableDetails.setEditTriggers( QTableView.AllEditTriggers)
        self.tableNavigation.setVisible(False)
        self.txtSearch.setVisible(False)
        self.label_4.setVisible(False)
        self.groupBox.setVisible(False)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Balance Inicial")

    def addRow(self):
        self.editModel.insertRow(0)
        self.btnRemove.setEnabled(self.editModel.rowCount()>2)

    def removeRow(self):
        filas = self.editModel.rowCount()
        if filas>2:
            self.editModel.removeRows( self.tableDetails.currentIndex().row(), 1)
            self.btnRemove.setEnabled(filas-1>2)
    
    @pyqtSlot()
    def on_buttonBox_rejected( self ):
        self.close()


    def save( self ):
        if QMessageBox.question(self, "Balance Inicial", u"¿Esta seguro que desea guardar el Balance Inicial?",QMessageBox.Yes | QMessageBox.No )==QMessageBox.Yes:
            try:
                pos = self.editModel.rowCount()-1
                if self.editModel.lines[pos].amount>0:
                    raise UserWarning("No puede iniciar operaciones con la cuenta de capital sobregirada")
                elif self.editModel.lines[pos].amount<0:
                    self.editModel.lines[pos].itemId = constantes.CAPITAL
                
                query = QSqlQuery()
    
    
                if not self.editModel.valid:
                    raise UserWarning( "El documento no es valido, no se puede guardar" )
    
                if not self.database.isOpen():
                    if not self.database.open():
                        raise UserWarning( "No se pudo conectar con la base de datos" )
    
                if not self.database.transaction():
                    raise Exception( u"No se pudo comenzar la transacción" )
    #               Cargar el numero del asiento actual
                query.prepare( """SELECT fnConsecutivo(%d,null);
                """%constantes.IDAJUSTECONTABLE )
    
                query.exec_()
                query.first()
                n = query.value( 0 ).toString()
               
                if not query.prepare( """
                INSERT INTO documentos (ndocimpreso, fechacreacion, idconcepto,   idtipodoc)
                VALUES (:ndocimpreso, :fechacreacion, :idconcepto,  %d)
                """ % constantes.IDAJUSTECONTABLE ):
                    raise Exception( "No se pudo preparar la consulta para guardar el documento" )
                query.bindValue( ":ndocimpreso", n )
                query.bindValue( ":fechacreacion", self.dtPicker.dateTime().toString( "yyyyMMddhhmmss" ) )
                query.bindValue( ":idconcepto",constantes.IDCONCEPTOBALANCEINICIAL)
    
                if not query.exec_():
                    raise Exception( "No se pudo ejecutar la consulta para guardar el asiento" )
    
                insertedId = query.lastInsertId().toInt()[0]
    
                if not query.prepare( """
                INSERT INTO personasxdocumento (idpersona, iddocumento, idaccion) 
                VALUES (:usuario, :documento, :idaccion)
                """ ):
                    raise Exception( "No se pudo preparar la consulta para insertar el usuario" )
                query.bindValue( ":usuario", self.user.uid )
                query.bindValue( ":documento", insertedId )
                query.bindValue( ":idaccion", constantes.ACCCREA )
    
                if not query.exec_():
                    raise Exception( u"No se pudo guardar la relación con el usuario" )
    
                for lineid, line in enumerate( self.editModel.lines ):
                    if line.valid:
                        line.save( insertedId, lineid + 1 )
    
                if not self.database.commit():
                    raise Exception( "No se pudo ejecutar la transaccion" )
                
                
                QMessageBox.information(self, "Balance Inicial","El Balance Inicial se ha guardado con exito")
                self.parent().inicial = False
                self.parent().status = True
                self.close()
            except UserWarning as inst:
                QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
                logging.error( inst )
            except Exception as inst:
                QMessageBox.critical( self, qApp.organizationName(), "Hubo un error al tratar de guardar Balance Inicial" )
                self.database.rollback()
                logging.critical( inst )
                logging.critical( query.lastError().text() )
            finally:
                if self.database.isOpen():
                    self.database.close()
                
                
                
class BalanceInicialModel(AccountsSelectorModel ):
    def __init__( self ):
        AccountsSelectorModel.__init__( self )

#    def setData( self, index, value, _role = Qt.EditRole ):
#        if index.row() == 0 and index.column() == 3  and Decimal( value.toString() ) < 0:
#            return False
#        return AccountsSelectorModel.setData( self, index, value, _role )

    def setData( self, index, value, _role = Qt.EditRole ):
        filas =self.rowCount()
        resultado = AccountsSelectorModel.setData( self, index, value, _role )
        if filas > self.rowCount():
            self.insertRow(filas)
            self.lines[filas-1].name = "CAPITAL"
            self.lines[filas-1].code = "320 001 000 000 000"
        return resultado
        
        
        
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if self.bloqueada( index ):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def bloqueada( self, index ):
        """
        Verdadero si el monto de la cuenta contable no debe de ser editada
        @rtype: bool
        """
#        if self.tipoDoc == constantes.IDDEPOSITO:
        if index.row() == index.model().rowCount()-1:
            return True
        else:
            return False
#        else:
#            return index.column() in ( 1, 2 ) and index.row() == 0
