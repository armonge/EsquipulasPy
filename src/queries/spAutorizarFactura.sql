DELIMITER $$

DROP PROCEDURE IF EXISTS `spAutorizarFactura` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAutorizarFactura`(
IDFACTURA INT,
IDGERENTE INT,
ACCIONAUTORIZAR INT,
CONFIRMADO INT,
VENTASNETAS INT,
CXCCLIENTE INT,
INVENTARIO INT,
COSTOSVENTAS INT,
IMPUESTOSXPAGAR INT
)
BEGIN

-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      SELECT False;
  END;

      START TRANSACTION;
      -- OBTENGO EL ESTADO ACTUAL DEL DOCUMENTO
          SELECT idestado FROM documentos WHERE iddocumento = IDFACTURA INTO @estado;

     -- VERIFICO QUE NO ESTE CONFIRMADO.
     IF @estado = CONFIRMADO THEN

        SELECT FALSE;

      ELSE








     -- OBTENGO EL CONSECUTIVO, EL TOTAL , EL SUBTOTAL, EL IVA, Y EL TOTAL COSTO

        SELECT

            fnconsecutivo(idtipodoc,NULL),

            total * tc.tasa as total,

            ROUND((total/(1 + (IFNULL(ca.valorcosto,0)/100)))*tc.tasa,4) as subtotal,

            ROUND((

            total - (total/(1 + (IFNULL(ca.valorcosto,0)/100)))

            )*tc.tasa,4) as totaliva,

            ROUND(SUM(-ad.unidades * ad.costounit),4) as totalcosto
        FROM documentos d
        JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
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
        UPDATE documentos SET idestado=CONFIRMADO,ndocimpreso = @numero WHERE iddocumento = IDFACTURA;

        -- INSERTO LA RELACION DE LA FACTURA CON LA PERSONA QUE LA AUTORIZA
        INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDFACTURA,ACCIONAUTORIZAR);

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

    COMMIT;
    SELECT TRUE;
   END IF;

END $$

DELIMITER ;