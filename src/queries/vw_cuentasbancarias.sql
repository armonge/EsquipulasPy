SELECT
cc.idcuenta,
b.descripcion,
c.ctabancaria,
tp.simbolo,
cc.codigo,
cc.descripcion
FROM cuentasbancarias c
JOIN bancos b ON b.idbanco=c.idbanco
JOIN tiposmoneda tp ON tp.idtipomoneda=c.idtipomoneda
JOIN cuentascontables cc ON cc.idcuenta=c.idcuentacontable
;
