# -*- coding: utf-8 -*-
"""
Module implementing frmConciliacion.
"""
from PyQt4.QtCore import pyqtSlot,QDateTime, QModelIndex, Qt, QTimer, QDate, QVariant
from PyQt4.QtGui import QSortFilterProxyModel, QDataWidgetMapper, QDialog, \
    QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
    QLineEdit, QDateTimeEdit, QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery

from decimal import Decimal
from document.conciliacion import ConciliacionModel, LineaConciliacion
from ui.Ui_conciliacion import Ui_frmConciliacion
from ui.Ui_dlgmovimientosbancarios import Ui_dlgMovimientosBancarios
from document.movimientosbancarios import MovimientosBancariosModel
from utility.accountselector import AccountsSelectorDelegate
from utility.base import Base
from utility import constantes
from utility.decorators import if_edit_model
from utility.moneyfmt import moneyfmt
import logging

FECHA, CONCEPTO, DEBE, HABER, SALDO, CONCILIADO, DELBANCO, \
IDTIPODOC = range( 8 )
FECHA, BANCO, CUENTABANCO, MONEDA, CUENTA, SALDOBANCO, SALDOLIBRO, \
IDCUENTABANCO, IDDOC = range( 9 )
class FrmConciliacion( Base , Ui_frmConciliacion ):
    """
    Formulario para crear nuevas conciliaciones bancarias
    """
    def __init__( self , parent = None ):
        """
        Constructor
        """

        super( FrmConciliacion, self ).__init__( parent )

        self.user = parent.user
        
        self.editmodel = None

        self.status = True

#        las acciones deberian de estar ocultas
        self.actionSave.setVisible( False )
        self.actionCancel.setVisible( False )

#        El modelo principal
        self.navmodel = RONavigationModel( self )
#        El modelo que filtra a self.navmodel
        self.navproxymodel = QSortFilterProxyModel( self )
        self.navproxymodel.setFilterKeyColumn( -1 )
        self.navproxymodel.setSourceModel( self.navmodel )
        self.navproxymodel.setFilterCaseSensitivity ( Qt.CaseInsensitive )

#        Este es el modelo con los datos de la tabla para navegar
        self.detailsmodel = ReadOnlyTableModel( self )
        self.proxymodel = QSortFilterProxyModel( self )
#        CREAR TODOS LOS PROXY MODEL
        self._create_filter_models()

        self.detailsmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )


#        Cargar los modelos en un hilo aparte
        QTimer.singleShot( 0, self.loadModels )


    def _create_filter_models( self ):
        #CREAR PROXY MODEL         


        self.proxymodel.setDynamicSortFilter( True )
        self.proxymodel.setFilterRole( Qt.EditRole )
        self.proxymodel.setFilterRegExp( "1" )
        self.proxymodel.setFilterKeyColumn( CONCILIADO )

#CREAR PROXY MODEL PARA VERIFICAR SI FUE GENERADO POR EL BANCO
        delbancoproxymodel = QSortFilterProxyModel( self )
        delbancoproxymodel.setSourceModel( self.proxymodel )
        delbancoproxymodel.setDynamicSortFilter( True )
        delbancoproxymodel.setFilterRole( Qt.EditRole )
        delbancoproxymodel.setFilterRegExp( "0" )
        delbancoproxymodel.setFilterKeyColumn( DELBANCO )

#CREAR PROXY MODEL PARA VERIFICAR SI FUE GENERADO  POR LA EMPRESA
        empresaproxymodel = QSortFilterProxyModel( self )
        empresaproxymodel.setSourceModel( self.proxymodel )
        empresaproxymodel.setDynamicSortFilter( True )
        empresaproxymodel.setFilterRole( Qt.EditRole )
        empresaproxymodel.setFilterRegExp( "1" )
        empresaproxymodel.setFilterKeyColumn( DELBANCO )

        filtroMenos = "^" + str( constantes.IDND ) + "$|^" + str( constantes.IDCHEQUE ) + "$|^" + str( constantes.IDERROR ) +"$|^" + str( constantes.IDERROR ) + "$"
        filtroMas = "[" + filtroMenos + "]"

#CREAR MODELO PARA DEPOSITOS
        self._setup_proxy_model(DetalleTableModel(self), empresaproxymodel, filtroMas, IDTIPODOC, self.tablalibromas)

#CREAR MODELO PARA CHEQUES
        self._setup_proxy_model(DetalleTableModel(self), empresaproxymodel, filtroMenos, IDTIPODOC, self.tablalibromenos)


