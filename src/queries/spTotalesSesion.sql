DELIMITER $$

DROP PROCEDURE IF EXISTS `esquipulasdb`.`spTotalesSesion` $$
CREATE PROCEDURE `esquipulasdb`.`spTotalesSesion` (IN IDSESION INT)
BEGIN

  SELECT
      p.tipopago,
      tp.descripcion,
      p.tipomoneda,
      tm.moneda,
      tm.simbolo,
  SUM(IFNULL(p.monto,d.total)) as Total
  FROM documentos d
  LEFT JOIN pagos p ON d.iddocumento = p.recibo
  LEFT JOIN tipospago tp ON p.tipopago = tp.idtipopago
  LEFT JOIN tiposmoneda tm ON p.tipomoneda = tm.idtipomoneda
  LEFT JOIN docpadrehijos ph ON ph.idhijo = d.iddocumento
  WHERE (d.idcaja IS NOT NULL) AND (d.idtipodoc NOT IN (5,23))
  AND (d.iddocumento = IDSESION OR ph.idpadre= IDSESION)
  GROUP BY IFNULL(p.tipomoneda,2),p.tipopago
  ;

END $$

DELIMITER ;