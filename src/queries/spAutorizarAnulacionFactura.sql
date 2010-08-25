DELIMITER $$

DROP PROCEDURE IF EXISTS `spAutorizarAnulacionFactura` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAutorizarAnulacionFactura`(
IDANULACION INT,
IDGERENTE INT,
TIPOPERSONA INT,
IDCONCEPTO INT
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

-- OBTENGO EL CONSECUTIVO DE LA ANULACION, Y EL ID DE LA FACTURA QUE FUE ANULADA
    SELECT
    fnConsecutivo(2,null),
    d.iddocumento
    from docpadrehijos ph
    JOIN documentos d ON ph.idpadre = d.iddocumento AND d.idtipodoc = 5
    WHERE ph.idhijo = IDANULACION
    INTO
    @numero,
    @factura
     ;

-- OBTENGO EL ID DEL RECIBO EN CASO DE QUE LA FACTURA FUERA AL CONTADO O HALLA SIDO PAGADA POR UN RECIBO
    SELECT
        rec.iddocumento,
        rec.total,
        rec.idtipocambio
    from docpadrehijos ph
    JOIN documentos fac ON ph.idpadre = @factura
    JOIN documentos rec ON ph.idhijo = rec.iddocumento  AND rec.idtipodoc=18
    WHERE fac.iddocumento = @factura
    AND (fac.total = ph.monto OR fac.escontado=0)
    INTO
    @recibo,
    @totalrecibo,
    @tcrecibo
    ;

-- ACTUALIZO EL ESTADO DE LA ANULACION Y LO PASO A CONFIRMADO
    UPDATE documentos SET idestado = 1, ndocimpreso = @numero where iddocumento = IDANULACION;

-- INSERTO LA RELACION DE LA ANULACION CON LA PERSONA QUE LA AUTORIZA
    INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDANULACION,TIPOPERSONA);

-- REVIERTO LAS CUENTAS CONTABLES DE LA FACTURA, RELACIONANDOLAS CON LA ANULACION
    INSERT INTO cuentasxdocumento
      SELECT IDANULACION,cxd.idcuenta,-cxd.monto,nlinea from documentos fac
       JOIN cuentasxdocumento cxd ON cxd.iddocumento = @factura
       where fac.iddocumento = @factura;

-- VERIFICO SI HAY RECIBO
    IF @recibo is not null then

-- SI HAY RECIBO CREO UN DOCUMENTO NOTA DE CREDITO QUE REVERTIRA LAS CUENTAS DEL RECIBO
-- YA QUE SE LE TUVO QUE DEVOLVER EL DINERO AL CLIENTE.
      INSERT INTO documentos (ndocimpreso,total,fechacreacion,idtipocambio,idconcepto,idestado,idtipodoc) VALUES
                            (fnConsecutivo(14,null),@totalrecibo,NOW(),@tcrecibo,IDCONCEPTO,1,14);


   -- OBTENGO EL ID DE LA NOTA DE CREDITO CREADA
      SET @NC = LAST_INSERT_ID();

-- INSERTO LA RELACION ENTRE LAS NOTAS DE CREDITO Y EL RECIBO, CON LA ANULACION, LA ANULACION ES EL PADRE.
      INSERT INTO docpadrehijos(idpadre,idhijo) VALUES
      (IDANULACION,@NC),
      (IDANULACION,@recibo)
       ;

-- ACTUALIZO EL ESTADO DEL RECIBO A ANULADO
      UPDATE documentos SET idestado = 2 where iddocumento = @recibo;

-- REVIERTO LAS CUENTAS CONTABLES DEL RECIBO RELACIONANDOLAS A LA NOTA DE CREDITO.
      INSERT INTO cuentasxdocumento
      SELECT @NC ,cxd.idcuenta,-cxd.monto,cxd.nlinea from cuentasxdocumento cxd
      WHERE cxd.iddocumento = @recibo
      ;
    END IF;

    COMMIT;

     SELECT TRUE;
END $$

DELIMITER ;