#CREAR MODELO PARA NOTAS DE CREDITO
        self._setup_proxy_model(DetalleTableModel(self), delbancoproxymodel, filtroMas, IDTIPODOC, self.tablabancomas)

#CREAR MODELO PARA NOTAS DE DEBITO
        self._setup_proxy_model(DetalleTableModel(self), delbancoproxymodel, filtroMenos, IDTIPODOC, self.tablabancomenos)

    def _setup_proxy_model(self, model, source, regexp, column, table, role = Qt.DisplayRole):
        model.setSourceModel( source )
        model.setFilterRegExp( regexp )
        model.setFilterKeyColumn( column )
        model.setFilterRole(role)
        table.setModel( model )
        

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:
            if not(QSqlDatabase.database().isOpen() or QSqlDatabase.database().open()):
                raise Exception( "No se pudo abrir la base" )

            self.navmodel.setQuery( """
            SELECT
                c.Fecha,
                b.descripcion as Banco,
                cb.ctabancaria,
                m.Simbolo,
                cc.Codigo,
                c.saldolibro,
                c.saldobanco,
                cb.idcuentacontable,
                c.iddocumento
                FROM conciliaciones c
                JOIN cuentasbancarias cb ON c.idcuentabancaria = cb.idcuentacontable
                JOIN bancos b ON b.idbanco = cb.idbanco
                JOIN tiposmoneda m ON m.idtipomoneda = cb.idtipomoneda
                JOIN cuentascontables cc ON cc.idcuenta = cb.idcuentacontable
                ORDER BY c.iddocumento
                ;
            """ )
#        Este objeto mapea una fila del modelo self.navproxymodel a los controles
            self.mapper.setSubmitPolicy( QDataWidgetMapper.ManualSubmit )
            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtbanco, BANCO )
            self.mapper.addMapping( self.txtmoneda, MONEDA )
            self.mapper.addMapping( self.txtcuentabanco, CUENTABANCO )
            self.mapper.addMapping( self.txtcuenta, CUENTA )


#        asignar los modelos a sus tablas
            self.tablenavigation.setModel( self.navproxymodel )
            self.tabledetails.setModel( self.detailsmodel )
            self.proxymodel.setSourceModel( self.detailsmodel )

            self.tablenavigation.setColumnHidden( SALDOBANCO, True )
            self.tablenavigation.setColumnHidden( SALDOLIBRO, True )
            self.tablenavigation.setColumnHidden( IDCUENTABANCO, True )
            self.tablenavigation.setColumnHidden( IDDOC, True )

            self._ocultar_columnas()

        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                u"Hubo un error al tratar de iniciar una nueva conciliación "\
                + "bancaria" )
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()

    def updateDetailFilter( self, _index ):
        if self.tabWidget.currentIndex() == 0:
            self.cargarMovimientos()

    def cargarMovimientos( self ):
        index = self.mapper.currentIndex()
        saldobanco = Decimal( self.navmodel.record( index ).value( "saldobanco" ).toString() )
        saldolibro = Decimal( self.navmodel.record( index ).value( "saldolibro" ).toString() )

        fecha = self.navmodel.record( index ).value( "fecha" ).toDate()
        self.lblfecha.setText( fecha.toString( "MMMM yyyy" ).upper() )
        ctaBanco = self.navmodel.record( index ).value( "idcuentacontable" ).toString()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise Exception( "No se pudo abrir la base" )
            self.detailsmodel.setQuery( "CALL spMovimientoCuenta(" + ctaBanco + "," + fecha.toString( "yyyyMMdd" ) + ");" )
            self.proxymodel.setSourceModel( self.detailsmodel )
        except Exception as inst:
            logging.error( unicode( inst ) )
        finally:
            if self.database.isOpen():
                self.database.close()
        self.tablenavigation.selectRow( self.mapper.currentIndex() )


        self.spbsaldobanco.setValue( saldobanco )
        self.txtsaldolibro.setText( moneyfmt( saldolibro, 4, "C$" ) )

        nc = self.tablabancomas.model().total
        nd = self.tablabancomenos.model().total
        depositos = self.tablalibromas.model().total
        cheques = self.tablalibromenos.model().total
        self.txtcheque.setText( moneyfmt( cheques, 4, "C$" ) )
        self.txtdeposito.setText( moneyfmt( depositos, 4, self.editmodel.moneda ) )
        self.txtnotacredito.setText( moneyfmt( nc, 4, self.editmodel.moneda ) )
        self.txtnotadebito.setText( moneyfmt( nd, 4, self.editmodel.moneda ) )

        self.txttotallibro.setText( moneyfmt( saldobanco + depositos + cheques, 4, self.editmodel.moneda ) )
        self.txttotalbanco.setText( moneyfmt( saldolibro + nc + nd , 4, self.editmodel.moneda ) )
        dif = saldobanco + depositos + cheques - ( saldolibro + nc + nd )
        self.lbldiferencia.setText( moneyfmt( dif, 4, self.editmodel.moneda ) if dif != 0 else "CONCILIADO" )

    def updateLabels( self ):
        self.txttotallibro.setText( moneyfmt( self.editmodel.total_libro, 4, self.editmodel.moneda ) )
        self.txtcheque.setText( moneyfmt( self.editmodel.total_cheques, 4, self.editmodel.moneda ) )
        self.txtdeposito.setText( moneyfmt( self.editmodel.total_depositos, 4, self.editmodel.moneda ) )
        self.txtnotacredito.setText( moneyfmt( self.editmodel.total_nota_credito, 4, self.editmodel.moneda ) )
        self.txtnotadebito.setText( moneyfmt( self.editmodel.total_nota_debito, 4, self.editmodel.moneda ) )

        self.txttotalbanco.setText( moneyfmt( self.editmodel.total_banco, 4, self.editmodel.moneda ) )

        dif = self.editmodel.diferencia
        self.lbldiferencia.setText( ( "Diferencia " + moneyfmt( dif, 4, self.editmodel.moneda ) ) if dif != 0 else "CONCILIADO" )



    @pyqtSlot( float )
    def on_spbsaldobanco_valueChanged ( self, value ):
        """
        Asignar el saldo inicial del banco al modelo
        """
        if not self.editmodel is None:
