# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
u"""
Modulo que se encarga de compilar el codigo en un solo ejecutable
@author: Andrés Reyes Monge

Utiliza py2exe para crear un ejecutable y una serie de dlls en Windows
"""

import os, sys
from setuptools import setup, find_packages


OPTIONS = {}
WINDOWS = {}
FILES = {}

if os.name == 'posix':
    pass
elif os.name == 'nt':
    import py2exe
    #Override the function in py2exe to determine if a dll should be included
    DLLLIST = ( 'mfc90.dll', 'msvcp90.dll', 'qtnetwork.pyd',
                'qtxmlpatterns4.dll', 'qtsvg4.dll' )
    ORIGISSSYSTEMDLL = py2exe.build_exe.isSystemDLL
    def is_system_dll( pathname ):
        """
        @param pathname: La ruta del ensamblado
        """
        if os.path.basename( pathname ).lower() in DLLLIST:
            return 0
        return ORIGISSSYSTEMDLL( pathname )
    py2exe.build_exe.isSystemDLL = is_system_dll

    WINDOWS = {
            'script':'esquipulas.py',
            'icon_resources':[( 1, os.getcwd() + r"\ui\res\logo.ico" )]
        },
    OPTIONS = {
            "py2exe": {
                "includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore",
                             "PyQt4.QtSql", "PyQt4.QtWebKit",
                             "PyQt4.QtNetwork"]
                }
        }

    if "py2exe" in sys.argv:
		FILES = [
			( 'sqldrivers', [
				r'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlmysql4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlite4.dll'
				]
			),
			( 'Scripts', [
				r'C:\Python26\Lib\site-packages\PyQt4\bin\libmySQL.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\assistant.exe',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\QtAssistantClient4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\qt.conf',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\mingwm10.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\libgcc_s_dw2-1.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\QtHelp4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\QtCLucene4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\QtXml4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\QtXmlPatterns4.dll',
				r'C:\Python26\Lib\site-packages\PyQt4\bin\phonon4.dll',


				os.getcwd() + r'\ui\res\logo.ico',
				os.getcwd() + r'\help\doc.qch',
				os.getcwd() + r'\help\esquipulashelpcollection.qhc',
				]
			),
			( 'translations', [
				os.getcwd() + r'\translations\qt_es.qm'
				]
			)
		]

setup( 
    name = 'misesquipulas',
    version = '1.0',
    description = 'Interfaz de Escritorio a Esquipulas',
    author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia,'\
    ' Marcos Antonio Moreno Gonzales',
    author_email = "armonge@gmail.com",
    packages = find_packages(),
    scripts = ['esquipulas.py'],
    data_files = FILES,
    options = OPTIONS,
    windows = WINDOWS,
 )

