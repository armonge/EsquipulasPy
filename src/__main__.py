# -*- coding: utf-8 -*-
u'''
El modulo de entrada a la aplicación
@author: Andrés Reyes Monge

G{importgraph}
'''


import sip
import sys
import os
sip.setapi( 'QString', 2 )

import logging
LOG_FILENAME = "esquipulas.log"
logging.basicConfig(level=logging.DEBUG,
                format='%(levelname)s -- %(asctime)s --En %(module)s funcion:%(funcName)s linea:%(lineno)d -- %(message)s',
                filename=LOG_FILENAME,
                )

from PyQt4 import QtGui, QtCore
from utility import database
from utility import constantes
from utility import user
from ui import res_rc

app = QtGui.QApplication( sys.argv )
app.setOrganizationName( "Llantera Esquipulas" )
app.setOrganizationDomain( "grupoeltriunfo.com.ni" )

translator = QtCore.QTranslator()
locale = QtCore.QLocale()
LOCALENAME = str(locale.system().name())
translator.load("qt_%s" % LOCALENAME, os.path.dirname(os.path.abspath( sys.argv[0] )) + r"/translations/")

app.installTranslator(translator)


app.setStyleSheet("""
QLabel{
    background:transparent;
}

dlgUserLogin .QFrame{
    background-image: url(:/images/res/passwd-bg.png);
    background-repeat:no-repeat;
    margin:0;
    padding:0;
}
QMainWindow > .QDockWidget, QMainWindow > .QDockWidget .QWidget {
    background-color:#5677FF;
}
QDockWidget::title {
    text-align: left;
    background: lightgray;
    margin:0;
    padding: 5px;
}
QToolBox::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border-radius: 5px;

}
QToolBox .QWidget{
    background-color:transparent;
}
QLabel[error=true]{
    color:red;
}
QMainWindow{
    background-image: url(:/images/res/logo-big.png);
    background-position:right bottom;
    background-repeat:no-repeat;
}
QMdiArea QMainWindow{
    background-image: url()
}
""")
if "--inventario" in sys.argv:
    app.setApplicationName( "Compras e Inventario" )
    from inventario.mainwindow import MainWindow
#    module = "inventario"
    module = constantes.ACCESOINVENTARIO
elif "--caja" in sys.argv:
    app.setApplicationName( "Caja" )
    from caja.mainwindow import MainWindow
#    module = "caja"
    module = constantes.ACCESOCAJA
elif "--contabilidad" in sys.argv:
    app.setApplicationName( "Contabilidad" )
    from contabilidad.mainwindow import MainWindow
#    module = "contabilidad"
    module = constantes.ACCESOCONTABILIDAD
else:
    raise Exception( "No se selecciono un modulo" )




if "--reportconfig" in sys.argv:
    settings = QtCore.QSettings()
    text, result = QtGui.QInputDialog.getText( None, u"Configuración del servidor de reportes", "Url base de los reportes", QtGui.QLineEdit.Normal, settings.value( "Reports/Base", "" ).toString() )
    if result:
        settings.setValue( "Reports/Base", text )


#Database.getDatabase("","--dbconfig" in sys.argv)
dlguser = user.dlgUserLogin()
#cont = 0
#valido = False
dlguser.txtPassword.setText("")
if dlguser.exec_() == QtGui.QDialog.Accepted:
    user.LoggedUser = dlguser.user
    if user.LoggedUser.valid:
        if  user.LoggedUser.hasAnyRole(module):


            mainwindow = MainWindow( )
            mainwindow.showMaximized()
            sys.exit(app.exec_())

        else:
            QtGui.QMessageBox.critical( None,
            QtGui.qApp.organizationName(),
            u"Usted no tiene permiso para acceder a este modulo",
            QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
    else:
        QtGui.QMessageBox.critical( None,
        QtGui.qApp.organizationName(),
        user.LoggedUser.error,
        QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )

sys.exit()