#            value = self.spbsaldobanco.value()           
            self.editmodel.saldo_inicial_banco = Decimal( str( value ) )
            self.updateLabels()

    @pyqtSlot(  )
    def on_btnAdd_clicked(self):
     
                
        if not self.database.isOpen():
            if not self.database.open():
                raise UserWarning( u"No se pudo establecer la conexión con "\
                                   + "la base de datos" )
        try:
            mov = dlgmovimientosbancarios(self)
#            Rellenar el combobox de las CONCEPTOS


            if mov.conceptosModel.rowCount() == 0:
                raise UserWarning( u"No existen conceptos en la base de "\
                                   + "datos que justifiquen la elaboración de Notas de Crédito o Débito" )
            
            mov.exec_()
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(), unicode( inst ) )
            logging.error( unicode( inst ) )
            logging.error( mov.conceptosModel.query().lastError().text() )
#        except Exception as inst:
#            QMessageBox.critical( self, qApp.organizationName(),
#                                   "Hubo un problema al tratar de crear"\
#                                   + " el nuevo pago" )
#            logging.critical( unicode( inst ) )
#            logging.error( query.lastError().text() )
        finally:
            if QSqlDatabase.database().isOpen():
                QSqlDatabase.database().close()


        
        #        notas = dlgMovimientosBancarios( self )
#        notas.setWindowModality( Qt.WindowModal )
#        if notas.exec_() == QDialog.Accepted:
#            row = self.editmodel.rowCount()
#
#            datosDoc = notas.editmodel.datos
#
#            linea = LineaConciliacion( self.editmodel )
#            linea.fecha = datosDoc.dateTime.toString( "dd/MM/yy" )
#            linea.monto = datosDoc.total
#            linea.idTipoDoc = datosDoc.idTipoDoc
#
#            linea.concepto = notas.editmodel.codigoDoc + " " + linea.fecha
#            linea.saldo = self.editmodel.lines[row - 1].saldo + linea.monto
#            linea.conciliado = 1
#            linea.delBanco = 1
#            linea.concepto2 = notas.editmodel.descripcionDoc + " " + linea.fecha
#            linea.idDoc = 0
#            linea.datos = datosDoc
#            self.editmodel.insertRows( row )
#            self.editmodel.lines[row] = linea
#            index = self.editmodel.index( row, CONCILIADO )
#            self.editmodel.dataChanged.emit( index, index )
        


    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
        self.btnAdd.setVisible( not status )
        self.btnRemove.setVisible( not status )
        self.actionSave.setVisible( not status )
        self.actionCancel.setVisible( not status )
        self.tabnavigation.setEnabled( status )
        self.actionNew.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )
        self.actionPreview.setVisible( status )

        self.spbsaldobanco.setReadOnly( status )
