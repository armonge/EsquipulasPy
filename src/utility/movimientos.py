# -*- coding: utf-8 -*-
'''
@author: Luis Carlos Mejia

Modulo que contendra las funciones para insertar los movimientos contables a la base de datos
'''

from PyQt4.QtSql import QSqlQuery

PERDIDAS = "334"
"""
El id de la cuenta OG Robos o Perdidas, 650 001 000 000
@type: string 
"""

OTROSINGRESOS = "356"
"""
El id de la cuenta OTROS INGRESOS, 420 000 000 000
@type: string 
"""

VENTASNETAS = "173"
"""
El id de la cuenta Ventas Netas, 410 003 000 000
@type: string
"""

COSTOSVENTAS = "182"
"""
El id de la cuenta Costos de Ventas, 510 001 000 000 000
@type: string
"""

IMPUESTOSXPAGAR = "133"
"""
El id de la cuenta Impuesto por pagar, 210 008 001 001 000
@type:string
"""

IMPUESTOSPAGADOSIVA = "34"
"""
El id de la cuenta Impuestos pagados por anticipado (IVA), 110 005 003 000 000
@type:string
"""

RETENCIONXPAGAR = "119"
"""
El id de la cuenta RP IR en la Fuente por Pagar 2%, 210 006 001 000 000
@type: string
"""

RETENCIONPAGADA = "35"
"""
PA Impuestos Anticipados (IR), 110 005 004 000 000
@type:string
"""

CAJAGENERAL = "5"
"""
El id de la cuenta Caja genera, 110 001 001 000
@type:string
"""

INVENTARIO = "22"
"""
El id de la cuenta Inventario, 110 003 001 000 000
@type:string
"""

CXCCLIENTE = "14"
"""
El id de la cuenta Cuentas por cobar, 110 002 001 000
@type:string
"""

PROVEEDORLOCAL = "89"
"""
El id de la cuenta PE PUENTE INVENTARIO-PROVEEDORES, 210 001 002 008 000
@type:string
"""

PRODUCTOSFINANCIEROS = "323"
"""
El id de la cuenta PRODUCTOS FINANCIEROS, 640 001 000 000 000
@type:string
"""

def movFacturaContado( iddoc, subtotal, impuesto, retencion, totalcosto ):
    '''
    MOVIMIENTOS CONTABLE PARA LA FACTURA AL CONTADO
    
    (-)subtotal             > entra a Ventas netas: id=173, cod=410 003 000 000
    
    (-)impuesto             > entra a impuesto por pagar:id=133, cod=210 008 001 001 000
    
    (+)retencion                               > entra a retencion pagadas por anticipado: id=118, cod=210 006 000 000 000
    
    (+)total a pagar                           > entra a caja genera:id=5, cod=110 001 001 000 

    (-)total precio costo   > Sale de Inventario:id=22, cod=110 003 001 000 000
    
    (+)total precio costo                      > entra a Costos de Ventas:id=182, cod=510 001 000 000 000
    
    @param iddoc: El id del documento que genera estos documentos
    @type iddoc: int
    
    @param subtotal: TODO 
    @type subtotal: Decimal
    @param impuesto: TODO
    @type impuesto: Decimal
    @param retencion: TODO
    @type retencion: Decimal
    @param totalcosto: TODO
    @type totalcosto: Decimal
    

    '''
    totalcosto = totalcosto.to_eng_string()
    iddoc = str( iddoc )
    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + VENTASNETAS + "," + iddoc + ",-:subtotal)," +
    ( "" if impuesto == 0 else "(" + IMPUESTOSXPAGAR + "," + iddoc + ",-:impuesto)," ) +
    ( "" if retencion == 0 else "(" + RETENCIONPAGADA + "," + iddoc + ",:retencion)," ) +
    "(" + CAJAGENERAL + "," + iddoc + ",:totalpagar)," +
    "(" + INVENTARIO + "," + iddoc + ",-" + totalcosto + ")," +
    "(" + COSTOSVENTAS + "," + iddoc + "," + totalcosto + ")" )
    print( query.lastQuery() )
    #query.bindValue(":iddoc", iddoc)
    query.bindValue( ":subtotal", subtotal.to_eng_string() )
    query.bindValue( ":impuesto", impuesto.to_eng_string() )
    query.bindValue( ":retencion", retencion.to_eng_string() )
    query.bindValue( ":totalpagar", ( subtotal + impuesto - retencion ).to_eng_string() )


    if not query.exec_():
        print( iddoc )
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )

