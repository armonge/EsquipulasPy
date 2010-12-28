#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
'''
Created on 11/07/2010

@author: Andrés Reyes Monge
'''
from PyQt4.QtCore import QTimer, Qt, pyqtSlot, QDateTime, QModelIndex
from PyQt4.QtGui import QSortFilterProxyModel, QVBoxLayout, QDialogButtonBox, \
    QFormLayout, QLineEdit, QDialog, QTableView, QAbstractItemView, QMessageBox, \
    qApp
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from decimal import Decimal
from document.kardex import KardexModel, LineaKardex, KardexDelegate
from ui.Ui_kardex import Ui_frmKardex
from utility import constantes
from utility.base import Base
import logging
from utility.decorators import if_edit_model




#DETAILS
IDARTICULO, DESCRIPCION, UNIDADES, AJUSTE, IDDOCUMENTOT = range( 5 )
#NAVIGATION
IDDOCUMENTO, NDOCIMPRESO, NKARDEX, NOMBREBODEGA, FECHA, OBSERVACIONK , \
OBSERVACION, BODEGA = range( 8 )
class FrmKardex( Ui_frmKardex, Base ):
    '''
    Esta clase implementa la funcionalidad para los movimientos de entrada y 
    salida de kardex, en ella el encargado de bodega da cuenta de cuando entra
    o sale algo de bodega
    '''
    def __init__( self, tiposdoc, parent = None, edit = True ):
        '''
        Constructor
        '''
        super( FrmKardex, self ).__init__( parent )
        self.tiposdoc = ",".join( [str( item ) for item in tiposdoc] )

        self.edit = edit



        self.navigationmodel = QSqlQueryModel()

        self.detailsModel = QSqlQueryModel()


        self.navproxymodel = QSortFilterProxyModel()
        self.navproxymodel.setSourceModel( self.navigationmodel )

        self.detailsproxymodel = QSortFilterProxyModel()
        self.detailsproxymodel.setSourceModel( self.detailsModel )


        self.tabledetails.setModel( self.detailsproxymodel )
        self.tablenavigation.setModel( self.navproxymodel )

        self.editmodel = None

        QTimer.singleShot( 0, self.loadModels )


    def updateModels( self ):
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"Existen problemas de conexión "\
                                       + "con la base de datos" )
            query = u"""
            SELECT
                d.iddocumento,
                CONCAT_WS(' ',tdc.descripcion, d.ndocimpreso) as 'Documento Referencia',
                kx.ndocimpreso as 'Numero Kardex',
                b.nombrebodega as 'Bodega',
                d.fechacreacion as 'Fecha',
                kx.observacion as 'Observacion Kardex',
                d.observacion as 'Observacion Doc',
                d.idbodega
            FROM documentos d
            JOIN tiposdoc tdc ON tdc.idtipodoc = d.idtipodoc
            JOIN bodegas b ON b.idbodega = d.idbodega
            JOIN docpadrehijos dpd ON dpd.idpadre = d.iddocumento
            JOIN documentos kx ON kx.iddocumento = dpd.idhijo AND kx.idtipodoc = %d
            WHERE d.idtipodoc IN (%s)
            GROUP BY d.iddocumento
            """ % ( constantes.IDKARDEX, self.tiposdoc )
            self.navigationmodel.setQuery( query )

            query = u"""
           SELECT 
                axd.idarticulo, 
                ad.descripcion as 'Articulo', 
                axd.unidades as 'Unidades',
                IF(akx.unidades > 0,    CONCAT('+',akx.unidades),     IFNULL(akx.unidades,0)) as 'Ajuste', 
                axd.iddocumento
            FROM articulosxdocumento axd
            JOIN vw_articulosdescritos ad ON ad.idarticulo = axd.idarticulo
            JOIN documentos d ON axd.iddocumento = d.iddocumento AND d.idtipodoc IN ( %s)
            JOIN docpadrehijos dph ON dph.idpadre = d.iddocumento
            JOIN documentos kardex ON kardex.iddocumento = dph.idhijo AND kardex.idtipodoc = %d
            LEFT JOIN articulosxdocumento akx ON akx.iddocumento = kardex.iddocumento
            GROUP BY ad.idarticulo, kardex.iddocumento
            """ % ( self.tiposdoc , constantes.IDKARDEX )
            self.detailsModel.setQuery( query )

            self.mapper.setModel( self.navproxymodel )
            self.mapper.addMapping( self.txtParentPrintedDocumentNumber,
                                    NDOCIMPRESO )
            self.mapper.addMapping( self.txtPrintedDocumentNumber, NKARDEX )
            self.mapper.addMapping( self.dtPicker, FECHA )
            self.mapper.addMapping( self.txtWarehouse, NOMBREBODEGA )
            self.mapper.addMapping( self.txtKardexObservation,
                                    OBSERVACIONK, "plainText" )
            self.mapper.addMapping( self.txtDocObservation,
                                     OBSERVACION, "plainText" )


