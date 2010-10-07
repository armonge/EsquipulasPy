# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
u"""
Modulo que se encarga de compilar el codigo en un solo ejecutable
@author: Andrés Reyes Monge

Utiliza py2exe para crear un ejecutable y una serie de dlls en Windows
"""

import platform
import os

if platform.system() == 'Windows':
    from distutils.core import setup
    import py2exe
    #Override the function in py2exe to determine if a dll should be included
    dllList = ( 'mfc90.dll', 'msvcp90.dll', 'qtnetwork.pyd', 'qtxmlpatterns4.dll', 'qtsvg4.dll' )
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL( pathname ):
        if os.path.basename( pathname ).lower() in dllList:
            return 0
        return origIsSystemDLL( pathname )
    py2exe.build_exe.isSystemDLL = isSystemDLL
    setup(
        name = 'MIS Esquipulas',
        version = '1.0',
        description = 'Interfaz de Escritorio a Esquipulas',
        author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia, Marcos Antonio Moreno Gonzales',
        windows = [{
            'script':'esquipulas.py',
            'icon_resources':[( 1, os.getcwd() + r"\ui\res\logo.ico" )]
            }],
        options = {
            "py2exe": {
                "includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore", "PyQt4.QtSql", "PyQt4.QtWebKit", "PyQt4.QtNetwork"],
                "dist_dir":r"..\dist"
                }
            },
        data_files =  [
                ( 'sqldrivers', [
                    'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlmysql4.dll'
                    ]
                ),
                ( '', [
                    r'C:\Python26\Lib\site-packages\PyQt4\bin\libmySQL.dll'
                    ]
                ),
                ( 'translations', [
                        os.getcwd() + r'\translations\qt_es.qm'
                    ]
                ),
                ( 'help', [
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\assistant.exe',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtAssistantClient4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\qt.conf',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\mingwm10.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\libgcc_s_dw2-1.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtCore4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtGui4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtHelp4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtCLucene4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtNetwork4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtSql4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtXml4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtWebKit4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\QtXmlPatterns4.dll',
                        r'C:\Python26\Lib\site-packages\PyQt4\bin\phonon4.dll',
                        os.getcwd() + r'\help\doc.qch',
                        os.getcwd() + r'\help\assistant.bat',
                        os.getcwd() + r'\help\esquipulashelpcollection.qhc',
                    ]
                ),
                (r'help\sqldrivers',[
                    r'C:\Python26\Lib\site-packages\PyQt4\plugins\sqldrivers\qsqlite4.dll'
                    ]
                ),
           ]
        )
else:
   from setuptools import setup, find_packages
   setup(
            name = 'MIS Esquipulas',
            version = '1.0',
            description = 'Interfaz de Escritorio a Esquipulas',
            author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia, Marcos Antonio Moreno Gonzales',
            author_email = "armonge@gmail.com",
            include_package_data = True,
            packages = find_packages(),
            scripts = ['esquipulas.py'],
        )
        
