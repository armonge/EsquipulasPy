SELECT fnImpuestos(15,18000,9000,1350,1035) as impuestototal;

SELECT * FROM liquidaciones l
JOIN articulosxdocumento ad ON ad.iddocumento = l.iddocumento
JOIN costosxarticuloliquidacion ca ON ca.idarticuloxdocumento = ad.idarticuloxdocumento
;
      SELECT
          SUM(IF(c.idtipocosto = 1,c.valorcosto/100,0)) as iva,
          SUM(IF(c.idtipocosto = 4,c.valorcosto,0)) as spe,
          SUM(IF(c.idtipocosto = 6,c.valorcosto/100,0)) as iso,
          SUM(IF(c.idtipocosto = 5,c.valorcosto,0)) as tsim,
          SUM(IF(c.idtipocosto = 5,t.factorpeso,0)) as factorpeso,
          l.peso
      FROM costosagregados c
      LEFT JOIN tsim t ON t.idtsim = c.idcostoagregado
      JOIN costosxdocumento cx ON cx.idcostoagregado=c.idcostoagregado
      JOIN liquidaciones l ON l.iddocumento = cx.iddocumento
      WHERE l.iddocumento = 14