DELIMITER $$

DROP PROCEDURE IF EXISTS `spAutorizarAnulacionFactura` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAutorizarAnulacionFactura`(
IDFACTURA INT,
IDGERENTE INT,
TIPOANULACION INT,
TIPOFACTURA INT,
TIPORECIBO INT,
TIPOKARDEX INT,
PENDIENTEANULAR INT,
CONFIRMADO INT,
ANULADO INT,
ACCIONAUTORIZAR INT
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
          fac.ndocimpreso,
          fac.idestado AS anulacionEstado,
          fac.idtipodoc ,
          SUM(IF(hijo.idtipodoc = TIPOANULACION,hijo.iddocumento,0)) AS anulacionId,
          SUM(IF(hijo.idtipodoc = TIPOKARDEX,hijo.iddocumento,0)) AS kardexId,
          fac.escontado AS facturaContado
      FROM documentos fac
      JOIN docpadrehijos ph ON ph.idpadre = fac.iddocumento
      JOIN documentos hijo ON ph.idhijo = hijo.iddocumento AND hijo.idtipodoc in (TIPOANULACION,TIPOKARDEX)
       WHERE
      -- fac.idtipodoc =5
       --  AND
         fac.iddocumento = IDFACTURA
    INTO
    @nfactura,
    @anulEstado,
    @tipo,
    @anulacion,
    @kardex,
    @esContado
     ;

    SELECT
        rec.iddocumento,
        COUNT(iddocumento) as nrecibo
    FROM documentos rec
    JOIN  docpadrehijos ph ON ph.idhijo = rec.iddocumento
    AND rec.idtipodoc=TIPORECIBO
    AND ph.idpadre =IDFACTURA
    INTO
    @recibo,
    @nrec
    ;


  IF @tipo <> TIPOFACTURA OR (@anulEstado <> PENDIENTEANULAR) OR (@esContado = 0 AND (@nrec > 0)) THEN

      SELECT FALSE;

  ELSE

-- OBTENGO EL ID DEL RECIBO EN CASO DE QUE LA FACTURA FUERA AL CONTADO O HALLA SIDO PAGADA POR UN RECIBO


-- INSERTO LA RELACION DE LA ANULACION CON LA PERSONA QUE LA AUTORIZA
    INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,@anulacion,ACCIONAUTORIZAR);

-- REVIERTO LAS CUENTAS CONTABLES DE LA FACTURA, RELACIONANDOLAS CON LA ANULACION
    INSERT INTO cuentasxdocumento
      SELECT
         @anulacion,
         cxd.idcuenta,
         SUM(-cxd.monto) AS monto,
         nlinea
         FROM documentos doc
         JOIN cuentasxdocumento cxd ON  cxd.iddocumento = doc.iddocumento AND cxd.iddocumento IN (IDFACTURA,@recibo)
         GROUP BY cxd.idcuenta
         HAVING SUM(-cxd.monto)<>0
         ;

    IF @kardex = 0 THEN

        INSERT INTO articulosxdocumento(iddocumento,idarticulo,unidades,costocompra,costounit,precioventa,nlinea)
        SELECT @anulacion,idarticulo,-unidades,costocompra,costounit,precioventa,nlinea
        FROM articulosxdocumento
        WHERE iddocumento = IDFACTURA;

    END IF;

    -- VERIFICO SI HAY RECIBO
    IF @recibo is not null then

-- INSERTO LA RELACION ENTRE EL RECIBO Y  LA ANULACION, LA ANULACION ES EL HIJO.
      INSERT INTO docpadrehijos(idpadre,idhijo) VALUES
      (@recibo,@anulacion)
       ;

-- ACTUALIZO EL ESTADO DEL RECIBO A ANULADO
      UPDATE documentos SET idestado = ANULADO where iddocumento = @recibo LIMIT 1;
   END IF;

-- ACTUALIZO EL ESTADO DE LA FACTURA A ANULADO
      UPDATE documentos SET idestado = ANULADO where iddocumento = IDFACTURA LIMIT 1;

-- ACTUALIZO EL ESTADO DE LA ANULACION Y LO PASO A CONFIRMADO, Y LE PONGO EL NUMERO DE LA FACTURA EN NDOCIMPRESO
    UPDATE documentos SET idestado = CONFIRMADO, ndocimpreso =@nfactura WHERE iddocumento = @anulacion LIMIT 1;


    COMMIT;
    SELECT TRUE;
   END IF;
END $$

DELIMITER ;