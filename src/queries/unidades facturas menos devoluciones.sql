select v.idarticulo,v.descripcion,sum(unidades) as existencia
from articulosxdocumento facs
join vw_articulosdescritos v on facs.idarticulo=v.idarticulo
Left join docpadrehijos devs on devs.idhijo=facs.iddocumento
where facs.iddocumento=273 or devs.idpadre=273
group by v.idarticulo;
;