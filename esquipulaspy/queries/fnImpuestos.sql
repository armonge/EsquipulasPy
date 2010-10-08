DELIMITER $$
DROP FUNCTION IF EXISTS `esquipulasdb`.`fnImpuestos` $$
CREATE FUNCTION `esquipulasdb`.`fnImpuestos` (IDLIQ INT,CIFTOTAL DECIMAL(12,4),CIFPARCIAL DECIMAL(12,4),DAI DECIMAL(12,4),ISC DECIMAL(12,4)) RETURNS DECIMAL(12,4)
NOT DETERMINISTIC
READS SQL DATA
BEGIN


      DECLARE imp DECIMAL(12,4);
      SET @imp = 0;

      SELECT
          SUM(IF(c.idtipocosto = 1,c.valorcosto/100,0)) as iva,
          SUM(IF(c.idtipocosto = 4,c.valorcosto,0)) as spe,
          SUM(IF(c.idtipocosto = 6,c.valorcosto/100,0)) as iso,
          SUM(IF(c.idtipocosto = 5,c.valorcosto,0)) as tsim,
          SUM(IF(c.idtipocosto = 5,t.factorpeso,0)) as factorpeso,
          l.peso
      FROM costosagregados c
      LEFT JOIN tsim t ON t.idtsim = c.idcostoagregado
      JOIN costosxdocumento cx ON cx.idcostoagregado=c.idcostoagregado
      JOIN liquidaciones l ON l.iddocumento = cx.iddocumento
      WHERE l.iddocumento = IDLIQ
      INTO @iva,@spe,@iso,@tsim,@factorpeso,@peso
      ;

      SET @factorcif = (CIFPARCIAL/CIFTOTAL);
-- RETURN @factorcif;
      SET @tsim = IFNULL((CEIL(@peso/@factorpeso) * @tsim * @factorcif) ,0) ;
-- RETURN @tsim;
-- RETURN CEIL(@peso/@factorpeso);
--  RETURN @tsim;
      SET @spe = IFNULL(@spe * @factorcif,0);
      SET @iso = IFNULL(@iso * CIFPARCIAL,0);
--       RETURN @;
      SET @iva = IFNULL((CIFPARCIAL + DAI + ISC + @tsim) * @iva,0);
      SET @imp =  IFNULL(@iva +  @spe + @tsim + @iso +  DAI + ISC,0) ;

      RETURN ROUND(@imp,4);

END $$

DELIMITER ;