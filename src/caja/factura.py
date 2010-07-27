# -*- coding: utf-8 -*-
'''
Created on 25/05/2010

@author: Luis Carlos Mejia
'''
from PyQt4.QtGui import QMainWindow, QDataWidgetMapper, QSortFilterProxyModel, QMessageBox, QAbstractItemView, QCompleter
from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL, QModelIndex, QTimer, QDateTime,QDate
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase
from decimal import Decimal
import functools
from PyQt4.QtSql import  QSqlQuery

from utility.base import Base
from ui.Ui_factura import Ui_frmFactura
from document.factura.facturadelegate import FacturaDelegate
from document.factura.facturamodel import FacturaModel
from utility.moneyfmt import moneyfmt
from utility.reports import frmReportes
from recibo import dlgRecibo

#controles
IDDOCUMENTO, NDOCIMPRESO, CLIENTE,VENDEDOR, SUBTOTAL, IVA, TOTAL, OBSERVACION, FECHA, BODEGA, TASA,TASAIVA,ANULADO = range( 13 )

#table
IDARTICULO, DESCRIPCION, CANTIDAD, PRECIO, TOTALPROD, IDDOCUMENTOT = range( 6 )
class frmFactura( Ui_frmFactura, QMainWindow, Base ):
    """
    Implementacion de la interfaz grafica para entrada compra
    """

    def __init__( self, user, parent ):
        '''
        Constructor
        '''
        super( frmFactura, self ).__init__( parent )

        self.setupUi( self )
        self.parentWindow = parent
        Base.__init__( self )
        self.__status = True

#       las acciones deberian de estar ocultas
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )
#        El modelo principal
        self.navmodel = QSqlQueryModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = RONavigationModel( self )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )
#        Este es el modelo con los datos de la con los detalles
        self.detailsmodel = QSqlQueryModel( self )
        self.detailsproxymodel = RODetailsModel( self )
        self.detailsproxymodel.setSourceModel( self.detailsmodel )

        #inicializando el documento
        self.editmodel = None
        self.lblanulado.setHidden(True)

        QTimer.singleShot( 0, self.loadModels )


    def updateModels( self ):
        """
        Recargar todos los modelos
        """

        try:

            if not QSqlDatabase.database().isOpen():
                QSqlDatabase.database().open()


#        El modelo principal
            self.navmodel.setQuery( """
                SELECT
                    d.iddocumento,
                    d.ndocimpreso as 'No. Factura',
                    GROUP_CONCAT(IF(p.tipopersona=1,p.nombre,"") SEPARATOR '') as Cliente,
                    GROUP_CONCAT(IF(p.tipopersona=3,p.nombre,"") SEPARATOR '') as Vendedor,
                    (
                    @subtotal:=
                    (
                    d.total / (1+ IF(valorcosto IS NULL,0,valorcosto/100))
                    )
                    ) as subtotal,
                    d.total-@subtotal as iva,
                    d.Total,
                    d.observacion,
                    DATE_FORMAT(d.fechacreacion,'%d/%m/%Y') as Fecha,
                    b.nombrebodega as Bodega,
                    tc.tasa as 'Tipo de Cambio Oficial',
                    valorcosto as tasaiva,
                    d.anulado as Anulada
                FROM documentos d
                JOIN bodegas b ON b.idbodega=d.idbodega
                JOIN tiposcambio tc ON tc.idtc=d.idtipocambio
                JOIN personasxdocumento pxd ON pxd.iddocumento=d.iddocumento
                JOIN personas p ON p.idpersona=pxd.idpersona
                LEFT JOIN costosxdocumento cd ON cd.iddocumento=d.iddocumento
                LEFT JOIN costosagregados ca ON ca.idcostoagregado=cd.idcostoagregado
                WHERE d.idtipodoc=5
                GROUP BY iddocumento
                ;
            """ )
    #        El modelo que filtra a self.navmodel
