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
LOG_FILENAME = os.path.join( os.path.expanduser( '~' ), "esquipulas.log" )
logging.basicConfig( level = logging.DEBUG,
                format = '%(levelname)s -- %(asctime)s --En %(module)s funcion:%(funcName)s linea:%(lineno)d -- %(message)s',
                filename = LOG_FILENAME,
                )

from PyQt4 import QtGui, QtCore
import utility

app = QtGui.QApplication( sys.argv )
app.setOrganizationName( "Llantera Esquipulas" )
app.setOrganizationDomain( "grupoeltriunfo.com.ni" )

translator = QtCore.QTranslator()
locale = QtCore.QLocale()
if os.name == 'posix':
    translator.load( os.path.join( "/usr/share/qt4/translations" , "qt_es.qm" ) )
else:
    translator.load( os.path.join( os.path.dirname( os.path.abspath( sys.argv[0] ) ) , r"translations" , "qt_es.qm" ) )

app.installTranslator( translator )


app.setStyleSheet( """
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
""" )
if "--inventario" in sys.argv:
    app.setApplicationName( "Compras e Inventario" )
    from inventario.mainwindow import MainWindow
#    module = "inventario"
    module = utility.constantes.ACCESOINVENTARIO
elif "--caja" in sys.argv:
    app.setApplicationName( "Caja" )
    from caja.mainwindow import MainWindow
#    module = "caja"
    module = utility.constantes.ACCESOCAJA
elif "--contabilidad" in sys.argv:
    app.setApplicationName( "Contabilidad" )
    from contabilidad.mainwindow import MainWindow
#    module = "contabilidad"
    module = utility.constantes.ACCESOCONTABILIDAD
else:
    raise Exception( "No se selecciono un modulo" )




if "--reportconfig" in sys.argv:
    settings = QtCore.QSettings()
    text, result = QtGui.QInputDialog.getText( None, u"Configuración del servidor de reportes", "Url base de los reportes", QtGui.QLineEdit.Normal, settings.value( "Reports/Base", "" ).toString() )
    if result:
        settings.setValue( "Reports/Base", text )


#Database.getDatabase("","--dbconfig" in sys.argv)
dlguser = utility.user.dlgUserLogin()
#cont = 0
#valido = False
dlguser.txtPassword.setText( "" )
if dlguser.exec_() == QtGui.QDialog.Accepted:
    utility.user.LoggedUser = dlguser.user
    if utility.user.LoggedUser.valid:
        if  utility.user.LoggedUser.hasAnyRole( module ):


            mainwindow = MainWindow( module )
            mainwindow.showMaximized()
            sys.exit( app.exec_() )

        else:
            QtGui.QMessageBox.critical( None,
            QtGui.qApp.organizationName(),
            u"Usted no tiene permiso para acceder a este modulo",
            QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
    else:
        QtGui.QMessageBox.critical( None,
        QtGui.qApp.organizationName(),
        utility.user.LoggedUser.error,
        QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )

sys.exit()