#        self.tabledetails.setColumnHidden(DELBANCO,not status)
        if status:
            self.navigate( 'last' )
            self.tabledetails.setEditTriggers( QAbstractItemView.NoEditTriggers )
        else:
            self.tabledetails.setEditTriggers( QAbstractItemView.AllEditTriggers )
            self.spbsaldobanco.setValue( 0 )
            self.tabWidget.setCurrentIndex( 0 )

    def newDocument( self ):
        """
        Iniciar un nuevo documento
        """
        query = QSqlQuery()
        try:
            if not QSqlDatabase.database().isOpen() and not QSqlDatabase.database().open():
                raise UserWarning( u"No se pudo establecer una conexión "
                                   "con la base de datos" )

            dlgCuenta = dlgSelectCuenta( self )

            fila = -1
    #REPETIR MIENTRAS NO SELECCIONE UNA FILA
            while fila == -1:
                if dlgCuenta.exec_() == QDialog.Accepted:
                    fila = dlgCuenta.tblCuenta.selectionModel().currentIndex().row()
                    if fila == -1:
                        QMessageBox.information( self, qApp.organizationName(),
                                              "Por favor seleccione una cuenta" )
                else:
    #SALIR
                    return




    # SI SELECCIONO UNA FILA SIGUE
            self.editmodel = ConciliacionModel( 
                dlgCuenta.data['saldo_inicial_libro'],
                dlgCuenta.data['fecha'],
                dlgCuenta.data['banco'],
                dlgCuenta.data['cuenta_bancaria'],
                dlgCuenta.data['id_cuenta_contable'],
                dlgCuenta.data['codigo_cuenta_contable'],
                dlgCuenta.data['moneda']
            )

            self.txtbanco.setText( self.editmodel.banco )
            self.txtcuentabanco.setText( self.editmodel.cuenta_bancaria )
            self.txtmoneda.setText( self.editmodel.moneda )
            self.txtcuenta.setText( self.editmodel.codigo_cuenta_contable )
            self.lblfecha.setText( self.editmodel.datetime.toString( "MMMM yyyy" ).upper() )



            if not query.exec_( "CALL spMovimientoCuenta( %d, %s )" % ( 
                    self.editmodel.id_cuenta_contable,
                    self.editmodel.fecha_conciliacion.toString( "yyyyMMdd" )
                )
            ):
                raise Exception( query.lastError().text() )

            row = 0
            while query.next():
                linea = LineaConciliacion( 
                    query.value( 5 ).toBool(), #del_banco
                    Decimal( query.value( 3 ).toString() ), #saldo_inicial
                    Decimal( query.value( DEBE ).toString() ), #monto
                    QDate.fromString( query.value( FECHA ).toString(), 'dd/M/yy' ), #fecha
                    query.value( 6 ).toInt()[0], # tipo_doc
                    query.value( 8 ).toInt()[0], # id_documento
                    query.value( CONCEPTO ).toString() #descripcion
                )
                
                linea.monto = Decimal( query.value( 2 ).toString() )
                self.editmodel.insertRows( row )
                self.editmodel.lines[row] = linea
                row += 1

            #self.editmodel.saldoInicialLibro = self.editmodel.lines[row - 1].saldo
            self.txtsaldolibro.setText( moneyfmt( self.editmodel.saldo_inicial_libro, 4, self.editmodel.moneda ) )
            self.updateLabels()

            self.proxymodel.setSourceModel( self.editmodel )

            self.setControls( False )
            self.tabnavigation.setEnabled( False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setModel( self.editmodel )

            self.tabledetails.resizeColumnsToContents()

            self._ocultar_columnas()

            self.editmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )

        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   u"Hubo un error al intentar iniciar una"
                                   + u" nueva conciliación" )
        finally:
            if self.database.isOpen():
                self.database.close()

    def _ocultar_columnas( self ):
        for table in ( self.tablabancomas, self.tablalibromas, self.tablabancomenos, self.tablalibromenos):
            table.setColumnHidden( HABER, True )
            table.setColumnHidden( CONCILIADO, True )
            table.setColumnHidden( SALDO, True )
            table.setColumnHidden( IDTIPODOC, True )
            table.setColumnHidden( DELBANCO, True )

        self.tabledetails.setColumnHidden( IDTIPODOC, True )



    def save( self ):
        """
        Guardar el documento actual
        """
        if not self.valid:
            return None

        if QMessageBox.question( self,
                                 qApp.organizationName(),
                                  u"¿Desea guardar el documento?",
                                   QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
            if self.editmodel.save():
                QMessageBox.information( self,
                                         qApp.organizationName(),
                     u"El documento se ha guardado con éxito" )
                self.editmodel = None
                self.updateModels()
                self.navigate( 'last' )
                self.status = True
            else:
                QMessageBox.critical( self,
                     qApp.organizationName(),
                    "Ha ocurrido un error al guardar el documento" )




    def cancel( self ):
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsmodel )
        self.proxymodel.setSourceModel( self.detailsmodel )
        self._ocultar_columnas()
        self.status = True


    @pyqtSlot( bool )
    @if_edit_model
    def on_btnremove_clicked( self, _checked ):

        filas = []
        for index in self.tabledetails.selectedIndexes():
            pos = index.row()
            if pos > 0 and  not  pos in filas and self.editmodel.lines[pos].idDoc == 0:
                filas.append( pos )

        if len( filas ) > 0:
            filas.sort( None, None, True )
            for pos in filas:
                self.editmodel.removeRows( pos )

            self.updateLabels()


