USE `esquipulasdb`;

CREATE  OR REPLACE VIEW `esquipulasdb`.`vw_articulosenbodegas` AS
Select 
axd.idarticulo,
a.descripcion,
c.valor*(1+a.ganancia/100) as precio,
c.valor as costodolar,
c.valor * tc.tasa as costo,
SUM(IF(axd.unidades>0 AND doc.kardex IS NULL,0,axd.unidades)) as existencia,
b.idbodega
FROM articulosxdocumento axd
JOIN vw_articulosdescritos a ON a.idarticulo=axd.idarticulo
JOIN costosarticulo c ON a.idarticulo=c.idarticulo
JOIN tiposcambio tc ON tc.idtc= c.idtc
JOIN vw_documentosconkardex doc ON doc.id = axd.iddocumento
JOIN bodegas b ON b.idbodega=doc.idbodega
GROUP BY axd.idarticulo,b.idbodega
;