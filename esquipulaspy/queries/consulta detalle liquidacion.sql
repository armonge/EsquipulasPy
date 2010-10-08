SELECT * from articuloxdocumento a
join liquidacion l on l.iddocumento=a.iddocumento
join bodegas b on b.idbodega=a.idbodega WHERE a.iddocumento=226 order by a.nlinea;

SELECT
a.idarticulo
,a.unidades
,a.costocompra
,@fob:=(a.unidades * a.costocompra) as fob
,@flete:=(l.fletetotal / f.fobt) * @fob as flete
,@seguro:=(l.segurototal / f.fobt) * @fob as seguro
,@ogastos:=(l.otrosgastos / f.fobt) * @fob as 'otros gastos'
,@cif:=(@fob+@flete+@seguro+@ogastos) as cif

,@impuesto:=(
    cal.dai+
    cal.isc+
    (costos.iso*@cif)+
    (costos.tsim * CEILING(l.peso/costos.factorpeso)/cift.total*@cif)+
    costos.spe/cift.total*@cif +
    (costos.iva*(@cif + cal.dai + cal.isc + (costos.tsim * CEILING(l.peso/costos.factorpeso)/cift.total*@cif))
    )) as impuesto

,cal.comision
,@agencia:=(l.totalagencia / cift.total) * @cif as agencia
,@almacen:=(l.totalalmacen / cift.total) * @cif as almacen
,@pap:=(l.porcentajepapeleria /100) * a.unidades as papeleria
,@trans:=(l.porcentajetransporte /100) * a.unidades as transporte
,@total:=@cif+@impuesto+cal.comision+@agencia+@almacen+@pap+@trans as total
,@total*tc.tasa as 'total C$'
,b.nombrebodega
,cift.total

from articuloxdocumento a
join liquidacion l on l.iddocumento=a.iddocumento
join bodegas b on b.idbodega=a.idbodega
join costosxarticuloliquidacion cal on cal.idarticuloxdocumento=a.idarticuloxdocumento
JOIN (SELECT SUM(unidades*costocompra) as fobt FROM articuloxdocumento where iddocumento=228 group by iddocumento) f
JOIN
(
SELECT
sum(if(c.idtipocosto=1,valorcosto,0))/100 as iva
,sum(if(c.idtipocosto=4,valorcosto,0)) as spe
,sum(if(c.idtipocosto=5,valorcosto,0)) as tsim
,sum(if(c.idtipocosto=5,factorpeso,0)) as factorpeso
,sum(if(c.idtipocosto=6,valorcosto,0))/100 as iso
FROM costoagregado c
left join tsim t on c.idcostoagregado=t.idtsim and c.idtipocosto in (1,4,5,6)
join costoxdocumento cd on c.idcostoagregado=cd.idcostoagregado where cd.iddocumento=228
) costos

JOIN documento d on d.iddocumento=l.iddocumento
JOIN tipocambio tc on tc.idtc=d.tipocambio
join

(SELECT sum((a.unidades*a.costocompra) + (l.fletetotal+l.segurototal+l.otrosgastos) * ((a.unidades*a.costocompra)/f.fobt)) as total
from articuloxdocumento a
join liquidacion l on l.iddocumento=a.iddocumento and l.iddocumento=228
JOIN (SELECT SUM(unidades*costocompra) as fobt FROM articuloxdocumento where iddocumento=228 group by iddocumento) f) cift

WHERE a.iddocumento=228
order by a.nlinea ;

SELECT sum((a.unidades*a.costocompra) + (l.fletetotal+l.segurototal+l.otrosgastos) * ((a.unidades*a.costocompra)/f.fobt)) as cift
from articuloxdocumento a
join liquidacion l on l.iddocumento=a.iddocumento and l.iddocumento=228
JOIN (SELECT SUM(unidades*costocompra) as fobt FROM articuloxdocumento where iddocumento=228 group by iddocumento) f;

SELECT * FROM vw_costosdeldocumento v;