DROP VIEW IF EXISTS `vw_articulosprorrateados`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_articulosprorrateados` AS
select `a`.`idarticulo` AS `idarticulo`,`a`.`unidades` AS `unidades`,
`a`.`costocompra` AS `costocompra`,(`a`.`unidades` * `a`.`costocompra`) AS `fob`,
round(((`l`.`fletetotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `flete`,
round(((`l`.`segurototal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `seguro`,
round(((`l`.`otrosgastostotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `otrosgastos`,
round(((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `cif`,
round((((((`cal`.`dai` + `cal`.`isc`) + ((`l`.`iso` * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`spe` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (`l`.`iva` * (((((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) + `cal`.`dai`) + `cal`.`isc`) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))))),4) AS `impuestos`,
`cal`.`comision` AS `comision`,round((((`l`.`agenciatotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `agencia`,round((((`l`.`almacentotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `almacen`,round((`l`.`tasapapeleria` * `a`.`unidades`),4) AS `papeleria`,
round((`l`.`tasatransporte` * `a`.`unidades`),4) AS `transporte`,`a`.`iddocumento` AS `iddocumento`,(`a`.`costounit` * `a`.`unidades`) AS `costototal`,`a`.`costounit` AS `costounit`,
a.nlinea
from ((`articulosxdocumento` `a` join `vw_liquidacionescontodo` `l` on((`a`.`iddocumento` = `l`.`iddocumento`))) join `costosxarticuloliquidacion` `cal` on((`cal`.`idarticuloxdocumento` = `a`.`idarticuloxdocumento`)));