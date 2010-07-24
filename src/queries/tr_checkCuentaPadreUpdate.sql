-- Trigger DDL Statements
USE `esquipulasdb`;
DROP TRIGGER IF EXISTS `esquipulasdb`.`tr_checkCuentaPadreUpdate`;
DELIMITER //

CREATE TRIGGER `esquipulasdb`.`tr_checkCuentaPadreUpdate`
BEFORE INSERT ON `esquipulasdb`.`cuentascontables`
FOR EACH ROW
BEGIN

  IF NEW.padre IS NOT NULL THEN
        SET @codHijo:=REPLACE(NEW.codigo,' 000','');
        SELECT LEFT(@codHijo,CHAR_LENGTH(@codHijo)-4) INTO @codHijo;

        SELECT REPLACE(codigo,' 000','')
        FROM cuentascontables cc
        where cc.idcuenta = NEW.padre
        into @cod;


    IF @cod NOT LIKE @codHijo THEN
      SET NEW = NULL;
    END IF;

  END IF;

END//