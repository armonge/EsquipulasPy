SELECT
cc.idcuenta,
cc.codigo,
cc.descripcion,
SUM(monto) as saldo,
cc.esdebe,
MAX(d.fechacreacion)
FROM cuentasxdocumento cd
JOIN cuentascontables cc ON cc.idcuenta = cd.idcuenta
JOIN documentos d ON d.iddocumento = cd.iddocumento
WHERE d.fechacreacion<LAST_DAY(CURDATE())+ INTERVAL 1 DAY
GROUP BY cd.idcuenta
;