#            self.tabledetails.horizontalHeader().setStretchLastSection( True )
            self.tabledetails.setColumnHidden(0,True)
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                  unicode( inst ) )
            logging.error( inst )
        except Exception as inst:
            logging.critical( inst )

    def updateDetailFilter( self, index ):
        self.detailsproxymodel.setFilterKeyColumn( IDDOCUMENTOT )
        self.detailsproxymodel.setFilterRegExp( "^" +
                                             self.navigationmodel.record( index
                                                           ).value( IDDOCUMENTO
                                                        ).toString() + "$" )
        self.tablenavigation.selectRow( self.mapper.currentIndex() )


    def cancel( self ):
        self.editmodel = None
        self.tabledetails.setModel( self.detailsproxymodel )
        self.status = True

    @pyqtSlot()
    @if_edit_model
    def on_txtKardexObservation_textChanged( self ):
        self.editmodel.observations = self.txtKardexObservation.toPlainText()

    def setControls( self, status ):
        self.tabnavigation.setEnabled( status )
        self.actionPrint.setVisible( status )
        self.actionGoFirst.setVisible( status )
        self.actionGoPrevious.setVisible( status )
        self.actionGoNext.setVisible( status )
        self.actionGoLast.setVisible( status )

        self.actionNew.setVisible( status )
        self.actionPreview.setVisible( status )

        self.dtPicker.setReadOnly( status )

        self.actionCancel.setVisible( not status )
        self.actionSave.setVisible( not status )

        self.tablenavigation.setColumnHidden( IDDOCUMENTO, True )
        self.tablenavigation.setColumnHidden( OBSERVACION, True )
        self.tablenavigation.setColumnHidden( OBSERVACIONK, True )
        self.tablenavigation.setColumnHidden( BODEGA, True )

        self.tabledetails.setColumnHidden( AJUSTE, True )

        self.tabledetails.setColumnHidden( IDDOCUMENTOT, True )
        if status:
            self.tabledetails.setEditTriggers( 
                                          QAbstractItemView.NoEditTriggers )
        else:
            self.tabledetails.setEditTriggers( 
                                          QAbstractItemView.AllEditTriggers )
        self.tabledetails.resizeColumnsToContents()
#            self.tabledetails.horizontalHeader().setStretchLastSection( True )

        self.txtKardexObservation.setReadOnly( status )

#        self.tabledetails.horizontalHeader().setStretchLastSection( True )



    def newDocument( self ):
        """
        Slot documentation goes here.
        """
        query = QSqlQuery()
        try:
            if not self.database.isOpen():
                if not self.database.open():
                    raise UserWarning( u"No se pudo establecer una conexión"\
                                       + " con la base de datos" )

            dlgdoc = dlgSelectDoc( self.tiposdoc )
            if dlgdoc.exec_() == QDialog.Accepted:
                self.editmodel = KardexModel()
                row = dlgdoc.tblBills.selectionModel().currentIndex().row()
                self.editmodel.parentId = dlgdoc.filtermodel.index( row, 0
                                                            ).data().toInt()[0]
                self.editmodel.uid = self.user.uid
                self.editmodel.parentPrinted = dlgdoc.filtermodel.index( row, 1
                                                             ).data().toString()
                self.editmodel.warehouseId = dlgdoc.filtermodel.index( row, 4
                                                           ).data().toInt()[0]
                self.editmodel.warehouseName = dlgdoc.filtermodel.index( row, 2
                                                          ).data().toString()

                self.txtDocObservation.setPlainText( 
                                        dlgdoc.filtermodel.index( row, 5 )
                                        .data().toString() )
                self.txtParentPrintedDocumentNumber.setText( 
                                                self.editmodel.parentPrinted )
                self.txtWarehouse.setText( self.editmodel.warehouseName )

                if not query.prepare( """
                SELECT
                    axd.idarticulo,
                    vw.descripcion,
                    axd.unidades,
                    cxa.valor
                FROM articulosxdocumento axd
                JOIN costosarticulo cxa ON cxa.idarticulo = axd.idarticulo AND cxa.activo = 1
                JOIN vw_articulosdescritos vw ON vw.idarticulo = axd.idarticulo
                WHERE axd.iddocumento = %d
                """ % self.editmodel.parentId ):
                    raise Exception( "No se pudo preparar la consulta para "\
                                     + "obtener las lineas del documento" )

                if not query.exec_():
                    raise Exception( "No se pudo ejecutar la consulta para"\
                                     + " obtener las lineas del documento" )

                if not query.size() > 0:
                    raise Exception( "La consulta para las lineas del "\
                                     + "documento no devolvio nada" )
                while query.next():
                    linea = LineaKardex()
                    linea.itemId = query.value( 0 ).toInt()[0]
                    linea.itemDescription = query.value( 1 ).toString()
                    linea.numdoc = query.value( 2 ).toInt()[0]
                    linea.itemCost = Decimal( query.value( 3 ).toString() )
                    row = self.editmodel.rowCount()
                    self.editmodel.insertRows( row )
                    self.editmodel.lines[row] = linea

