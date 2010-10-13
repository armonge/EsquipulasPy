# -*- coding: utf-8 -*-
'''
Created on 11/06/2010

@author: Administrator
'''
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from ui.Ui_apertura import Ui_dlgApertura
from utility import constantes
class FrmCierreCaja ( QDialog, Ui_dlgApertura ):
    def __init__( self, user, user2, sesion, parent = None ):
        super( FrmCierreCaja, self ).__init__( parent )
        self.setupUi( self )
        self.user = user
        self.user2 = user2
        self.db = QSqlDatabase.database()
        self.query = QSqlQuery( """
        SELECT 
            d.fechacreacion,
            c.idcaja,
            c.descripcion 
        FROM documentos d
        LEFT JOIN docpadrehijos dp ON dp.idpadre=d.iddocumento
        LEFT JOIN documentos hijo ON dp.idhijo=hijo.iddocumento AND hijo.idtipodoc=%d
        JOIN cajas c on d.idcaja=c.idcaja
        WHERE d.idtipodoc=%d and d.idusuario= %d 
        AND hijo.iddocumento IS  NULL 
        ORDER BY d.iddocumento DESC
        LIMIT 1;""" % ( constantes.IDAPERTURA, constantes.IDAPERTURA, user.uid ) )

        if not self.query.exec_():
            raise Exception( "No se pudo preparar la Query" )
        self.query.first()
        self.dtFechaTime.setDate( self.query.value( 0 ).toDate() )
        self.cboCaja.addItem( self.query.value( 2 ).toString() )
        self.txtUsuario.setText( self.user.user )
        self.txtUsuario.setReadOnly( True )
        self.dtFechaTime.setReadOnly( True )
        self.dtFechaTime.dateTime().toString( "yyyyMMddhhmmss" )
        self.sesion = sesion
    @pyqtSlot()
    def on_buttonBox_accepted( self ):
        """
        Agrega una apertura de caja        
        """

        try:
            query = QSqlQuery()
            query = QSqlQuery( """
            SELECT
            MAX(CAST(ndocimpreso AS SIGNED))+1
            FROM documentos d
            WHERE idtipodoc=17
            ;
            """ )
            if not query.exec_():
                raise Exception( "No se puedo prepara el query del numero de cierre" )
            query.first()
            ndocimpreso = query.value( 0 ).toString()
            if ndocimpreso == "0" :
                ndocimpreso = "1"
            if not query.prepare( """
            INSERT INTO documentos(ndocimpreso,total,fechacreacion,
            idtipodoc,idusuario,idcaja,observacion)
            VALUES(:ndocimpreso,:total,:fecha,:tipodoc,
            :usuario,:caja,:observacion)""" ):
                raise Exception( query.lastError().text() )
            query.bindValue( ":ndocimpreso", ndocimpreso )
            query.bindValue( ":total", self.txtMonto.text() )
            query.bindValue( ":fecha", self.dtFechaTime.dateTime().toString( "yyyyMMddhhmmss" ) )
            query.bindValue( ":tipodoc", constantes.IDCIERRESESION )
            query.bindValue( ":usuario", self.user.uid )
            query.bindValue( ":caja", self.query.value( 1 ) )
            query.bindValue( ":observacion", self.user2 )

            if not query.exec_():
                raise Exception( " Insert de cierre " )

            idcierre = self.query.lastInsertId().toInt()[0]
            if not query.prepare( """
            INSERT INTO docpadrehijos(idpadre,idhijo,monto) 
            VALUES(:idpadre,:idhijo,:monto)""" ):
                raise Exception( query.lastError().text() )
            query.bindValue( ":idpadre", self.sesion )
            query.bindValue( ":idhijo", idcierre )
            query.bindValue( ":monto", self.txtMonto.text() )

            if not query.exec_():
                raise Exception( " Insert de docpadrehijos" )

            self.accept()
        except Exception as inst:
            print inst
            self.reject()

    def on_buttonBox_cancelled( self ):
        """
        Cancela la apertura de caja        
        """
        self.reject()
