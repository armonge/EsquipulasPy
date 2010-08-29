DELIMITER $$

DROP PROCEDURE IF EXISTS `spAutorizarAnulacionFactura` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAutorizarAnulacionFactura`(
IDANULACION INT,
IDGERENTE INT
)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      SELECT False;
  END;

-- INICIO TRANSACCION
    START TRANSACTION;

-- OBTENGO EL ID DE LA FACTURA QUE FUE ANULADA
     SELECT
          anul.idestado AS anulacionEstado,
          anul.idtipodoc ,
          fac.iddocumento AS facturaId,
          fac.escontado AS facturaContado
     FROM documentos anul
     JOIN docpadrehijos PH on ph.idhijo = IDANULACION
      JOIN documentos fac ON ph.idpadre = fac.iddocumento AND fac.idtipodoc = 5
      WHERE anul.iddocumento = IDANULACION
    INTO
    @anulEstado,
    @tipo,
    @factura,
    @esContado
     ;

    SELECT
        rec.iddocumento
    FROM documentos rec
    JOIN  docpadrehijos ph ON ph.idhijo = rec.iddocumento
    AND rec.idtipodoc=18
    AND ph.idpadre = @factura
    INTO
    @recibo
    ;


  IF @tipo <> 2 OR (@anulEstado IN (1,NULL)) OR (@esContado = 0 AND (@recibo IS NOT NULL)) THEN

      SELECT FALSE;

  ELSE

-- OBTENGO EL ID DEL RECIBO EN CASO DE QUE LA FACTURA FUERA AL CONTADO O HALLA SIDO PAGADA POR UN RECIBO


-- INSERTO LA RELACION DE LA ANULACION CON LA PERSONA QUE LA AUTORIZA
    INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDANULACION,5);

-- REVIERTO LAS CUENTAS CONTABLES DE LA FACTURA, RELACIONANDOLAS CON LA ANULACION
    INSERT INTO cuentasxdocumento
      SELECT
         IDANULACION,
         cxd.idcuenta,
         SUM(-cxd.monto) AS monto,
         nlinea
         FROM documentos doc
         JOIN cuentasxdocumento cxd ON  cxd.iddocumento = doc.iddocumento AND cxd.iddocumento IN (@factura,@recibo)
         GROUP BY cxd.idcuenta
         HAVING SUM(-cxd.monto)<>0
         ;

    -- VERIFICO SI HAY RECIBO
    IF @recibo is not null then

-- INSERTO LA RELACION ENTRE EL RECIBO Y  LA ANULACION, LA ANULACION ES EL HIJO.
      INSERT INTO docpadrehijos(idpadre,idhijo) VALUES
      (@recibo,IDANULACION)
       ;

-- ACTUALIZO EL ESTADO DEL RECIBO A ANULADO
      UPDATE documentos SET idestado = 2 where iddocumento = @recibo;
   END IF;

-- ACTUALIZO EL ESTADO DE LA ANULACION Y LO PASO A CONFIRMADO
    UPDATE documentos SET idestado = 1 WHERE iddocumento = IDANULACION;


    COMMIT;
    SELECT TRUE;
   END IF;
END $$

DELIMITER ;