SELECT
factura.iddocumento,
factura.ndocimpreso,
factura.total - SUM(IFNULL(abono.monto,0)) - IFNULL(devolucion.total,0)  AS saldo,
p.idpersona,
p.nombre
FROM documentos factura
JOIN personasxdocumento pd ON pd.iddocumento=factura.iddocumento
JOIN personas p ON pd.idpersona=p.idpersona AND p.tipopersona=1
LEFT JOIN docpadrehijos abono ON abono.idpadre=factura.iddocumento
LEFT JOIN documentos recibo ON abono.idhijo=recibo.iddocumento AND recibo.idtipodoc=18
LEFT JOIN documentos devolucion ON abono.idhijo=devolucion.iddocumento AND devolucion.idtipodoc=10
WHERE factura.idtipodoc=5
AND factura.anulado=0
GROUP BY factura.iddocumento
;