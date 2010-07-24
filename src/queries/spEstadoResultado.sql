DELIMITER $$

DROP PROCEDURE IF EXISTS `spEstadoResultado` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spEstadoResultado`(IN FECHA DATE)
BEGIN

    SELECT LAST_DAY(FECHA)+ INTERVAL 1 DAY INTO @fecha;

--    SET @CONT:=0;

    SET @temptotal:=0;

    DROP TEMPORARY TABLE IF EXISTS temp;

    CREATE TEMPORARY TABLE temp
SELECT
          cc.codigo,
          cc.descripcion,
          SUM(IFNULL(cd.monto,0)) as saldo,

          @temptotal:=@temptotal+ IFNULL(cd.monto,0) as total,
          cc.esdebe,
          cc.padre,
          cc.idcuenta,
          IF(
          cc.idcuenta = 173,
          1
          ,2) as orden
FROM cuentascontables cc
LEFT JOIN cuentasxdocumento cd ON cc.idcuenta = cd.idcuenta
LEFT JOIN documentos d ON d.iddocumento = cd.iddocumento
-- WHERE d.fechacreacion<(LAST_DAY(now())+ INTERVAL 1 DAY)
-- AND
WHERE
cc.idcuenta IN (173,182)
GROUP BY cc.idcuenta
;


 INSERT INTO temp VALUES('','UTILIDAD BRUTA',@temptotal,@temptotal,1,null,0,3);


 SET @total2:=0;
 INSERT INTO temp
SELECT
          cc.codigo,
          cc.descripcion,
          SUM(IFNULL(cd.monto,0)) as saldo,
          @total2:=@total2+ SUM(IFNULL(cd.monto,0)) as total,
          cc.esdebe,
          cc.padre,
          cc.idcuenta,
          IF(
          cc.idcuenta = 180,
          4
          ,IF(
          cc.idcuenta = 248,
          5
          ,IF(
          cc.idcuenta = 184,
          6
          ,IF(
          cc.idcuenta = 314,
          7
          ,IF(
          cc.idcuenta = 327,
          8
          ,IF(
          cc.idcuenta = 323,
          9
          ,0
          )))))) as orden
FROM cuentascontables cc
LEFT JOIN cuentasxdocumento cd ON cc.idcuenta = cd.idcuenta
LEFT JOIN documentos d ON d.iddocumento = cd.iddocumento
-- WHERE d.fechacreacion<(LAST_DAY(now())+ INTERVAL 1 DAY)
-- AND
WHERE
cc.idcuenta IN (180,248,184,314,327,323)
GROUP BY cc.idcuenta
;

INSERT INTO temp VALUES('','TOTAL GASTOS',@total2,@total2,1,null,0,10);
INSERT INTO temp VALUES('','UTILIDAD NETA',@temptotal+@total2,@temptotal+@total2,1,null,0,11);

SELECT
         codigo,
         descripcion,
         IF(idcuenta=0,'',saldo) as saldo,
         IF(idcuenta=0,total,'') as total,
         esdebe,
         padre,
         idcuenta
-- ,          cont
 from temp
 ORDER BY orden
 ;
   DROP TEMPORARY TABLE temp;

END $$

DELIMITER ;