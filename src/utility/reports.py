# -*- coding: utf-8 -*-
from PyQt4.QtGui import QMainWindow, QPrinter, QPrintDialog, QDialog, QLineEdit
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtCore import pyqtSignature, QUrl, SIGNAL, QSettings

from Ui_reports import Ui_frmReportes

class frmReportes( QMainWindow, Ui_frmReportes ):
    """
    Este es un formulario generico que muestra los reportes web generados para las 
    """
    def __init__( self, web, user, parent = None ):
        """
        @param user: El objeto usuario asociado con esta sesión
        @param web: La dirección web a la que apunta el reporte
        """
        QMainWindow.__init__( self, parent )

        self.setupUi( self )

        settings = QSettings()
        base = settings.value( "Reports/base" ).toString()

        self.txtSearch = QLineEdit()
        action = self.toolBar.addWidget( self.txtSearch )
        action.setVisible( True )


        self.webView.load( QUrl( base + web + "&uname=" + user.user + "&hash=" + user.hash ) )
        self.connect( self.txtSearch, SIGNAL( "textEdited(QString)" ), self.search )

    @pyqtSignature( "" )
    def on_actionPrint_activated( self ):
        """
        Imprimir el reporte
        """
        printer = QPrinter( QPrinter.HighResolution )
        printer.setPaperSize(QPrinter.Letter)
        printer.setPageMargins(0,0,0,0, QPrinter.Inch)
        printdialog = QPrintDialog( printer, self )
        printdialog.setWindowTitle( "Imprimir" )
        if printdialog.exec_() != QDialog.Accepted:
            return
        
        printer.setDocName( "Reporte" )
        self.webView.print_( printer )

    def search( self, text ):
        """
        Buscar en el contenido del reporte
        @param text:  el texto a buscar
        """
        self.webView.findText( text, QWebPage.HighlightAllOccurrences )

    @pyqtSignature( "int" )
    def on_verticalSlider_valueChanged( self, value ):
        self.webView.setZoomFactor( value * 0.2 )


