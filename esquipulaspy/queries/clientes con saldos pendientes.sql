SELECT
p.idpersona,
p.nombre,
sum(s.saldo) as SaldoTotal
FROM personas p
JOIN
(SELECT
padre.iddocumento,
CAST(padre.ndocimpreso AS SIGNED) AS ndocimpreso,
padre.total -sum(if(ph.monto is null,0,ph.monto))- SUM(IF(hijo.idtipodoc=10,hijo.total,0 )) AS Saldo ,
padre.idpersona
FROM documentos padre
left JOIN docpadrehijos ph ON ph.idpadre=padre.iddocumento
left JOIN documentos hijo ON ph.idhijo=hijo.iddocumento
where padre.idtipodoc=5 and (hijo.idtipodoc=18 OR hijo.idtipodoc=10 )and padre.anulado=0
group by padre.iddocumento
) s ON s.idpersona=p.idpersona
WHERE s.saldo>0
group by p.idpersona
ORDER BY p.nombre
;