#               Cargar el numero de kardex 
                query = QSqlQuery( """
               CALL spConsecutivo(%d,NULL);
                """ % constantes.IDKARDEX )

                if not query.exec_():
                    raise UserWarning( u"No se pudo calcular el numero de"\
                                       + " la devolución" )
                query.first()
                self.editmodel.printedDocumentNumber = query.value( 0 ).toString()

                self.txtPrintedDocumentNumber.setText( 
                                      self.editmodel.printedDocumentNumber )


                self.status = False
                self.tabnavigation.setEnabled( False )
                self.tabWidget.setCurrentIndex( 0 )
                self.tabledetails.setModel( self.editmodel )

                delegate = KardexDelegate()
                self.tabledetails.setItemDelegate( delegate )


                self.dtPicker.setDateTime( QDateTime.currentDateTime() )
                self.editmodel.dataChanged[QModelIndex, QModelIndex].connect( self.updateLabels )
                self.tabledetails.resizeColumnsToContents()
        except UserWarning as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                   unicode( inst ) )
            logging.warning( inst )
            self.cancel()
        except Exception as inst:
            QMessageBox.critical( self, qApp.organizationName(),
                                   "No se pudo iniciar el documento kardex" )
            logging.critical( inst )
            self.cancel()
        finally:
            if self.database.isOpen():
                self.database.close()



    def updateLabels( self ):
        pass

class dlgSelectDoc( QDialog ):
    def __init__( self, tiposdoc, parent = None ):
        super( dlgSelectDoc, self ).__init__( parent )
        self.setupUi()

        self.model = QSqlQueryModel()
        query = u"""
        SELECT 
            d.iddocumento, 
            CONCAT_WS(' ', tdc.descripcion, d.ndocimpreso) as 'Documento',
            b.nombrebodega as 'Bodega',        
            d.fechacreacion as 'Fecha',
            b.idbodega,
            d.observacion
        FROM documentos d
        JOIN tiposdoc tdc ON tdc.idtipodoc = d.idtipodoc
        JOIN bodegas b ON b.idbodega = d.idbodega
        LEFT JOIN docpadrehijos dpd ON dpd.idpadre = d.iddocumento
        LEFT JOIN documentos h ON h.iddocumento = dpd.idhijo AND h.idtipodoc = %d
        WHERE d.idtipodoc IN (%s) AND d.idestado = %d
        GROUP BY d.iddocumento
        HAVING SUM(h.idtipodoc) IS NULL
        """ % ( constantes.IDKARDEX , tiposdoc, constantes.CONFIRMADO )
        self.model.setQuery( query )




        self.setWindowTitle( u"Seleccione el documento con los artículos" )
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel( self.model )
        self.filtermodel.setFilterCaseSensitivity( Qt.CaseInsensitive )
        self.filtermodel.setFilterKeyColumn( -1 )

        self.tblBills.setModel( self.filtermodel )

#        self.tblBills.horizontalHeader().setStretchLastSection( True )

        iddoc, _ndocimpreso, _bodega, _fecha, idbodega, observacion = range( 6 )
        self.tblBills.setColumnHidden( iddoc, True )
        self.tblBills.setColumnHidden( idbodega, True )
        self.tblBills.setColumnHidden( observacion, True )
        self.tblBills.resizeColumnsToContents()

        self.buttonbox.accepted.connect( self.accept )
        self.buttonbox.rejected.connect( self.reject )
        self.txt_search.textChanged[unicode].connect( self.update_filter )

    def setupUi( self ):
        self.tblBills = QTableView()
        self.tblBills.setSelectionMode( QAbstractItemView.SingleSelection )
        self.tblBills.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.tblBills.selectRow( 0 )

        self.buttonbox = QDialogButtonBox( QDialogButtonBox.Ok |
                                           QDialogButtonBox.Cancel )

        self.txt_search = QLineEdit()
        formlayout = QFormLayout()

        formlayout.addRow( "&Buscar", self.txt_search )

        layout = QVBoxLayout()

        layout.addWidget( self.tblBills )
        layout.addLayout( formlayout )
        layout.addWidget( self.buttonbox )
        self.setLayout( layout )

        self.setMinimumWidth( 450 )

    def update_filter( self, text ):
        self.filtermodel.setFilterWildcard( text )

