DROP VIEW IF EXISTS `vw_saldofacturas`;
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_saldofacturas` AS

SELECT
fac.iddocumento,
fac.ndocimpreso,
fac.total AS saldo,
IFNULL(ca.valorcosto,0) AS tasaiva,
p.idpersona,
p.nombre
FROM documentos fac 
JOIN personasxdocumento pd ON pd.iddocumento = fac.iddocumento
JOIN personas p ON p.idpersona = pd.idpersona AND p.tipopersona = 1
LEFT JOIN costosxdocumento cd ON cd.iddocumento = fac.iddocumento
LEFT JOIN costosagregados ca ON cd.idcostoagregado = ca.idcostoagregado AND ca.idtipocosto = 1
WHERE fac.idtipodoc = 5 AND fac.idestado = 1
ORDER BY CAST(fac.ndocimpreso AS SIGNED);
