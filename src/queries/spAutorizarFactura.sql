DELIMITER $$

DROP PROCEDURE IF EXISTS `esquipulasdb`.`spAutorizarFactura` $$
CREATE PROCEDURE `esquipulasdb`.`spAutorizarFactura` (IDFACTURA INT,IDGERENTE INT,VENTASNETAS INT,CXCCLIENTE INT, INVENTARIO INT,COSTOSVENTAS INT,IMPUESTOSXPAGAR INT)
BEGIN

      START TRANSACTION;
      -- OBTENGO EL ESTADO ACTUAL DEL DOCUMENTO
          SELECT idestado FROM documentos WHERE iddocumento = IDFACTURA INTO @estado;

     -- VERIFICO QUE NO ESTE CONFIRMADO.
     IF @estado <>1 THEN


     -- OBTENGO EL CONSECUTIVO, EL TOTAL , EL SUBTOTAL, EL IVA, Y EL TOTAL COSTO
        SELECT
            fnconsecutivo(idtipodoc,NULL),
            total,
            ROUND(total/(1 + IFNULL(ca.valorcosto,0)/100),4),
            total-ROUND(total/(1 + IFNULL(ca.valorcosto,0)/100),4),
            SUM(-ad.unidades * ad.costounit)
        FROM
        documentos d
        JOIN costosxdocumento cd ON cd.iddocumento = IDFACTURA
        JOIN articulosxdocumento ad ON ad.iddocumento = IDFACTURA
        LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado
        WHERE d.iddocumento = IDFACTURA
        INTO
        @numero,
        @total,
        @subtotal,
        @iva,
        @costo
         ;

        -- LE PASO EL ESTADO A CONFIRMAOD Y LE PONGO EL CONSECUTIVO QUE LE CORRESPONDE
        UPDATE documentos SET idestado=1,ndocimpreso = @numero WHERE iddocumento = IDFACTURA;

        -- INSERTO LA RELACION DE LA FACTURA CON LA PERSONA QUE LA AUTORIZA
        INSERT INTO personasxdocumento(idpersona, iddocumento,autoriza) VALUES (IDGERENTE,IDFACTURA,1);

        -- INSERTO LA RELACION DE LAS CUENTAS CONTABLES CON LA FACTURA
        INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto) VALUES
        (IDFACTURA,VENTASNETAS,-@subtotal),
        (IDFACTURA,CXCCLIENTE,@total),
        (IDFACTURA,INVENTARIO,-@costo),
        (IDFACTURA,COSTOSVENTAS,@costo)
        ;

        -- SOLO SI TIENE IVA INSERTO EL REGISTRO
        IF @iva >0 then
                INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto) VALUES
                (IDFACTURA,IMPUESTOSXPAGAR,-@iva);
        END IF;

     END IF;

      COMMIT;


END $$

DELIMITER ;