USE `esquipulasdb`;

CREATE  OR REPLACE VIEW `esquipulasdb`.`vw_articulosenbodegas` AS

SELECT 
axd.idarticulo,
a.descripcion,
c.valor*(1+a.ganancia/100) as precio,
c.valor as costodolar,
c.valor * tc.tasa as costo,
SUM(IF((axd.unidades > 0 AND kardex.iddocumento IS NULL) AND d.idtipodoc<>27 ,0,axd.unidades)) as existencia,
d.idbodega
FROM `esquipulasdb`.`articulosxdocumento` axd
JOIN vw_articulosdescritos a ON a.idarticulo=axd.idarticulo
JOIN costosarticulo c ON a.idarticulo=c.idarticulo AND c.activo=1
JOIN tiposcambio tc ON tc.idtc= c.idtc
JOIN documentos d ON d.iddocumento = axd.iddocumento
LEFT JOIN docpadrehijos ph ON ph.idpadre = axd.iddocumento
LEFT JOIN documentos kardex ON ph.idhijo = kardex.iddocumento AND kardex.idtipodoc=27
GROUP BY axd.idarticulo,d.idbodega
;