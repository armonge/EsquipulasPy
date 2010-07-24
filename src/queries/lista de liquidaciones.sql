SELECT d.iddocumento, d.ndocimpreso, d.fechacreacion, l.procedencia, d.total
FROM documento d
JOIN liquidacion l ON l.iddocumento = d.iddocumento
