# -*- coding: utf-8 -*-
u"""
Modulo que se encarga de compilar el codigo en un solo ejecutable
@author: Andrés Reyes Monge

Utiliza py2exe para crear un ejecutable y una serie de dlls en Windows
"""
from distutils.core import setup
import py2exe
import os

Mydata_files = [
            ( 'sqldrivers', [
                'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlmysql4.dll'
                ] )
]

setup( 
	name = 'Esquipulas',
	version = '1.0',
	description = 'Interfaz de Escritorio a Esquipulas',
	author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia, Marcos Antonio Moreno Gonzales',
	packages = ['inventario', 'compras', 'caja', 'contabilidad', 'utility', 'ui', 'document'],
	py_modules = ['__main__'],
	windows = [{
		'script':'__main__.py',
		'icon_resources':[( 1, os.getcwd() + r"\ui\res\logo.ico" )]
		}],
	options = {
		"py2exe": {
			"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore", "PyQt4.QtSql", "PyQt4.QtWebKit", "PyQt4.QtNetwork"]
			}
		},
	data_files = Mydata_files
	)
