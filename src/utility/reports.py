# -*- coding: utf-8 -*-
from PyQt4.QtGui import  QPrinter, QPrintPreviewDialog,  QLineEdit, QMessageBox
from PyQt4.QtWebKit import QWebPage, QWebView
from PyQt4.QtCore import pyqtSlot, QUrl, QSettings, SIGNAL

from Ui_reports import Ui_frmReportes

class frmReportes( QPrintPreviewDialog ):
    """
    Este es un formulario generico que muestra los reportes web generados para las 
    """
    def __init__( self, web, user, parent = None, orientation = QPrinter.Portrait ):
        """
        @param user: El objeto usuario asociado con esta sesión
        @param web: La dirección web a la que apunta el reporte
        """
        super(frmReportes, self).__init__( parent )
        self.webview = QWebView()

        settings = QSettings()
        base = settings.value( "Reports/base" ).toString()

        self.orientation = orientation
        self.txtSearch = QLineEdit()


        self.webview.load( QUrl( base + web + "&uname=" + user.user + "&hash=" + user.hash ) )
        
        
        self.paintRequested[QPrinter].connect(self.webview.print_)
        self.webview.loadFinished[bool].connect(self.on_webview_loadFinished)

        
        
    def on_webview_loadFinished(self, status):
        if not status:
            QMessageBox.critical(self, "Llantera Esquipulas", "El reporte no se pudo cargar")
            return 
        self.emit(SIGNAL("paintRequested"), QPrinter())
    
    
