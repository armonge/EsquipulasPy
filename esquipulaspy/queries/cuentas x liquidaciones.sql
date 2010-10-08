SELECT 
	cc.codigo as Cuenta,
	cc.Descripcion,
	FORMAT(dxc.monto,4) as 'Monto C$',
	d.iddocumento 
FROM documentoxcuenta dxc
JOIN cuentacontable cc ON dxc.idcuenta=cc.idcuenta
JOIN documento d ON d.iddocumento = dxc.iddocumento
JOIN liquidacion l ON l.iddocumento = d.iddocumento
ORDER BY dxc.nlinea;