class dlgmovimientosbancarios (QDialog,Ui_dlgMovimientosBancarios):
    def __init__( self, parent  ):
        super( dlgmovimientosbancarios, self ).__init__( parent ) 
        self.conceptosModel = QSqlQueryModel() 
        self.setupUi( self )
        self.database = QSqlDatabase.database()
        self.proxymodel = QSortFilterProxyModel()
        self.editmodel = MovimientosBancariosModel()
        
        
        fecha = self.parent().editmodel.fechaConciliacion
        self.dtPicker.setMaximumDate(fecha)
        self.dtPicker.setMinimumDate(QDate(fecha.year(),fecha.month(),1))
        self.cbtipodoc.addItem(u"Nota de Crédito")
        self.cbtipodoc.addItem(u"Nota de Débito")
        
        self.conceptosModel.setQuery( """
               SELECT idconcepto, descripcion,idtipodoc FROM conceptos c WHERE idtipodoc in (%d,%d );
            """ %(constantes.IDNOTACREDITO,constantes.IDND) )
        
        
        self.proxymodel.setSourceModel(self.conceptosModel)
        self.proxymodel.setFilterKeyColumn(2)
        self.proxymodel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cbconcepto.setModel(self.proxymodel)
        self.cbconcepto.setModelColumn(1)
        self.buttonBox.rejected.connect( self.reject )
        self.buttonBox.accepted.connect( self.aceptar )
        
        self.editmodel.tipoDoc = constantes.IDDEPOSITO 

        
        self.cuentasDelegate = AccountsSelectorDelegate( QSqlQuery( """
            SELECT c.idcuenta, c.codigo, c.descripcion
            FROM cuentascontables c
            JOIN cuentasxdocumento cd ON c.idcuenta = cd.idcuenta
            WHERE c.idcuenta in (%d,%d,%d)
            """ %(constantes.CAJAGENERAL,constantes.CAJACHICA, constantes.CAPITAL) ) )


        self.editmodel.insertRow( 1 )
        self.editmodel.lines[0].itemId = parent.editmodel.idCuentaContable
        self.editmodel.lines[0].code = parent.txtcuenta.text()
        self.editmodel.lines[0].name = parent.txtcuenta.toolTip()
        

        self.editmodel.insertRow( 1 )
        self.editmodel.fechaDoc = QDateTime.currentDateTime()
        self.editmodel.autorId = parent.user.uid
            #        Crea un edit delegate para las cuentas
        self.tabledetails.setItemDelegate( self.cuentasDelegate )
        self.tabledetails.setModel( self.editmodel )
        self.tabledetails.setEditTriggers( 
                          QAbstractItemView.EditKeyPressed |
                          QAbstractItemView.AnyKeyPressed |
                          QAbstractItemView.DoubleClicked )

        self.tabledetails.setColumnHidden(0,False)
        
        
    
    @pyqtSlot( int )
    def on_cbtipodoc_currentIndexChanged(self,index):
        self.editmodel.tipoDoc = constantes.IDNOTACREDITO if self.cbtipodoc.currentIndex()== 0 else constantes.IDND
        self.proxymodel.setFilterRegExp("%d"%self.editmodel.tipoDoc)

    @pyqtSlot( int )
    def on_cbconcepto_currentIndexChanged(self,index):
        self.editmodel.conceptoId =self.conceptosModel.record( index ).value( "idconcepto" ).toInt()[0]
        
     
    def aceptar(self):
        """
    Guardar el documento actual
        """
        self.editmodel.totalDoc =    self.editmodel.lines[0].amount 
        self.editmodel.tipoDoc = constantes.IDNOTACREDITO if self.cbtipodoc.currentIndex()== 0 else constantes.IDND
        if self.editmodel.valid:
