# -*- coding: utf-8 -*-
"""
Module implementing frmConciliacion.
"""
from PyQt4.QtCore import pyqtSlot, QModelIndex, Qt, QTimer, QDate, QVariant
from PyQt4.QtGui import QSortFilterProxyModel, QDataWidgetMapper, QDialog, \
    QTableView, QDialogButtonBox, QVBoxLayout, QAbstractItemView, QFormLayout, \
    QLineEdit, QDateTimeEdit, QMessageBox, qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from decimal import Decimal
from document.conciliacion import ConciliacionModel, LineaConciliacion
from ui.Ui_conciliacion import Ui_frmConciliacion
from utility.base import Base
from utility.constantes import IDND, IDCHEQUE, IDERROR
from utility.decorators import if_edit_model
from utility.moneyfmt import moneyfmt
import logging





from movimientosbancarios import FrmMovimientosBancarios


FECHA, CONCEPTO, DEBE, HABER, SALDO, CONCILIADO, DELBANCO, \
IDTIPODOC = range( 8 )
FECHA, BANCO, CUENTABANCO, MONEDA, CUENTA, SALDOBANCO, SALDOLIBRO, \
IDCUENTABANCO, IDDOC = range( 9 )
class FrmConciliacion( Ui_frmConciliacion, Base ):
    """
    Formulario para crear nuevas conciliaciones bancarias
    """
    def __init__( self , parent = None ):
        """
        Constructor
        """

        super( FrmConciliacion, self ).__init__( parent )


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
        self.crearModelosFiltrados()

        self.detailsmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )


#        Cargar los modelos en un hilo aparte
        QTimer.singleShot( 0, self.loadModels )


    def crearModelosFiltrados( self ):
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
        delbancoproxymodel.setFilterRegExp( "1" )
        delbancoproxymodel.setFilterKeyColumn( DELBANCO )

#CREAR PROXY MODEL PARA VERIFICAR SI FUE GENERADO  POR LA EMPRESA
        empresaproxymodel = QSortFilterProxyModel( self )
        empresaproxymodel.setSourceModel( self.proxymodel )
        empresaproxymodel.setDynamicSortFilter( True )
        empresaproxymodel.setFilterRole( Qt.EditRole )
        empresaproxymodel.setFilterRegExp( "0" )
        empresaproxymodel.setFilterKeyColumn( DELBANCO )

        filtroMenos = "^" + str( IDND ) + "$|^" + str( IDCHEQUE ) + "$|^" + str( IDERROR ) + "$"
        filtroMas = "[" + filtroMenos + "]"

#CREAR MODELO PARA DEPOSITOS
        depositosproxymodel = DetalleTableModel( self )
        depositosproxymodel.setSourceModel( empresaproxymodel )
        depositosproxymodel.setFilterRegExp( filtroMas )
        depositosproxymodel.setFilterKeyColumn( IDTIPODOC )
        self.tablalibromas.setModel( depositosproxymodel )

#CREAR MODELO PARA CHEQUES
        chequesproxymodel = DetalleTableModel( self )
        chequesproxymodel.setSourceModel( empresaproxymodel )
        chequesproxymodel.setFilterRegExp( filtroMenos )
        chequesproxymodel.setFilterKeyColumn( IDTIPODOC )
        self.tablalibromenos.setModel( chequesproxymodel )


#CREAR MODELO PARA NOTAS DE CREDITO
        notascreditoproxymodel = DetalleTableModel( self )
        notascreditoproxymodel.setSourceModel( delbancoproxymodel )
        notascreditoproxymodel.setFilterRegExp( filtroMas )
        notascreditoproxymodel.setFilterKeyColumn( IDTIPODOC )
        self.tablabancomas.setModel( notascreditoproxymodel )

#CREAR MODELO PARA NOTAS DE DEBITO
        notasdebitoproxymodel = DetalleTableModel( self )
        notasdebitoproxymodel.setSourceModel( delbancoproxymodel )
        notasdebitoproxymodel.setFilterRegExp( filtroMenos )
        notasdebitoproxymodel.setFilterKeyColumn( IDTIPODOC )
        self.tablabancomenos.setModel( notasdebitoproxymodel )

    def updateModels( self ):
        """
        Recargar todos los modelos
        """
        try:
            if not QSqlDatabase.database().isOpen():
                if not QSqlDatabase.database().open():
                    raise Exception( "No se pudo abrir la base" )

