DELIMITER $$

DROP PROCEDURE IF EXISTS `esquipulasdb`.`spEliminarFactura`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spEliminarFactura`(IN iddoc INT)
BEGIN
       START TRANSACTION;

            DELETE FROM personasxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM costosxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM articulosxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM docpadrehijos WHERE idhijo=iddoc;
	    DELETE FROM creditos WHERE iddocumento=iddoc;
            DELETE FROM documentos WHERE iddocumento=iddoc;
		
       COMMIT;

END$$

DELIMITER ;
