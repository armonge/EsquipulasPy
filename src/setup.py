# -*- coding: utf-8 -*-
u"""
Modulo que se encarga de compilar el codigo en un solo ejecutable
@author: Andrés Reyes Monge

Utiliza py2exe para crear un ejecutable y una serie de dlls en Windows
"""
from distutils.core import setup
import platform
import os

if platform.system() == 'Windows':
    import py2exe
    Mydata_files = [
            ( 'sqldrivers', [
                'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlmysql4.dll'
                ] ),
            ( 'translations', [
                os.getcwd() + r'\translations\qt_es.qm'
            ] ),
            
    ]
else:
    Mydata_files = [
                ( 'translations', [
                    os.getcwd() + r'/translations/qt_es.qm'
                ] ),
                
    ]

setup( 
	name = 'Esquipulas',
	version = '1.0',
	description = 'Interfaz de Escritorio a Esquipulas',
	author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia, Marcos Antonio Moreno Gonzales',
    includes = ['__main__.py','__init__.py'],
	windows = [{
		'script':'__main__.py',
		'icon_resources':[( 1, os.getcwd() + r"\ui\res\logo.ico" )]
		}],
	options = {
		"py2exe": {
			"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore", "PyQt4.QtSql", "PyQt4.QtWebKit", "PyQt4.QtNetwork"],
            "dist_dir":r"..\dist"
			}
		},
    data_files = Mydata_files
	)
