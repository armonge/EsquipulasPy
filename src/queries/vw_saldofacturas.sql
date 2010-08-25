DROP VIEW IF EXISTS `vw_saldofacturas`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_saldofacturas` AS

select
 fac.iddocumento as iddocumento,
 fac.ndocimpreso,
fac.total as totalfacturado,
fac.total- SUM(IF(otros.idtipodoc=10,otros.total,0)) - SUM(IF(otros.idtipodoc=18,ph.monto,0)) as saldo,
  SUM(IF(otros.idtipodoc=10,otros.total,0)) as totaldevolucion,
  SUM(IF(otros.idtipodoc=18,ph.monto,0)) as totalabono,
  ca.valorcosto as tasaiva,
  p.idpersona,
  p.nombre,
  fac.idestado
from documentos fac
join personasxdocumento pxd ON pxd.iddocumento = fac.iddocumento AND pxd.idaccion = 1
JOIN personas p ON p.idpersona = pxd.idpersona
left join costosxdocumento cd ON cd.iddocumento = fac.iddocumento
left join costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado
left join docpadrehijos ph on ph.idpadre = fac.iddocumento
left join documentos otros on ph.idhijo = otros.iddocumento AND otros.idestado =1
WHERE
-- fac.iddocumento = 40 AND
fac.idtipodoc = 5
GROUP BY fac.iddocumento
;