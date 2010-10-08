
JOIN personasxdocumento pxd ON pxd.idpersona = p.idpersona
JOIN (
) pago ON pago.iddocumento = cxd.iddocumento
GROUP BY
;

SUM(IF(mc.idtipomoneda=1,mc.monto,0)) as totalc,
SUM(IF(mc.idtipomoneda=2,mc.monto,0)) as totald




SELECT
d.iddocumento,
d.ndocimpreso,
d.fechacreacion,
d.observacion,
con.descripcion
FROM documentos d
JOIN conceptos con ON con.idconcepto = d.idconcepto
JOIN costosxdocumento cxd ON cxd.iddocumento = d.iddocumento
JOIN costosagregados ca ON ca.idcostoagregado = ca.idcostoagregado
WHERE d.idtipodoc=30
;

SELECT
pago.iddocumento,
pago.ndocimpreso  as 'No. Comprobante',
pago.nombre as Beneficiario,
pago.Concepto,
SUM(IF(mc.idtipomoneda =1,mc.monto,0)) as totalc,
SUM(IF(mc.idtipomoneda =2,mc.monto,0)) as totald,
pago.fecha,
pago.tasa,
pago.total,
pago.total / (1 +SUM(IF(ca.idtipocosto=1,ca.valorcosto/100,0))) as subtotal,
(pago.total / (1 +SUM(IF(ca.idtipocosto=1,ca.valorcosto/100,0))) ) * SUM(IF(ca.idtipocosto in (8,9),ca.valorcosto/100,0)) as retencion
FROM costosagregados ca
JOIN costosxdocumento cxd ON ca.idcostoagregado = cxd.idcostoagregado
JOIN movimientoscaja mc ON mc.iddocumento = cxd.iddocumento
JOIN
(
SELECT
d.iddocumento,
d.ndocimpreso,
GROUP_CONCAT(IF(pxd.idaccion=2,p.nombre,'') SEPARATOR '') as nombre,
DATE_FORMAT(d.fechacreacion,'%d/%m/%Y') AS fecha,
d.observacion,
con.descripcion as concepto,
tc.tasa,
d.total
FROM documentos d
JOIN conceptos con ON con.idconcepto = d.idconcepto
JOIN personasxdocumento pxd ON pxd.iddocumento = d.iddocumento
JOIN personas p ON p.idpersona = pxd.idpersona
JOIN tiposcambio tc ON tc.idtc=d.idtipocambio
WHERE d.idtipodoc=30
GROUP BY d.iddocumento
) pago on pago.iddocumento = cxd.iddocumento
GROUP BY pago.iddocumento
;