#            Base.save( self, True )
            if QMessageBox.question( self,
                                     qApp.organizationName(),
                                      u"¿Desea guardar el documento?",
                                       QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes:
                if self.editmodel.save():
                    QMessageBox.information( self,
                                             qApp.organizationName(),
                         u"El documento se ha guardado con éxito" )
                else:
                    QMessageBox.critical( self,
                         qApp.organizationName(),
                        "Ha ocurrido un error al guardar el documento" )
            self.accept()

            
        else:
            QMessageBox.information(None, "Datos Incompletos", self.editmodel.mensajeError)



#************************************************
class dlgSelectCuenta( QDialog ):

    def __init__( self, parent = None ):
        super( dlgSelectCuenta, self ).__init__( parent )
        self.padre = parent

        self.ctaBancomodel = QSqlQueryModel()
        self.ctaBancomodel.setQuery( """
        SELECT
            b.descripcion as Banco,
            cb.ctabancaria as 'No. Cuenta',
            tm.simbolo as Moneda,
            c.codigo as 'Codigo Contable',
            c.idcuenta as Id,
            c.descripcion as 'Cuenta Contable',
            IF(
                con.fecha IS NULL,
                LAST_DAY(MIN(d.fechacreacion)),
                (MAX(con.fecha) + INTERVAL 1 MONTH))
                AS conciliar

        FROM cuentasbancarias cb
        JOIN bancos b ON cb.idbanco=b.idbanco
        JOIN cuentascontables c ON c.idcuenta=cb.idcuentacontable
        JOIN tiposmoneda tm ON tm.idtipomoneda=cb.idtipomoneda
        LEFT JOIN conciliaciones con ON con.idcuentabancaria=cb.idcuentacontable
        LEFT JOIN cuentasxdocumento cd ON cd.idcuenta=c.idcuenta
        LEFT JOIN documentos d ON cd.iddocumento = d.iddocumento
        WHERE d.iddocumento IS NOT NULL
        GROUP BY c.idcuenta
         ;
        """ )
#        
#        if self.ctaBancomodel.rowCount() == 0 :
#            QMessageBox.critical(self,"Cuentas Bancarias","No existe ninguna cuenta bancaria")
#            self.destroy()


        self.setWindowTitle( u"Elija fecha y cuenta bancaria para la conciliación" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.ctaBancomodel )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )

        self.tblCuenta = QTableView()
        self.tblCuenta.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tblCuenta.setSelectionBehavior( QAbstractItemView.SelectRows )

        self.tblCuenta.setModel( self.filtermodel )
        buttonbox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )

        self.txtSearch = QLineEdit()
        formlayout = QFormLayout()

        formlayout.addRow( "&Buscar", self.txtSearch )



        self.dtPicker = QDateTimeEdit()
        self.dtPicker.setReadOnly( True )
#        self.dtPicker.setCalendarPopup(True)                                       
        self.dtPicker.setAlignment( Qt.AlignHCenter )
        self.dtPicker.setDisplayFormat( "MMMM 'd'el yyyy" )
