DELIMITER $$

DROP PROCEDURE IF EXISTS `esquipulasdb`.`spCierreMensual`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spCierreMensual`(IN IDCIERRE INTEGER,
							      IN MES INTEGER, 
    							  IN ESTADO INTEGER, 
							      IN ANO INTEGER,
							      IN INGRESOSXVENTA INTEGER,
							      IN OTROSINGRESOS INTEGER,
							      IN COSTOSGASTOSOPERACIONES INTEGER,
							      IN GASTOSXVENTAS INTEGER,
							      IN GASTOS INTEGER,
							      IN GASTOSFINANCIEROS INTEGER,
							      IN PRODUCTOSFINANCIEROS INTEGER,
					              IN OTROSGASTOS INTEGER)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      SELECT False;
  END;

START TRANSACTION;

SET @concierre := (SELECT d.iddocumento FROM documentos d WHERE d.idtipodoc=IDCIERRE AND MONTH(fechacreacion)=MES AND YEAR(d.fechacreacion)=ANO);
	IF @concierre is null THEN
		SELECT fnconsecutivo(IDCIERRE,NULL) INTO @NUMERO;
		INSERT INTO documentos (NDOCIMPRESO,TOTAL,IDTIPODOC,IDESTADO,FECHACREACION)VALUES(@NUMERO,0,IDCIERRE,ESTADO,now());
		SET @NDOCCIERRE := LAST_INSERT_ID();
-- Inserta los movimientos con saldo invertido para convertir el saldo de las cuentas
-- a CERO y estas a su vez son asignadas al documento cierre que se crea en este procedimiento		
		
		INSERT into cuentasxdocumento

		SELECT

			@NDOCCIERRE,
                	cc.idcuenta,
                	SUM(IFNULL(monto*-1,0)) monto
			,null

        FROM cuentascontables cc
		JOIN cuentascontables ccc ON ccc.codigo LIKE CONCAT(SUBSTR(cc.codigo,1,5),'%')
        LEFT JOIN cuentasxdocumento cxd ON ccc.idcuenta = cxd.idcuenta
		JOIN documentos d on d.iddocumento=cxd.iddocumento
	    wHERE cc.idcuenta IN (INGRESOSXVENTA,
	    			  OTROSINGRESOS,
	    			  COSTOSGASTOSOPERACIONES,
	    			  GASTOSXVENTAS,
	    			  GASTOS,
	    			  GASTOSFINANCIEROS,
	    			  PRODUCTOSFINANCIEROS,
	    			  OTROSGASTOS) 
	    AND MONTH(d.fechacreacion)=MES AND YEAR(d.fechacreacion)=ANO	
        GROUP BY cc.idcuenta
        HAVING monto!=0;
	COMMIT;
    	SELECT TRUE;
	
	ELSE
		ROLLBACK;
		SELECT FALSE;	
	END IF;

END$$

DELIMITER ;
