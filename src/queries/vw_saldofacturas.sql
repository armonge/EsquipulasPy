DROP VIEW IF EXISTS `vw_saldofacturas`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_saldofacturas` AS

select fac.iddocumento AS iddocumento,
fac.ndocimpreso AS ndocimpreso,
(fac.total - sum(ifnull(ph.monto,0))) AS saldo,
ifnull(ca.valorcosto,0) AS tasaiva,
p.idpersona AS idpersona,
p.nombre AS nombre
from documentos fac
join personasxdocumento pd on pd.iddocumento = fac.iddocumento
join personas p on p.idpersona = pd.idpersona and p.tipopersona = 1
left join docpadrehijos ph on ph.idpadre = fac.iddocumento
left join documentos recibo on ph.idhijo = recibo.iddocumento and recibo.idtipodoc = 18
left join costosxdocumento cd on cd.iddocumento = fac.iddocumento
left join costosagregados ca on
cd.idcostoagregado = ca.idcostoagregado  and ca.idtipocosto = 1
where fac.idtipodoc = 5 and fac.idestado = 1
group by fac.iddocumento order by cast(fac.ndocimpreso as signed);