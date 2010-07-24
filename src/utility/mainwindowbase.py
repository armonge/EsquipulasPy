# -*- coding: UTF-8 -*-
'''
Created on 11/06/2010

@author: armonge
'''
from PyQt4.QtCore import SIGNAL, QSettings, pyqtSlot
from PyQt4.QtGui import QDialog, QMessageBox
from utility.user import dlgUserLogin, User

class MainWindowBase( object ):
    '''
    classdocs
    '''
    def __init__( self ):
        '''
        Constructor
        '''
        settings = QSettings()
        self.restoreGeometry( settings.value( "MainWindow/Geometry" ).toByteArray() )
        self.connect( self.mdiArea, SIGNAL( "subWindowActivated(QMdiSubWindow *)" ), self.showtoolbar )

    def showtoolbar( self, *args ):
        """
        mostrar la toolbar de la ventana que se acaba de mostrar
        """
        for window in self.mdiArea.subWindowList():
            window.widget().toolBar.setVisible( False )
        for window in args:
            if not window is None:
                window.widget().toolBar.setVisible( True )
        

    def setStatus( self, status ):
        self.__status = status
        self.setControls( self.__status )
    def getStatus( self ):
        return self.__status
    status = property( getStatus, setStatus )

    def setControls( self, status ):
        raise NotImplementedError()

    def closeEvent( self, event ):
        settings = QSettings()
        settings.setValue( "MainWindow/Geometry", self.saveGeometry() )

    @pyqtSlot(  )
    def on_actionLockSession_triggered( self ):
        self.status = False

    @pyqtSlot(  )
    def on_actionUnlockSession_triggered( self ):
        dlg = dlgUserLogin( self )
        if dlg.exec_() == QDialog.Accepted:
            tmpuser = User( dlg.txtUser.text(), dlg.txtPassword.text() )
            if tmpuser.valid:
                if tmpuser.uid == self.user.uid or tmpuser.hasRole( 'root' ):
                    self.status = True
                else:
                    QMessageBox.critical( self, \
                                         "Llantera Esquipulas", \
                                         u"Usted esta intentando desbloquear una sesión que no le pertenece", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )
            else:
                QMessageBox.critical( self, \
                                         "Llantera Esquipulas", \
                                         u"No ha sido posible autenticarle", \
                                         QMessageBox.Ok, \
                                         QMessageBox.Ok )



