# -*- coding: utf-8 -*-
u"""
Modulo en el que se maneja la logica de usuarios

@author: Andrés Reyes Monge
"""
import hashlib
import functools
import logging
import sys
import re

from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtCore import  Qt, QTimer, QSize
from PyQt4.QtGui import QDialog,  qApp, QDesktopWidget, QPixmap, QDialogButtonBox,\
QFormLayout, QVBoxLayout, QLineEdit,  QMessageBox, QLabel, QProgressBar, QHBoxLayout, \
QFrame, QGridLayout, QSpacerItem, QSizePolicy, QFont, qApp
import database
from ui import res_rc

UID, FULLNAME, ROLE = range( 3 )
LoggedUser = None
class dlgAbstractUserLogin(QDialog):
    """
    Clase base para todos los dialogos que requieren autenticar a un usuario
    """
    def __init__(self, parent = None, maxAttempts = 3):
        super(dlgAbstractUserLogin, self).__init__()
        self.setupUi()
        self.parent = parent
        self.user = None
        self.maxAttempts = maxAttempts
        self.attempts = 0

        #self.txtUser.setText('root')
        #self.txtBd.setText('Esquipulasdb')

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)


    def accept(self):
        self.user = User( self.txtUser.text(), self.txtPassword.text())
        if self.user.valid or self.attempts == self.maxAttempts -1:
            super(dlgAbstractUserLogin, self).accept()
        else:
            self.txtPassword.setText("")
            self.lblError.setText(u"Hay un error en su usuario o su contraseña")
            self.lblError.setVisible(True)
            self.attempts+=1
            QTimer.singleShot(3000, functools.partial(self.lblError.setVisible, False))

    def setupUi(self):
        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtUser = QLineEdit()

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.lblError = QLabel()
        self.lblError.setProperty("error", True)
        self.lblError.setText(u"El usuario o la contraseña son incorrectos")
        self.lblError.setVisible(False)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(u"&Usuario", self.txtUser)
        self.formLayout.addRow(u"&Contraseña", self.txtPassword)

        self.txtUser.setWhatsThis("Escriba aca su usuario")
        self.txtPassword.setWhatsThis(u"Escriba aca su contraseña, tenga en cuenta que el sistema hace diferencia entre minusculas y mayusculas")
        
        self.txtApplication = QLabel()

class dlgUserLogin( dlgAbstractUserLogin ):
    """
    Dialogo utilizado para pedir valores de usuario, contraseña y base de datos al inicio de sesión
    """
    def accept(self):
        database.getDatabase(self.txtBd.text(), "--dbconfig" in qApp.arguments() )
        super(dlgUserLogin, self).accept()
        
        
    def setupUi(self):
        super(dlgUserLogin, self).setupUi()

        #No mostrar el marco de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.resize(519, 311)
        self.setMinimumSize(QSize(519, 311))
        self.setMaximumSize(QSize(519, 311))

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setMargin(0)

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)

        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setMargin(0)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 6)

        

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtApplication.sizePolicy().hasHeightForWidth())
        self.txtApplication.setSizePolicy(sizePolicy)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.txtApplication.setFont(font)
        self.txtApplication.setAutoFillBackground(False)
        self.txtApplication.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.txtApplication, 1, 0, 1, 5)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 6)
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 6)
        spacerItem3 = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 0, 1, 1)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 5, 1, 1, 1)
        spacerItem5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 5, 2, 1, 1)


        self.label = QLabel()

        self.txtBd = QLineEdit()

        self.formLayout.addRow(u"Base de datos", self.txtBd)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.gridLayout.addLayout(self.formLayout, 5, 3, 1, 1)
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 5, 4, 1, 1)
        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 5, 5, 1, 1)
        self.lblError = QLabel(self.frame)
        self.lblError.setProperty("error", True)
        self.gridLayout.addWidget(self.lblError, 6, 3, 1, 2)
        spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 7, 0, 1, 6)
        self.buttonbox = QDialogButtonBox(self.frame)
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttonbox, 8, 0, 1, 5)
        spacerItem9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 9, 0, 1, 6)
        self.horizontalLayout.addWidget(self.frame)


        self.txtApplication.setText(qApp.organizationName() +": "+ qApp.applicationName() )
        self.lblError.setVisible(False)

        #Centrar el dialogo en la pantalla
        dw = QDesktopWidget()
        geometry = dw.screenGeometry()
        self.setGeometry( (geometry.width() -519) / 2, (geometry.height() -311)  / 2  , 519, 311)
        
        #mostrar redondeado el dialogo
        pixmap = QPixmap(":/images/res/passwd-bg.png");
        self.setMask(pixmap.mask());

