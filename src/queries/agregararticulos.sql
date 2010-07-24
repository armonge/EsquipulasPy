DELIMITER $$

DROP PROCEDURE IF EXISTS `agregararticulos` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `agregararticulos`(IN proveedor INTEGER,IN ivaincluido TINYINT,IN descuento TINYINT,IN activo TINYINT,IN marca INTEGER, IN subcategoria INTEGER, IN dai INTEGER, IN isc INTEGER, IN iva INTEGER)
BEGIN
DECLARE EXIT HANDLER FOR SQLSTATE '23000'
       START TRANSACTION;
--          SET @flag='0'
--            DECLARE CONTINUE HANDLER FOR SQLSTATE '23000' SET @flag = '1';

            INSERT INTO articulos (idproveedor,ivaincluido,admitedescuento,activo,idmarca,idcategoria) VALUES (proveedor,ivaincluido,descuento,activo,marca,subcategoria);
            SET @ultimoarticulo := LAST_INSERT_ID();
            INSERT INTO costoagregado (valorcosto,activo,idtipocosto) VALUES(dai,1,3);
            SET @costo1 := LAST_INSERT_ID();
            INSERT INTO costoagregado (valorcosto,activo,idtipocosto) VALUES(iva,1,1);
            SET @costo2 := LAST_INSERT_ID();
            INSERT INTO costoagregado (valorcosto,activo,idtipocosto) VALUES(isc,1,2);
            SET @costo3 := LAST_INSERT_ID();

            INSERT INTO costoagregadoarticulo (idcostoagregado,idarticulo) values(@costo1,@ultimoarticulo);
            INSERT INTO costoagregadoarticulo (idcostoagregado,idarticulo) values(@costo2,@ultimoarticulo);
            INSERT INTO costoagregadoarticulo (idcostoagregado,idarticulo) values(@costo3,@ultimoarticulo);
       COMMIT;

--    IF @flag=0 then
  --     COMMIT;
   -- ELSE
    --   ROLLBACK;
   -- END IF;
END $$

DELIMITER ;