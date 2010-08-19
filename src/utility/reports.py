# -*- coding: utf-8 -*-
import logging

from PyQt4.QtGui import  QPrinter, QPrintPreviewDialog,  QLineEdit, QMessageBox, QProgressBar, QPrintPreviewWidget
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import  QUrl, QSettings


        
        
class frmReportes( QPrintPreviewDialog ):
    """
    Este es un formulario generico que muestra los reportes web generados para las 
    """
    def __init__( self, web, user, printer = QPrinter() ,parent = None, ):
        """
        @param user: El objeto usuario asociado con esta sesión
        @param web: La dirección web a la que apunta el reporte
        @param printer: El objeto QPrinter en el que se imprime, esto es usado por si se desea alguna configuración especifica del reporte
        """
        super(frmReportes, self).__init__(printer, parent )
        settings = QSettings()
        base = settings.value( "Reports/base" ).toString()
        self.report =  base + web + "&uname=" + user.user + "&hash=" + user.hash 
        self.webview = QWebView()

        

        
        self.txtSearch = QLineEdit()

        self.loaded = False

        
        self.webview.load( QUrl(self.report) )
        self.progressbar = QProgressBar(self)

        
        
        
        self.paintRequested[QPrinter].connect(self.reprint)
        self.webview.loadFinished[bool].connect(self.on_webview_loadFinished)
        self.webview.loadProgress[int].connect(self.on_webview_loadProgress)
        
        
    
    def reprint(self, printer):
        self.webview.print_(printer)
    
    def on_webview_loadProgress(self, progress):
        self.progressbar.setValue(progress)
    
    def showEvent(self, event):
        if not self.loaded:
            self.progressbar.show()
            
    def on_webview_loadFinished(self, status):
        if self.progressbar.isVisible():
            self.progressbar.hide()
        if not status:
            QMessageBox.critical(self, "Llantera Esquipulas", "El reporte no se pudo cargar")
            logging.error("No se pudo cargar el reporte: %s" % self.report)
            self.accept()
        
        self.loaded = True
        
        w = self.findChild(QPrintPreviewWidget)
        w.updatePreview()
        
        
