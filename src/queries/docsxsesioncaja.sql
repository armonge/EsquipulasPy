SELECT 
d.iddocumento,
ph.idpadre,
d.fechacreacion,
-- d.total,
SUM(d.total),
tp.descripcion,
c.descripcion
FROM documentos d
JOIN tiposdoc tp ON tp.idtipodoc=d.idtipodoc
LEFT JOIN cajas c ON c.idcaja = d.idcaja
LEFT JOIN docpadrehijos ph ON d.iddocumento=ph.idhijo
LEFT JOIN documentos apertura ON apertura.iddocumento=ph.idpadre
WHERE (apertura.idtipodoc=22 OR d.idtipodoc=22)
AND d.idtipodoc<>5
GROUP BY IFNULL(ph.idpadre,d.iddocumento)
;