# -*- coding: utf-8 -*-
u'''
El modulo de entrada a la aplicación
@author: armonge

G{importgraph}
'''
if __name__ == '__main__':
    import sip
    import sys
    import os
    sip.setapi( 'QString', 2 )


    from PyQt4 import QtGui, QtCore 
    from utility.database import Database
    from utility.user import dlgUserLogin, User
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

    """)
    if "--inventario" in sys.argv:
        app.setApplicationName( "Inventario" )
        from inventario.mainwindow import MainWindow
        module = "inventario"
    elif "--caja" in sys.argv:
        app.setApplicationName( "Caja" )
        from caja.mainwindow import MainWindow
        module = "caja"
    elif "--contabilidad" in sys.argv:
        app.setApplicationName( "Contabilidad" )
        from contabilidad.mainwindow import MainWindow
        module = "contabilidad"
    else:
        raise Exception( "No se selecciono un modulo" )


    db = Database.getDatabase( "--dbconfig" in sys.argv )

    if "--reportconfig" in sys.argv:
        text, result = QtGui.QInputDialog.getText( None, u"Configuración del servidor de reportes", "Url base de los reportes", QtGui.QLineEdit.Normal )
        if result:
            settings = QtCore.QSettings()
            settings.setValue( "Reports/Base", text )


    if db:
        dlguser = dlgUserLogin()


        if dlguser.exec_() == QtGui.QDialog.Accepted:
            user = User( dlguser.txtUser.text(), dlguser.txtPassword.text() )

            if user.valid:
                if user.hasRole( module ):
                    mainwindow = MainWindow( user )
                    mainwindow.showMaximized()
                    sys.exit( app.exec_() )
                else:
                    QtGui.QMessageBox.critical( None,
                    "Llantera Esquipulas",
                    u"Usted no tiene permiso para acceder a este modulo",
                    QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
            else:
                QtGui.QMessageBox.critical( None,
                    "Llantera Esquipulas",
                    user.error,
                    QtGui.QMessageBox.StandardButtons( QtGui.QMessageBox.Ok ) )
    else:
        QtGui.QMessageBox.critical( None,
            "Llantera Esquipulas",
            u"No puede continuar sin una configuración de base de datos",
            QtGui.QMessageBox.StandardButtons( \
                QtGui.QMessageBox.Ok ) )
    sys.exit()