#        El modelo principal
            self.navmodel.setQuery( """
            SELECT
                c.fecha,
                b.descripcion as banco,
                cb.ctabancaria,
                m.simbolo,
                cc.codigo,
                c.saldolibro,
                c.saldobanco,
                cb.idcuentacontable,
                c.iddocumento
                FROM conciliaciones c
                JOIN cuentasbancarias cb ON c.idcuentacontable = cb.idcuentacontable
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

            self.ocultarCols()

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
#            print self.mapper.currentIndex()
#            self.tablenavigation.selectRow( self.mapper.currentIndex() )
            self.cargarMovimientos()

#        
#    @pyqtSlot( "int" )
#    def on_tabWidget_currentChanged(self,index):
#        pass
##        if index == 0:
##            self.cargarMovimientos()
#            
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
            index = self.detailsmodel.index( self.detailsmodel.rowCount() - 1, CONCILIADO )
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
        self.txtdeposito.setText( moneyfmt( depositos, 4, "C$" ) )
        self.txtnotacredito.setText( moneyfmt( nc, 4, "C$" ) )
        self.txtnotadebito.setText( moneyfmt( nd, 4, "C$" ) )

        self.txttotallibro.setText( moneyfmt( saldobanco + depositos + cheques, 4, "C$" ) )
        self.txttotalbanco.setText( moneyfmt( saldolibro + nc + nd , 4, "C$" ) )
        dif = saldobanco + depositos + cheques - ( saldolibro + nc + nd )
        self.lbldiferencia.setText( moneyfmt( dif, 4, "C$" ) if dif != 0 else "CONCILIADO" )

    def updateLabels( self ):
        self.txttotallibro.setText( moneyfmt( self.editmodel.totalLibro, 4, "C$" ) )
        self.txtcheque.setText( moneyfmt( self.editmodel.cheques, 4, "C$" ) )
        self.txtdeposito.setText( moneyfmt( self.editmodel.depositos, 4, "C$" ) )
        self.txtnotacredito.setText( moneyfmt( self.editmodel.notascredito, 4, "C$" ) )
        self.txtnotadebito.setText( moneyfmt( self.editmodel.notasdebito, 4, "C$" ) )

        self.txttotalbanco.setText( moneyfmt( self.editmodel.totalBanco, 4, "C$" ) )
        dif = self.editmodel.diferencia
        self.lbldiferencia.setText( ( "Diferencia " + moneyfmt( dif, 4, "C$" ) ) if dif != 0 else "CONCILIADO" )




    @pyqtSlot( float )
    def on_spbsaldobanco_valueChanged ( self, value ):
        """
        Asignar el saldo inicial del banco al modelo
        """
        if not self.editmodel is None:
#            value = self.spbsaldobanco.value()           
            self.editmodel.saldoInicialBanco = Decimal( str( value ) )
            self.updateLabels()


    def setControls( self, status ):
        """
        En esta funcion cambio el estado enabled de todos los items en el formulario
        @param status: false = editando        true = navegando
        """
        self.actionPrint.setVisible( status )
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
            if not QSqlDatabase.database().open():
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
            self.editmodel = ConciliacionModel()
            self.editmodel.uid = self.user.uid
            self.txtbanco.setText( dlgCuenta.filtermodel.index( fila, 0 ).data().toString() )
            self.txtcuentabanco.setText( dlgCuenta.filtermodel.index( fila, 1 ).data().toString() )
            self.txtmoneda.setText( dlgCuenta.filtermodel.index( fila, 2 ).data().toString() )
            self.txtcuenta.setText( dlgCuenta.filtermodel.index( fila, 3 ).data().toString() )
            self.txtcuenta.setToolTip( dlgCuenta.filtermodel.index( fila, 5 ).data().toString() )

            self.editmodel.idCuentaContable = dlgCuenta.filtermodel.index( fila, 4 ).data().toInt()[0]

            fecha = dlgCuenta.dtPicker.date()
            self.lblfecha.setText( fecha.toString( "MMMM yyyy" ).upper() )
            self.editmodel.fechaConciliacion = QDate( fecha.year(), fecha.month(), fecha.daysInMonth() )


            if not query.exec_( "CALL spMovimientoCuenta( %d, %s )" % ( self.editmodel.idCuentaContable,
                self.editmodel.fechaConciliacion.toString( "yyyyMMdd" ) ) ):
                raise Exception( query.lastError().text() )

            row = 0
            while query.next():
                linea = LineaConciliacion( self.editmodel )
                linea.fecha = query.value( FECHA ).toString()
                linea.concepto = query.value( CONCEPTO ).toString()
                linea.monto = Decimal( query.value( DEBE ).toString() )
                linea.saldo = Decimal( query.value( 3 ).toString() )

                linea.delBanco = query.value( 5 ).toInt()[0]
                linea.conciliado = linea.delBanco

                linea.idTipoDoc = query.value( 6 ).toInt()[0]
                linea.concepto2 = query.value( 7 ).toString()
                linea.idDoc = query.value( 8 ).toInt()[0]

                self.editmodel.insertRows( row )
                self.editmodel.lines[row] = linea
                row = row + 1

            self.editmodel.saldoInicialLibro = self.editmodel.lines[row - 1].saldo
            self.txtsaldolibro.setText( moneyfmt( self.editmodel.lines[row - 1].saldo, 4, "C$" ) )
            self.updateLabels()

            self.proxymodel.setSourceModel( self.editmodel )

            self.setControls( False )
            self.tabnavigation.setEnabled( False )
            self.tabWidget.setCurrentIndex( 0 )
            self.tabledetails.setModel( self.editmodel )

            self.tabledetails.resizeColumnsToContents()

            self.ocultarCols()

            self.editmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )

        except UserWarning as inst:
            logging.error( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
        except Exception as inst:
            logging.critical( unicode( inst ) )
            QMessageBox.critical( self, qApp.organizationName(),
                                   u"Hubo un error al intentar iniciar una"
                                   + " nueva conciliación" )
        finally:
            if self.database.isOpen():
                self.database.close()

    def ocultarCols( self ):
        #OCULTAR COLUMNAS    
        self.ocultarColumnas( self.tablalibromas )
        self.ocultarColumnas( self.tablalibromenos )
        self.ocultarColumnas( self.tablabancomas )
        self.ocultarColumnas( self.tablabancomenos )

    def ocultarColumnas( self, tabla ):
        tabla.setColumnHidden( HABER, True )
        tabla.setColumnHidden( CONCILIADO, True )
        tabla.setColumnHidden( SALDO, True )
        tabla.setColumnHidden( IDTIPODOC, True )
        tabla.setColumnHidden( DELBANCO, True )
        self.tabledetails.setColumnHidden( IDTIPODOC, True )
#        self.tabledetails.setColumnHidden(DELBANCO,True)


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

    @property
    def valid( self ):
        modelo = self.editmodel
        if modelo.idCuentaContable == 0:
            QMessageBox.warning( self,
                     qApp.organizationName(),
                     "Por favor elija la cuenta bancaria" )
        elif modelo.diferencia != 0:
            QMessageBox.warning( self,
                     qApp.organizationName(),
                     u"Los saldos según Banco y según libro no están conciliados" )
        else:
            return True

        return False


    def cancel( self ):
        self.editmodel = None
        self.tablenavigation.setModel( self.navproxymodel )
        self.tabledetails.setModel( self.detailsmodel )
        self.proxymodel.setSourceModel( self.detailsmodel )
        self.ocultarCols()
        self.status = True

    @pyqtSlot( bool )
    @if_edit_model
    def on_btnNotasCD_clicked( self, _checked ):
#        notas = dlgMovimientosBancarios( self )
        notas.setWindowModality( Qt.WindowModal )
        if notas.exec_() == QDialog.Accepted:
            row = self.editmodel.rowCount()

            datosDoc = notas.editmodel.datos

            linea = LineaConciliacion( self.editmodel )
            linea.fecha = datosDoc.dateTime.toString( "dd/MM/yy" )
            linea.monto = datosDoc.total
            linea.idTipoDoc = datosDoc.idTipoDoc

            linea.concepto = notas.editmodel.codigoDoc + " " + linea.fecha
            linea.saldo = self.editmodel.lines[row - 1].saldo + linea.monto
            linea.conciliado = 1
            linea.delBanco = 1
            linea.concepto2 = notas.editmodel.descripcionDoc + " " + linea.fecha
            linea.idDoc = 0
            linea.datos = datosDoc
            self.editmodel.insertRows( row )
            self.editmodel.lines[row] = linea
            index = self.editmodel.index( row, CONCILIADO )
            self.editmodel.dataChanged.emit( index, index )

    @pyqtSlot( bool )
    @if_edit_model
    def on_btnremove_clicked( self, _checked ):
        filas = []
        for index in self.tabledetails.selectedIndexes():
            pos = index.row()
            if pos > 0 and ( not ( pos in filas ) ):
                if self.editmodel.lines[pos].idDoc == 0:
                    filas.append( pos )

        if len( filas ) > 0:
            filas.sort( None, None, True )
            for pos in filas:
                self.editmodel.removeRows( pos )

            self.updateLabels()



#                


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