#        self.dtPicker.setMinimumDate(QDate(2009,1,1))
        fecha = QDate.currentDate()
        self.dtPicker.setDate( QDate( fecha.year(), fecha.month(), fecha.daysInMonth() ) )

        fechalayout = QFormLayout()
        fechalayout.addRow( "&Fecha", self.dtPicker )

        layout = QVBoxLayout()


        layout.addLayout( fechalayout )
        layout.addWidget( self.tblCuenta )
        layout.addLayout( formlayout )
        layout.addWidget( buttonbox )
        self.setLayout( layout )

        self.setMinimumWidth( 400 )

        buttonbox.accepted.connect( self.aceptar )
        buttonbox.rejected.connect( self.reject )
        self.txtSearch.textChanged[unicode].connect( self.updateFilter )
        self.tblCuenta.selectionModel().currentChanged[QModelIndex, QModelIndex].connect( self.on_tblCuenta_currentChanged )

        self.setModal( True )
        self.setWindowFlags( Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint )
        self.show()
        self.tblCuenta.setFocus()
        self.tblCuenta.selectRow( 0 )
        self.tblCuenta.setColumnHidden( 4, True )
        self.tblCuenta.setColumnHidden( 5, True )
        self.tblCuenta.setColumnHidden( 6, True )
        self.tblCuenta.horizontalHeader().setStretchLastSection( True )
        self.tblCuenta.resizeColumnsToContents()

    @property
    def data( self ):
        data = {}
        fila = self.tblCuenta.selectionModel().currentIndex().row()
        fecha = self.dtPicker.date()

        data['banco'] = self.filtermodel.index( fila, 0 ).data().toString()
        data['id_cuenta_contable'] = self.filtermodel.index( fila, 4 ).data().toInt()[0]
        data['codigo_cuenta_contable'] = self.filtermodel.index( fila, 3 ).data().toString()
        data['cuenta_bancaria'] = self.filtermodel.index( fila, 5 ).data().toString()
        data['fecha'] = QDate( fecha.year(), fecha.month(), fecha.daysInMonth() )
        data['moneda'] = self.filtermodel.index( fila, 2 ).data().toString()


        if not QSqlDatabase.database().isOpen() and not QSqlDatabase.open():
            raise Exception( QSqlDatabase.lastError() )

        query = QSqlQuery()
        if not query.exec_( "CALL spSaldoCuenta( %d, %s )" % ( 
                data['id_cuenta_contable'],
                QDate( data['fecha'].year(), data['fecha'].month(), data['fecha'].daysInMonth() ).toString( "yyyyMMdd" )
            )
        ):
            raise Exception( query.lastError().text() )

        query.first()

        data['saldo_inicial_libro'] = Decimal( query.value( 0 ).toString() )



        return data

    def aceptar( self ):
        fecha = QDate.currentDate()
        fecha = QDate( fecha.year(), fecha.month(), fecha.daysInMonth() )
        if self.dtPicker.date() > fecha:
            QMessageBox.information( None, "Cuentas Bancarias", "La cuenta seleccionada ya fue conciliada" )
        else:
            return self.accept()


    def exec_( self ):
        if self.ctaBancomodel.rowCount() == 0:
            QMessageBox.critical( self.padre, "Cuentas Bancarias",
                "No existe ninguna cuenta bancaria con movimientos en este mes" )
            return self.reject()
        else:
            return QDialog.exec_( self )

    def updateFilter( self, str ):
        self.filtermodel.setFilterWildcard( str )

#    @pyqtSlot( "QModelIndex" )
#    def on_tblCuenta_clicked(self, index):
    def on_tblCuenta_currentChanged( self, _current, _previous ):
        fila = self.tblCuenta.selectionModel().currentIndex().row()
        fecha = self.filtermodel.index( fila, 6 ).data().toDate()
        if fecha.toString() != "":
            self.dtPicker.setDate( fecha )
        else:
            fecha = QDate.currentDate()
#            self.dtPicker.setMaximumDate(QDate(fecha.year(),fecha.month(),fecha.daysInMonth()))


