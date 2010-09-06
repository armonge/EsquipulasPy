CREATE DEFINER=`root`@`localhost` PROCEDURE `spDenegar`(IN IDDOC INTEGER, IN ESTADO INTEGER,IN ANULACION INTEGER)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      SELECT False;
  END;

START TRANSACTION;

SET @anulacion := (SELECT d.iddocumento FROM documentos d join docpadrehijos dh on d.iddocumento=dh.idhijo where dh.idpadre=IDDOC and d.idtipodoc=ANULACION);
	IF @anulacion>0 THEN
	
	UPDATE documentos d SET idestado=ESTADO where iddocumento=IDDOC LIMIT 1;
	delete from docpadrehijos where idhijo=@anulacion;
	delete from personasxdocumento where iddocumento=@anulacion;
	delete from documentos where iddocumento=@anulacion;

	ELSE

	SELECT FALSE;

  	END IF;
COMMIT;

END