class dlgSmallUserLogin(dlgAbstractUserLogin):
    """
    Dialogo para autenticar a un usuario, contiene lo minimo necesario
    """
    def setupUi(self):
        super(dlgSmallUserLogin, self).setupUi()
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.lblError)
        self.verticalLayout.addWidget(self.buttonbox)
        self.setLayout(self.verticalLayout)
    
class dlgPasswordChange(QDialog):
    """
    Dialogo utilizado para cambiar la contraseña
    """
    def __init__(self, user):
        super(dlgPasswordChange, self).__init__()
        self.setupUi(self)
        
        
        self.user = user


        self.txtNewPassword.textChanged[unicode].connect(self.update)
        self.txtRepeatPassword.textChanged[unicode].connect(self.update)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def update(self, passwd):
        """
        Actualizar el valor de la barra indicadora de la fuerza de la contraseña, tambien ocultar o mostrar el texto de error
        """
        self.bar.setValue(self.user.checkPassword(passwd))
        self.lblError.setText("" if self.txtNewPassword.text() == self.txtRepeatPassword.text() else u"Las contraseñas no coinciden" )
        self.lblError.setVisible(self.txtNewPassword.text() != self.txtRepeatPassword.text())
        
    def accept(self):
        
        
        oldp = self.txtOldPassword.text()
        newp = self.txtNewPassword.text()
        repeatp = self.txtRepeatPassword.text()
        
        try:
            if self.user.changePassword(oldp, newp, repeatp):
                logging.info(u"La contraseña del usuario %s ha sido cambiada" % self.user.user)
                super(dlgPasswordChange, self).accept()
        except UserWarning as inst:
            self.lblError.setText(unicode(inst) )
            self.lblError.setVisible(True)
            logging.warning(unicode(inst))
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

        self.bar = QProgressBar()
        self.bar.setMinimum(0)
        self.bar.setMaximum(5)
        
        self.layout = QVBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        self.lblError = QLabel()
        self.lblError.setAlignment(Qt.AlignHCenter)
        self.lblError.setProperty("error", True)
        self.lblError.setVisible(False)
        
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.lblError)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)
        
        
        
        
class User:
    secret = '7/46u23opA)P231popas;asdf3289AOP23'
    u"""
    @cvar: El hash usado en esta aplicación para los usuarios
    @type: string  
    """
    def __init__( self, user, password ):
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
        self.db = QSqlDatabase.database()
        try:
            if not self.db.open():
                raise UserWarning( u'Existen problemas de conectividad con la base de datos' )
            else:
                query = QSqlQuery()
                if not query.prepare( """
                SELECT
                    u.idusuario AS uid,
                    p.nombre,
                    GROUP_CONCAT(r.nombre) as roles
                FROM usuarios u
                JOIN personas p ON p.idpersona = u.idusuario
                JOIN usuarios_has_roles ur ON u.idusuario = ur.idusuario
                JOIN roles r ON r.idrol = ur.idrol
                WHERE u.estado = 1
                AND u.username LIKE BINARY :user
                AND u.password LIKE BINARY SHA1(:password)
                GROUP BY u.idusuario
                LIMIT 1
                """ ):
                    raise UserWarning( "No se pudo preparar la consulta para validar el usuario" )
                query.bindValue( ":user", self.user )
                query.bindValue( ":password", self.password + self.secret )

                if not query.exec_():
                    raise Exception( "La consulta no se pudo ejecutar" )

                if query.size() != 1:
                    raise UserWarning( "No se ha podido autenticar al usuario %s" %self.user )
                else:
                    logging.info(u"El usuario %s se ha autenticado" % self.user)
                    query.first()
                    self.__valid = True
                    self.__uid = query.value( UID ).toInt()[0]
                    self.__fullname = query.value( FULLNAME ).toString()
                    self.__roles = query.value( ROLE ).toString().split(",")
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
        @type role: string
        @rtype: bool 
        """
        if self.valid:
            if 'root' in self.__roles:
                return True
            else:
                return role in self.__roles
        return False

    def hasAnyRole(self, rolelist):
        """
        Esta función comprueba tiene algún  rol de una lista de roles
        @param rolelist: La lista de roles a comprobar
        @type rolelist: list
        @rtype:bool
        """
        if self.valid:
            if 'root' in self.__roles:
                return True
            else:
                return any([permission in rolelist for permission in self.roles ])
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
        elif not self.checkPassword(new)>3:
            raise UserWarning(u"La contraseña es demasiado sencilla")
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


    def checkPassword(self, password):
        #strength = ['Blank','Very Weak','Weak','Medium','Strong','Very Strong']
        score = 1

        if len(password) < 1:
            return 0
        if len(password) < 4:
            return 1

        if len(password) >=8:
            score = score + 1
        if len(password) >=11:
            score = score + 1

        if re.search('\d+',password):
            score = score + 1
        if re.search('[a-z]',password) and re.search('[A-Z]',password):
            score = score + 1
        if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]',password):
            score = score + 1

        return score