#************************************************
class RONavigationModel( QSqlQueryModel ):
    """
        Esta funcion redefine data en la clase base, es el metodo 
        que se utiliza para mostrar los datos del modelo
    """
    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo 
        que se utiliza para mostrar los datos del modelo
        """
        if not index.isValid():
            return None
        value = QSqlQueryModel.data( self, index, role )
        if index.column() == FECHA and role == Qt.DisplayRole:
            value = value.toDate().toString( "MMMM yyyy" )
        return value


    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if  section == FECHA:
                return "Fecha"
            elif section == CUENTABANCO:
                return "No. Bancaria"
            elif section == BANCO:
                return "Banco"
            elif section == MONEDA:
                return "Moneda"



        return QSqlQueryModel.headerData( self, section , orientation, role )

#
class ReadOnlyTableModel( QSqlQueryModel ):
    """
    """
    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:

            if  section == FECHA:
                return "Fecha"
            elif section == CONCEPTO:
                return "Concepto"
            elif section == DEBE:
                return "DEBE"
            elif section == HABER:
                return "HABER"
            elif section == SALDO:
                return "SALDO"
            elif section == CONCILIADO:
                return "Conciliado"
            elif section == DELBANCO:
                return "Doc. Externo"

        return int( section + 1 )
    def columnCount( self, _index = QModelIndex() ):
        return 8

    def flags( self, index ):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == CONCILIADO:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo 
        que se utiliza para mostrar los datos del modelo
        """

        if not index.isValid():
            return None

        column = index.column()

        value = QSqlQueryModel.data( self, index, role )

        if column == CONCILIADO:
            if role == Qt.CheckStateRole and index.row() > 0:
                value = QSqlQueryModel.data( self, self.index( index.row(), 4 ), Qt.DisplayRole ).toInt()[0]
                return QVariant( Qt.Checked ) if value == 1 else QVariant( Qt.Unchecked )
            elif role == Qt.EditRole:
                return QSqlQueryModel.data( self, self.index( index.row(), 4 ), Qt.DisplayRole ).toInt()[0]
            else:
                return None
        elif column == SALDO:
            if role == Qt.DisplayRole:
                value = QSqlQueryModel.data( self, self.index( index.row(), 3 ), Qt.DisplayRole )
                value = Decimal( value.toString() )
                return moneyfmt( value, 4, "C$" )
        elif column == DEBE:
            if role == Qt.DisplayRole:
                value = Decimal( value.toString() )
                return moneyfmt( value, 4, "C$" ) if value > 0 else ""
            elif role == Qt.EditRole:
                return value
        elif column == HABER:
            if role == Qt.DisplayRole:
                value = Decimal( QSqlQueryModel.data( self, self.index( index.row(), DEBE ), role ).toString() )
                return moneyfmt( value * -1, 4, "C$" ) if value < 0 else ""
        elif column == CONCEPTO:
            if role == Qt.ToolTipRole:
                value = QSqlQueryModel.data( self, self.index( index.row(), 7 ), Qt.DisplayRole )
                return value
            elif role == Qt.DisplayRole:
                return value
            else:
                return None
        elif column == DELBANCO:
            if role == Qt.EditRole:
                value = QSqlQueryModel.data( self, self.index( index.row(), 5 ), Qt.DisplayRole )
                return value
            elif role == Qt.DisplayRole and index.row() > 0:
                value = QSqlQueryModel.data( self, self.index( index.row(), 5 ), Qt.DisplayRole )
                return "Si" if value == 1 else "No"
        elif column == IDTIPODOC:
            if role == Qt.EditRole:
                value = QSqlQueryModel.data( self, self.index( index.row(), 6 ), Qt.DisplayRole )
                return value
        elif column == FECHA:
            return value
        return None

class DetalleTableModel( QSortFilterProxyModel ):
    """
    El modelo que maneja la tabla en la que se previsualizan los documentos,
    basicamente esta creado para darle formato al total y al precio
    """
    def __init__( self, _dbcursor = None ):
        super( QSortFilterProxyModel, self ).__init__()
        self.setDynamicSortFilter( True )
        self.setFilterRole( Qt.EditRole )

    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int( Qt.AlignLeft | Qt.AlignVCenter )
            return int( Qt.AlignRight | Qt.AlignVCenter )
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:

            if  section == FECHA:
                return "Fecha"
            elif section == CONCEPTO:
                return "Concepto"
            elif section == DEBE:
                return "Monto"
            elif section == SALDO:
                return "Saldo"

        return int( section + 1 )
    def rowCount( self, _index = QModelIndex() ):
        return QSortFilterProxyModel.rowCount( self )

    def flags( self, _index ):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable



    def data( self, index, role = Qt.DisplayRole ):
        """
        Esta funcion redefine data en la clase base, es el metodo que 
        se utiliza para mostrar los datos del modelo
        """
        if not index.isValid():
            return None

        if index.column() == DEBE:
            _row = self.mapToSource( index ).row()
#            value = self.sourceModel().sourceModel().lines[row].monto
#            try:
            value = QSortFilterProxyModel.data( self, index, Qt.EditRole ).toString()
            value = Decimal( value if value != "" else 0 )

            if role == Qt.EditRole:
                return QSortFilterProxyModel.data( self, index, Qt.EditRole )
            elif role == Qt.DisplayRole:
                self.dataChanged.emit( index, index )
                return moneyfmt( value, 4, '' )
        else:
            return QSortFilterProxyModel.data( self, index, role )


    @property
    def total( self ):
        """
        El subtotal del documento, esto es el total antes de aplicarse el IVA
        """
        fin = self.rowCount()

        tmpsubtotal = sum( [Decimal( self.index( i, DEBE ).data( Qt.EditRole ).toString() ) for i in range( 0, fin )] )
        return tmpsubtotal if tmpsubtotal != 0 else Decimal( 0 )
