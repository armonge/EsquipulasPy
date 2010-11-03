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
from decimal import Decimal


def moneyfmt( value, places = 4, curr = '', sep = ',', dp = '.', pos = '', neg = '-', trailneg = '' ):
    """
    Convert Decimal to a money formatted string.

    @param places:  required number of places after the decimal point
    @type places: int
    @param curr:    optional currency symbol before the sign (may be blank)
    @type curr: string
    @param  sep:     optional grouping separator (comma, period, space, or blank)
    @type sep: string
    @param dp:      decimal point indicator (comma or period)  only specify as blank when places is zero
    @type dp: string
    @param pos:     optional sign for positive numbers: '+', space or blank
    @type pos: string
    @param neg:     optional sign for negative numbers: '-', '(', space or blank
    @type neg: string
    @param trailneg: optional trailing minus indicator:  '-', ')', space or blank
    @type trailneg: string
    @rtype: string

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.8901'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.0200>'

    """
    q = Decimal( 10 ) ** -places      # 2 places --> '0.01'
    sign, digits, _exp = value.quantize( q ).as_tuple()
    result = []
    digits = map( str, digits )
    build, next = result.append, digits.pop
    if sign:
        build( trailneg )
    for _i in range( places ):
        build( next() if digits else '0' )
    build( dp )
    if not digits:
        build( '0' )
    i = 0
    while digits:
        build( next() )
        i += 1
        if i == 3 and digits:
            i = 0
            build( sep )
    build( curr )
    build( neg if sign else pos )
    return ''.join( reversed( result ) )

