# -*- coding: utf-8 -*-
'''
Created on 13/07/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtGui import QDialog, QCompleter,QAbstractItemView,QSortFilterProxyModel,QMessageBox,QStyledItemDelegate,QDoubleSpinBox
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import pyqtSignature, pyqtSlot, Qt, QDate , QVariant,SIGNAL
from utility.accountselector import AccountsSelectorModel
from utility.constantes import IDCONTABILIDAD,IDERROR,IDCONCILIACION,IDDEPOSITO,IDCONCEPTODEPOSITO
from utility.searchpaneldelegate import SearchPanelDelegate

from document.movimientosbancarios.datosdocmodel import DatosDocModel
from utility.movimientos import CAJAGENERAL

class MovimientosBancariosModel(object):
    def __init__( self,userId):
        object.__init__(self)
        
        self.idCuentaBanco = 0
        self.codigoDoc = ""
        self.descripcionDoc = ""
        
        self.editmodel = Modelo()
        self.datos = DatosDocModel()
        self.datos.idUser = userId
        

    def setConceptos(self,combobox,swconcepto=None):
    #            Rellenar el combobox de las CONCEPTOS
        self.conceptosModel = QSqlQueryModel()
        self.conceptosModel.setQuery( """
           SELECT 
               idconcepto,
               descripcion
            FROM conceptos c WHERE modulo=3;
        """ )
        combobox.setModel( self.conceptosModel )
        combobox.setModelColumn( 1 )
        combobox.setCurrentIndex(-1)
        combobox.setEnabled(False)
        completerconcepto = QCompleter()
        completerconcepto.setCaseSensitivity( Qt.CaseInsensitive )
        completerconcepto.setModel( self.conceptosModel )
        completerconcepto.setCompletionColumn( 1 )
        if swconcepto!=None:
            swconcepto.setCurrentIndex(0)

    
    def setCuentasBancarias(self,cbcuenta,swcuenta):
        self.cuentasModel = QSqlQueryModel()            
        self.cuentasModel.setQuery( """
                   SELECT
            c.idcuenta as Id,
            cb.ctabancaria as 'No. Cuenta',
            b.descripcion as Banco,
            tm.simbolo as Moneda,
            c.codigo as 'Codigo Contable',
            c.descripcion as 'Cuenta Contable',
            DATE_FORMAT(Max(con.fecha),'%d/%m/%Y') AS 'Conciliado'
        FROM cuentasbancarias cb
        JOIN bancos b ON cb.idbanco=b.idbanco
        JOIN cuentascontables c ON c.idcuenta=cb.idcuentacontable
        JOIN tiposmoneda tm ON tm.idtipomoneda=cb.idtipomoneda
        LEFT JOIN conciliaciones con ON con.idcuentacontable=cb.idcuentacontable
        GROUP BY cb.idcuentacontable
         ;
        """ )
#        cbcuenta = SearchPanel(self.cuentasModel,None,True)
        cbcuenta.setModel(self.cuentasModel)
        cbcuenta.pFilterModel.setFilterKeyColumn(-1)
        cbcuenta.setCurrentIndex(-1)
        cbcuenta.setColumnHidden(5)
        swcuenta.setCurrentIndex(0)
        cbcuenta.setFocus()

            
    def setTiposDoc(self,cbtipodoc,swtipodoc=None):
        self.tiposModel = QSqlQueryModel()
        filtro = str(IDCONCILIACION)
        if swtipodoc==None:
            filtro += "," + str(IDDEPOSITO)
        else:
            filtro += "," + str(IDERROR)
            
        self.tiposModel.setQuery( "SELECT idtipodoc,descripcion,codigodoc FROM tiposdoc t WHERE modulo=" + str(IDCONTABILIDAD) + " AND idtipodoc NOT IN (" + filtro + ")" )
        cbtipodoc.setModel( self.tiposModel )
        cbtipodoc.setModelColumn( 1 )
        if swtipodoc!=None:
            swtipodoc.setCurrentIndex(0)
        cbtipodoc.setCurrentIndex(-1)
        cbtipodoc.setEnabled(False)
        
        
        
    def setAccountTable(self,tabledetails):
        delegate = SearchPanelDelegate("""
            SELECT cc.idcuenta, cc.codigo, cc.descripcion
            FROM cuentascontables cc
            WHERE cc.codigo != '---' AND cc.codigo != ''
            """ )
        tabledetails.setModel( self.editmodel )
        tabledetails.setColumnHidden( 0, True )
        
        tabledetails.setItemDelegate( delegate )
        tabledetails.resizeColumnsToContents()
        tabledetails.setEditTriggers( QAbstractItemView.AllEditTriggers)
        
        
    def save(self):
        if self.datos.idTipoDoc == IDDEPOSITO:
            self.editmodel.lines[1].itemId = int(CAJAGENERAL)
                  
        if not self.valid:
            return False
        if QMessageBox.question(None, u"Movimientos Bancarios",u"¿Desea guardar el documento?" ,QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.datos.lineas = self.editmodel.lines
            self.datos.total = self.editmodel.lines[0].amount
            if self.datos.save():
                QMessageBox.information( None,
                                         u"Movimientos Bancarios",
                                         u"El documento se ha guardado con éxito" )
                return True
            else:
                QMessageBox.critical( None,
                        u"Movimientos Bancarios",
                        u"El documento no pudo guardarse")
        

         

    @property
    def valid( self ):
        
        if self.idCuentaBanco ==0:
            QMessageBox.warning( None,
                    u"Movimientos Bancarios" ,
                    u"Por favor elija la cuenta bancaria" )
        elif self.datos.idTipoDoc ==0:
            QMessageBox.warning( None,
                    u"Movimientos Bancarios",
                    u"Por favor elija el tipo de documento")
        elif self.datos.idConcepto ==0:
            QMessageBox.warning( None,
                    u"Movimientos Bancarios",
                    u"Por favor elija el concepto")
      
        elif not self.editmodel.valid:
            QMessageBox.warning( None,
                    u"Movimientos Bancarios",
                    u"Por favor especifique las cuentas que fueron afectadas" )            
        elif self.datos.total == None:
            raise Exception("No fue asignado el total")
        else:
            self.datos.lineas = self.editmodel.lines
            return True 
        
        return False

    def tipoDocChanged(self,cbconcepto,index):
        nuevoTipo = self.tiposModel.record( index ).value( "idtipodoc" ).toInt()[0]
        if self.datos.idTipoDoc !=nuevoTipo:
            if  self.datos.idTipoDoc == IDDEPOSITO:
                self.editmodel.lines[1].code = "" 
                self.editmodel.lines[1].name = ""
                celda = self.editmodel.index(1,2)
                self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
                celda = self.editmodel.index(1,1)
                self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
                cbconcepto.setEnabled(True)
                cbconcepto.setCurrentIndex(-1)

                
        self.datos.idTipoDoc = nuevoTipo
        self.editmodel.idTipoDoc = nuevoTipo 
        self.codigoDoc = self.tiposModel.record( index ).value( "codigodoc" ).toString()
        self.descripcionDoc = self.tiposModel.record( index ).value( "descripcion" ).toString()

        if self.datos.idTipoDoc == IDDEPOSITO:
            self.editmodel.removeRows(1,self.editmodel.rowCount()-1)
            self.editmodel.insertRow(1)
            self.editmodel.lines[1].code = "110 001 001 000 000" 
            self.editmodel.lines[1].name = "CYB Caja General"
            celda = self.editmodel.index(1,2)
            self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
            celda = self.editmodel.index(1,1)
            self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
            cbconcepto.setEnabled(False)
            if cbconcepto.currentIndex()!=IDCONCEPTODEPOSITO:
                cbconcepto.setCurrentIndex(IDCONCEPTODEPOSITO)
     
    def cuentaBancariaChanged(self,tabledetails,index,dtPicker,cbconcepto,cbtipodoc):
        if index == -1 or self.editmodel == None:
            return None
        
        if self.editmodel.rowCount() == 0:
            self.editmodel.insertRows(0)
            dtPicker.setReadOnly(False)
            cbconcepto.setEnabled(True)
            cbtipodoc.setEnabled(True) 
        
        self.idCuentaBanco =  self.cuentasModel.record( index ).value( "id" ).toInt()[0]
        
        delegate = tabledetails.itemDelegate() 
#ELIMINAR EL ID DE LA CUENTA ANTERIOR
        delegate.removeFromFilter(str(self.editmodel.lines[0].itemId))
#Quitar fila si ya existia en la tabla
        lineas = self.editmodel.lines
        id = self.idCuentaBanco
        for i in range(1,self.editmodel.rowCount()):
            if lineas[i].itemId == id:
                monto2 = lineas[0].amount
                monto = lineas[i].amount 
                delegate.removeFromFilter(str(id))
                self.editmodel.removeRow(i)
                lineas[0].amount =monto2 + monto

#AGREGAR EL ID DE LA CUENTA ACTUAL        
        delegate.filtrados.append(str(self.idCuentaBanco))
        self.editmodel.lines[0].itemId = self.idCuentaBanco
        
        
        self.editmodel.lines[0].code = self.cuentasModel.record( index ).value( "Codigo Contable" ).toString() 
        self.editmodel.lines[0].name = self.cuentasModel.record( index ).value( "Cuenta Contable" ).toString()
        celda = self.editmodel.index(0,2)
        self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
        celda = self.editmodel.index(0,1)
        self.editmodel.emit( SIGNAL( "dataChanged(QModelIndex, QModelIndex)" ), celda, celda )
        
        tabledetails.resizeColumnsToContents()
        value= self.cuentasModel.record( index ).value( "Conciliado" ).toString()
        
        dtPicker.setMaximumDate(QDate.currentDate())
        if value!="":
            value = QDate.fromString(value,"dd/MM/yyyy").addDays(1)
            dtPicker.setMinimumDate(value)
#            if value >QDate.currentDate():
##                self.btnguardar.setEnabled(False)
#                return None    
        else:
            dtPicker.setMinimumDate(QDate(2009,11,1))
        
    def conceptoChanged(self,index):
        self.datos.idConcepto = self.conceptosModel.record( index ).value( "idconcepto" ).toInt()[0]
                    

class Modelo( AccountsSelectorModel ):
    def __init__( self ):
        AccountsSelectorModel.__init__( self )
        self.idTipoDoc = 0
    
    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled
        
        if self.bloqueada(index):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable    
        
    def bloqueada(self,index):
        if self.idTipoDoc == IDDEPOSITO:
            if index.row() == 0:
                return index.column() in (1,2)
            else:
                return True
        else:
            return index.column() in (1,2) and index.row() == 0
                    
        
        