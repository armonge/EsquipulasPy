-- Trigger DDL Statements
USE `esquipulasdb`;
DELIMITER //

CREATE
DEFINER=`root`@`localhost`
TRIGGER `esquipulasdb`.`tr_checkndoc`
BEFORE INSERT ON `esquipulasdb`.`documentos`
FOR EACH ROW
BEGIN

  DECLARE id int;

  IF NEW.idtipodoc IN (5,6) THEN
    SELECT iddocumento FROM documentos where (ndocimpreso=NEW.ndocimpreso AND (idtipodoc=5 or idtipodoc=6)) LIMIT 1    into id;
  ELSE
    SELECT iddocumento FROM documentos where ndocimpreso=NEW.ndocimpreso AND idtipodoc=NEW.idtipodoc LIMIT 1    into id;
  END IF;

  IF id IS NOT NULL THEN
    SET  NEW=NULL;
     
  END IF;


END//