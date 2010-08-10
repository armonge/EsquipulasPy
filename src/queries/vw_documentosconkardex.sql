SELECT 
d.iddocumento as id,
kardex.iddocumento as kardex,
d.idbodega
FROM `esquipulasdb`.`documentos` d
LEFT JOIN docpadrehijos ph ON ph.idpadre=d.iddocumento
LEFT JOIN documentos kardex ON kardex.idtipodoc=27 AND kardex.iddocumento=ph.idhijo
GROUP BY d.iddocumento