def movFacturaCredito( iddoc, subtotal, impuesto, totalcosto ):
    '''
    MOVIMIENTOS CONTABLE PARA LA FACTURA AL CONTADO
    
    (-)subtotal             > entra a Ventas netas: id=173, cod=410 003 000 000
    
    (-)impuesto             > entra a impuesto por pagar:id=133, cod=210 008 001 001 000
    
    (+)total factura                           > entra aCuentas por cobar: id=14 , cod= 110 002 001 000 

    (-)total precio costo   > Sale de Inventario:id=22, cod=110 003 001 000 000
    
    (+)total precio costo                      > entra a Costos de Ventas:id=182, cod=510 001 000 000 000
    
    @param iddoc: El id del documento que genera este movimiento
    @type iddoc: int
    
    @param subtotal: TODO
    @type subtotal: Decimal
    @param impuesto: TODO
    @type impuesto: Decimal
    @param totalcosto: TODO
    @type totalcosto: Decimal

    
    '''
    totalcosto = totalcosto.to_eng_string()
    iddoc = str( iddoc )
    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + VENTASNETAS + "," + iddoc + ",-:subtotal)," +
    ( "" if impuesto == 0 else "(" + IMPUESTOSXPAGAR + "," + iddoc + ",-:impuesto)," ) +
    "(" + CXCCLIENTE + "," + iddoc + ",:totalpagar)," +
    "(" + INVENTARIO + "," + iddoc + ",-" + totalcosto + ")," +
    "(" + COSTOSVENTAS + "," + iddoc + "," + totalcosto + ")" )
    query.bindValue( ":subtotal", subtotal.to_eng_string() )
    query.bindValue( ":impuesto", impuesto.to_eng_string() )
    query.bindValue( ":totalpagar", ( subtotal + impuesto ).to_eng_string() )


    if not query.exec_():
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )


def movAbonoDeCliente( iddoc, total, retencion,ganancia ):
    '''
    MOVIMIENTOS CONTABLE PARA LA UN RECIBO
    
    (-)total             > entra a Ventas netas: id=173, cod=410 003 000 000
    
    (+)retencion                               > entra a retencion pagadas por anticipado: id=118, cod=210 006 000 000 000
    
    (+)total pagado                          > entra a caja genera:id=5, cod=110 001 001 000 
  
    @param iddoc: El id del documento que genera este documento
    @type iddoc: int
    
    @param total: TODO
    @type total: Decimal
    @param retencion: TODO
    @type retencion: Decimal
    '''    
    iddoc = str( iddoc )
    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + CXCCLIENTE + "," + iddoc + ",-:total)," +
    ("" if ganancia == 0  else "(" + PRODUCTOSFINANCIEROS + "," + iddoc + ",-:ganancia)," )+
    ( "" if retencion == 0 else "(" + RETENCIONPAGADA + "," + iddoc + ",:retencion)," ) +
    "(" + CAJAGENERAL + "," + iddoc + ",:totalpagar)" )

    query.bindValue( ":total", total.to_eng_string() )
    query.bindValue( ":ganancia", ganancia.to_eng_string() )
    query.bindValue( ":retencion", retencion.to_eng_string() )
    query.bindValue( ":totalpagar", ( total - retencion + ganancia ).to_eng_string() )


    if not query.exec_():
        print( iddoc )
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )


def movPagoRealizado( iddoc, subtotal, impuesto , retencion , ctabanco_caja = CAJAGENERAL, ctaproveedor_gasto = PROVEEDORLOCAL ):
    '''
    MOVIMIENTOS CONTABLE PARA UN ABONO A PROVEEDOR
    
    (-)total             > entra de proveedores PE PUENTE INVENTARIO-PROVEEDORES:id=89, cod=210 001 002 008 000
    
    (+)retencion                               > entra a RP IR en la Fuente por Pagar 2%: id = 119, cod=210 006 001 000 000
    
    (+)total pagado                          > sale de banco ctabanco_caja
    @param iddoc: El id del documento que genera estos movimientos
    @type iddoc: int
    
    @param subtotal: TODO
    @type subtotal: Decimal
    @param impuesto: TODO
    @type impuesto: Decimal
    @param retencion: TODO
    @type retencion: Decimal
    @param ctabanco_caja: TODO
    @type ctabanco_caja: string
    @param ctaproveedor_gasto: TODO
    @type ctaproveedor_gasto:string 

    
    '''

    iddoc = str( iddoc )

    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + ctaproveedor_gasto + "," + iddoc + ",:subtotal)," +
	( "" if retencion == 0 else "(" + RETENCIONXPAGAR + "," + iddoc + ",-:retencion)," ) +
	( "" if impuesto == 0 else "(" + IMPUESTOSPAGADOSIVA + "," + iddoc + ",:impuesto)," ) +
    "(" + ctabanco_caja + "," + iddoc + ",-:totalpagar)" )

    query.bindValue( ":subtotal", subtotal.to_eng_string() )
    query.bindValue( ":retencion", retencion.to_eng_string() )
    query.bindValue( ":impuesto", impuesto.to_eng_string() )
    query.bindValue( ":totalpagar", ( subtotal + impuesto - retencion ).to_eng_string() )

    print( subtotal.to_eng_string() )
    print( retencion.to_eng_string() )

    if not query.exec_():
        print( iddoc )
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )


