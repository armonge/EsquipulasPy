DROP VIEW IF EXISTS `vw_liquidacioncontotales`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_liquidacioncontotales` AS
select l.iddocumento AS iddocumento,
sum(a.unidades) AS unidadestotal,
sum(cal.comision) AS comisiontotal,
sum((a.unidades * a.costocompra)) AS fobtotal,
l.fletetotal AS fletetotal,
l.segurototal AS segurototal,
l.otrosgastos AS otrosgastostotal,
(((sum((a.unidades * a.costocompra)) + l.fletetotal) + l.segurototal) + l.otrosgastos) AS ciftotal,
FNIMPUESTOS(l.iddocumento,(((sum((a.unidades * a.costocompra)) + l.fletetotal) + l.segurototal) + l.otrosgastos),(((sum((a.unidades * a.costocompra)) + l.fletetotal) + l.segurototal) + l.otrosgastos), 
sum(cal.dai),
sum(cal.isc)
) AS impuestototal,
l.peso AS pesototal,
l.totalagencia AS agenciatotal,
l.totalalmacen AS almacentotal,
round(((l.porcentajepapeleria / 100) * sum(a.unidades)),
4) AS papeleriatotal,
round(((l.porcentajetransporte / 100) * sum(a.unidades)),
4) AS transportetotal,
(l.porcentajepapeleria / 100) AS tasapapeleria,
(l.porcentajetransporte / 100) AS tasatransporte,
l.procedencia AS procedencia 
from (((liquidaciones l join articulosxdocumento a on((l.iddocumento = a.iddocumento))) join costosxarticuloliquidacion cal on((a.idarticuloxdocumento = cal.idarticuloxdocumento))) join vw_liquidacionesconcostos lcc on((lcc.iddocumento = l.iddocumento))) group by l.iddocumento;