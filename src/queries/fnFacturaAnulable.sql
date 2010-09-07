DELIMITER $$

DROP FUNCTION IF EXISTS `fnFacturaAnulable` $$
CREATE DEFINER=`root`@`localhost` FUNCTION `fnFacturaAnulable`(
IDFACTURA INT,
TIPOFACTURA INT,
TIPORECIBO INT,
TIPONC INT,
CONFIRMADO INT,
PENDIENTEAUTORIZACION INT
)
RETURNS tinyint(4)
BEGIN

RETURN (SELECT
IF(fac.idestado in (CONFIRMADO,PENDIENTEAUTORIZACION),
IF(
-- Si la factura es de hoy verificar el estado
DATE(fac.fechacreacion) = DATE(NOW()),

-- si el estado es confirmado o pendiente de credito verificar si es al credito y tiene abonos
IF(
(fac.escontado=1) OR (SUM(IF(hijo.idtipodoc=TIPORECIBO,1,0))=0),

 -- si no tiene abonos o es al contado verificar si tiene devoluciones
IF(
SUM(IF(hijo.idtipodoc=TIPONC,1,0))=0,
-- Si cumple todas las condiciones devolver 1 que significa que se puede anular
1
-- si la factura tiene devoluciones devolver 5
,
5)
-- si la factura es al credito y tiene abono devolver 4
,
4)
,
-- Si la factura no tiene el estado confirmado o pendiente de autorizacion  retornar 3
3)
,
-- Si la factura no es de hoy retorna 2
2) as anulable
FROM documentos fac
LEFT JOIN docpadrehijos ph ON ph.idpadre = fac.iddocumento
LEFT JOIN documentos hijo ON ph.idhijo = hijo.iddocumento AND hijo.idtipodoc in (TIPORECIBO,TIPONC)
where fac.idtipodoc =TIPOFACTURA  and fac.iddocumento = IDFACTURA);

END $$

DELIMITER ;