#            self.navproxymodel = QSortFilterProxyModel( self )

    #        Este es el modelo con los datos de la tabla para navegar
            self.detailsmodel.setQuery( """
                SELECT
                    ad.idarticulo,
                    ad.descripcion,
                    -a.unidades as Unidades,
                    a.precioventa as 'Precio Unit $',
                    -a.unidades*a.precioventa as 'Total $',
                    a.iddocumento
                FROM articulosxdocumento a
                JOIN vw_articulosdescritos ad on a.idarticulo=ad.idarticulo
                WHERE a.precioventa IS NOT NULL
                ;
            """ )

    #        Este objeto mapea una fila del modelo self.navproxymodel a los controles

            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.lblnfac, NDOCIMPRESO , "text" )
            self.mapper.addMapping( self.mtxtobservaciones, OBSERVACION )
            self.mapper.addMapping( self.txtcliente, CLIENTE, "text" )
            self.mapper.addMapping( self.txtvendedor, VENDEDOR, "text" )
            self.mapper.addMapping( self.txtbodega, BODEGA, "text" )


    #        asignar los modelos a sus tablas
            
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsproxymodel )
            self.tabledetails.setColumnHidden( IDARTICULO, True )

            self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
            self.tablenavigation.setColumnHidden( OBSERVACION, True )
            self.tablenavigation.setColumnHidden( SUBTOTAL, True )
            self.tablenavigation.setColumnHidden( IVA, True )
            self.tablenavigation.setColumnHidden( TASAIVA, True )
            self.tablenavigation.setColumnHidden( TASA, True )
#            
#            self.navigate( 'last' )

        except Exception as inst:
            print inst
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()



    def updateLabels( self ):
        self.lblsubtotal.setText( moneyfmt( self.editmodel.subtotal, 4, "$" ) )
        self.lbliva.setText( moneyfmt( self.editmodel.IVA, 4, "$" ) )
        self.lbltotal.setText( moneyfmt( self.editmodel.total, 4, "$" ) )

        self.tabledetails.resizeColumnsToContents()

    def removeLine( self ):
        """
        Funcion usada para borrar lineas de la tabla
        """
        index = self.tabledetails.currentIndex()

        if not index.isValid():
            return
        row = index.row()

        self.tabledetails.removeRows( row )
        self.updateLabels()

# MANEJO EL EVENTO  DE SELECCION EN EL RADIOBUTTON
    @pyqtSlot( "bool" )
    def on_rbcontado_toggled( self, on ):
        """
        Asignar las observaciones al objeto __qdocument
        """
        if not self.editmodel is None:
            self.editmodel.escontado = 1 if on else 0


    @pyqtSlot(  )
    def on_actionPreview_activated( self ):
        """
        Funcion usada para mostrar el reporte de una entrada compra
        """

        report = frmReportes( "facturas.php?doc=%d" % self.navmodel.record( self.mapper.currentIndex() ).value( "iddocumento" ).toInt()[0] , self.parentWindow.user, self )

        report.show()


    @pyqtSlot(  )
    def on_actionNew_activated( self ):
        """
        activar todos los controles, llenar los modelos necesarios, crear el modelo EntradaCompraModel, aniadir una linea a la tabla
        """
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception( u"No se pudo establecer la conexión con la base de datos" )
    
                QMessageBox.warning( None,
                "Llantera Esquipulas",
                """Hubo un error al conectarse con la base de datos""",
                QMessageBox.StandardButtons( \
                    QMessageBox.Ok ),
                QMessageBox.Ok )
            else:
    #            Rellenar el combobox de los CLLIENTES
                self.clientesModel = QSqlQueryModel()
                self.clientesModel.setQuery( """
                    SELECT idpersona , nombre AS cliente 
                    FROM personas
                    WHERE tipopersona = 1
                """ )
    
    #Verificar si existen clientes            
                if self.clientesModel.rowCount() == 0:
                    QMessageBox.information( None, "Factura", "No existen clientes en la base de datos" )
                    return ""

    #            Rellenar el combobox de los vendedores
                self.vendedoresModel = QSqlQueryModel()
                self.vendedoresModel.setQuery( """
                    SELECT idpersona , nombre AS cliente 
                    FROM personas
                    WHERE tipopersona = 3
                """ )
    
    #Verificar si existen clientes            
                if self.vendedoresModel.rowCount() == 0:
                    QMessageBox.information( None, "Factura", "No existen vendedores en la base de datos" )
                    return ""
    
    #Crear el delegado con los articulo y verificar si existen articulos
                query = QSqlQuery("""
                        SELECT
            a.idarticulo,
            a.descripcion,
            c.valor*(1+a.ganancia/100) as precio,
            c.valor as costodolar,
            c.valor * tc.tasa as costo,
            SUM(ad.unidades) as Existencia,
            b.idbodega
        FROM vw_articulosdescritos a
        JOIN costosarticulo c ON a.idarticulo=c.idarticulo
        JOIN articulosxdocumento ad ON ad.idarticulo=a.idarticulo
        JOIN documentos d ON d.iddocumento = ad.iddocumento
        JOIN bodegas b ON b.idbodega=d.idbodega
        JOIN tiposcambio tc ON tc.idtc= c.idtc
        WHERE c.activo=1
        GROUP BY ad.idarticulo,b.idbodega
        HAVING SUM(ad.unidades) >0
                """)             
                self.accounts = QSqlQueryModel()
                self.accounts.setQuery(query)
                self.proxyAccounts = QSortFilterProxyModel()
                self.proxyAccounts.setSourceModel(self.accounts)
                self.proxyAccounts.setFilterKeyColumn(6)

                delegate = FacturaDelegate(self.proxyAccounts)
                if delegate.proxymodel.rowCount() == 0:
                    QMessageBox.information( None, "Factura", "No hay articulos en existencia" )
                    return ""
