# -*- coding: utf-8 -*-
import logging

from PyQt4.QtGui import  QPrinter, QPrintPreviewDialog,  QLineEdit, QMessageBox, QProgressBar, QPrintPreviewWidget, qApp
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import  QUrl, Qt

import  user


class ReportConfig(object):
    url = ""

class frmReportes( QPrintPreviewDialog ):
    """
    Este es un formulario generico que muestra los reportes web generados para las 
    """
    def __init__( self, web,  printer ,parent = None ):
        """
        @param web: La dirección web a la que apunta el reporte
        @param printer: El objeto QPrinter en el que se imprime, esto es usado por si se desea alguna configuración especifica del reporte
        """
        super(frmReportes, self).__init__(printer, parent )
        
        base = Reports.url
        
        if base == "":
            raise UserWarning(u"No existe una configuración para el servidor de reportes")
            
        
        self.report =  base + web + "&uname=" + user.LoggedUser.user + "&hash=" + user.LoggedUser.hash
        self.webview = QWebView()
        self.setWindowFlags(self.windowFlags()|Qt.WindowMaximizeButtonHint)

        

        
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
            QMessageBox.critical(self, qApp.organizationName(), "El reporte no se pudo cargar")
            logging.error("No se pudo cargar el reporte: %s" % self.report)
            self.accept()
        
        self.loaded = True
        
        w = self.findChild(QPrintPreviewWidget)
        w.updatePreview()
        
        
Reports = ReportConfig()