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
'''
Created on 02/11/2010

Este modulo corre todas las pruebas en el sistema, asumiendo que se llamen
tests.py
@author: armonge
'''

import os, subprocess
import fnmatch

ROOT = os.path.dirname( __file__ )
PATTERN = "tests.py"

filepaths = []
for dirpath, dirnames, filenames in os.walk ( ROOT ):
    filepaths.extend ( 
      os.path.join ( dirpath, f ) for f in fnmatch.filter ( filenames, PATTERN )
    )

for file in filepaths:
    subprocess.call( ['/usr/bin/env', 'python', file ] )
