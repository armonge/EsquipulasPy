# -*- coding: utf-8 -*-
'''
Created on 03/07/2010

@author: Administrator
'''
from utility.base import Base
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase,QSqlQuery
from PyQt4.QtCore import pyqtSlot, pyqtSignature, Qt, QDateTime, SIGNAL, QModelIndex, QTimer,QSize
from PyQt4.QtGui import QMainWindow,QSortFilterProxyModel,QMessageBox,QCompleter,QDataWidgetMapper,QStyledItemDelegate, QDoubleSpinBox, QPrinter
from decimal import Decimal, InvalidOperation
import functools
from utility.moneyfmt import moneyfmt
from ui.Ui_cheques import Ui_frmCheques
from document.cheque.chequemodel import ChequeModel
from utility.accountselector import  AccountsSelectorDelegate, AccountsSelectorLine,AccountsSelectorModel
from utility import constantes
from utility.widgets.searchpanel import SearchPanel
from utility.reports import frmReportes
IDDOCUMENTO,NCHEQUE,CUENTABANCARIA,NOMBRE,FECHA,CONCEPTO,TOTAL,ANULADO,TASARETENCION,TOTALRETENCION,TIPOCAMBIO,SUBTOTAL,IVA=range(13)
#accounts model
IDDOC, IDCUENTA,CODIGO,DESCRIPCION, MONTO= range( 5 )
class frmCheques( Ui_frmCheques, QMainWindow,Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """


    def __init__( self, user, parent ):
        '''
        Constructor
        '''
        super( frmCheques, self ).__init__( parent )

        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        self.user = user
        self.navmodel = QSqlQueryModel( self )
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        
        self.accountsModel = QSqlQueryModel()
        self.accountsProxyModel = ROAccountsModel(self)
        self.accountsProxyModel.setSourceModel( self.accountsModel )
        
        #        El modelo que filtra a self.navmodel
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
        self.editmodel = None  

        self.status = True
        #las acciones deberian de estar ocultas
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
          
        
        QTimer.singleShot( 0, self.loadModels )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def updateDetailFilter( self, index ):
        self.accountsProxyModel.setFilterKeyColumn( IDDOCUMENTO )
        self.accountsProxyModel.setFilterRegExp( self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )

    def updateModels(self):
    #inicializando el documento
    #El modelo principal
    #FIXME Revisar escape del %
            
        self.navmodel.setQuery(u"""SELECT  padre.iddocumento,
        padre.ndocimpreso as 'No. Cheque',
        cb.descripcion as 'Cuenta Bancaria',
        p.nombre,
        DATE(padre.fechacreacion) as 'El dia',
        c.descripcion as 'En concepto de',
        IF (tm.simbolo="C$",CONCAT(tm.simbolo,padre.total*tc.tasa),CONCAT(tm.simbolo,padre.total)) as Total,
        padre.anulado AS Anulado,
        CONCAT(valorcosto, '%s') as 'Retencion',
        IF(hijo.total IS NULL, '-' ,CONCAT(tm.simbolo,hijo.total))   as 'Total Ret C$',
        tc.tasa as TipoCambio,
        IF(hijo.total='-',@subtotal:=padre.total/1.15,@subtotal:=(padre.total+hijo.total)/1.15) as 'subtotal',
        concat(tm.simbolo,format(padre.total+hijo.total- @subtotal,4)) as IVA
        FROM documentos padre
        JOIN tiposcambio tc on padre.idtipocambio=tc.idtc
        JOIN personasxdocumento pd ON padre.iddocumento=pd.iddocumento
        JOIN personas p ON p.idpersona=pd.idpersona
        JOIN conceptos c ON  c.idconcepto=padre.idconcepto

        LEFT JOIN costosxdocumento cd ON cd.iddocumento=padre.iddocumento
        LEFT JOIN  costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
        LEFT JOIN docpadrehijos ph ON  padre.iddocumento=ph.idpadre
        LEFT JOIN documentos hijo ON hijo.iddocumento=ph.idhijo
        JOIN cuentasxdocumento cuentasdoc on cuentasdoc.iddocumento=padre.iddocumento
        JOIN cuentascontables cb ON cb.idcuenta=cuentasdoc.idcuenta
        JOIN cuentasbancarias cbank on cb.idcuenta=cbank.idcuentacontable
        JOIN tiposmoneda tm on tm.idtipomoneda=cbank.idtipomoneda 
        WHERE padre.idtipodoc= %d AND p.tipopersona = %d
        GROUP BY padre.iddocumento
        ORDER BY CAST(padre.ndocimpreso AS SIGNED)

        """ % ('%',constantes.IDCHEQUE,constantes.PROVEEDOR))
#        El modelo que filtra a self.navmodel
                
        
        self.tablenavigation.resizeColumnsToContents()
        
        #Este es el modelo para las cuentas
        
        
        
    
 
        self.accountsModel.setQuery( """
        SELECT
            c.iddocumento, 
            c.idcuenta,
            cc.codigo as Codigo,
            cc.descripcion as Nombre,
            c.monto as Monto
        FROM cuentasxdocumento c 
        JOIN documentos d ON c.iddocumento = d.iddocumento
        JOIN cuentascontables cc ON cc.idcuenta = c.idcuenta
        WHERE d.idtipodoc = 12
        ORDER BY nlinea
        """ )

        
        self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
        self.mapper.setModel( self.navproxymodel )
        self.mapper.addMapping( self.lblncheque, NCHEQUE,"text" )
        self.mapper.addMapping( self.dtPicker, FECHA,"date" )
        self.mapper.addMapping( self.lblbeneficiario, NOMBRE,"text")
        self.mapper.addMapping( self.total, TOTAL,"text" )
        self.mapper.addMapping( self.lblconcepto, CONCEPTO,"text" )
        self.mapper.addMapping( self.retencion, TOTALRETENCION, "text" )
        self.mapper.addMapping( self.lblretencion, TASARETENCION, "text" )
        self.mapper.addMapping( self.lbltipocambio, TIPOCAMBIO, "text" )
        self.mapper.addMapping( self.subtotal, SUBTOTAL )
        self.mapper.addMapping( self.iva, IVA, "text" )   
        self.mapper.addMapping( self.lblcuenta, CUENTABANCARIA, "text" )
        
        self.tablenavigation.setModel(self.navproxymodel)            
        self.tabledetails.setModel( self.accountsProxyModel )

        self.tabledetails.setColumnHidden( IDCUENTA, True )
        self.tabledetails.setColumnHidden( IDDOC, True )

        
    def setControls( self, status ):
        """
        @param status false = editando        true = navegando
        """
        self.dtPicker.setReadOnly(  status )
        self.subtotal.setReadOnly( status )
        self.txtobservaciones.setReadOnly( status)
        
        self.actionSave.setVisible(  not status )
        self.actionCancel.setVisible( not status )
        self.actionNew.setVisible( status)
        self.actionPreview.setVisible( status)
        self.ckretencion.setEnabled(not status)
        if not status:
            self.total.setText("0.0")
            self.subtotal.setValue(0)
            self.iva.setText("0.0")
            self.retencion.setText("0.0")
            self.txtobservaciones.setPlainText( "" )
            self.editmodel.uid = self.user.uid 
        
    @pyqtSignature( "bool" )
    def on_ckretencion_toggled( self, on ):
        """
        """
        if not self.editmodel is None:
            
            self.editmodel.hasretencion=True
            if on :
                self.retencionwidget.setCurrentIndex(1)
            else:
                self.retencionwidget.setCurrentIndex(0)
            #self.cboretencion.    
        
    @pyqtSlot( "int" )
    def on_cboconcepto_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.conceptoId= self.conceptosmodel.record( index ).value( "idconcepto" ).toInt()[0]
    
    @pyqtSlot( "int" )
    def on_cbocuenta_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    QMessageBox.warning( None,
                    "Llantera Esquipulas",
                    """Hubo un error al conectarse con la base de datos""",
                    QMessageBox.StandardButtons( \
                        QMessageBox.Ok ),
                    QMessageBox.Ok )
            
            self.editmodel.setData(self.editmodel.index(0,2),
                            [self.cuentabancaria.record( index ).value( "idcuentacontable" ).toInt()[0],
                             self.cuentabancaria.record( index ).value( "codigo" ).toString(),
                             self.cuentabancaria.record( index ).value( "descripcion" ).toString()])
            self.accountseditdelegate.accounts.setFilterRegExp("[^%d]"%self.cuentabancaria.record( index ).value( "idcuentacontable" ).toInt()[0])
            
            self.editmodel.moneda=self.cuentabancaria.record( index ).value( "IDMONEDA" ).toInt()[0]
            self.editmodel.simbolo=self.cuentabancaria.record( index ).value( "simbolo" ).toString()
            # Cargar el numero del cheque actual
            if index>-1:
                query = QSqlQuery( """
                CALL spConsecutivo(12,"""+self.cuentabancaria.record( index ).value( "idcuentacontable").toString()+")")
                if not query.exec_():
                    raise UserWarning("No se pudo obtener el numero consecutivo del cheque")
                query.first()    
                n = query.value( 0 ).toString()
    
                self.lblncheque.setText( n )
                self.editmodel.printedDocumentNumber = n            
               
                self.editmodel.setData(self.editmodel.index(0,3), self.editmodel.totalCordobas)                
                self.updateTotals()
                
    @pyqtSlot( "int" )
    def on_cboretencion_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.retencionId = self.retencionModel.record( index ).value( "idcostoagregado" ).toInt()[0]
            self.editmodel.retencionPorcentaje=Decimal(self.cboretencion.currentText()) if self.cboretencion.currentText()!="" else 0
            self.updateTotals()
            
    @pyqtSlot( "int" )
    def on_cbobeneficiario_currentIndexChanged( self, index ):
        if not self.editmodel is None:
            self.editmodel.proveedorId= self.proveedoresmodel.record( index ).value( "idpersona" ).toInt()[0]        

    @pyqtSlot( "double" )
    def on_subtotal_valueChanged(self,index):
              
        if not self.editmodel is None:
           self.updateTotals()
           self.editmodel.setData(self.editmodel.index(0,3), self.editmodel.totalCordobas)
               
                
    def updateTotals(self):
        self.editmodel.subtotal=Decimal(str(self.subtotal.value()))
        
        if self.editmodel.moneda==constantes.IDCORDOBAS:
                        
            self.total.setText(moneyfmt(self.editmodel.totalCordobas,4,self.editmodel.simbolo))
            self.iva.setText(moneyfmt(self.editmodel.iva,4,self.editmodel.simbolo))
            self.retencion.setText(moneyfmt(self.editmodel.retencion,4,self.editmodel.simbolo))
            
            self.total.setToolTip(moneyfmt(self.editmodel.totalDolares,4,"US$"))
            self.iva.setToolTip(moneyfmt(self.editmodel.iva,4,"US$"))
            self.retencion.setToolTip(moneyfmt(self.editmodel.retencion,4,"US$"))
            
        elif self.editmodel.moneda==constantes.IDDOLARES:
            self.total.setText(moneyfmt(self.editmodel.totalDolares,4,"US$"))
            self.iva.setText(moneyfmt(self.editmodel.iva,4,"US$"))
            self.retencion.setText(moneyfmt(self.editmodel.retencion,4,"US$"))
            
            self.total.setToolTip(moneyfmt(self.editmodel.totalCordobas,4,"C$"))
            self.iva.setToolTip(moneyfmt(self.editmodel.iva,4,"C$"))
            self.retencion.setToolTip(moneyfmt(self.editmodel.retencion,4,"C$"))
            
#    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )        
        
        self.tabledetails.setModel(self.accountsProxyModel)
        self.tabledetails.setColumnHidden(IDCUENTA,True)
        
        self.subtotal.setValue(0)
        self.total.setText("0.0")
        self.iva.setText("0.0")
        self.retencion.setText("0.0")
        
        self.status = True
        self.tabWidget.setCurrentIndex(1)               


    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        """
        Funcion usada para mostrar el reporte de una entrada compra
        """
        printer = QPrinter()
        printer.setPageSize(QPrinter.Letter)
        web = "cheques.php?doc=%d" % self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0]
        report = frmReportes( web , self.user, printer, self )
        report.exec_()

    def on_actionNew_activated( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel
        """
        self.tabWidget.setCurrentIndex(0)
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    QMessageBox.warning( None,
                    "Llantera Esquipulas",
                    """Hubo un error al conectarse con la base de datos""",
                    QMessageBox.StandardButtons( \
                        QMessageBox.Ok ),
                    QMessageBox.Ok )
                    raise UserWarning( u"No se pudo establecer la conexión con la base de datos" )
            
            #Crea modelo para edicion            
            self.editmodel = ChequeModel()
            
            #Sacar valor porcentaje del IVA
            query=QSqlQuery( """SELECT 
                valorcosto
            FROM costosagregados c 
            WHERE activo=1 AND idtipocosto=%d
            """ % (constantes.IVA))
            if not query.exec_():
                raise UserWarning( "No se pudo ejecutar la consulta para obtener los valores de los impuestos" )
            elif not query.size()>0:
                raise UserWarning( "No se pudieron obtener los valores de los impuestos" )
            query.first()
            self.editmodel.ivaRate=Decimal(query.value(0).toString())
            
            self.dtPicker.setDateTime(QDateTime.currentDateTime())
            self.lbltipocambio.setText(str(self.editmodel.exchangeRate))
            
                        
    #        Crea un edit delegate para las cuentas
            self.accountseditdelegate=ChequesFiltroDelegate(QSqlQuery("""SELECT c.idcuenta, c.codigo, c.descripcion 
            FROM cuentascontables c 
            JOIN cuentascontables p ON c.padre = p.idcuenta AND p.padre != 1
            WHERE c.padre != 1 AND c.idcuenta != 22
            """))    
            self.tabledetails.setItemDelegate( self.accountseditdelegate )
            self.tabledetails.setModel( self.editmodel )

            
    #            Rellenar el combobox de las retenciones
            self.retencionModel = QSqlQueryModel()
            self.retencionModel.setQuery( """             
                    SELECT
                        idcostoagregado, 
                        FORMAT(valorcosto,0) as tasa 
                    FROM costosagregados 
                    WHERE idtipocosto IN (%d,%d) AND 
                    activo=1 
                    ORDER BY valorcosto desc; 
                    """ % (constantes.RETENCIONPROFESIONALES, constantes.RETENCIONFUENTE))
    
            self.cboretencion.setModel( self.retencionModel )
            self.cboretencion.setCurrentIndex(-1)
            self.cboretencion.setModelColumn( 1 )
            
            
    #       Rellenar el combobox de los PROVEEDORES
            self.proveedoresmodel = QSqlQueryModel()
            self.proveedoresmodel.setQuery( """
              SELECT
                    p.idpersona,
                    p.nombre,
                    p.activo
                    FROM personas p
                    where p.tipopersona=2
                    group by p.idpersona
                    ORDER BY p.nombre
                    ;
            """ )
            
            self.proveedoresfiltro=QSortFilterProxyModel()
            self.proveedoresfiltro.setSourceModel(self.proveedoresmodel )
            self.proveedoresfiltro.setFilterKeyColumn(1)
    #        self.proveedoresfiltro.setFilterRegExp("0")
            self.cbobeneficiario.setModel(self.proveedoresfiltro)
            self.cbobeneficiario.setCurrentIndex(-1)
            self.cbobeneficiario.setModelColumn( 1)
    
            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.proveedoresmodel )
            completer.setCompletionColumn( 1 )
    
    #       Rellenar el combobox de los conceptos
            self.conceptosmodel = QSqlQueryModel()
            self.conceptosmodel.setQuery( """
              SELECT idconcepto,descripcion FROM conceptos c;
            """ )
            self.cboconcepto.setModel( self.conceptosmodel )
            self.cboconcepto.setCurrentIndex(-1)
            self.cboconcepto.setModelColumn( 1 )
    
            completer = QCompleter()
            completer.setCaseSensitivity( Qt.CaseInsensitive )
            completer.setModel( self.conceptosmodel )
            completer.setCompletionColumn( 1 )
    
            self.cuentabancaria = QSqlQueryModel()
            #self.status = False
    #            Rellenar el combobox de las CONCEPTOS
            
            self.cuentabancaria.setQuery( """
               SELECT idcuentacontable,cc.codigo,concat(cc.descripcion,"  Moneda: ",tm.moneda) as Descripcion,tm.moneda as Moneda,
               tm.simbolo as simbolo,tm.idtipomoneda as IDMONEDA
               FROM cuentasbancarias c 
               JOIN cuentascontables cc ON cc.idcuenta=c.idcuentacontable
               JOIN tiposmoneda tm ON tm.idtipomoneda=c.idtipomoneda;
            """ )
    
            
            line = AccountsSelectorLine()
            line.itemId = self.cuentabancaria.record( self.cbocuenta.currentIndex() ).value( "idcuentacontable" ).toInt()[0]
            line.code = self.cuentabancaria.record( self.cbocuenta.currentIndex() ).value( "codigo" ).toString()
            line.name = self.cuentabancaria.record( self.cbocuenta.currentIndex() ).value( "descripcion" ).toString()
            line.amount=self.subtotal.value()
            
            self.editmodel.insertRows(0,2)
            self.editmodel.lines[0]=line
            
            self.cbocuenta.setModel( self.cuentabancaria )
            self.cbocuenta.setCurrentIndex(-1)
            self.cbocuenta.setModelColumn( 2 )
            
            self.tabledetails.resizeColumnsToContents()       
            self.tabledetails.setColumnHidden(0,True)
    
    
            completercuenta = QCompleter()
            completercuenta.setCaseSensitivity( Qt.CaseInsensitive )
            completercuenta.setModel( self.cuentabancaria )
            completercuenta.setCompletionColumn( 1 )
            
            self.conceptowidget.setCurrentIndex(1)
            self.beneficiariowidget.setCurrentIndex(1)
            self.cuentawidget.setCurrentIndex(1)
            
            
            
            self.lblretencion.setText("")
            
            self.status = False
        except UserWarning as inst:
            QMessageBox.warning(self, "Llantera Esquipulas", str(inst))
            self.status = True
        except Exception as inst:
            print inst
            self.status = True
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()         
        
        
    
    @pyqtSlot( "QDateTime" )
    def on_dtPicker_dateTimeChanged( self, datetime ):
        """
        Asignar la fecha al objeto __document
        """
        if self.editmodel is not None:
            super(frmCheques, self).on_dtPicker_dateTimeChanged(datetime)
            self.lbltipocambio.setText(str(self.editmodel.exchangeRate))
            
class ROAccountsModel( QSortFilterProxyModel ):
    def __init__( self,dbcursor = None):
        super( QSortFilterProxyModel, self ).__init__()
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == MONTO:
                try:
                    return moneyfmt( Decimal( value.toString() ), 4, "C$" )
                except InvalidOperation:
                    return Decimal(0)
        return value

    
class ChequesFiltroDelegate(AccountsSelectorDelegate):
    def __init__(self,query):
        super(ChequesFiltroDelegate,self).__init__(query)
        self.__accounts=self.accounts
        self.accounts=QSortFilterProxyModel()
        self.accounts.setDynamicSortFilter(True)
        self.accounts.setSourceModel(self.__accounts)
        self.accounts.setFilterKeyColumn(0)
    
    def setModelData( self, editor, model, index ):

        if index.column() in ( 1, 2 ):
            model.setData( index, [
                                   self.accounts.index( editor.currentIndex(), 0 ).data(),
                                   self.accounts.index( editor.currentIndex(), 1 ).data(),
                                   self.accounts.index( editor.currentIndex(), 2 ).data()
                                   ] )
            try:
                index = self.accounts.mapToSource(self.accounts.index(editor.currentIndex(),0))
                del self.__accounts.items[index.row()]
            except IndexError:
                pass
        else:
            QStyledItemDelegate.setModelData( self, editor, model, index )

    def createEditor( self, parent, option, index ):
        
        if index.column() in ( 1, 2):
            if index.data() != "":
                self.__accounts.items.append( [
                                         index.model().lines[index.row()].itemId,
                                         index.model().lines[index.row()].code,
                                         index.model().lines[index.row()].name
                                         ] )
            sp = SearchPanel( self.accounts, parent )
            sp.setColumn( index.column() )
            return sp
        elif index.column() == 3:
            doublespinbox = QDoubleSpinBox( parent )
            doublespinbox.setMinimum( -1000000 )
            doublespinbox.setMaximum( 1000000 )
            doublespinbox.setDecimals( 4 )

            return doublespinbox