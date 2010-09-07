-- Trigger DDL Statements
DELIMITER $$

USE `esquipulasdb`$$

DROP TRIGGER IF EXISTS `esquipulasdb`.`tr_promediarcosto` $$

CREATE
DEFINER=`root`@`localhost`
TRIGGER `esquipulasdb`.`tr_promediarcosto`
AFTER INSERT ON `esquipulasdb`.`articulosxdocumento`
FOR EACH ROW
BEGIN



      DECLARE costo DECIMAL(12,4);

      DECLARE idtc  INTEGER;

	  DECLARE tasa DECIMAL(12,4);



      IF (select IF(idtipodoc in (21,7),1,0) from documentos where iddocumento = NEW.iddocumento) = 1 AND NEW.unidades>0 THEN



		SELECT idtipocambio,tc.tasa FROM documentos d

    JOIN tiposcambio tc ON tc.idtc=d.idtipocambio

    WHERE iddocumento = NEW.iddocumento INTO @idtc, @tasa;

      IF @tasa IS NULL THEN
          SET NEW='La tasa del tipo de cambio para calcular el costo promedio no puede ser null';
      END IF;

        SELECT SUM((unidades*costounit * @tasa))/SUM(unidades)  FROM articulosxdocumento a WHERE a.idarticulo= NEW.idarticulo INTO @costo;

        IF @costo IS NULL THEN
          SET @costo=NEW.costounit;
        ELSE
          SET @costo=@costo/@tasa;
       END IF;

        UPDATE costosarticulo SET activo=0 WHERE idarticulo=NEW.idarticulo AND activo=1;

        INSERT INTO costosarticulo (valor,idarticulo,idtc) VALUES (@costo,NEW.idarticulo,@idtc);

      END IF;

END$$

