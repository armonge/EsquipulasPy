SELECT cc.*, SUM(cxd.monto)
FROM cuentascontables cc
JOIN cuentascontables padre ON padre.idcuenta = cc.padre
JOIN cuentascontables abuelo ON padre.padre = abuelo.idcuenta AND abuelo.padre = 1
LEFT JOIN cuentascontables hijos ON hijos.codigo LIKE CONCAT(SUBSTRING_INDEX(cc.codigo,' ',2), "%")
JOIN cuentasxdocumento cxd ON cxd.idcuenta = hijos.idcuenta 
JOIN documentos d ON d.iddocumento = cxd.iddocumento AND MONTH(NOW()) = MONTH(d.fechacreacion) AND YEAR(d.fechacreacion) = YEAR(NOW())
WHERE cc.codigo NOT LIKE '' 
GROUP BY cc.idcuenta
ORDER  BY cc.idcuenta
