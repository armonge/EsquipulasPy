CREATE VIEW vw_liquidacionesguardadas
AS
SELECT
l.iddocumento AS iddocumento,
d.ndocimpreso AS ndocimpreso,
l.procedencia AS procedencia,
l.totalagencia AS totalagencia,
l.totalalmacen AS totalalmacen,
l.porcentajepapeleria AS porcentajepapeleria,
l.porcentajetransporte AS porcentajetransporte,
l.peso AS peso,
l.fletetotal AS fletetotal,
l.segurototal AS segurototal,
l.otrosgastos AS otrosgastos,
d.idtipocambio AS tipocambio,
tc.fecha AS fecha,
tc.tasa AS tasa,
p.idpersona AS idpersona,
p.nombre AS Proveedor,
d.anulado AS anulado
FROM
liquidaciones l
JOIN documentos d ON  l.iddocumento = d.iddocumento
JOIN tiposcambio tc ON d.idtipocambio = tc.idtc
JOIN personasxdocumento pd ON pd.iddocumento = d.iddocumento
JOIN personas p ON pd.idpersona = p.idpersona;