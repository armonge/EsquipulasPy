DELIMITER $$

DROP PROCEDURE IF EXISTS `spAutorizarDevolucion` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAutorizarDevolucion`(
IDNC INT,
IDGERENTE INT,
AUTORIZAR INT,
TIPONC INT,
TIPOFACTURA INT,
TIPOCIERRE INT,
TIPORECIBO INT,
CONFIRMADO INT,
PENDIENTE INT,
VENTAS INT,
COSTOVENTA INT,
IVAXPAGAR INT,
RETENCIONPAGADA INT,
CAJA INT,
INVENTARIO INT


)
BEGIN

--  DECLARE EXIT HANDLER FOR SQLEXCEPTION
--  BEGIN
--      ROLLBACK;
--      SELECT False;
--  END;


    START TRANSACTION;


SELECT
-- *
fnConsecutivo(TIPONC,null) as ndocimpreso,
fac.iddocumento as idfactura,
-- ROUND(dev.total * tc.tasa,4) as 'totaldev C$',
ROUND((dev.total * tc.tasa) / (1 + (ca.valorcosto/100)),4) as 'subtotal dev',
ca.valorcosto as 'tasaIVA',
 tc.tasa,
-- phrec.monto,0)) as 'total abono'
dev.total 'totaldev $',
-- (SUM(IFNULL(phrec.monto,0)) - SUM(IFNULL(phrecdev.monto,0))) as totalabonos,
-- -- SUM(IFNULL(phrec.monto,0)) as abono,
-- SUM(IFNULL(phrecdev.monto,0)) as abonosdevueltos,
(
(dev.total <= (SUM(IFNULL(phrec.monto,0)) - SUM(IFNULL(phrecdev.monto,0)))) AND
dev.idestado IN (PENDIENTE))

 AS aceptable,
IF(cierre.iddocumento IS NULL,0,1) AS cerrado

FROM documentos dev

JOIN docpadrehijos ph ON ph.idhijo = dev.iddocumento
JOIN documentos fac ON ph.idpadre = fac.iddocumento AND fac.idtipodoc = TIPOFACTURA

LEFT JOIN docpadrehijos phcierre ON phcierre.idpadre = fac.iddocumento
LEFT JOIN documentos cierre ON phcierre.idhijo = cierre.iddocumento AND cierre.idtipodoc = TIPOCIERRE


LEFT JOIN docpadrehijos phrec ON phrec.idpadre = fac.iddocumento
LEFT JOIN documentos rec ON phrec.idhijo = rec.iddocumento AND rec.idtipodoc = TIPORECIBO

LEFT JOIN docpadrehijos phrecdev ON phrecdev.idpadre = rec.iddocumento
LEFT JOIN documentos recdev ON phrecdev.idhijo = recdev.iddocumento AND recdev.idtipodoc=TIPONC


JOIN tiposcambio tc on tc.idtc = fac.idtipocambio
LEFT JOIN costosxdocumento cd ON cd.iddocumento = fac.iddocumento
LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado
WHERE
dev.iddocumento =IDNC
    INTO
    @numeroNC,
    @idfactura,
    @subtotal,
    @tasaIVA,
    @tasa,
    @totaldev,
    @aceptable,
    @cerrado
     ;

IF @aceptable <> 1 OR @cerrado =1 THEN
  SELECT FALSE;

ELSE

SET @totalret:=0;

DROP TEMPORARY TABLE IF EXISTS devolucionxabono;
CREATE TEMPORARY TABLE devolucionxabono
SELECT
rec.iddocumento as idrecibo,
phrec.monto as totalabono,
SUM(
IFNULL(phrecdev.monto,0)
) as totaldevuelto,

phrec.monto - SUM(IFNULL(phrecdev.monto,0)) as saldoactual,

@totaldev as totaldev,
ROUND(
IF(
IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),
IFNULL(@totaldev,0),
phrec.monto - SUM(IFNULL(phrecdev.monto,0))
) ,4) as devparcial,
ROUND(
IF(
IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),
IFNULL(@totaldev,0),
phrec.monto - SUM(IFNULL(phrecdev.monto,0))
) /
(
(100 + @tasaIVA)/
ca.valorcosto
)
,4) as retencionparcial,
(
@totalret:=
@totalret +
ROUND(
IF(
IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),
IFNULL(@totaldev,0),
phrec.monto - SUM(IFNULL(phrecdev.monto,0))
) /
(
(100 + @tasaIVA)/
ca.valorcosto
)
,4)
)as sumaret,
(
@totaldev:=
ROUND(
@totaldev -
IF(
@totaldev <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),
@totaldev,
phrec.monto - SUM(IFNULL(phrecdev.monto,0))
)
,4)
) AS devrestante
FROM
docpadrehijos phrec
JOIN documentos rec ON phrec.idhijo =rec.iddocumento AND rec.idtipodoc = TIPORECIBO
LEFT JOIN docpadrehijos phrecdev ON phrecdev.idpadre = rec.iddocumento
LEFT JOIN documentos recdev ON phrecdev.idhijo = recdev.iddocumento AND recdev.idtipodoc = TIPONC
LEFT JOIN costosxdocumento cd ON cd.iddocumento = rec.iddocumento
LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado
WHERE phrec.idpadre = @idfactura
GROUP BY rec.iddocumento
;

-- INSERTAR LA RELACION CON LOS recibos
INSERT INTO docpadrehijos(idpadre,idhijo,monto)
SELECT
idrecibo,
IDNC,
devparcial
FROM devolucionxabono
WHERE devparcial <> 0
;

IF @cerrado = 1 THEN
  SET @totalret:= 0;
  SET @totalIVA:= 0;
ELSE
  SET @totalret:= @totalret * @tasa;
  SET @totalIVA:= @subtotal * ROUND(@tasaIVA/100,4);
END IF;



select SUM(ROUND(unidades * costounit,4)) from articulosxdocumento WHERE iddocumento = IDNC INTO @totalcosto;





INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)
VALUES (IDNC,VENTAS,@subtotal),
(IDNC,CAJA,-(@subtotal + @totalIVA - @totalret))
;

IF @totalIVA >0 THEN
  INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)
  VALUES (IDNC,IVAXPAGAR,@totalIVA);
END IF;


IF @totalret >0 THEN
  INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)
  VALUES (IDNC,RETENCIONPAGADA,-@totalret);
END IF;


-- Revertir el costo de venta
INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)
VALUES (IDNC,INVENTARIO,@totalcosto),
(IDNC,COSTOVENTA,-@totalcosto)
;


INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDNC,AUTORIZAR);

UPDATE documentos SET idestado = CONFIRMADO, ndocimpreso =@numeroNC where iddocumento = IDNC LIMIT 1;




     COMMIT;
     SELECT TRUE;
END IF;

END $$

DELIMITER ;