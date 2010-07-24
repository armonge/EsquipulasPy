SELECT
a.idarticulo,-a.unidades,
@a:=(
SELECT
if(ad.idarticulo=a.idarticulo,sum(unidades),0)
FROM
articuloxdocumento ad
join docpadrehijos ph on ad.iddocumento=ph.idhijo

where ph.idpadre=a.iddocumento and idarticulo=a.idarticulo
) as 'Unidades Devueltas',
-cast(a.unidades+@a as signed) as Total
FROM articuloxdocumento a where iddocumento=78;


SELECT a.idarticulo,-sum(a.unidades) FROM articuloxdocumento a left join docpadrehijos ph on a.iddocumento=ph.idhijo where a.iddocumento=78 or ph.idpadre=78 group by a.idarticulo;



FACTURA QUE SE PUEDEN DEVOLVER
SELECT a.iddocumento, sum(-cast(
a.unidades+
(SELECT if(ad.idarticulo=a.idarticulo,sum(unidades),0) FROM articuloxdocumento ad join docpadrehijos ph on ad.iddocumento=ph.idhijo where ph.idpadre=a.iddocumento and idarticulo=a.idarticulo) as signed)
) as Total
FROM articuloxdocumento a join documento d on a.iddocumento=d.iddocumento where d.idtipodoc in (5,6)  group by a.iddocumento;