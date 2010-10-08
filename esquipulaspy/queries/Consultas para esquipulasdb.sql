/*CONSULTA DE SALDO INICIAL MENSUAL PARA UNA CUENTA BANCARIA*/
SELECT SUM(monto)- (	SELECT sum(monto)	FROM documentoxcuenta, documento	WHERE entraaldebe=0  AND fechacreacion < 20060101  and documento.iddocumento= documentoxcuenta.iddocumento   and documentoxcuenta.idcuenta=c.idcuenta) AS saldo FROM cuentacontable c JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta JOIN documento d ON dx.iddocumento=d.iddocumento WHERE entraaldebe=1 AND fechacreacion < 20060101 and c.idcuenta=1

/*CONSULTA DE DEBE,HABER Y SALDO INICIAL MENSUAL PARA UNA CUENTA CONTABLE*/
SELECT c.`idcuenta`, sum(monto) AS deber, @haber:=(	SELECT sum(monto)	FROM documentoxcuenta, documento	WHERE entraaldebe=0  AND fechacreacion < 20060101   and documento.iddocumento= documentoxcuenta.iddocumento   and documentoxcuenta.idcuenta=c.idcuenta   ) AS haber, SUM(monto)-@haber AS saldo FROM cuentacontable c JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta JOIN documento d ON dx.iddocumento=d.iddocumento WHERE entraaldebe=1 AND fechacreacion < 20060101 and c.idcuenta=1

/*CONSULTA DE DEBE,HABER Y SALDO TODAS LAS CUENTAS CONTABLE*/
SELECT c.`idcuenta`, sum(monto) AS deber, @haber:=(	SELECT sum(monto)	FROM documentoxcuenta, documento	WHERE entraaldebe=0  AND fechacreacion < 20060101   and documento.iddocumento= documentoxcuenta.iddocumento   and documentoxcuenta.idcuenta=c.idcuenta   ) AS haber, SUM(monto)-@haber AS saldo FROM cuentacontable c JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta JOIN documento d ON dx.iddocumento=d.iddocumento WHERE entraaldebe=1 GROUP BY c.idcuenta

/*CONSULTA DE MOVIMIENTO DE UNA CUENTA CONTABLE EN UN MES*/
SELECT c.`idcuenta`, d.iddocumento, @deber:=IF(dx.entraaldebe=0, monto, 0) AS deber, @haber:=IF(dx.entraaldebe=1, monto, 0) AS haber FROM cuentacontable c JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta JOIN documento d ON dx.iddocumento=d.iddocumento AND MONTH(fechacreacion) = 9 AND YEAR(fechacreacion)=2006 AND c.idcuenta=10 GROUP BY  dx.iddocumento ORDER BY iddocumento

/*MOVIMIENTO DE UNA CUENTA CONTABLE EN UN MES CON SU CONCEPTO Y DESCRIPCION*/
SELECT DATE_FORMAT(fechacreacion,'%d/%m/%Y') as Fecha, td.descripcion as Concepto, IF(dx.entraaldebe=0, monto, '') AS Deber, IF(dx.entraaldebe=1, monto, '') AS Haber FROM cuentacontable c JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta JOIN documento d ON dx.iddocumento=d.iddocumento JOIN tipodoc td ON d.idtipodoc=td.idtipodoc AND MONTH(fechacreacion) = 9 AND YEAR(fechacreacion)=2006 AND c.idcuenta=10 GROUP BY  dx.iddocumento ORDER BY fechacreacion

/*
MOVIMIENTOS DE UNA CUENTA EN UN MES,  CALCULA EL SALDO INICIAL
*/
SELECT fecha, concepto, IF(c.entraaldebe=1, monto, '')  AS deber,
IF(c.entraaldebe=0, monto, '')  AS haber,
IF(entraaldebe=1, 		@montoanterior:=@montoanterior + monto,		@montoanterior:=@montoanterior - monto) as saldo
FROM
(SELECT DATE_FORMAT(fechacreacion,'%d/%m/%Y') as fecha,
td.descripcion as concepto, monto, entraaldebe
FROM cuentacontable c
JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta
JOIN documento d ON dx.iddocumento=d.iddocumento
JOIN tipodoc td ON d.idtipodoc=td.idtipodoc
AND MONTH(fechacreacion) = /*el mes */
AND YEAR(fechacreacion)= /*el año*/
AND c.idcuenta=/*numero de cuenta*/
GROUP BY  dx.iddocumento
) as c,

/*aca se calcula el saldo anterior */
(SELECT @montoanterior:=(
SELECT SUM(monto)- (
SELECT SUM(monto)
FROM documentoxcuenta, documento
WHERE entraaldebe=0
AND fechacreacion < /*el primer dia del mes */
AND documento.iddocumento= documentoxcuenta.iddocumento
AND documentoxcuenta.idcuenta=c.idcuenta) AS saldo

FROM cuentacontable c
JOIN documentoxcuenta dx ON dx.idcuenta=c.idcuenta
JOIN documento d ON dx.iddocumento=d.iddocumento
WHERE entraaldebe=1
AND fechacreacion < /*el primer dia del mes */
AND c.idcuenta=1
)) r
ORDER BY fecha
