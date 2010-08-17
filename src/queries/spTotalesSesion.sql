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
--      p.monto,
 SUM(IFNULL(p.monto,d.total)) as Total
  FROM documentos d
  JOIN pagos p ON d.iddocumento = p.recibo
  JOIN tipospago tp ON p.tipopago = tp.idtipopago
  JOIN tiposmoneda tm ON p.tipomoneda = tm.idtipomoneda
  LEFT JOIN docpadrehijos ph ON ph.idhijo = d.iddocumento
  WHERE (d.iddocumento = IDSESION OR ph.idpadre= IDSESION)
  GROUP BY p.tipomoneda,p.tipopago
  ;

END $$

DELIMITER ;