#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       
#       Copyright 2010 Andrés Reyes Monge <armonge@armonge-laptop.site>
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

from PyQt4.QtGui import QSortFilterProxyModel
class TreeFilterProxyModel( QSortFilterProxyModel ):
    #FIXME: Funciona pero es endemoniadamente lento
    def __init__( self, parent = None ):
        super( TreeFilterProxyModel, self ).__init__( parent )
        self.__showAllChildren = False

    def showAllChildren( self ):
        return self.__showAllChildren;

    def setShowAllChildren( self, showAllChildren ):
        if showAllChildren == self.__showAllChildren:
            return
        self.__showAllChildren = showAllChildren
        self.invalidateFilter()

    def filterAcceptsRow ( self, source_row, source_parent ):
        if self.filterRegExp() == "" :
            return True #Shortcut for common case

        if  super( TreeFilterProxyModel, self ).filterAcceptsRow( source_row, source_parent ) :
            return True

        #one of our children might be accepted, so accept this row if one of our children are accepted.
        source_index = self.sourceModel().index( source_row, 0, source_parent )
        for i in range( self.sourceModel().rowCount( source_index ) ):
            if self.filterAcceptsRow( i, source_index ):
                return True

        return False
