SELECT
b.idbodega as Id,
nombrebodega as Bodega
,SUM(a.unidades) as Existencia
,idarticulo
FROM articuloxdocumento a
JOIN bodegas b ON a.idbodega=b.idbodega
GROUP BY a.idbodega,idarticulo