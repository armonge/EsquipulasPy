-- Trigger DDL Statements
USE `esquipulasdb`;
DROP TRIGGER IF EXISTS `esquipulasdb`.`tr_checkNivelCuenta`;
DELIMITER //

CREATE TRIGGER `esquipulasdb`.`tr_checkNivelCuenta`
BEFORE INSERT ON `esquipulasdb`.`cuentascontables`
FOR EACH ROW
BEGIN

  SELECT padre.padre
  FROM cuentascontables hijo
  JOIN cuentascontables padre ON hijo.padre=padre.idcuenta
  where hijo.idcuenta = NEW.idcuenta
  into @padre;

    IF @padre=1 OR (@padre IS NULL) THEN
      SET  NEW=NULL;
    END IF;

END//