#
#                self.proxyAccounts.setFilterRegExp('0')
#                print "filas " + str(self.proxyAccounts.rowCount())
                
    #            Rellenar el combobox de las BODEGAS
                self.bodegasModel = QSqlQueryModel()
                self.bodegasModel.setQuery( """
                 SELECT
                        b.idbodega,
                        b.nombrebodega as Bodega
                FROM bodegas b
                JOIN documentos d ON b.idbodega=d.idbodega
        JOIN articulosxdocumento ad ON ad.iddocumento=d.iddocumento
        GROUP BY ad.idarticulo,b.idbodega
        HAVING SUM(ad.unidades)>0    
                """ )
    
    #Verificar si existen bodegas            
                if self.bodegasModel.rowCount() == 0:
                    QMessageBox.information( None, "Factura", "No existe ninguna bodega en la base de datos" )
                    return ""
    
#Verificar IVA    
                query = QSqlQuery( """
                SELECT idcostoagregado, valorcosto 
                FROM costosagregados c 
                WHERE idtipocosto = 1 AND activo = 1 
                ORDER BY idtipocosto;
                """ )
                query.exec_()
                if not query.size() == 1:
                    QMessageBox.information( None, "Factura", "No fue posible obtener el porcentaje del IVA" )
                    return ""
                query.first()

                self.editmodel = FacturaModel( self.parentWindow.datosSesion )
                self.editmodel.ivaId = query.value( 0 ).toInt()[0]
                self.lbltasaiva.setText(query.value( 1 ).toString() + '%')
                self.editmodel.ivaTasa = Decimal( query.value( 1 ).toString() ) 
                self.status = False
                
                self.dtPicker.setDate(self.parentWindow.datosSesion.fecha)
                

    
                self.cbcliente.setModel( self.clientesModel )
                self.cbcliente.setCurrentIndex( -1 )
                self.cbcliente.setFocus()
                self.cbcliente.setModelColumn( 1 )
                completer = QCompleter()
                completer.setCaseSensitivity( Qt.CaseInsensitive )
                completer.setModel( self.clientesModel )
                completer.setCompletionColumn( 1 )
                self.cbcliente.setCompleter(completer)
    
    
                self.cbbodega.setModel( self.bodegasModel )
                self.cbbodega.setCurrentIndex( -1 )
                self.cbbodega.setModelColumn( 1 )    
                completerbodega = QCompleter()
                completerbodega.setCaseSensitivity( Qt.CaseInsensitive )
                completerbodega.setModel( self.bodegasModel )
                completerbodega.setCompletionColumn( 1 )
                self.cbbodega.setCompleter(completerbodega)

                self.cbvendedor.setModel( self.vendedoresModel )
                self.cbvendedor.setCurrentIndex( -1 )
                self.cbvendedor.setModelColumn( 1 )
                completerVendedor = QCompleter()
                completerVendedor.setCaseSensitivity( Qt.CaseInsensitive )
                completerVendedor.setModel( self.vendedoresModel )
                completerVendedor.setCompletionColumn( 1 )
                self.cbvendedor.setCompleter(completerVendedor)
                
                
                
    #           Cargar el numero de la factura actual
                query = QSqlQuery( """
                SELECT
                      MAX(CAST(ndocimpreso AS SIGNED))+1
                FROM documentos d
                WHERE idtipodoc=5
                ;
                """ )
    
                query.exec_()
                query.first()
    
                n = query.value( 0 ).toString()
                if n == "0" or n=="" :
                    n = "1"
    
                self.lblnfac.setText( n )
                self.editmodel.printedDocumentNumber = n
    
    
                self.tabledetails.setModel( self.editmodel )
                self.tabledetails.setItemDelegate( delegate )
    
    
    
    
                self.addLine()
                self.connect( self.editmodel, SIGNAL( "dataChanged(QModelIndex,QModelIndex)" ), self.updateLabels )
        except Exception as inst:
            QMessageBox.critical(self, "Llantera Esquipulas", "El sistema no pudo iniciar una nueva factura")
            print inst
            self.status = True
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()


    @pyqtSlot(  )
    def on_actionCancel_activated( self ):
        """
        Aca se cancela la edicion del documento
        """
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsproxymodel )
        self.status = True


    def updateDetailFilter( self, index ):
        self.lbliva.setText(moneyfmt(Decimal(self.navmodel.record( index ).value( "iva" ).toString())))
        self.lblsubtotal.setText(moneyfmt(Decimal(self.navmodel.record( index ).value( "subtotal" ).toString())))
        self.lbltotal.setText(moneyfmt(Decimal(self.navmodel.record( index ).value( "total" ).toString())))
        self.lbltasaiva.setText(self.navmodel.record( index ).value( "tasaiva" ).toString() +'%')
        self.lblanulado.setHidden(self.navmodel.record( index ).value( "Anulada" ).toInt()[0]==0)
        self.dtPicker.setDate(QDate.fromString(self.navmodel.record( index ).value( "Fecha" ).toString(),"dd/MM/yyyy"))
        
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        print self.navmodel.record( index ).value( "iddocumento" ).toString() 
        self.detailsproxymodel.setFilterRegExp( self.navmodel.record( index ).value( "iddocumento" ).toString() )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )
        





    def setControls( self, status ):
        """
        @param status: false = editando        true = navegando
        """
        self.mtxtobservaciones.setReadOnly( status )
        self.rbcontado.setEnabled( ( not status ) )
        self.rbcredito.setEnabled( not status )

        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )
        if status:
            self.navigate( 'last' )
            self.swcliente.setCurrentIndex( 1 )
            self.swbodega.setCurrentIndex( 1 )
            self.swvendedor.setCurrentIndex( 1 )

            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
            self.tabWidget.setCurrentIndex( 0 )
            self.lblnfac.setText( "500" )
            self.mtxtobservaciones.setPlainText( "" )
            self.swcliente.setCurrentIndex( 0 )
            self.swbodega.setCurrentIndex( 0 )
            self.swvendedor.setCurrentIndex( 0 )
            self.lblsubtotal.setText( "0.0000" )
            self.lbliva.setText( "0.0000" )
            self.lbltotal.setText( "0.0000" )
            self.tabledetails.setEditTriggers( QAbstractItemView.EditKeyPressed | QAbstractItemView.AnyKeyPressed | QAbstractItemView.DoubleClicked )
            self.lblanulado.setHidden(True)


    @pyqtSlot(  )
    def on_txtDocumentNumber_editingFinished( self ):
        """
        Asignar el contenido al objeto documeto
        """
        if not self.editmodel is None:
            self.editmodel.printedDocumentNumber = self.txtDocumentNumber.text()



    @pyqtSlot( "QDate" )
    def on_dtPicker_dateChanged( self, date ):
        """
        Asignar la fecha al objeto __document
        """
        if not self.editmodel is None:
            self.editmodel.datetime = date


    @pyqtSlot(  )
    def on_mtxtobservaciones_textChanged( self ):
        """
        Asignar las observaciones al objeto __document
        """
        if not self.editmodel is None:
            self.editmodel.observations = self.mtxtobservaciones.toPlainText()

    @pyqtSlot( "int" )
    def on_cbcliente_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.clienteId = self.clientesModel.record( index ).value( "idpersona" ).toInt()[0]

    @pyqtSlot( "int" )
    def on_cbvendedor_currentIndexChanged( self, index ):
        """
        asignar proveedor al objeto self.editmodel
        """
        if not self.editmodel is None:
            self.editmodel.vendedorId = self.vendedoresModel.record( index ).value( "idpersona" ).toInt()[0]

    @pyqtSlot( "int" )
    def on_cbbodega_currentIndexChanged( self, index ):
        """
        asignar la bodega al objeto self.editmodel
        """
        if not self.editmodel is None:
            if self.editmodel.rowCount() > 0 and self.editmodel.lines[0].itemDescription != "":
                for line in self.editmodel.lines:
                    if line.itemId > 0 :
                        self.tabledetails.itemDelegate().filtrados=[]
                self.editmodel.removeRows( 0, self.editmodel.rowCount() )
                self.editmodel.insertRow( 0 )

            self.editmodel.bodegaId = self.bodegasModel.record( index ).value( "idbodega" ).toInt()[0]
            self.proxyAccounts.setFilterRegExp('%d'%self.editmodel.bodegaId)           
            
            self.updateLabels()

    @property
    def valid( self ):
        """
        Un documento es valido cuando 
        self.printedDocumentNumber != ""
        self.providerId !=0
        self.validLines >0
        self.ivaId !=0
        self.uid != 0
        self.warehouseId != 0
        """
        if int( self.editmodel.userId ) == 0: 
            raise Exception("No existe el usuario")
        elif int( self.editmodel.clienteId ) == 0:
            QMessageBox.warning(None,"Factura Incompleta","Por favor elija el cliente")
            self.cbcliente.setFocus()
        elif int( self.editmodel.vendedorId ) == 0:
            QMessageBox.warning(None,"Factura Incompleta","Por favor elija el vendedor")
            self.cbvendedor.setFocus()
        elif int( self.editmodel.bodegaId ) == 0:
            QMessageBox.warning(None,"Factura Incompleta","Por favor elija la bodega")
            self.cbbodega.setFocus()
        elif int( self.editmodel.validLines ) == 0:
            QMessageBox.warning(None,"Factura Incompleta","Algunas filas de la factura estan incompletas")
        else:
            return True
        return False
    
    
    @pyqtSlot(  )
    def on_actionSave_activated( self ):
        """
        Guardar el documento actual
        """
        dialog = dlgRecibo(self)
        if dialog.exec_():
            print "OK"
        else:
            print "Cancel"
        
        return ""
        if self.valid:
            if QMessageBox.question(self, "Llantera Esquipulas", u"¿Esta seguro que desea guardar la factura?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
#                dialog = dlgRecibo(self)
#                if dialog.exec_():
#                    print "OK"
#                else:
#                    print "Cancel"
#                
#                return ""
                if not QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().open()
                
                datetime =QDateTime.currentDateTime()
                datetime.setDate(self.editmodel.datetime)
                self.editmodel.datetime=datetime
                
                if self.editmodel.save():
                    QMessageBox.information( None,
                         "Llantera Esquipulas" ,
                         """El documento se ha guardado con exito""" ) 
                    self.editmodel = None
                    self.updateModels()
                    self.navigate( 'last' )
                    self.status = True
                else:
                    QMessageBox.critical( None,
                        "Llantera Esquipulas" ,
                         """Ha ocurrido un error al guardar el documento""" ) 
    
                if QSqlDatabase.database().isOpen():
                    QSqlDatabase.database().close()



class RONavigationModel( QSortFilterProxyModel ):
    """
    basicamente le da formato a la salida de mapper
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if not value.isValid():
            return None
        if index.column() in ( SUBTOTAL, IVA, TOTAL ):
            if role == Qt.DisplayRole:
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
        elif index.column() == ANULADO:
            if role == Qt.DisplayRole:
                return "Anulada" if value.toInt()[0]==1 else ""
                
        return value

class RODetailsModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los os,
    basicamente esta creado para darle formato al total y al precio
    """
    def __init__( self, dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()

    def columnCount( self, index = QModelIndex() ):
        return 5

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == DESCRIPCION:
                return u"Descripción"
            elif section == PRECIO:
                return "Precio"
            elif section == TOTALPROD:
                return "TOTAL"
            elif section == CANTIDAD:
                return "Cantidad"
        return int( section + 1 )

    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que se utiliza para mostrar los datos del modelo
        """
        value = QSortFilterProxyModel.data( self, index, role )
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() in ( TOTALPROD, PRECIO ):
                return moneyfmt( Decimal( value.toString() ), 4, "US$" )
        return value


