# -*- coding: utf-8 -*-
"""
Modulo en el que se maneja la logica de usuarios
"""
import hashlib
import functools
import logging
import sys

from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtCore import  SIGNAL, SLOT, Qt, QTimer
from PyQt4.QtGui import QDialog,  qApp, QDesktopWidget, QPixmap, QDialogButtonBox,\
QFormLayout, QVBoxLayout, QLineEdit, qApp, QMessageBox, QLabel
from utility.database import Database
from ui import res_rc
from ui.Ui_user import Ui_dlgUserLogin

UID, FULLNAME, ROLE = range( 3 )

class dlgUserLogin( QDialog, Ui_dlgUserLogin ):
    """
    Dialogo utilizado para pedir valores de usuario y contraseña
    """
    def __init__( self, parent = None, max = 3 ):
        super( dlgUserLogin, self ).__init__( parent )

        self.setupUi(self)
        self.user = None
        self.max = max
        self.attempts = 0

        self.txtApplication.setText(self.txtApplication.text() +": "+ qApp.applicationName() )
        self.txtUser.setText('root')

        self.lblError.setVisible(False)

        #No mostrar el marco de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)

        #Centrar el dialogo en la pantalla
        dw = QDesktopWidget()
        geometry = dw.screenGeometry()
        self.setGeometry( (geometry.width() -519) / 2, (geometry.height() -311)  / 2  , 519, 311)


        #mostrar redondeado el dialogo
        pixmap = QPixmap(":/images/res/passwd-bg.png");
        self.setMask(pixmap.mask());



    def accept(self):
        self.user = User( self.txtUser.text(), self.txtPassword.text(),self.txtBd.text() )
        if self.user.valid or self.attempts == self.max -1:
            super(dlgUserLogin, self).accept()
        else:
            self.txtPassword.setText("")
            self.lblError.setVisible(True)
            self.attempts+=1
            QTimer.singleShot(3000, functools.partial(self.lblError.setVisible, False))