def movEntradaCompra( iddoc, total, impuestopagado ):
    '''
    MOVIMIENTOS CONTABLE PARA UNA ENTRADA COMPRA
    
    (-)total de la compra                            > entra a PE PUENTE INVENTARIO-PROVEEDORES:id=89, cod=210 001 002 008 000
    
    (+)iva                                            > entra a PA Impuestos  Anticipados (IVA): id=34, cod=110 005 003 000 000
    
    (+)total de la compra                           > entra de Inventario:id=22, cod=110 003 001 000 000

  
    @param iddoc: El id del documento que genera estos movimientos
    @type iddoc: int
    
    @param total: TODO
    @type total: Decimal
    @param impuestopagado: TODO
    @type impuestopagado: Decimal
     
    
    '''
    iddoc = str( iddoc )
    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + PROVEEDORLOCAL + "," + iddoc + ",-:total)," +
    "(" + IMPUESTOSPAGADOSIVA + "," + iddoc + ",:iva)," +

    "(" + INVENTARIO + "," + iddoc + ",:subtotal)" )

    query.bindValue( ":total", total.to_eng_string() )
    query.bindValue( ":iva", impuestopagado.to_eng_string() )
    query.bindValue( ":subtotal", ( total - impuestopagado ).to_eng_string() )

    if not query.exec_():
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )

def movDeposito( iddoc, deposito, ctabanco ):
    '''
    MOVIMIENTOS CONTABLE PARA UNA ENTRADA COMPRA
    
    (-)deposito        > sale de Caja genera:id=5, cod=110 001 001 000 
    
    (+)deposito                            > entra a cuenta del banco ctabanco
    @param iddoc: El id del documento que genera estos movimientos 
    @type iddoc: int
    @param deposito: TODO
    @type deposito: Decimal
    @param ctabanco: TODO
    @type ctabanco: Decimal
    
    
    '''
    iddoc = str( iddoc )
    total = deposito.to_eng_string()
    ctabanco = str( ctabanco )

    query = QSqlQuery()
    query.prepare( "INSERT INTO cuentasxdocumento (idcuenta,iddocumento,monto) values " +
    "(" + CAJAGENERAL + "," + iddoc + ",-" + total + ")," +
    "(" + ctabanco + "," + iddoc + "," + total + ")" )
    if not query.exec_():
        print( iddoc )
        print( query.lastError().text() )
        raise Exception( "NO SE PUDIERON INSERTAR LAS CUENTAS CONTABLES" )
    
def movKardex(iddoc, total):
    '''
    MOVIMIENTO CONTABLE PARA UNA ENTRADA DE BODEGA POR LIQUIDACION O ENTRADA LOCAL
    
    @param iddoc: El id del documento que genera estos movimientos
    @type iddoc: int
    @param total: El total del movimiento
    @type total: Decimal 
    '''
    query = QSqlQuery()
    iddoc = str(iddoc)
    if total == 0:
        raise Exception("Se trato de hacer un movimiento de monto 0")
    elif total > 0:
        query.prepare("INSERT INTO cuentasxdocumento ( idcuenta, iddocumento, monto) VALUES " +
                      " ( " + INVENTARIO + " , " + iddoc + " , " + total.to_eng_string() + " ) , " +
                      " ( " + OTROSINGRESOS + " , " + iddoc + " , -" + total.to_eng_string() + " )  ")
    
    else:
        query.prepare("INSERT INTO cuentasxdocumento ( idcuenta, iddocumento, monto) VALUES " +
                      " ( " + INVENTARIO + " , " + iddoc + " , " + total.to_eng_string() + " ) , " +
                      " ( " + PERDIDAS + " , " + iddoc + " , -" + total.to_eng_string() + " )  ")
        
    if not query.exec_():
        print query.lastError().text()
        raise Exception("No se pudo ejecutar la consulta para el movimiento contable de kardex")