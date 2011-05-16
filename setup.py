# -*- coding: utf-8 -*-
u"""
@author: Andrés Reyes Monge
"""

import os, sys
from setuptools import setup, find_packages


OPTIONS = {}
FILES = {'doc':['doc/manual/*']}

SCRIPTS = []

setup( 
    name = 'misesquipulas',
    version = '1.1',
    description = 'Interfaz de Escritorio a Esquipulas',
    author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia,'\
    ' Marcos Antonio Moreno Gonzales',
    author_email = "armonge@gmail.com",
    url = 'https://sourceforge.net/projects/misesquipulas/',
    license = "GPL V3",
    packages = [
        'esquipulaspy',
        'esquipulaspy.caja',
        'esquipulaspy.contabilidad',
        'esquipulaspy.document',
        'esquipulaspy.inventario',
        'esquipulaspy.ui',
        'esquipulaspy.utility',
    ],
    package_dir={'esquipulaspy': 'esquipulaspy'},
    package_data={'esquipulaspy': ['translations/*.qm']},
    scripts = SCRIPTS,
    options = OPTIONS,
    classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: X11 Applications :: Qt",
    "License :: OSI Approved :: GNU General Public License (GPL)"
    "Natural Language :: Spanish",
    "Programming Language :: Python :: 2.7",
    "Topic :: Office/Business",
    ],

 )

