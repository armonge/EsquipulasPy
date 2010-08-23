DROP VIEW IF EXISTS `vw_articulosprorrateados`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_articulosprorrateados` AS
select
a.idarticulo AS idarticulo,
a.unidades AS unidades,
a.costocompra AS costocompra,
(a.unidades * a.costocompra) AS fob,
ROUND((l.fletetotal / l.fobtotal) * (a.unidades * a.costocompra),4) AS flete,
ROUND((l.segurototal / l.fobtotal) * (a.unidades * a.costocompra),4) AS seguro,
ROUND((l.otrosgastostotal / l.fobtotal) * (a.unidades * a.costocompra),4) AS otrosgastos,
ROUND((l.ciftotal / l.fobtotal) * (a.unidades * a.costocompra),4) AS cif,
ROUND(((((cal.dai + cal.isc) + ((l.iso * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra))) + (((l.tsimtotal / l.ciftotal) * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra))) + (((l.spe / l.ciftotal) * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra))) + (l.iva * (((((l.ciftotal / l.fobtotal) * (a.unidades * a.costocompra)) + cal.dai) + cal.isc) + (((l.tsimtotal / l.ciftotal) * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra)))),4) AS impuestos,
cal.comision AS comision,
ROUND(((l.agenciatotal / l.ciftotal) * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra),4) AS agencia,
ROUND(((l.almacentotal / l.ciftotal) * (l.ciftotal / l.fobtotal)) * (a.unidades * a.costocompra),4) AS almacen,
ROUND(l.tasapapeleria * a.unidades,4) AS papeleria,
ROUND(l.tasatransporte * a.unidades,4) AS transporte,
a.iddocumento AS iddocumento,
a.costounit * a. unidades as costototal,
a.costounit
from articulosxdocumento a
join vw_liquidacionescontodo l on (a.iddocumento = l.iddocumento)
join costosxarticuloliquidacion cal on(cal.idarticuloxdocumento = a.idarticuloxdocumento)
;