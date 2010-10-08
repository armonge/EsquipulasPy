# -*- coding: utf-8 -*-
u"""
@author: Andrés Reyes Monge
"""

import os, sys
from setuptools import setup, find_packages


OPTIONS = {}
FILES = {}

if os.name == 'posix':
    SCRIPTS = ['esquipulas-inventario', 'esquipulas-caja', 'esquipulas-contabilidad'],
elif os.name == 'nt':
    SCRIPTS = []

setup( 
    name = 'misesquipulas',
    version = '1.0',
    description = 'Interfaz de Escritorio a Esquipulas',
    author = u'Andrés Reyes Monge, Luis Carlos Mejia Garcia,'\
    ' Marcos Antonio Moreno Gonzales',
    author_email = "armonge@gmail.com",
    packages = find_packages(),
    scripts = SCRIPTS,
    data_files = FILES,
    options = OPTIONS,
 )