class dlgPasswordChange(QDialog):
    def __init__(self, user):
        super(dlgPasswordChange, self).__init__()
        self.setupUi(self)
        
        
        self.user = user

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
    def accept(self):
        oldp = self.txtOldPassword.text()
        newp = self.txtNewPassword.text()
        repeatp = self.txtRepeatPassword.text()
        
        try:
            if self.user.changePassword(oldp, newp, repeatp):
                logging.info(u"La contraseña del usuario %s ha sido cambiada" % self.user.user)
                super(dlgPasswordChange, self).accept()
            else:
                logging.warning(u"Intento fallido de cambiar la contraseña del usuario %s" % self.user.user)
        except UserWarning as inst:
            self.lblError.setText(unicode(inst) )
            self.lblError.setVisible(True)
            QTimer.singleShot(3000, functools.partial(self.lblError.setVisible, False))
            
            
    def setupUi(self, parent):
        
        
        self.setWindowTitle(qApp.organizationName() + ": " +qApp.applicationName())
        
        self.txtOldPassword = QLineEdit()
        self.txtOldPassword.setEchoMode(QLineEdit.Password)
        
        self.txtNewPassword = QLineEdit()
        self.txtNewPassword.setEchoMode(QLineEdit.Password)
        
        self.txtRepeatPassword = QLineEdit()
        self.txtRepeatPassword.setEchoMode(QLineEdit.Password)
        
        self.form = QFormLayout()
        self.form.addRow(u"Contraseña anterior", self.txtOldPassword)
        self.form.addRow(u"Nueva contraseña", self.txtNewPassword)
        self.form.addRow(u"Repita la nueva contraseña", self.txtRepeatPassword)
        
        self.layout = QVBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        self.lblError = QLabel()
        self.lblError.setAlignment(Qt.AlignHCenter)
        self.lblError.setProperty("error", True)
        self.lblError.setVisible(False)
        
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.lblError)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)
        
        
        
        
class User:
#    TODO:Crear o utilizar algún algoritmo para determinar que tan buena es una contraseña
    secret = '7/46u23opA)P231popas;asdf3289AOP23'
    u"""
    @cvar: El hash usado en esta aplicación para los usuarios
    @type: string  
    """
    def __init__( self, user, password,db ):
        self.__user = user
        """
        @ivar: el nombre de usuario
        @type:string
        """
        self.__password = password
        u"""
        @ivar: La contraseña
        @type:string
        """
        self.__database = db
        u"""
        @ivar: La contraseña
        @type:string
        """
        
        self.__roles = []
        """
        @ivar: La lista de permisos de un usuario
        @type: string[]
        """
        self.__valid = False
        """
        @ivar: si el usuario es valido o no
        @type: bool 
        """
        self.__fullname = ""
        """
        @ivar:El nombre completo de este usuario
        @type: string 
        """
        self.__uid = 0
        """
        @ivar: El id de este usuario
        @type: int
        """
        self.error = ""
        """
        @ivar:Posibles errores
        @type:string
        """
        self.db = Database.getDatabase(self.__database)
        print self.__database
        try:
            if not self.db.open():
                raise UserWarning( u'Existen problemas de conectividad con la base de datos' )
            else:
                query = QSqlQuery()
                if not query.prepare( """
                SELECT 
                    u.idusuario AS uid, 
                    p.nombre, 
                    r.nombre as rol 
                FROM usuarios u
                JOIN personas p ON p.idpersona = u.idusuario
                JOIN usuarios_has_roles ur ON u.idusuario = ur.idusuario
                JOIN roles r ON r.idrol = ur.idrol
                WHERE u.estado = 1
                AND u.username LIKE BINARY :user
                AND u.password LIKE BINARY SHA1(:password)
                """ ):
                    raise UserWarning( "No se pudo preparar la consulta para validar el usuario" )
                query.bindValue( ":user", self.user )
                query.bindValue( ":password", self.password + self.secret )

                if not query.exec_():
                    raise Exception( "La consulta no se pudo ejecutar" )

                if query.size() == 0:
                    raise UserWarning( "No se ha podido autenticar al usuario %s" %self.user )
                else:
                    logging.info(u"El usuario %s se ha autenticado" % self.user)
                    while query.next():
                        self.__valid = True
                        self.__uid = query.value( UID ).toInt()[0]
                        self.__fullname = query.value( FULLNAME ).toString()
                        self.__roles.append( query.value( ROLE ).toString() )
        except UserWarning as inst:
            self.error = unicode( inst )
            logging.error(unicode(inst))
        except Exception as inst:
            logging.critical(unicode(inst))
        finally:
            if self.db.isOpen():
                self.db.close()
    @property
    def user( self ):
        """
        El nombre de usuario que se utilizo para validar el usuario
        @rtype: string
        """
        return self.__user

    @property
    def password( self ):
        """
        La contraseña que se utilizo para validar el usuario
        @rtype: string
        """
        return self.__password

    @property
    def valid( self ):
        """
        Si el usuario es valido o no
        @rtype: bool
        """
        return self.__valid

    @property
    def hash( self ):
        return  hashlib.sha1( hashlib.sha1( self.password + self.secret ).hexdigest() + self.secret ).hexdigest() if self.valid else ""

    @property
    def roles( self ):
        """
        La lista de roles del Usuario
        @rtype: list
        """
        return self.__roles if self.valid else []

    @property
    def fullname( self ):
        """
        El nombre completo del usuario según lo definido en la base de datos
        @rtype: string
        """
        return self.__fullname
    
    @property
    def uid( self ):
        """
        El id del usuario en la base de datos
        @rtype: int
        """
        return self.__uid
    
    def hasRole( self, role ):
        """
        Esta función comprueba si  un usuario tiene determinado permiso
        @param role: este parametro es el rol que se quiere comprobar
        @rtype: bool 
        """
        if self.valid:
            if 'root' in self.__roles:
                return True
            else:
                return role in self.__roles
        return False

    def __createPassword(self, password):
        u"""
        Esta función crea la contraseña nueva a ingresar al servidor de bases de datos
        @param password: La contraseña a partir de la cual se crea la nueva contraseña
        @type password: string
        @return: La contraseña lista para usarse en la consulta
        @rtype: string
        """
        return hashlib.sha1(password + self.secret ).hexdigest()
        
    def changePassword(self, old, new, repeat):
        u"""
        Esta función cambia la contraseña del usuario
        @param old: La contraseña anterior del usuario
        @param new: La nueva contraseña del usuario
        @param repeat: La nueva contraseña del usuario 
        
        @type old:string
        @type new:string
        @type repeat: string
        
        @return: Si se pudo o no cambiar la contraseña
        @rtype:bool
        """
        if not old == self.password:
            raise UserWarning(u"La contraseña anterior que escribio no es correcta")
        elif not new == repeat:
            raise UserWarning(u"Las contraseñas no coinciden")
        
        if not self.db.isOpen():
            if not self.db.open():
                raise UserWarning(u"No se pudo abrir la conexión con la base de datos")
            
        query = QSqlQuery()
        if not query.prepare("""
        UPDATE usuarios SET password = :password WHERE idusuario = :id LIMIT 1
        """):
            raise Exception(u"No se pudo preparar la consulta para cambiar la contraseña")
        
        query.bindValue(":password" , self.__createPassword(new) )
        query.bindValue(":id" , self.uid )
        
        if not query.exec_():
            raise Exception("No se pudo cambiar la contraseña")
        
        self.__password = new
        
        return True
        
        
        
        
        
        
        