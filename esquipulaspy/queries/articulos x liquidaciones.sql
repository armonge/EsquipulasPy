SELECT 
	v.idarticulo,
	v.descripcion,
	v.dai,
	v.isc,
	v.comision,
	a.unidades,
	a.costocompra as punit,
	a.unidades*a.costocompra as fob,
	v.comision*a.unidades as comision, 
	a.idbodega,
	b.nombrebodega,
	d.iddocumento
FROM vw_articulosconcostosactuales v 
JOIN articuloxdocumento a ON v.idarticulo=a.idarticulo 
JOIN bodegas b ON b.idbodega=a.idbodega 
JOIN documento d ON a.iddocumento = d.iddocumento
JOIN liquidacion l ON d.iddocumento = l.iddocumento
ORDER BY a.nlinea