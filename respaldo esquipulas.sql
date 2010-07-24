-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.1.37


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema esquipulasdb
--

CREATE DATABASE IF NOT EXISTS esquipulasdb;
USE esquipulasdb;

--
-- Temporary table structure for view `vw_articulosconcostosactuales`
--
DROP TABLE IF EXISTS `vw_articulosconcostosactuales`;
DROP VIEW IF EXISTS `vw_articulosconcostosactuales`;
CREATE TABLE `vw_articulosconcostosactuales` (
  `idarticulo` int(10) unsigned,
  `descripcion` varchar(77),
  `dai` decimal(30,2),
  `isc` decimal(30,2),
  `comision` decimal(30,2),
  `ganancia` smallint(5) unsigned,
  `activo` tinyint(1) unsigned
);

--
-- Temporary table structure for view `vw_articulosdescritos`
--
DROP TABLE IF EXISTS `vw_articulosdescritos`;
DROP VIEW IF EXISTS `vw_articulosdescritos`;
CREATE TABLE `vw_articulosdescritos` (
  `idarticulo` int(10) unsigned,
  `descripcion` varchar(77),
  `idcategoria` int(10) unsigned,
  `categorias` varchar(25),
  `idsubcategoria` int(10) unsigned,
  `subcategoria` varchar(25),
  `idmarca` int(10) unsigned,
  `marcas` varchar(25),
  `activo` tinyint(1) unsigned,
  `ganancia` smallint(5) unsigned
);

--
-- Temporary table structure for view `vw_articulosprorrateados`
--
DROP TABLE IF EXISTS `vw_articulosprorrateados`;
DROP VIEW IF EXISTS `vw_articulosprorrateados`;
CREATE TABLE `vw_articulosprorrateados` (
  `idarticulo` int(10) unsigned,
  `unidades` int(11),
  `costocompra` decimal(12,4),
  `fob` decimal(22,4),
  `flete` decimal(42,12),
  `seguro` decimal(42,12),
  `otros gastos` decimal(42,12),
  `cif` decimal(65,12),
  `impuestos` decimal(65,24),
  `comision` decimal(12,4),
  `agencia` decimal(65,20),
  `almacen` decimal(65,20),
  `papeleria` decimal(18,6),
  `transporte` decimal(18,6),
  `iddocumento` int(10) unsigned
);

--
-- Temporary table structure for view `vw_costosdeldocumento`
--
DROP TABLE IF EXISTS `vw_costosdeldocumento`;
DROP VIEW IF EXISTS `vw_costosdeldocumento`;
CREATE TABLE `vw_costosdeldocumento` (
  `idcostoagregado` int(10) unsigned,
  `Descripcion` varchar(45),
  `valorcosto` decimal(8,2),
  `iddocumento` int(10) unsigned,
  `TipoDoc` varchar(45),
  `activo` tinyint(1)
);

--
-- Temporary table structure for view `vw_liquidacioncontotales`
--
DROP TABLE IF EXISTS `vw_liquidacioncontotales`;
DROP VIEW IF EXISTS `vw_liquidacioncontotales`;
CREATE TABLE `vw_liquidacioncontotales` (
  `iddocumento` int(10) unsigned,
  `fobtotal` decimal(44,4),
  `fletetotal` decimal(12,4),
  `segurototal` decimal(12,4),
  `otrosgastostotal` decimal(12,4),
  `ciftotal` decimal(47,4),
  `pesototal` decimal(12,4),
  `agenciatotal` decimal(12,4),
  `almacentotal` decimal(12,4),
  `tasapapeleria` decimal(8,6),
  `tasatransporte` decimal(8,6),
  `procedencia` varchar(45)
);

--
-- Temporary table structure for view `vw_liquidacionesconcostos`
--
DROP TABLE IF EXISTS `vw_liquidacionesconcostos`;
DROP VIEW IF EXISTS `vw_liquidacionesconcostos`;
CREATE TABLE `vw_liquidacionesconcostos` (
  `iddocumento` int(10) unsigned,
  `tsimtotal` decimal(44,2),
  `iva` decimal(34,6),
  `spe` decimal(30,2),
  `iso` decimal(34,6)
);

--
-- Temporary table structure for view `vw_liquidacionescontodo`
--
DROP TABLE IF EXISTS `vw_liquidacionescontodo`;
DROP VIEW IF EXISTS `vw_liquidacionescontodo`;
CREATE TABLE `vw_liquidacionescontodo` (
  `iddocumento` int(10) unsigned,
  `fobtotal` decimal(44,4),
  `fletetotal` decimal(12,4),
  `segurototal` decimal(12,4),
  `otrosgastostotal` decimal(12,4),
  `ciftotal` decimal(47,4),
  `agenciatotal` decimal(12,4),
  `almacentotal` decimal(12,4),
  `tsimtotal` decimal(44,2),
  `tasapapeleria` decimal(8,6),
  `tasatransporte` decimal(8,6),
  `iva` decimal(34,6),
  `spe` decimal(30,2),
  `iso` decimal(34,6),
  `pesototal` decimal(12,4),
  `procedencia` varchar(45)
);

--
-- Temporary table structure for view `vw_liquidacionesguardadas`
--
DROP TABLE IF EXISTS `vw_liquidacionesguardadas`;
DROP VIEW IF EXISTS `vw_liquidacionesguardadas`;
CREATE TABLE `vw_liquidacionesguardadas` (
  `iddocumento` int(10) unsigned,
  `ndocimpreso` varchar(20),
  `procedencia` varchar(45),
  `totalagencia` decimal(12,4),
  `totalalmacen` decimal(12,4),
  `porcentajepapeleria` decimal(4,2),
  `porcentajetransporte` decimal(4,2),
  `peso` decimal(12,4),
  `fletetotal` decimal(12,4),
  `segurototal` decimal(12,4),
  `otrosgastos` decimal(12,4),
  `tipocambio` mediumint(8) unsigned,
  `fecha` date,
  `tasa` decimal(8,4) unsigned,
  `idpersona` int(10) unsigned,
  `Proveedor` varchar(100),
  `anulado` tinyint(1)
);

--
-- Temporary table structure for view `vw_saldofacturas`
--
DROP TABLE IF EXISTS `vw_saldofacturas`;
DROP VIEW IF EXISTS `vw_saldofacturas`;
CREATE TABLE `vw_saldofacturas` (
  `iddocumento` int(10) unsigned,
  `ndocimpreso` bigint(60),
  `Saldo` decimal(36,4),
  `idpersona` int(10) unsigned
);

--
-- Definition of table `articulos`
--

DROP TABLE IF EXISTS `articulos`;
CREATE TABLE `articulos` (
  `idarticulo` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idmarca` int(10) unsigned NOT NULL,
  `idcategoria` int(10) unsigned NOT NULL,
  `ganancia` smallint(5) unsigned NOT NULL DEFAULT '10' COMMENT 'El porcentaje de ganancia \nque se aplica a este\narticulo para obtener el \nprecio sugerido',
  `activo` tinyint(1) unsigned NOT NULL COMMENT 'Si un articulo\nse encuentra \nactivo o no',
  PRIMARY KEY (`idarticulo`) USING BTREE,
  UNIQUE KEY `uniqueproduct` (`idmarca`,`idcategoria`),
  UNIQUE KEY `articulounico` (`idmarca`,`idcategoria`),
  KEY `fk_articulos_marca1` (`idmarca`),
  KEY `fk_articulos_categoria1` (`idcategoria`),
  CONSTRAINT `fk_articulos_categoria1` FOREIGN KEY (`idcategoria`) REFERENCES `categorias` (`idcategoria`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_marca1` FOREIGN KEY (`idmarca`) REFERENCES `marcas` (`idmarca`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `articulos`
--

/*!40000 ALTER TABLE `articulos` DISABLE KEYS */;
/*!40000 ALTER TABLE `articulos` ENABLE KEYS */;


--
-- Definition of table `articulosxdocumento`
--

DROP TABLE IF EXISTS `articulosxdocumento`;
CREATE TABLE `articulosxdocumento` (
  `idarticuloxdocumento` int(11) NOT NULL AUTO_INCREMENT,
  `iddocumento` int(10) unsigned NOT NULL,
  `idarticulo` int(10) unsigned NOT NULL COMMENT 'El id del articulo',
  `unidades` int(11) NOT NULL COMMENT 'La cantidad de articulos\nen este documento',
  `costocompra` decimal(12,4) DEFAULT NULL COMMENT 'El costo de compra de este\narticulo',
  `costounit` decimal(12,4) DEFAULT NULL COMMENT 'El costo unitario para\neste articulo',
  `precioventa` decimal(12,4) DEFAULT NULL COMMENT 'El precio de venta de este articulo',
  `nlinea` smallint(6) NOT NULL COMMENT 'para ordenar en la interfaz grafica',
  PRIMARY KEY (`idarticuloxdocumento`),
  UNIQUE KEY `articuloxdoc` (`iddocumento`,`idarticulo`),
  KEY `fk_articuloxdocumento_articulos1` (`idarticulo`),
  KEY `fk_articuloxdocumento_documento1` (`iddocumento`),
  CONSTRAINT `fk_articuloxdocumento_documentos1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `articulosxdocumento`
--

/*!40000 ALTER TABLE `articulosxdocumento` DISABLE KEYS */;
/*!40000 ALTER TABLE `articulosxdocumento` ENABLE KEYS */;


--
-- Definition of trigger `tr_promediarcosto`
--

DROP TRIGGER /*!50030 IF EXISTS */ `tr_promediarcosto`;

DELIMITER $$

CREATE DEFINER = `root`@`localhost` TRIGGER `tr_promediarcosto` AFTER INSERT ON `articulosxdocumento` FOR EACH ROW BEGIN

      DECLARE costo DECIMAL(12,4);
      DECLARE idtc  INTEGER;
	  DECLARE tasa DECIMAL(12,4);

      IF NEW.unidades>0 THEN

		SELECT idtipocambio,tc.tasa FROM documentos d
    JOIN tiposcambio tc ON tc.idtc=d.idtipocambio
    WHERE iddocumento = NEW.iddocumento INTO @idtc, @tasa;



      IF @tasa IS NULL THEN
          SET NEW= NULL;
      END IF;

        SELECT SUM((unidades*costounit * @tasa))/SUM(unidades)  FROM articulosxdocumento a WHERE a.idarticulo= NEW.idarticulo INTO @costo;


        IF @costo IS NULL THEN
          SET @costo=NEW.costounit;
        ELSE
          SET @costo=@costo/@tasa;
       END IF;


        UPDATE costosarticulo SET activo=0 WHERE idarticulo=NEW.idarticulo AND activo=1;

        INSERT INTO costosarticulo (valor,idarticulo,idtc) VALUES (@costo,NEW.idarticulo,@idtc);
      END IF;

END $$

DELIMITER ;

--
-- Definition of table `bancos`
--

DROP TABLE IF EXISTS `bancos`;
CREATE TABLE `bancos` (
  `idbanco` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del banco',
  `descripcion` varchar(45) NOT NULL COMMENT 'El nombre del banco',
  PRIMARY KEY (`idbanco`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bancos`
--

/*!40000 ALTER TABLE `bancos` DISABLE KEYS */;
INSERT INTO `bancos` (`idbanco`,`descripcion`) VALUES 
 (1,'BAC'),
 (2,'BANCENTRO');
/*!40000 ALTER TABLE `bancos` ENABLE KEYS */;


--
-- Definition of table `bodegas`
--

DROP TABLE IF EXISTS `bodegas`;
CREATE TABLE `bodegas` (
  `idbodega` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la bodega',
  `nombrebodega` varchar(45) NOT NULL COMMENT 'El nombre de la bodega',
  PRIMARY KEY (`idbodega`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bodegas`
--

/*!40000 ALTER TABLE `bodegas` DISABLE KEYS */;
INSERT INTO `bodegas` (`idbodega`,`nombrebodega`) VALUES 
 (1,'Llantas Express'),
 (2,'Bodega 2'),
 (3,'Bodega 3'),
 (4,'Bodega 4');
/*!40000 ALTER TABLE `bodegas` ENABLE KEYS */;


--
-- Definition of trigger `tr_validarnombrebodega`
--

DROP TRIGGER /*!50030 IF EXISTS */ `tr_validarnombrebodega`;

DELIMITER $$

CREATE DEFINER = `root`@`localhost` TRIGGER `tr_validarnombrebodega` BEFORE INSERT ON `bodegas` FOR EACH ROW BEGIN

    IF NEW.nombrebodega ='' THEN
       SET NEW = NULL;
    END IF;

END $$

DELIMITER ;

--
-- Definition of table `cajas`
--

DROP TABLE IF EXISTS `cajas`;
CREATE TABLE `cajas` (
  `idcaja` tinyint(3) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la caja',
  `descripcion` varchar(45) NOT NULL COMMENT 'El nombre de la caja',
  PRIMARY KEY (`idcaja`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cajas`
--

/*!40000 ALTER TABLE `cajas` DISABLE KEYS */;
INSERT INTO `cajas` (`idcaja`,`descripcion`) VALUES 
 (1,'Caja 1');
/*!40000 ALTER TABLE `cajas` ENABLE KEYS */;


--
-- Definition of table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE `categorias` (
  `idcategoria` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la categoria',
  `nombre` varchar(25) NOT NULL COMMENT 'El nombre de la categoria',
  `padre` int(10) unsigned DEFAULT NULL COMMENT 'El id de la categoria padre',
  PRIMARY KEY (`idcategoria`),
  KEY `fk_catsubcategoria_catsubcategoria1` (`padre`),
  CONSTRAINT `fk_catsubcategoria_catsubcategoria1` FOREIGN KEY (`padre`) REFERENCES `categorias` (`idcategoria`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=288 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `categorias`
--

/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` (`idcategoria`,`nombre`,`padre`) VALUES 
 (1,'\"BATERIAS\"',NULL),
 (2,'FRICCIONES*',NULL),
 (3,'NEUMATICOS',NULL),
 (4,'VARIOS',NULL),
 (5,'VALVULAS',NULL),
 (6,'GATOS DE CHASSIS',NULL),
 (7,'RINES PARA AUTO',NULL),
 (8,'GATOS DE 3/4 TONELAD',NULL),
 (9,'RINES PARA CAMIONETA',NULL),
 (10,'PULIDORAS',NULL),
 (11,'FORRO DE TIMON',NULL),
 (12,'FORRO DE ASIENTO',NULL),
 (13,'MOFLE',NULL),
 (14,'EXTENCION P/MUFLER',NULL),
 (15,'ROCIADORES',NULL),
 (16,'LLANTAS',NULL),
 (17,'ALFOMBRAS',NULL),
 (18,'SPOILER',NULL),
 (19,'CORTINA DE CARRO',NULL),
 (20,'COPAS PARA AUTO',NULL),
 (21,'COPAS P/LLANTAS',NULL),
 (22,'LAMPARA',NULL),
 (23,'TELEFONO',NULL),
 (24,'COJIN DE CARRO',NULL),
 (25,'MANUBRIO',NULL),
 (26,'KIT',NULL),
 (27,'DISCO DE FRENO',NULL),
 (28,'MARCO',NULL),
 (29,'CONO',NULL),
 (30,'GAMUSA',NULL),
 (31,'TAPAS',NULL),
 (32,'ACCESORIOS',NULL),
 (33,'T.V',NULL),
 (34,'TRIANGULO',NULL),
 (35,'CORTINA',NULL),
 (36,'LUZ',NULL),
 (37,'BASE',NULL),
 (38,'ADAPTADOR',NULL),
 (39,'TIMON DE AUTO',NULL),
 (40,'ESPEJOS',NULL),
 (41,'RADIO',NULL),
 (42,'REPRODUCTOR',NULL),
 (43,'MUFFLER',NULL),
 (44,'LIMPIA PARA BRISA',NULL),
 (45,'BOCINAS',NULL),
 (46,'CABLE',NULL),
 (47,'MONITOR',NULL),
 (48,'ANTENAS',NULL),
 (49,'AMPLIFICADOR',NULL),
 (50,'ECUALIZADOR',NULL),
 (51,'MODULADOR',NULL),
 (52,'D.V.D',NULL),
 (53,'SUB-WOOFER',NULL),
 (54,'TWEETERS',NULL),
 (55,'ALARMAS',NULL),
 (56,'KIT DE CIERRE',NULL),
 (57,'MOTOR DS-2.1',NULL),
 (58,'MODULO',NULL),
 (59,'RELAY',NULL),
 (60,'SOCKET',NULL),
 (61,'AIRE',NULL),
 (62,'TUBOS',NULL),
 (63,'PALANCAS DE CAMBIO',NULL),
 (64,'tv 21 Pulg',NULL),
 (65,'11-22.5MOD',1),
 (66,'11R22.5MOD66',1),
 (67,'11R24.5',1),
 (68,'175-70R13',1),
 (69,'185 R 14',1),
 (70,'185-70R 13',1),
 (71,'195 R 14',1),
 (72,'195 R 15',1),
 (73,'205-70 R 14',1),
 (74,'205R16',1),
 (75,'31x10.50 R 15',1),
 (76,'5-50-13',1),
 (77,'6-50-14',1),
 (78,'7-00-16',1),
 (79,'7-50-16',1),
 (80,'8-19.5',1),
 (81,'235/75R15',1),
 (82,'750R16',1),
 (83,'305-45 R22',1),
 (84,'18570R14',1),
 (85,'10-00-200 T212',1),
 (86,'1000-20 T101 RANGER',1),
 (87,'5-00-12',1),
 (88,'20560R13',1),
 (89,'5-50-14',1),
 (90,'825 15 14',1),
 (91,'700 12 14',1),
 (92,'600 9 10',1),
 (93,'155-R12',1),
 (94,'15.5 X 38',1),
 (95,'205/50R15',1),
 (96,'60014',1),
 (97,'60013',1),
 (98,'285/50R20',1),
 (99,'195/50R15',1),
 (100,'70015',1),
 (101,'305-40 X 22',1),
 (102,'26570R16 KUMHO',1),
 (103,'14.9 x 24',1),
 (104,'30X9.50R15',1),
 (105,'215/75R15',1),
 (106,'215 40 R17',1),
 (107,'10-00-20',1),
 (108,'185/60R14',1),
 (109,'10 50 R 15',1),
 (110,'750 15',1),
 (111,'700 15 12',1),
 (112,'205 40 R 17',1),
 (113,'19570R14 KUMHO',1),
 (114,'265 75 16 W',1),
 (115,'309 50 R15',1),
 (116,'18-4-30-12',1),
 (117,'23-1-30-8',1),
 (118,'1300-24-12',1),
 (119,'TT TR270 18.4-30.8',1),
 (120,'TS19 15.5 38.8',1),
 (121,'7-50-20 TS 23',1),
 (122,'19570R14',1),
 (123,'16580R13',1),
 (124,'215/60R16',1),
 (125,'155/70R13',1),
 (126,'215/70R15',1),
 (127,'175/65R14',1),
 (128,'11R22.5 REENCAUCHE',1),
 (129,'650-10-10',1),
 (130,'600-9-10',1),
 (131,'215-R14 SUMITOMO',1),
 (132,'175 65 R14',1),
 (133,'175-70R14',1),
 (134,'700 R 16',1),
 (135,'LLANTA 825X16',1),
 (136,'215-65R16',1),
 (137,'185-60R15 NEXEN',1),
 (141,'750-15-12',1),
 (142,'26570SR16',1),
 (143,'31-10.50R15',1),
 (144,'30-9.50R15',1),
 (145,'18565R14 KUMHO',1),
 (146,'16570R13',1),
 (147,'9-00-20',1),
 (148,'BATERIA  1111MF',2),
 (149,'BATERIA  1150MF',2),
 (150,'BATERIA  N-120',2),
 (151,'BATERIA  N-150',2),
 (152,'BATERIA  N-200',2),
 (153,'BATERIA  N-40',2),
 (154,'BATERIA 75 AMPERIO',2),
 (155,'BATERIA NX110MF',2),
 (156,'BATERIA N-200',2),
 (157,'BATERIA N-180 CHARGE',2),
 (158,'BATERIA N 40 Z 35AMP',2),
 (159,'BATERIA 30H 100AM',2),
 (160,'31T 670/AMP',2),
 (161,'31P 670/AMP',2),
 (162,'N-X 120 MF',2),
 (163,'BATERIA N-42-550',2),
 (164,'BATERIA G-27 (N-70)',2),
 (165,'BATERIA G-31 (30HP)',2),
 (166,'BATERIA G-22F ( N50)',2),
 (167,'BATERIA G-24 (N-50)',2),
 (168,'BATERIA N 40 L',2),
 (169,'NS70MF',2),
 (170,'K42R5MF',2),
 (171,'BATERIA  N-50',2),
 (172,'BATERIA  N-70',2),
 (173,'BATERIA N-200',2),
 (174,'FRICCION',3),
 (175,'BATERIA 42-550',3),
 (176,'BATERIA N-701',3),
 (177,'FRICCION KORENA ',3),
 (178,'NEUMATICOS',4),
 (179,'VALVULAS',5),
 (180,'VARIOS2',6),
 (181,'25110',7),
 (182,'26110',7),
 (183,'GATOS DE TALLER',7),
 (184,'3/4 DE TONELADA',7),
 (185,'229.5',8),
 (186,'3/4 DE TONELADA',9),
 (187,'RINES 20x8.56x5.5 CH',10),
 (188,'RINES 17*7',10),
 (189,'RINES 15*7',10),
 (190,'RINES 13*5.5',10),
 (191,'RINES 15x7.54/100 HB',10),
 (192,'S/N',11),
 (193,'FORRO DE TIMON CUERI',12),
 (194,'FORRO PARA TIMON',12),
 (195,'FORRO DE TIMON GRIS',12),
 (196,'FORRO MASAGE TOYOTA',12),
 (197,'FORRO DE TIMON NEGRO',12),
 (198,'FORRO PARA ASIENTO',13),
 (199,'FORRO GRIS P/ASIENTO',13),
 (200,'FORRO AUTO GRIS',13),
 (201,'MOFLE MUFLER',14),
 (202,'EXTENSION PARA MUFLE',15),
 (203,'ROCIADORES PARABRISA',16),
 (204,'ALFOMBRAS DE CAUCHO',17),
 (205,'ALFOMBRAS AUTO NEGRO',17),
 (206,'ALFOMBRAS GRIS',17),
 (207,'ALFOMBRA AZUL',17),
 (208,'ALFOMBRA CHOCOLATE',17),
 (209,'ALFOMBRAS NEGRO',17),
 (210,'COLA DE PATO SPOILER',18),
 (211,'CORTINA DE PALMERA',19),
 (212,'CORTINA PLASTICA',19),
 (213,'COPAS CROMADA AZUL',20),
 (214,'COPAS CROMADA NEGRA',20),
 (215,'COPAS CROMADA ROJA',20),
 (216,'COPAS PARA LLANTAS',21),
 (217,'COPAS P/LLANTAS 13',21),
 (218,'COPAS P/LLANTAS 13 P',21),
 (219,'COPAS P/LLANTAS 14 P',21),
 (220,'LAMPARA ORIENTAL',22),
 (221,'LAMPARA DE INTERIOR',22),
 (222,'LAMPARA DE TECHO',22),
 (223,'LAMPARA HALOGENO',22),
 (224,'TELEFONO ANTIGUO',23),
 (225,'COJIN PARA CARRO',24),
 (226,'MANUBRIO PALAN. DE C',25),
 (227,'KIT DE ACCESORIOS',26),
 (228,'DISCO DE FRENOS',27),
 (229,'MARCO P/PLACA',28),
 (230,'CONO HIEDRA',29),
 (231,'GAMUSA ACC.',30),
 (232,'TAPAS P/TANQUE',31),
 (233,'ACCESORIOS',32),
 (234,'TVD P/AUTO',33),
 (235,'TRIANGULO REFLECTIVO',34),
 (236,'CORTINA FRONTAL',35),
 (237,'LUZ PARA BUMPER',36),
 (238,'BASE DE TIMON',37),
 (239,'ADAPTADOR PARA TIMON',38),
 (240,'TIMON DE AUTO',39),
 (241,'TIMON STEERING WHEEL',39),
 (242,'ESPEJOS P/AUTO',40),
 (243,'RADIO P/AUTO',41),
 (244,'REPRODUCTOR DE DVD',42),
 (245,'MUFFLER METALICO',43),
 (246,'LIMPIA PARA BRISA',44),
 (247,'BOCINAS 240W',45),
 (248,'BOCINAS 460W',45),
 (249,'BOCINAS TSP-1066',45),
 (250,'BOCINAS SILVER POINT',45),
 (251,'BOCINAS SPEAKERS BOX',45),
 (252,'BOCINAS 440W',45),
 (253,'BOCINAS 1000W',45),
 (254,'BOCINAS 300W',45),
 (255,'BOCINAS 160W',45),
 (256,'BOCINAS 220W',45),
 (257,'CABLE PARA AMP.',46),
 (258,'MONITOR LCD',47),
 (259,'ANTENA P/AUTO',48),
 (260,'AMPLIFICADOR',49),
 (261,'ECUALIZADOR',50),
 (262,'MODULADOR',51),
 (263,'D.V.D',52),
 (264,'SUBWOOFER P/AUTOS',53),
 (265,'TWEETERS P/AUTOS',54),
 (266,'K-9 MUNDIAL SS',55),
 (267,'REVOLUTION',55),
 (268,'KIT DE CIERRE CENTRA',56),
 (269,'MOTOR DS 2.1',57),
 (270,'MODULO MUNDIAL 3',58),
 (271,'RELAY 20/30',59),
 (272,'SOCKET',60),
 (273,'AIRE SPLIT',61),
 (274,'TUBOS PARA BJO BASS',62),
 (275,'PALANCAS DE CAMBIO',63),
 (276,'TV 21 PULG.',64),
 (280,'LAST',NULL),
 (281,'PEDRO',NULL),
 (282,'Sillas',NULL),
 (283,'Llantas Reencauchadas',NULL),
 (284,'Condensador',NULL),
 (285,'Sub',284),
 (286,'VARIOSLAST',4),
 (287,'VAL',NULL);
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;


--
-- Definition of table `cierrescontables`
--

DROP TABLE IF EXISTS `cierrescontables`;
CREATE TABLE `cierrescontables` (
  `idcierrecontable` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idCuenta` int(10) unsigned NOT NULL,
  `monto` decimal(12,4) NOT NULL,
  `fechacierre` datetime NOT NULL,
  `esmensual` tinyint(1) NOT NULL,
  PRIMARY KEY (`idcierrecontable`),
  KEY `fk_cierrecontable_cuentacontable1` (`idCuenta`),
  CONSTRAINT `fk_cierrecontable_cuentacontable1` FOREIGN KEY (`idCuenta`) REFERENCES `cuentascontables` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cierrescontables`
--

/*!40000 ALTER TABLE `cierrescontables` DISABLE KEYS */;
/*!40000 ALTER TABLE `cierrescontables` ENABLE KEYS */;


--
-- Definition of table `conceptos`
--

DROP TABLE IF EXISTS `conceptos`;
CREATE TABLE `conceptos` (
  `idconcepto` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `modulo` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`idconcepto`) USING BTREE,
  KEY `fk_conceptos_modulo1` (`modulo`),
  CONSTRAINT `fk_conceptos_modulo1` FOREIGN KEY (`modulo`) REFERENCES `modulos` (`idmodulos`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `conceptos`
--

/*!40000 ALTER TABLE `conceptos` DISABLE KEYS */;
INSERT INTO `conceptos` (`idconcepto`,`descripcion`,`modulo`) VALUES 
 (1,'Abono al Saldo Pendiente',2),
 (2,'Cancelación Saldo de Factura',2);
/*!40000 ALTER TABLE `conceptos` ENABLE KEYS */;


--
-- Definition of table `costosagregados`
--

DROP TABLE IF EXISTS `costosagregados`;
CREATE TABLE `costosagregados` (
  `idcostoagregado` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del costo agregado',
  `valorcosto` decimal(8,2) NOT NULL COMMENT 'El valor del costo agregado',
  `fechaestablecido` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'La fecha en la que este costo agregado fue establecido',
  `activo` tinyint(1) NOT NULL COMMENT 'Si este costo esta activo o no',
  `idtipocosto` int(10) unsigned NOT NULL COMMENT 'El id del tipo de costo',
  `idarticulo` int(10) unsigned DEFAULT NULL COMMENT 'id del articulo cuando sea DAI, ISC o COMISION',
  PRIMARY KEY (`idcostoagregado`),
  KEY `fk_CostoAgregado_TipoCosto1` (`idtipocosto`),
  KEY `fk_costoagregado_articulos1` (`idarticulo`),
  CONSTRAINT `fk_costoagregado_articulos1` FOREIGN KEY (`idarticulo`) REFERENCES `articulos` (`idarticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_CostoAgregado_TipoCosto1` FOREIGN KEY (`idtipocosto`) REFERENCES `tiposcosto` (`idtipocosto`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `costosagregados`
--

/*!40000 ALTER TABLE `costosagregados` DISABLE KEYS */;
/*!40000 ALTER TABLE `costosagregados` ENABLE KEYS */;


--
-- Definition of table `costosarticulo`
--

DROP TABLE IF EXISTS `costosarticulo`;
CREATE TABLE `costosarticulo` (
  `idcostoarticulo` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del costoarticulo',
  `valor` decimal(12,4) unsigned NOT NULL COMMENT 'El valor del costo articulo',
  `idarticulo` int(10) unsigned NOT NULL COMMENT 'El id del articulo',
  `activo` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT 'Si este costo esta activo o no',
  `idtc` mediumint(8) unsigned NOT NULL COMMENT 'El id del tipo de cambio',
  PRIMARY KEY (`idcostoarticulo`),
  KEY `fk_costoarticulo_articulos1` (`idarticulo`),
  KEY `fk_costosarticulo_tiposcambio1` (`idtc`),
  CONSTRAINT `fk_costoarticulo_articulos1` FOREIGN KEY (`idarticulo`) REFERENCES `articulos` (`idarticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_costosarticulo_tiposcambio1` FOREIGN KEY (`idtc`) REFERENCES `tiposcambio` (`idtc`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `costosarticulo`
--

/*!40000 ALTER TABLE `costosarticulo` DISABLE KEYS */;
/*!40000 ALTER TABLE `costosarticulo` ENABLE KEYS */;


--
-- Definition of table `costosxarticuloliquidacion`
--

DROP TABLE IF EXISTS `costosxarticuloliquidacion`;
CREATE TABLE `costosxarticuloliquidacion` (
  `idarticuloxdocumento` int(11) NOT NULL COMMENT 'El id del registro articuloxdodumento',
  `dai` decimal(12,4) NOT NULL COMMENT 'El valor del costo DAI',
  `isc` decimal(12,4) NOT NULL COMMENT 'El valor del costo ISC',
  `comision` decimal(12,4) NOT NULL COMMENT 'El valor de la comisión',
  PRIMARY KEY (`idarticuloxdocumento`),
  KEY `fk_table1_articuloxdocumento1` (`idarticuloxdocumento`),
  CONSTRAINT `fk_table1_articuloxdocumento1` FOREIGN KEY (`idarticuloxdocumento`) REFERENCES `articulosxdocumento` (`idarticuloxdocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `costosxarticuloliquidacion`
--

/*!40000 ALTER TABLE `costosxarticuloliquidacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `costosxarticuloliquidacion` ENABLE KEYS */;


--
-- Definition of table `costosxdocumento`
--

DROP TABLE IF EXISTS `costosxdocumento`;
CREATE TABLE `costosxdocumento` (
  `iddocumento` int(10) unsigned NOT NULL COMMENT 'El id del documento',
  `idcostoagregado` int(10) unsigned NOT NULL COMMENT 'El id del costo agregado',
  PRIMARY KEY (`iddocumento`,`idcostoagregado`),
  KEY `fk_documento_has_costoagregado_documento1` (`iddocumento`),
  KEY `fk_documento_has_costoagregado_costoagregado1` (`idcostoagregado`),
  CONSTRAINT `fk_documento_has_costoagregado_costoagregado1` FOREIGN KEY (`idcostoagregado`) REFERENCES `costosagregados` (`idcostoagregado`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_documento_has_costoagregado_documento1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `costosxdocumento`
--

/*!40000 ALTER TABLE `costosxdocumento` DISABLE KEYS */;
/*!40000 ALTER TABLE `costosxdocumento` ENABLE KEYS */;


--
-- Definition of table `cuentasbancarias`
--

DROP TABLE IF EXISTS `cuentasbancarias`;
CREATE TABLE `cuentasbancarias` (
  `idcuentabancaria` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la cuenta bancaria',
  `idcuentacontable` int(10) unsigned NOT NULL COMMENT 'El id de la cuenta contable',
  `idbanco` int(10) unsigned NOT NULL COMMENT 'El id del banco',
  `ctabancaria` varchar(45) NOT NULL COMMENT 'El numero de la cuenta bancaria',
  `fechacancelado` date DEFAULT NULL COMMENT 'La fecha en que esta cuenta bancaria fue cerrada',
  `fechaapertura` date NOT NULL COMMENT 'La fecha en que esta cuenta bancaria fue cerrada',
  `idtipomoneda` tinyint(3) unsigned NOT NULL COMMENT 'El id del tipo de moneda en esta cuenta bancaria',
  PRIMARY KEY (`idcuentabancaria`),
  KEY `fk_cuentabancaria_banco1` (`idbanco`),
  KEY `fk_cuentabancaria_cuentacontable1` (`idcuentacontable`),
  KEY `fk_cuentabancaria_tipomoneda1` (`idtipomoneda`),
  CONSTRAINT `fk_cuentabancaria_banco1` FOREIGN KEY (`idbanco`) REFERENCES `bancos` (`idbanco`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cuentabancaria_cuentacontable1` FOREIGN KEY (`idcuentacontable`) REFERENCES `cuentascontables` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cuentabancaria_tipomoneda1` FOREIGN KEY (`idtipomoneda`) REFERENCES `tiposmoneda` (`idtipomoneda`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cuentasbancarias`
--

/*!40000 ALTER TABLE `cuentasbancarias` DISABLE KEYS */;
INSERT INTO `cuentasbancarias` (`idcuentabancaria`,`idcuentacontable`,`idbanco`,`ctabancaria`,`fechacancelado`,`fechaapertura`,`idtipomoneda`) VALUES 
 (1,9,1,'004-13116-5',NULL,'2010-07-01',1),
 (2,8,2,'240-201-518',NULL,'2010-07-01',1),
 (3,11,2,'241-200-825',NULL,'2010-07-01',2);
/*!40000 ALTER TABLE `cuentasbancarias` ENABLE KEYS */;


--
-- Definition of table `cuentascontables`
--

DROP TABLE IF EXISTS `cuentascontables`;
CREATE TABLE `cuentascontables` (
  `idcuenta` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la cuenta contable',
  `padre` int(10) unsigned DEFAULT NULL COMMENT 'El id del padre de esta cuenta contable ',
  `codigo` varchar(20) NOT NULL COMMENT 'El codigo contable',
  `descripcion` varchar(45) NOT NULL COMMENT 'La descripción de esta cuenta',
  `esdebe` tinyint(1) NOT NULL COMMENT 'Para definir si es activo, pasivo o capital',
  PRIMARY KEY (`idcuenta`),
  KEY `fk_cuenta_cuenta1` (`padre`),
  CONSTRAINT `fk_cuenta_cuenta1` FOREIGN KEY (`padre`) REFERENCES `cuentascontables` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=356 DEFAULT CHARSET=utf8 COMMENT='Es un catalogo de cuentas';

--
-- Dumping data for table `cuentascontables`
--

/*!40000 ALTER TABLE `cuentascontables` DISABLE KEYS */;
INSERT INTO `cuentascontables` (`idcuenta`,`padre`,`codigo`,`descripcion`,`esdebe`) VALUES 
 (1,NULL,'---','ES UNA CLASIFICACION',1),
 (2,1,'','ACTIVO CORRIENTE',1),
 (3,2,'110 000 000 000 000','ACTIVOS CORRIENTES',1),
 (4,3,'110 001 000 000 000','CYB Caja',1),
 (5,4,'110 001 001 000 000','CYB Caja General',1),
 (6,4,'110 001 002 000 000','CYB Caja Chica',1),
 (7,4,'110 001 003 000 000','CYB Banco de Moneda Nacional',1),
 (8,7,'110 001 003 001 000','BMN Bancentro 240-201-518',1),
 (9,7,'110 001 003 002 000','BMN BAC 004-13116-5',1),
 (10,4,'110 001 004 000 000','CYB Banco de Moneda Extranjero',1),
 (11,10,'110 001 004 001 000','BME Bancentro 241-200-825',1),
 (12,4,'110 001 005 000 000','C Efectivo en Caja',1),
 (13,3,'110 002 000 000 000','CUENTAS Y DOCUMENTOS POR COBRAR',1),
 (14,13,'110 002 001 000 000','CDC Cuentas por Cobrar Clientes',1),
 (15,13,'110 002 002 000 000','CDC Estimacion para Cuentas Incb Clientes',1),
 (16,13,'110 002 003 000 000','CDC Documentos por Cobrar',1),
 (17,13,'110 002 004 000 000','CDC Estimacion para Cuentas Incob Doc x Co',1),
 (18,13,'110 002 005 000 000','CDC Cuentas por Liquidar',1),
 (19,13,'110 002 006 000 000','CDC Cuentas por Cobrar Empleados',1),
 (20,13,'110 002 007 000 000','CDC Otras Cuentas por Cobrar',1),
 (21,3,'110 003 000 000 000','INVENTARIOS',1),
 (22,21,'110 003 001 000 000','INV Inventario de Bodega',1),
 (23,21,'110 003 002 000 000','INV Mercaderia en Transito',1),
 (24,21,'110 003 003 000 000','INV Piezas y Repuestos',1),
 (25,21,'110 003 004 000 000','INV Herramientas y Utiles',1),
 (26,21,'110 003 005 000 000','INV Materiales de Oficinas',1),
 (27,21,'110 003 006 000 000','INV Otros',1),
 (28,3,'110 004 000 000 000','ANTICIPO A JUSTIFICAR',1),
 (29,28,'110 004 001 000 000','AJ Anticipo para Compras y Gastos',1),
 (30,28,'110 004 002 000 000','AJ Otros',1),
 (31,3,'110 005 000 000 000','PAGOS ANTICIPADOS',1),
 (32,31,'110 005 001 000 000','PA Anticipos a Contrtista',1),
 (33,31,'110 005 002 000 000','PA Anticipos a Proveedores',1),
 (34,31,'110 005 003 000 000','PA Impuestos  Anticipados (IVA)',1),
 (35,31,'110 005 004 000 000','PA Impuestos Anticipados (IR)',1),
 (36,31,'110 005 005 000 000','PA Otros',1),
 (37,31,'110 005 006 000 000','PA Saldos Iniciales',1),
 (38,31,'110 005 007 000 000','PA ANTICIPOS DE ARRIENDOS',1),
 (39,38,'110 005 007 001 000','PA ANTICIPOS DE ARRIENDOS',1),
 (40,1,'','ACTIVO FIJOS',1),
 (41,40,'120 000 000 000 000','PROPIEDAD PLANTAS Y EQUIPOS',1),
 (42,41,'120 001 000 000 000','PPE Terrenos',1),
 (43,41,'120 002 000 000 000','PPE Edificios',1),
 (44,41,'120 003 000 000 000','PPE Mobiliario y Equipo de Oficina',1),
 (45,44,'120 003 001 000 000','MEO Puertas ,  Ventanas, etc.',1),
 (46,44,'120 003 002 000 000','MEO Sillas, Escritorios, Maq Escrib, etc',1),
 (47,44,'120 003 003 000 000','MEO Fotocopiadora',1),
 (48,41,'120 004 000 000 000','PPE Equipo de Computacion',1),
 (49,41,'120 005 000 000 000','PPE Equipo Rodante',1),
 (50,41,'120 006 000 000 000','PPE Vehiculos',1),
 (51,41,'120 007 000 000 000','PPE Equipo de Comunicacion',1),
 (52,41,'120 008 000 000 000','PPE Radio Wolkie Toki, Telefonos,etc',1),
 (53,41,'120 009 000 000 000','PPE Otros Activos Fijos',1),
 (54,40,'130 000 000 000 000','DEPRECIACION ACUMULADA',0),
 (55,54,'130 001 000 000 000','DA Depreciacion Acumulada de Edificios',0),
 (56,54,'130 002 000 000 000','DA Dep Acum de Mob y Equipo de Oficina',0),
 (57,54,'130 003 000 000 000','DA Dep Acum de Equipo de Computacion',0),
 (58,54,'130 004 000 000 000','DA Dep de  Equipo Rodante',0),
 (59,54,'130 005 000 000 000','DA Dep Acum de Comunicacion',0),
 (60,54,'130 006 000 000 000','DA Dep  Acum de Otros Activos',0),
 (61,54,'130 007 000 000 000','DA Saldos Iniciales',0),
 (62,1,'','ACTIVOS DIFERIDOS',1),
 (63,62,'140 000 000 000 000','ACTIVOS DIFERIDOS',1),
 (64,63,'140 001 000 000 000','AD Gastos de Constitucion',1),
 (65,63,'140 002 000 000 000','AD Gastos de Organizacion',1),
 (66,63,'140 003 000 000 000','AD Gastos de Instalacion',1),
 (67,63,'140 004 000 000 000','AD Mejoras en Propiedades Arrendadas',1),
 (68,63,'140 005 000 000 000','AD Remodelaciones de Oficinas',1),
 (69,63,'140 006 000 000 000','AD Primas de Seguros y Finanzas',1),
 (70,1,'','OTROS ACTIVOS',1),
 (71,70,'150 000 000 000 000','OTROS ACTIVOS',1),
 (72,71,'150 001 000 000 000','OA Reparaciones Capitalizables',1),
 (73,71,'150 002 000 000 000','OA Marcas y Patentes',1),
 (74,71,'150 003 000 000 000','OA Depositos en Garantias',1),
 (75,1,'','PASIVO CORRIENTE',0),
 (76,75,'210 000 000 000 000','PASIVO CIRCULANTE',0),
 (77,76,'210 001 000 000 000','PC Proveedores',0),
 (78,77,'210 001 001 000 000','P  Proveedores Locales',0),
 (79,78,'210 001 001 001 000','PL GRUPO Q',0),
 (80,78,'210 001 001 002 000','PL COTARSA',0),
 (81,77,'210 001 002 000 000','P Proveedores del Exterio',0),
 (82,81,'210 001 002 001 000','PE N VISION',0),
 (83,81,'210 001 002 002 000','PE  NSC LOGISTICS',0),
 (84,81,'210 001 002 003 000','PE GRUPO HUANG',0),
 (85,81,'210 001 002 004 000','PE TRIANGLE PANAMA',0),
 (86,81,'210 001 002 005 000','PE SUOTH DADE EEUU',0),
 (87,81,'210 001 002 006 000','PE GEDEON',0),
 (88,81,'210 001 002 007 000','PE STEPHANIE TIRES EEUU',0),
 (89,81,'210 001 002 008 000','PE PUENTE INVENTARIO-PROVEEDORES',0),
 (90,81,'210 001 002 009 000','PE Saldo Inicial',0),
 (91,81,'210 001 002 010 000','PE Puente Inv. Proveedores en Efectivo',0),
 (92,81,'210 001 002 011 000','PE Puente Inv. Proveedores en Consignacion',0),
 (93,81,'210 001 002 012 000','PE MT - C S',0),
 (94,81,'210 001 002 013 000','PE ABC TORE GROUP INC',0),
 (95,81,'210 001 002 014 000','PL Reyoli Tires',0),
 (96,81,'210 001 002 015 000','ANTON IMPORTADORA Y EXPORTADORA',0),
 (97,81,'210 001 002 016 000','PE AUDIO CENTRO INTERNACIONAL, S.A ACISA',0),
 (98,81,'210 001 002 017 000','LUCY TIRES INC',0),
 (99,81,'210 001 002 018 000','PE MASTER TIRES & RUBBER, S.A.',0),
 (100,81,'210 001 002 019 000','PE MURESSA INTERTRADE, S.A.',0),
 (101,81,'210 001 002 020 000','MULTILLANTAS',0),
 (102,76,'210 002 000 000 000','ACREEDORES DIVERSOS',0),
 (103,102,'210 002 001 000 000','AD Alquileres y Arriendos',0),
 (104,102,'210 002 002 000 000','AD Otros',0),
 (105,102,'210 002 003 000 000','AD Saldo Inicial',0),
 (106,76,'210 003 000 000 000','PRESTAMOS BANCARIOS A CORTO PLAZO',0),
 (107,106,'210 003 001 000 000','PBCP Prestamos Bancarios para Operaciones',0),
 (108,106,'210 003 002 000 000','PBCP Prestamos para Inversiones',0),
 (109,76,'210 004 000 000 000','INTERESES ACUMULADOS POR PAGAR',0),
 (110,109,'210 004 001 000 000','IAP Intereses por Prestamos para Operacion',0),
 (111,109,'210 004 002 000 000','IAP Intereses por Prest para Inversion',0),
 (112,109,'210 004 003 000 000','IAP Intereses Moratorios',0),
 (113,76,'210 005 000 000 000','PRESTACIONES SOCIALES POR PAGAR',0),
 (114,113,'210 005 001 000 000','PSP Vacaciones',0),
 (115,113,'210 005 002 000 000','PSP Aguinaldo',0),
 (116,113,'210 005 003 000 000','PSP Indemnizacion  por Ley',0),
 (117,113,'210 005 004 000 000','PSP Saldo Inicial',0),
 (118,76,'210 006 000 000 000','RETENCIONES POR PAGAR',0),
 (119,118,'210 006 001 000 000','RP IR en la Fuente por Pagar 2%',0),
 (120,118,'210 006 002 000 000','RP Retenciones a Empleados (IR)',0),
 (121,118,'210 006 003 000 000','RP Cuota al INSS Empleados',0),
 (122,118,'210 006 004 000 000','RP Otras Retenciones',0),
 (123,118,'210 006 005 000 000','IP RETENCION EN LA FUENTE SER. PROF(10%)',0),
 (124,118,'210 006 006 000 000','RP Saldo Inicial',0),
 (125,76,'210 007 000 000 000','GASTOS ACUMULADOS POR PAGAR',0),
 (126,125,'210 007 001 000 000','GAP Reembolsos de Caja Chica',0),
 (127,125,'210 007 002 000 000','SERVICIOS PUBLICOS',0),
 (128,127,'210 007 002 001 000','SP ENACAL',0),
 (129,127,'210 007 002 002 000','SP DISSUR',0),
 (130,127,'210 007 002 003 000','SP ENITEL',0),
 (131,76,'210 008 000 000 000','IMPUESTOS Y APORTES POR PAGAR',0),
 (132,131,'210 008 001 000 000','IMPUESTO POR PAGAR',0),
 (133,132,'210 008 001 001 000','IP IVA por Pagar',0),
 (134,132,'210 008 001 002 000','IP  IR Anual',0),
 (135,131,'210 008 002 000 000','APORTES A PAGAR',0),
 (136,135,'210 008 002 001 000','AP Aportes Patronal al INSS',0),
 (137,135,'210 008 002 002 000','AP Aportes de 2% al INATEC',0),
 (138,135,'210 008 002 003 000','AP Aportes del 1%  de Alcaldia',0),
 (139,135,'210 008 002 004 000','AP Otros Aportes por Pagar',0),
 (140,135,'210 008 002 005 000','IP Saldo Inicial',0),
 (141,76,'210 009 000 000 000','PASIVO A LARGO PLAZO',0),
 (142,141,'210 009 001 000 000','PLP Cuentas por Pagar a Largo Plazo',0),
 (143,142,'210 009 001 001 000','CPLA Prestamos Bancarios a Largo Plazo',0),
 (144,76,'210 010 000 000 000','PASIVOS DIFERIDOS',0),
 (145,144,'210 010 001 000 000','PA Creditos  Diferidos',0),
 (146,145,'210 010 001 001 000','PD Cobros Anticipados',0),
 (147,76,'210 011 000 000 000','OTROS PASIVOS',0),
 (148,1,'','CAPITAL',0),
 (149,148,'300 000 000 000 000','CUENTAS DE CAPITAL CONTABLE',0),
 (150,148,'310 000 000 000 000','CUENTAS DE CAPITAL CONTABLE',0),
 (151,150,'310 001 000 000 000','CAPITAL CONTRIBUIDO',0),
 (152,151,'310 001 001 000 000','CC Capital Social Autorizado',0),
 (153,151,'310 001 002 000 000','CC Aporte para Fut Aumento de Cpital',0),
 (154,151,'310 001 003 000 000','CC Donaciones',0),
 (155,150,'310 002 000 000 000','RESERVAS',0),
 (156,155,'310 002 001 000 000','R Reserva Legal',0),
 (157,155,'310 002 002 000 000','R Rerservas Eventuales',0),
 (158,148,'320 000 000 000 000','CAPITAL  GANADO',0),
 (159,158,'320 001 000 000 000','CAPITAL',0),
 (160,159,'320 001 001 000 000','CG Utilidades y/o Perdidas Acumuladas',0),
 (161,159,'320 001 002 000 000','CG Ajuste por Revaluacion de Activo Fijo',0),
 (162,159,'320 001 003 000 000','CG Utilidades y/o Perdidas Netas del Ejerc',0),
 (163,159,'320 001 004 000 000','CG Ajuste a Periodos Anteriores',0),
 (164,159,'320 001 005 000 000','CG Ajuste por Deslizamiento Monetaria',0),
 (165,159,'320 001 006 000 000','CG Utilidad del Ejercicio PF 2003-2004',0),
 (166,159,'320 001 007 000 000','CG Utilidad del Ejercicio PF 2004-2005',0),
 (167,159,'320 001 008 000 000','CG Utilidad del Ejerecicio PF 2005-2006',0),
 (168,148,'999 000 000 000 000','SUPERÁVIT O (DÉFICIT) DEL PERÍODO',0),
 (169,1,'','INGRESOS CORRIENTES',0),
 (170,169,'410 000 000 000 000','INGRESOS POR VENTAS',0),
 (171,170,'410 001 000 000 000','IG. Ventas Brutas',0),
 (172,170,'410 002 000 000 000','IG. Devoluciones y Rebajas sobre Ventas',1),
 (173,170,'410 003 000 000 000','IG. Ventas Netas',0),
 (174,1,'','OTROS INGRESOS',0),
 (175,174,'420 000 000 000 000','OTROS INGRESOS',0),
 (176,175,'420 001 000 000 000','OI. Saldos Iniciales',0),
 (177,175,'420 002 000 000 000','OI. Ajuste de Precisión - Dólar',0),
 (178,175,'420 003 000 000 000','DESCUENTOS',1),
 (179,178,'420 003 001 000 000','Devoluciones y Rebajas sobre Compras',1),
 (180,1,'','GASTOS DE OPERACIONES',1),
 (181,180,'510 000 000 000 000','COSTOS Y GASTOS DE OPERACIONES',1),
 (182,181,'510 001 000 000 000','Costos de Ventas',1),
 (183,180,'610 000 000 000 000','GASTOS DE VENTAS',1),
 (184,183,'610 001 000 000 000','GASTOS DE VENTAS',1),
 (185,184,'610 001 001 000 000','GASTOS DE PERSONAL',1),
 (186,185,'610 001 001 001 000','GP Salario Personal de Venta',1),
 (187,185,'610 001 001 002 000','GP Viatico de Alimentacion',1),
 (188,185,'610 001 001 003 000','GP Viaticos (Alojamiento , Transpoprte, et',1),
 (189,185,'610 001 001 004 000','GP Horas Extras',1),
 (190,185,'610 001 001 005 000','GP Incentivos  Bonificaciones',1),
 (191,185,'610 001 001 006 000','GP Comisiones Sobre Venta',1),
 (192,185,'610 001 001 007 000','GV Vacaciones',1),
 (193,185,'610 001 001 008 000','GP  Aguinaldo',1),
 (194,185,'610 001 001 009 000','GP Indemnizacion por Ley',1),
 (195,185,'610 001 001 010 000','GP Utiles y Suministros de Cafeteria',1),
 (196,185,'610 001 001 011 000','GP Uniformes y Equipos de Seguridad',1),
 (197,185,'610 001 001 012 000','GPP Medicina y Suministros Clinicaos Medic',1),
 (198,185,'610 001 001 013 000','GP Productos y Obsequios al Personal',1),
 (199,185,'610 001 001 014 000','GP Reuniones y Celebraciones al Personal',1),
 (200,185,'610 001 001 015 000','GP Gastos Navideños',1),
 (201,185,'610 001 001 016 000','GP Otros Gastos del Personal',1),
 (202,185,'610 001 001 017 000','GP Aporte Patronal al INSS',1),
 (203,185,'610 001 001 018 000','GP Otras Prestaciones Sociales',1),
 (204,185,'610 001 001 019 000','GP Gastos de Representacion',1),
 (205,185,'610 001 001 020 000','GP Gastos de Capacitacion',1),
 (206,185,'610 001 001 021 000','GP. Saldos Iniciales',1),
 (207,184,'610 001 002 000 000','MATERIALES Y SUMINISTROS',1),
 (208,207,'610 001 002 001 000','MS Baterias, Llantas, Neumaticos, Rines',1),
 (209,207,'610 001 002 002 000','MS Piezas de Repuestos y Accesorios',1),
 (210,207,'610 001 002 003 000','MS Herramientas y utiles',1),
 (211,207,'610 001 002 004 000','MS Materiales para Aseo y Limpieza',1),
 (212,207,'610 001 002 005 000','MS Materiales y Utiles de Oficina',1),
 (213,207,'610 001 002 006 000','MS Materiales para Aseo y Limpieza de Vehi',1),
 (214,207,'610 001 002 007 000','MS Otros Materiales',1),
 (215,207,'610 001 002 008 000','GV. Gastos por Oferta',1),
 (216,184,'610 001 003 000 000','COMBUSTIBLES Y LUBRICANTES',1),
 (217,216,'610 001 003 001 000','CL Dissel y Gasolina',1),
 (218,216,'610 001 003 002 000','CL Aceites y Lubricantes',1),
 (219,216,'610 001 003 003 000','CL Otros Combustibles y Lubricantes',1),
 (220,184,'610 001 004 000 000','SERVICIOS COMPRADOS',1),
 (221,220,'610 001 004 001 000','SC Agua, Luz, Telefono y Correos',1),
 (222,220,'610 001 004 002 000','SC Fletes y  Acarreos',1),
 (223,220,'610 001 004 003 000','SC Servicios Comerciales y Bancarios',1),
 (224,220,'610 001 004 004 000','SC Publicidad y Propaganda',1),
 (225,220,'610 001 004 005 000','SC Alquileres y Arriendos',1),
 (226,220,'610 001 004 006 000','SC Servicios y Mant de Equipos de Oficina',1),
 (227,220,'610 001 004 007 000','SC Servicios y Mantenimiento de  Edificio',1),
 (228,220,'610 001 004 008 000','SC Servicios y Mantenimiento de Equipo Rod',1),
 (229,220,'610 001 004 009 000','SC Servicios de Fotocopias',1),
 (230,220,'610 001 004 010 000','SC Suscripciones',1),
 (231,220,'610 001 004 011 000','SC Poliza  de Seguro',1),
 (232,220,'610 001 004 012 000','SC Otros Servicios Comprados',1),
 (233,220,'610 001 004 013 000','SC Servicios Profesionales y Tecnicos',1),
 (234,220,'610 001 004 014 000','SC Servicios Prestados',1),
 (235,220,'610 001 004 015 000','SC Impuestos y Contribuciones',1),
 (236,184,'610 001 005 000 000','GASTOS DE INSTALACION',1),
 (237,184,'610 001 006 000 000','MEJORAS EN PROPIEDADES ARRENDADAS',1),
 (238,184,'610 001 007 000 000','DEPRECIACIONES',1),
 (239,238,'610 001 007 001 000','D Depreciacion  Acumulada de  Edificio',1),
 (240,238,'610 001 007 002 000','D Dep Acum de Prop Planta y Equipo',1),
 (241,238,'610 001 007 003 000','D Dep. Acum. de Equipo Rodante',1),
 (242,238,'610 001 007 004 000','D Dep. Acum de Comunicacion',1),
 (243,238,'610 001 007 005 000','D Dep Acum de Otros Activos',1),
 (244,184,'610 001 008 000 000','ESTIMACIONES DE COBRO DUDOSO',1),
 (245,244,'610 001 008 001 000','ECD Est. de Cobros Dudoso Cliente',1),
 (246,244,'610 001 008 002 000','ECD Est de Cobros Dudoso Doc por Cobrar',1),
 (247,1,'','GASTOS DE ADMINISTRACION',1),
 (248,247,'620 000 000 000 000','GASTOS DE ADMINISTRACION',1),
 (249,248,'620 001 000 000 000','GASTOS',1),
 (250,249,'620 001 001 000 000','GA Gastos del Personal',1),
 (251,250,'620 001 001 001 000','GP Salario Personal de Administracion',1),
 (252,250,'620 001 001 002 000','GP Viaticos de Alimentacion',1),
 (253,250,'620 001 001 003 000','GP Viaticos (Alojamiento, Transporte ,etc)',1),
 (254,250,'620 001 001 004 000','GP Horas Extras',1),
 (255,250,'620 001 001 005 000','GP Incentivos, Bonificaciones',1),
 (256,250,'620 001 001 006 000','GP Comisiones Sobre Ventas',1),
 (257,250,'620 001 001 007 000','GP  Vacaciones',1),
 (258,250,'620 001 001 008 000','GP Aguinaldo',1),
 (259,250,'620 001 001 009 000','GP Indemnizacion por Ley',1),
 (260,250,'620 001 001 010 000','GP Utiles y Suministros de Cafeteria',1),
 (261,250,'620 001 001 011 000','GP Uniforme & Equipo de Seguridad',1),
 (262,250,'620 001 001 012 000','GP Medicina y Suministros Clinica Medica',1),
 (263,250,'620 001 001 013 000','GP Productos y Obsequios al Personal',1),
 (264,250,'620 001 001 014 000','GP Reuniones y Celebraciones al Personal',1),
 (265,250,'620 001 001 015 000','GP Gastos Navideños',1),
 (266,250,'620 001 001 016 000','GP Otros Gastos del Personal',1),
 (267,250,'620 001 001 017 000','GP Aportes Patronal al INSS',1),
 (268,250,'620 001 001 018 000','GP Gastos de Capacitacion',1),
 (269,250,'620 001 001 019 000','GP Gastos de Representacion',1),
 (270,250,'620 001 001 020 000','GP Otras Prestaciones Sociales',1),
 (271,250,'620 001 001 021 000','GP. Saldos Iniciales',1),
 (272,249,'620 001 002 000 000','MATERIALES Y SUMINISTROS',1),
 (273,272,'620 001 002 001 000','MS Baterias, Llantas, Neumaticos, Rines',1),
 (274,272,'620 001 002 002 000','MS Pieza de Pespuestos y Accesorios',1),
 (275,272,'620 001 002 003 000','MS Herramientas y Utiles',1),
 (276,272,'620 001 002 004 000','MS Materiales para Aseo y Limpieza',1),
 (277,272,'620 001 002 005 000','MS Materiales y Utiles de Oficina',1),
 (278,272,'620 001 002 006 000','MS Materiales para Aseo y Limpieza de Vehi',1),
 (279,272,'620 001 002 007 000','MS Otros Materiales',1),
 (280,249,'620 001 003 000 000','COMBUSTIBLES Y LUBRICANTES',1),
 (281,280,'620 001 003 001 000','CL Diessel y Gasolina',1),
 (282,280,'620 001 003 002 000','CL Aceites y Lubricantes',1),
 (283,280,'620 001 003 003 000','CL Otros Combustibles y Lubricantes',1),
 (284,249,'620 001 004 000 000','SERVICIOS COMPRADOS',1),
 (285,284,'620 001 004 001 000','SC Agua, Luz, Teléfono, Correos',1),
 (286,284,'620 001 004 002 000','SC Fletes y Acarreos',1),
 (287,284,'620 001 004 003 000','SC Servicios Comerciales y Bancarios',1),
 (288,284,'620 001 004 004 000','SC Publicidad y Promocion',1),
 (289,284,'620 001 004 005 000','SC Alquileres y Arriendos',1),
 (290,284,'620 001 004 006 000','SC Servicios y Mant de Equip de Oficina',1),
 (291,284,'620 001 004 007 000','SC Servicios y Mantenimiento de Edificio',1),
 (292,284,'620 001 004 008 000','SC Servicio y Mantenimiento de Eqp Rodante',1),
 (293,284,'620 001 004 009 000','SC Servicios de Fotocopias',1),
 (294,284,'620 001 004 010 000','SC Suscripciones',1),
 (295,284,'620 001 004 011 000','SC Poliza de Seguros',1),
 (296,284,'620 001 004 012 000','SC Otros Servicios Comprados',1),
 (297,284,'620 001 004 013 000','SC Servicios Profesionales y Tecnicos',1),
 (298,284,'620 001 004 014 000','SC Servicios Prestados',1),
 (299,284,'620 001 004 015 000','SC Impuestos y Contribuciones (ALMA)',1),
 (300,249,'620 001 005 000 000','GASTOS DE INSTALACION',1),
 (301,249,'620 001 006 000 000','MEJORAS EN PROPIEDADES ARRENDADAS',1),
 (302,249,'620 001 007 000 000','DEPRECIACIONES',1),
 (303,302,'620 001 007 001 000','D Depreciaciones Acumuladas de Edificio',1),
 (304,302,'620 001 007 002 000','D Depreciacion Acumulada de Prop  Plat y E',1),
 (305,302,'620 001 007 003 000','D Dep Acumulada de Equipo Rodante',1),
 (306,302,'620 001 007 004 000','D Depreciacion  Acumulada de Comunicacion',1),
 (307,302,'620 001 007 005 000','D Depreciacion Acumulada de Otros Activos',1),
 (308,249,'620 001 008 000 000','ESTIMACIONES DE COBROS DUDOSOS',1),
 (309,308,'620 001 008 001 000','ECD Estrimaciones de Cobro Dudoso Cliente',1),
 (310,308,'620 001 008 002 000','ECD Est de Cobr Dudoso Doc por Cobrar',1),
 (311,249,'620 001 009 000 000','GASTOS DE ORGANIZACION',1),
 (312,249,'620 001 010 000 000','GASTOS DE CONSTITUCION',1),
 (313,1,'','GASTOS FINANCIEROS',1),
 (314,313,'630 000 000 000 000','GASTOS FINANCIEROS',1),
 (315,314,'630 001 000 000 000','GASTOS FINANCIEROS',1),
 (316,315,'630 001 001 000 000','GF Pago de Interes',1),
 (317,315,'630 001 002 000 000','GF GF Descuentos Concedidos',1),
 (318,315,'630 001 003 000 000','GF Comisiones Bancarias',1),
 (319,315,'630 001 004 000 000','GF Otros Gastos Financieros',1),
 (320,315,'630 001 005 000 000','GF. Saldos Iniciales',1),
 (321,1,'','PRODUCTOS FINANCIEROS',1),
 (322,321,'640 000 000 000 000','PRODUCTOS',1),
 (323,322,'640 001 000 000 000','PRODUCTOS FINANCIEROS',1),
 (324,323,'640 001 001 000 000','PF Cobro de Intereses',1),
 (325,323,'640 001 002 000 000','PF Descuentos Obtenidos',1),
 (326,1,'','OTROS GASTOS',1),
 (327,326,'650 000 000 000 000','OTROS GASTOS',1),
 (328,327,'650 001 000 000 000','OTROS GASTOS',1),
 (329,328,'650 001 001 000 000','OG Gastos de Atencion Social',1),
 (330,328,'650 001 002 000 000','OG Perdida por Baja de Activos Fijos',1),
 (331,328,'650 001 003 000 000','OG Multas , Indemnizacion y Compensaciones',1),
 (332,328,'650 001 004 000 000','OG Gastos de Representacion',1),
 (333,328,'650 001 005 000 000','OG Faltantes o Sobrantes',1),
 (334,328,'650 001 006 000 000','OG Robos o Perdidas',1),
 (335,328,'650 001 007 000 000','OG Otros Gastos no Especificados',1),
 (336,328,'650 001 008 000 000','OG. Saldos Iniciales',1),
 (337,328,'650 001 009 000 000','OG Ajuste por Precision - Córdobas',1),
 (338,1,'','CUENTAS DE ORDEN DEUDORA',1),
 (339,338,'810 000 000 000 000','CUENTAS DE ORDEN DEUDORA',1),
 (340,339,'810 001 000 000 000','SERVICIOS PROFESIONALES Y TECNICOS',1),
 (341,340,'810 001 004 000 000','SERVICIOS PROFESIONALES Y TECNICOS',1),
 (342,341,'810 001 004 013 000','Servicios profesionales y Tecnicos',1),
 (343,341,'810 001 004 014 000','Servicios Prestados',1),
 (344,339,'810 005 000 000 000','ANTICIPO DE ARRIENDO',1),
 (345,344,'810 005 007 000 000','ANTICIPO DE ARRIENDO',1),
 (346,345,'810 005 007 001 000','Antiicpo de Arriendo',1),
 (347,1,'','CUENTA DE ORDEN ACREEDORAS',0),
 (348,347,'910 000 000 000 000','CUENTAS DE ORDEN ACREEDORAS',0),
 (349,348,'910 001 000 000 000','SERVICIOS PROFESIONALES Y TECNICOS',0),
 (350,349,'910 001 004 000 000','SERVICIOS PROFESIONALES Y TECNICOS',0),
 (351,350,'910 001 004 013 000','Servicios Profesionales y Tecnicos',0),
 (352,350,'910 001 004 014 000','Servicios Prestados',0),
 (353,348,'910 005 000 000 000','ANTICIPO DE ARRIENDO',0),
 (354,353,'910 005 007 000 000','ANTICIPO DE ARRIENDO',0),
 (355,354,'910 005 007 001 000','Anticipo de Arriendo',0);
/*!40000 ALTER TABLE `cuentascontables` ENABLE KEYS */;


--
-- Definition of table `cuentasxdocumento`
--

DROP TABLE IF EXISTS `cuentasxdocumento`;
CREATE TABLE `cuentasxdocumento` (
  `idcuenta` int(10) unsigned NOT NULL COMMENT 'El id de la cuenta contable',
  `iddocumento` int(10) unsigned NOT NULL COMMENT 'El id del documento',
  `monto` decimal(12,4) NOT NULL COMMENT 'El monto que se afecta en este movimiento',
  `nlinea` smallint(6) DEFAULT NULL COMMENT 'Para ordenarlo en la interfaz grafica',
  PRIMARY KEY (`idcuenta`,`iddocumento`),
  KEY `fk_Documento_has_cuenta_cuenta1` (`idcuenta`),
  KEY `fk_documentoxcuenta_documento1` (`iddocumento`),
  CONSTRAINT `fk_documentoxcuenta_documento1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Documento_has_cuenta_cuenta1` FOREIGN KEY (`idcuenta`) REFERENCES `cuentascontables` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cuentasxdocumento`
--

/*!40000 ALTER TABLE `cuentasxdocumento` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuentasxdocumento` ENABLE KEYS */;


--
-- Definition of table `denominaciones`
--

DROP TABLE IF EXISTS `denominaciones`;
CREATE TABLE `denominaciones` (
  `iddenominacion` int(11) NOT NULL,
  `valor` float NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `idtipomoneda` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`iddenominacion`),
  KEY `fk_denominaciones_tiposmoneda1` (`idtipomoneda`),
  CONSTRAINT `fk_denominaciones_tiposmoneda1` FOREIGN KEY (`idtipomoneda`) REFERENCES `tiposmoneda` (`idtipomoneda`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `denominaciones`
--

/*!40000 ALTER TABLE `denominaciones` DISABLE KEYS */;
INSERT INTO `denominaciones` (`iddenominacion`,`valor`,`activo`,`idtipomoneda`) VALUES 
 (1,500,1,1),
 (2,200,1,1),
 (3,100,1,1),
 (4,50,1,1),
 (5,20,1,1),
 (6,10,1,1),
 (7,10,0,1),
 (8,5,0,1),
 (9,1,0,1),
 (10,0.5,0,1),
 (11,0.25,0,1),
 (12,0.1,0,1),
 (13,0.05,0,1),
 (14,100,1,2),
 (15,50,1,2),
 (16,20,1,2),
 (17,10,1,2),
 (18,5,1,2),
 (19,1,1,2);
/*!40000 ALTER TABLE `denominaciones` ENABLE KEYS */;


--
-- Definition of table `docpadrehijos`
--

DROP TABLE IF EXISTS `docpadrehijos`;
CREATE TABLE `docpadrehijos` (
  `idpadre` int(10) unsigned NOT NULL COMMENT 'El id del documento padre',
  `idhijo` int(10) unsigned NOT NULL COMMENT 'El id del documento hijo',
  `monto` decimal(12,4) unsigned DEFAULT NULL COMMENT 'El monto de esta relación',
  PRIMARY KEY (`idpadre`,`idhijo`) USING BTREE,
  KEY `fk_documento_has_documento_documento1` (`idpadre`) USING BTREE,
  KEY `fk_documento_has_documento_documento2` (`idhijo`) USING BTREE,
  CONSTRAINT `fk_documento_has_documento_documento1` FOREIGN KEY (`idpadre`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_documento_has_documento_documento2` FOREIGN KEY (`idhijo`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `docpadrehijos`
--

/*!40000 ALTER TABLE `docpadrehijos` DISABLE KEYS */;
/*!40000 ALTER TABLE `docpadrehijos` ENABLE KEYS */;


--
-- Definition of table `documentos`
--

DROP TABLE IF EXISTS `documentos`;
CREATE TABLE `documentos` (
  `iddocumento` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del documento',
  `ndocimpreso` varchar(20) NOT NULL COMMENT 'El numero de documento que el usuario ve',
  `total` decimal(12,4) NOT NULL COMMENT 'total en cordobas de doc como factura, entrada, salida',
  `fechacreacion` datetime NOT NULL COMMENT 'La fecha y hora en la que se creo este documento',
  `idtipodoc` int(10) unsigned NOT NULL COMMENT 'El id del tipo de documento',
  `observacion` varchar(100) DEFAULT NULL COMMENT 'Alguna observación que pueda tener el documento',
  `idtipocambio` mediumint(8) unsigned DEFAULT NULL COMMENT 'El id del tipo de cambio',
  `idbodega` int(10) unsigned DEFAULT NULL COMMENT 'El id de la bodega',
  `idconcepto` int(10) unsigned DEFAULT NULL COMMENT 'El concepto de este documento',
  `idcaja` tinyint(3) unsigned DEFAULT NULL COMMENT 'El id de la caja en la que se realizo este documento',
  `escontado` tinyint(1) DEFAULT '1' COMMENT 'Si este documento es de contado o credito',
  `anulado` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Anulacion de documentos como cheque factura y anular hijos',
  PRIMARY KEY (`iddocumento`),
  UNIQUE KEY `ndoc-unico` (`ndocimpreso`,`idtipodoc`),
  KEY `fk_documentos_cajas1` (`idcaja`),
  KEY `fk_documentos_tiposcambio1` (`idtipocambio`) USING BTREE,
  KEY `fk_documentos_bodegas1` (`idbodega`),
  KEY `fk_documentos_tiposdoc1` (`idtipodoc`),
  KEY `fk_documento_conceptos1` (`idconcepto`) USING BTREE,
  CONSTRAINT `fk_documentos_bodegas1` FOREIGN KEY (`idbodega`) REFERENCES `bodegas` (`idbodega`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_tiposcambio1` FOREIGN KEY (`idtipocambio`) REFERENCES `tiposcambio` (`idtc`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_documentos_tiposdoc1` FOREIGN KEY (`idtipodoc`) REFERENCES `tiposdoc` (`idtipodoc`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='Entrada y Salida de dinero y productos';

--
-- Dumping data for table `documentos`
--

/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
INSERT INTO `documentos` (`iddocumento`,`ndocimpreso`,`total`,`fechacreacion`,`idtipodoc`,`observacion`,`idtipocambio`,`idbodega`,`idconcepto`,`idcaja`,`escontado`,`anulado`) VALUES 
 (17,'1','10.0000','2010-06-30 22:55:44',22,'',242,NULL,NULL,1,1,0),
 (18,'2','-5.0000','2010-07-02 00:00:00',22,NULL,242,NULL,NULL,1,1,0);
/*!40000 ALTER TABLE `documentos` ENABLE KEYS */;


--
-- Definition of table `lineasarqueo`
--

DROP TABLE IF EXISTS `lineasarqueo`;
CREATE TABLE `lineasarqueo` (
  `idlineaarqueo` smallint(5) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la linea en el arqueo',
  `cantidad` smallint(5) unsigned NOT NULL COMMENT 'Las unidades en esta linea',
  `iddocumento` int(10) unsigned NOT NULL COMMENT 'El id del documento',
  `iddenominacion` int(11) NOT NULL,
  PRIMARY KEY (`idlineaarqueo`),
  KEY `fk_lineasarqueo_documentos1` (`iddocumento`),
  KEY `fk_lineasarqueo_denominaciones1` (`iddenominacion`),
  CONSTRAINT `fk_lineasarqueo_denominaciones1` FOREIGN KEY (`iddenominacion`) REFERENCES `denominaciones` (`iddenominacion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_lineasarqueo_documentos1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `lineasarqueo`
--

/*!40000 ALTER TABLE `lineasarqueo` DISABLE KEYS */;
/*!40000 ALTER TABLE `lineasarqueo` ENABLE KEYS */;


--
-- Definition of table `liquidaciones`
--

DROP TABLE IF EXISTS `liquidaciones`;
CREATE TABLE `liquidaciones` (
  `iddocumento` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del documento',
  `procedencia` varchar(45) NOT NULL COMMENT 'El país de procedencia de la liquidación',
  `totalagencia` decimal(12,4) NOT NULL COMMENT 'El total de agencia',
  `totalalmacen` decimal(12,4) NOT NULL COMMENT 'El total de almacen',
  `porcentajepapeleria` decimal(4,2) NOT NULL COMMENT 'El porcentaje papelería',
  `porcentajetransporte` decimal(4,2) NOT NULL COMMENT 'El porcentaje transporte',
  `peso` decimal(12,4) NOT NULL COMMENT 'El peso total ',
  `fletetotal` decimal(12,4) NOT NULL COMMENT 'El flete total',
  `segurototal` decimal(12,4) NOT NULL COMMENT 'El seguro total',
  `otrosgastos` decimal(12,4) NOT NULL COMMENT 'El total de otros gastos del documento',
  PRIMARY KEY (`iddocumento`),
  KEY `fk_liquidacion_documento1` (`iddocumento`),
  CONSTRAINT `fk_liquidacion_documento1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `liquidaciones`
--

/*!40000 ALTER TABLE `liquidaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `liquidaciones` ENABLE KEYS */;


--
-- Definition of table `marcas`
--

DROP TABLE IF EXISTS `marcas`;
CREATE TABLE `marcas` (
  `idmarca` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la marca',
  `nombre` varchar(25) DEFAULT NULL COMMENT 'El nombre de la marca',
  PRIMARY KEY (`idmarca`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `marcas`
--

/*!40000 ALTER TABLE `marcas` DISABLE KEYS */;
/*!40000 ALTER TABLE `marcas` ENABLE KEYS */;


--
-- Definition of table `modulos`
--

DROP TABLE IF EXISTS `modulos`;
CREATE TABLE `modulos` (
  `idmodulos` tinyint(3) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del modulo',
  `descripcion` varchar(20) NOT NULL COMMENT 'El nombre del modulo',
  PRIMARY KEY (`idmodulos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `modulos`
--

/*!40000 ALTER TABLE `modulos` DISABLE KEYS */;
INSERT INTO `modulos` (`idmodulos`,`descripcion`) VALUES 
 (1,'Compras'),
 (2,'Caja'),
 (3,'Contabilidad'),
 (4,'Inventario'),
 (5,'Administracion'),
 (6,'Reportes');
/*!40000 ALTER TABLE `modulos` ENABLE KEYS */;


--
-- Definition of table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
CREATE TABLE `pagos` (
  `recibo` int(10) unsigned NOT NULL COMMENT 'El id del documento recibo',
  `tipopago` tinyint(3) unsigned NOT NULL COMMENT 'El tipo de pago',
  `tipomoneda` tinyint(3) unsigned NOT NULL COMMENT 'El id del tipo de moneda',
  `monto` decimal(12,4) NOT NULL COMMENT 'El monto de este pago',
  `refexterna` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`recibo`,`tipopago`,`tipomoneda`),
  KEY `fk_pago_tipopago1` (`tipopago`),
  KEY `fk_pago_tipomoneda1` (`tipomoneda`),
  KEY `fk_pago_documento1` (`recibo`),
  CONSTRAINT `fk_pago_documento1` FOREIGN KEY (`recibo`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pago_tipomoneda1` FOREIGN KEY (`tipomoneda`) REFERENCES `tiposmoneda` (`idtipomoneda`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pago_tipopago1` FOREIGN KEY (`tipopago`) REFERENCES `tipospago` (`idtipopago`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pagos`
--

/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;


--
-- Definition of table `personas`
--

DROP TABLE IF EXISTS `personas`;
CREATE TABLE `personas` (
  `idpersona` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id de la persona',
  `nombre` varchar(100) NOT NULL COMMENT 'El nombre de la persona',
  `fechaIngreso` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'La fecha de ingreso al sistema',
  `telefono` varchar(45) DEFAULT NULL COMMENT 'El telefóno de la persona',
  `email` varchar(45) DEFAULT NULL COMMENT 'El e-mail de la persona',
  `ruc` varchar(20) DEFAULT NULL COMMENT 'EL numero de RUC de la persona\n',
  `activo` tinyint(1) NOT NULL COMMENT 'Si una persona esta activa o no',
  `tipopersona` tinyint(4) NOT NULL COMMENT '1 cliente 2 proveedor, 3 vendedor, 4 usuario\n',
  `idcuenta` int(10) unsigned DEFAULT NULL COMMENT 'El id de la cuenta de esta persona',
  PRIMARY KEY (`idpersona`),
  UNIQUE KEY `nombre_unico` (`nombre`,`tipopersona`) USING BTREE,
  KEY `fk_personas_cuentascontables1` (`idcuenta`),
  CONSTRAINT `fk_personas_cuentascontables1` FOREIGN KEY (`idcuenta`) REFERENCES `cuentascontables` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `personas`
--

/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` (`idpersona`,`nombre`,`fechaIngreso`,`telefono`,`email`,`ruc`,`activo`,`tipopersona`,`idcuenta`) VALUES 
 (1,'Administrador','2010-06-30 22:38:57',NULL,NULL,NULL,1,4,NULL);
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;


--
-- Definition of trigger `tr_validarnombre`
--

DROP TRIGGER /*!50030 IF EXISTS */ `tr_validarnombre`;

DELIMITER $$

CREATE DEFINER = `root`@`localhost` TRIGGER `tr_validarnombre` BEFORE INSERT ON `personas` FOR EACH ROW BEGIN

    IF NEW.nombre ='' THEN
       SET NEW = NULL;
    END IF;

END $$

DELIMITER ;

--
-- Definition of table `personasxdocumento`
--

DROP TABLE IF EXISTS `personasxdocumento`;
CREATE TABLE `personasxdocumento` (
  `iddocumento` int(10) unsigned NOT NULL,
  `idpersona` int(10) unsigned NOT NULL,
  PRIMARY KEY (`iddocumento`,`idpersona`),
  KEY `fk_documentos_has_personas_documentos1` (`iddocumento`),
  KEY `fk_documentos_has_personas_personas1` (`idpersona`),
  CONSTRAINT `fk_documentos_has_personas_documentos1` FOREIGN KEY (`iddocumento`) REFERENCES `documentos` (`iddocumento`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_has_personas_personas1` FOREIGN KEY (`idpersona`) REFERENCES `personas` (`idpersona`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `personasxdocumento`
--

/*!40000 ALTER TABLE `personasxdocumento` DISABLE KEYS */;
INSERT INTO `personasxdocumento` (`iddocumento`,`idpersona`) VALUES 
 (17,1);
/*!40000 ALTER TABLE `personasxdocumento` ENABLE KEYS */;


--
-- Definition of table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `idrol` tinyint(3) unsigned NOT NULL COMMENT 'El id del rol',
  `nombre` varchar(40) NOT NULL COMMENT 'El nombre del rol,\nesto es usado por el \nsistema a nivel interno',
  `descripcion` varchar(200) NOT NULL,
  `idmodulo` tinyint(3) unsigned NOT NULL COMMENT 'El id del modulo al que sirve este rol',
  PRIMARY KEY (`idrol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `roles`
--

/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`idrol`,`nombre`,`descripcion`,`idmodulo`) VALUES 
 (1,'root','Administrador del Sistema',0),
 (2,'gerencia','Gerencia Esquipulas',0),
 (3,'caja','Usuario de Caja',0),
 (4,'inventario','Usuario de Inventario',0),
 (5,'contabilidad','Usuario de Contabilidad',0),
 (6,'inventariorep','Reportes de Inventario',0),
 (7,'contabilidadrep','Reportes de Contabilidad',0),
 (8,'ventasrep','Reportes de Ventas',0);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;


--
-- Definition of table `tiposcambio`
--

DROP TABLE IF EXISTS `tiposcambio`;
CREATE TABLE `tiposcambio` (
  `idtc` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de cambio',
  `tasa` decimal(8,4) unsigned NOT NULL COMMENT 'La tasa de cambio oficial',
  `fecha` date NOT NULL COMMENT 'La fecha para este tipo de cambio',
  `tasabanco` decimal(8,4) DEFAULT NULL COMMENT 'La tasa del banco, definida por el usuario',
  PRIMARY KEY (`idtc`),
  UNIQUE KEY `fechaunica` (`fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tiposcambio`
--

/*!40000 ALTER TABLE `tiposcambio` DISABLE KEYS */;
INSERT INTO `tiposcambio` (`idtc`,`tasa`,`fecha`,`tasabanco`) VALUES 
 (213,'21.2683','2010-06-01',NULL),
 (214,'21.3110','2010-06-16',NULL),
 (215,'21.2711','2010-06-02',NULL),
 (216,'21.3138','2010-06-17',NULL),
 (217,'21.2740','2010-06-03',NULL),
 (218,'21.3167','2010-06-18',NULL),
 (219,'21.2768','2010-06-04',NULL),
 (220,'21.3195','2010-06-19',NULL),
 (221,'21.2797','2010-06-05',NULL),
 (222,'21.3224','2010-06-20',NULL),
 (223,'21.2825','2010-06-06',NULL),
 (224,'21.3252','2010-06-21',NULL),
 (225,'21.2853','2010-06-07',NULL),
 (226,'21.3281','2010-06-22',NULL),
 (227,'21.2882','2010-06-08',NULL),
 (228,'21.3309','2010-06-23',NULL),
 (229,'21.2910','2010-06-09',NULL),
 (230,'21.3338','2010-06-24',NULL),
 (231,'21.2939','2010-06-10',NULL),
 (232,'21.3366','2010-06-25',NULL),
 (233,'21.2967','2010-06-11',NULL),
 (234,'21.3395','2010-06-26',NULL),
 (235,'21.2996','2010-06-12',NULL),
 (236,'21.3423','2010-06-27',NULL),
 (237,'21.3024','2010-06-13',NULL),
 (238,'21.3452','2010-06-28',NULL),
 (239,'21.3053','2010-06-14',NULL),
 (240,'21.3480','2010-06-29',NULL),
 (241,'21.3081','2010-06-15',NULL),
 (242,'21.3509','2010-06-30',NULL);
/*!40000 ALTER TABLE `tiposcambio` ENABLE KEYS */;


--
-- Definition of table `tiposcosto`
--

DROP TABLE IF EXISTS `tiposcosto`;
CREATE TABLE `tiposcosto` (
  `idtipocosto` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de costo',
  `descripcion` varchar(45) NOT NULL COMMENT 'La descripción del tipo de costo',
  `esporcentaje` tinyint(1) NOT NULL COMMENT 'Si este costo es porcentaje o es un valor fijo',
  `cuentacontable` int(10) unsigned DEFAULT NULL COMMENT 'La cuenta contable del tipo de costo',
  PRIMARY KEY (`idtipocosto`),
  KEY `FK_tipocosto_CuentaContable` (`cuentacontable`),
  CONSTRAINT `FK_tipocosto_CuentaContable` FOREIGN KEY (`cuentacontable`) REFERENCES `cuentascontables` (`idcuenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tiposcosto`
--

/*!40000 ALTER TABLE `tiposcosto` DISABLE KEYS */;
/*!40000 ALTER TABLE `tiposcosto` ENABLE KEYS */;


--
-- Definition of table `tiposdoc`
--

DROP TABLE IF EXISTS `tiposdoc`;
CREATE TABLE `tiposdoc` (
  `idtipodoc` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de costo',
  `codigodoc` varchar(2) NOT NULL COMMENT 'El codigo del tipo de documento',
  `descripcion` varchar(45) NOT NULL COMMENT 'La descripción del tipo de costo',
  `modulo` tinyint(3) unsigned NOT NULL COMMENT 'El modulo en el quee ste documento se utiliza',
  PRIMARY KEY (`idtipodoc`) USING BTREE,
  KEY `fk_tipodoc_modulos1` (`modulo`),
  CONSTRAINT `fk_tipodoc_modulos1` FOREIGN KEY (`modulo`) REFERENCES `modulos` (`idmodulos`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tiposdoc`
--

/*!40000 ALTER TABLE `tiposdoc` DISABLE KEYS */;
INSERT INTO `tiposdoc` (`idtipodoc`,`codigodoc`,`descripcion`,`modulo`) VALUES 
 (1,'AE','AJUSTE DE ENTRADA',1),
 (2,'AF','ANULACION DE FACTURA',1),
 (3,'AS','AJUSTE DE SALIDA',1),
 (4,'EM','AJUSTE DE MONTO DE ENTRADA',1),
 (5,'FA','FACTURA',1),
 (6,'DT','DEPOSITO EN TRANSITO',1),
 (7,'IB','INGRESO A BODEGA',1),
 (8,'MS','AJUSTE DE MONTO DE SALIDA',1),
 (9,'SI','SALDO INICIAL',1),
 (10,'DV','DEVOLUCIONES',1),
 (11,'ND','NOTAS DE DEBITOS',1),
 (12,'CK','CHEQUES ',1),
 (13,'DP','DEPOSITOS',1),
 (14,'AD','AJUSTE DE DEBITO',1),
 (15,'AC','AJUSTE DE CREDITO',1),
 (16,'NC','NOTA DE CREDITO',1),
 (17,'CS','CIERRE DE SESION',2),
 (18,'RC','RECIBO',2),
 (19,'IR','CONSTANCIA DE RETENCION',2),
 (20,'IS','INICIO DE SESION',2),
 (21,'EC','ENTRADA DE COMPRAS LOCALES A BODEGA',1),
 (22,'CA','APERTURA DE CAJA',2),
 (23,'AR','ARQUEO',2),
 (24,'CB','CONCILIACION BANCARIA',3);
/*!40000 ALTER TABLE `tiposdoc` ENABLE KEYS */;


--
-- Definition of table `tiposmoneda`
--

DROP TABLE IF EXISTS `tiposmoneda`;
CREATE TABLE `tiposmoneda` (
  `idtipomoneda` tinyint(3) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de moneda',
  `moneda` varchar(45) NOT NULL COMMENT 'El nombre del tipo de moneda',
  PRIMARY KEY (`idtipomoneda`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tiposmoneda`
--

/*!40000 ALTER TABLE `tiposmoneda` DISABLE KEYS */;
INSERT INTO `tiposmoneda` (`idtipomoneda`,`moneda`) VALUES 
 (1,'CORDOBAS'),
 (2,'DOLARES');
/*!40000 ALTER TABLE `tiposmoneda` ENABLE KEYS */;


--
-- Definition of table `tipospago`
--

DROP TABLE IF EXISTS `tipospago`;
CREATE TABLE `tipospago` (
  `idtipopago` tinyint(3) unsigned NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de pago',
  `descripcion` varchar(45) DEFAULT NULL COMMENT 'La descripción de este tipo de pago',
  PRIMARY KEY (`idtipopago`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tipospago`
--

/*!40000 ALTER TABLE `tipospago` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipospago` ENABLE KEYS */;


--
-- Definition of table `tsim`
--

DROP TABLE IF EXISTS `tsim`;
CREATE TABLE `tsim` (
  `idtsim` int(10) unsigned NOT NULL COMMENT 'El id del TSIM',
  `factorpeso` decimal(10,4) NOT NULL COMMENT 'El factor peso de este TSIM',
  PRIMARY KEY (`idtsim`),
  CONSTRAINT `FK_tsim_1` FOREIGN KEY (`idtsim`) REFERENCES `costosagregados` (`idcostoagregado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

--
-- Dumping data for table `tsim`
--

/*!40000 ALTER TABLE `tsim` DISABLE KEYS */;
/*!40000 ALTER TABLE `tsim` ENABLE KEYS */;


--
-- Definition of table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `idusuario` int(10) unsigned NOT NULL COMMENT 'El id del usuario',
  `username` varchar(15) NOT NULL COMMENT 'El nombre de usuario',
  `password` varchar(50) NOT NULL COMMENT 'La contraseña de este usuario',
  `estado` tinyint(1) NOT NULL COMMENT 'El estado de este usuario, habilitado o deshabilitado',
  `tipousuario` tinyint(2) NOT NULL COMMENT 'El tipo de usuario',
  PRIMARY KEY (`idusuario`),
  KEY `fk_usuarios_personas1` (`idusuario`),
  CONSTRAINT `fk_usuarios_personas1` FOREIGN KEY (`idusuario`) REFERENCES `personas` (`idpersona`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `usuarios`
--

/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`idusuario`,`username`,`password`,`estado`,`tipousuario`) VALUES 
 (1,'root','e558b0a1f46f6922ed725bfb2e77bcd17d34c9d9',1,1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;


--
-- Definition of table `usuarios_has_roles`
--

DROP TABLE IF EXISTS `usuarios_has_roles`;
CREATE TABLE `usuarios_has_roles` (
  `idusuario` int(10) unsigned NOT NULL,
  `idrol` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`idusuario`,`idrol`),
  KEY `fk_usuarios_has_roles_usuarios1` (`idusuario`),
  KEY `fk_usuarios_has_roles_roles1` (`idrol`),
  CONSTRAINT `fk_usuarios_has_roles_roles1` FOREIGN KEY (`idrol`) REFERENCES `roles` (`idrol`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_roles_usuarios1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `usuarios_has_roles`
--

/*!40000 ALTER TABLE `usuarios_has_roles` DISABLE KEYS */;
INSERT INTO `usuarios_has_roles` (`idusuario`,`idrol`) VALUES 
 (1,1);
/*!40000 ALTER TABLE `usuarios_has_roles` ENABLE KEYS */;


--
-- Definition of procedure `spAgregarArticulos`
--

DROP PROCEDURE IF EXISTS `spAgregarArticulos`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spAgregarArticulos`(IN activo TINYINT,IN marca INTEGER, IN subcategoria INTEGER, IN dai INTEGER, IN isc INTEGER, IN comision INTEGER, IN tasaganancia INTEGER)
BEGIN

       START TRANSACTION;

            INSERT INTO articulos (activo,idmarca,idcategoria,ganancia) VALUES (activo,marca,subcategoria, tasaganancia);
            SET @ultimoarticulo := LAST_INSERT_ID();
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(dai,1,3,@ultimoarticulo);
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(comision,1,7,@ultimoarticulo);
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(isc,1,2,@ultimoarticulo);

       COMMIT;

END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spEntradasCompraDetalladas`
--

DROP PROCEDURE IF EXISTS `spEntradasCompraDetalladas`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`armonge-laptop.lan` PROCEDURE `spEntradasCompraDetalladas`(in iddoc int)
BEGIN
       if iddoc is not null  then
	SET @subtotal = (
		SELECT SUM(axd.unidades * axd.costounit) AS subtotal
		FROM articulosxdocumento axd
		WHERE axd.iddocumento = iddoc
	);
	SET @iva =(
		SELECT @subtotal * ( ca.valorcosto / 100) AS IVA
		FROM costosagregados ca
		JOIN costosxdocumento cxd ON cxd.idcostoagregado = ca.idcostoagregado
		JOIN documentos d ON cxd.iddocumento = d.iddocumento
		WHERE d.iddocumento = iddoc
	);

	SELECT  
		d.ndocimpreso,
		d.fechacreacion,
		p.nombre AS Proveedor,
		d.observacion,
		@subtotal AS subtotal,
		@iva AS IVA,
		@subtotal + @iva AS total	
	FROM documentos d  
	JOIN personas p ON d.idpersona = p.idpersona    
	WHERE  d.iddocumento = iddoc; 
	


        SELECT 
		a.idarticulo AS id,  
		CONCAT(m.nombre,' ' , c.nombre, ' ' , subc.nombre) AS descripcion,  
		b.nombrebodega AS Bodega,  
		axd.unidades AS Cantidad,   
		axd.costounit AS Precio,  
		(axd.unidades * axd.costounit) AS totalprod
	FROM documentos d  
	JOIN articulosxdocumento axd ON axd.iddocumento=d.iddocumento  
	JOIN articulos a ON a.idarticulo = axd.idarticulo  
	JOIN marcas m ON m.idmarca = a.idmarca  
	JOIN categorias subc ON a.idcategoria = subc.idcategoria  
	JOIN categorias c ON subc.padre = c. idcategoria  
	JOIN bodegas b ON axd.idbodega = b.idbodega  
	WHERE  d.iddocumento = iddoc;

 
        end if;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spEntradasCompraDetalladasParaSalida`
--

DROP PROCEDURE IF EXISTS `spEntradasCompraDetalladasParaSalida`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`armonge-laptop.lan` PROCEDURE `spEntradasCompraDetalladasParaSalida`(in iddoc int)
BEGIN
       if iddoc is not null  then
	
	SELECT  
		d.idpersona,
		p.nombre
	FROM documentos d
	JOIN personas p ON d.idpersona = p.idpersona
	WHERE d.iddocumento = iddoc;

	
	SELECT 
		axd.idarticulo, 
		ad.descripcion , 
		axd.costounit, 
		b.idbodega, 
		b.nombrebodega,  
		IF(inv.unidades < axd.unidades, inv.unidades, axd.unidades) AS unidades
	FROM articulosxdocumento axd
	JOIN (
		SELECT 	
			idarticulo, 
			SUM(unidades) AS unidades 
		FROM articulosxdocumento axd 
		WHERE axd.iddocumento = iddoc 
		GROUP BY idarticulo
	) AS inv ON inv.idarticulo = axd.idarticulo
	JOIN vw_articulosdescritos ad ON axd.idarticulo = ad.idarticulo
	JOIN bodegas b ON axd.idbodega = b.idbodega
	WHERE axd.iddocumento = iddoc;
	
	end if;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spLiquidacion_Abrir`
--

DROP PROCEDURE IF EXISTS `spLiquidacion_Abrir`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spLiquidacion_Abrir`(in iddoc int)
BEGIN
       if iddoc is not null then
        SELECT * FROM vw_liquidacionesguardadas v WHERE iddocumento=iddoc;

               SELECT c.idcostoagregado,ca.valorcosto, t.factorpeso,ca.idtipocosto FROM costosxdocumento c JOIN costosagregados ca ON c.idcostoagregado=ca.idcostoagregado left JOIN tsim t ON t.idtsim=c.idcostoagregado WHERE c.iddocumento=iddoc;

                SELECT v.idarticulo,v.descripcion,v.dai,v.isc,v.comision,a.unidades,a.costocompra AS punit,a.unidades*a.costocompra AS fob,v.comision*a.unidades AS comision, a.idbodega, b.nombrebodega FROM vw_articulosconcostosactuales v JOIN articulosxdocumento a ON v.idarticulo=a.idarticulo JOIN bodegas b ON b.idbodega=a.idbodega WHERE iddocumento=iddoc order by a.nlinea;

                SELECT c.codigo AS Cuenta,c.Descripcion,FORMAT(d.monto,4) AS 'Monto C$' FROM documentoxcuenta d JOIN cuentacontable c ON d.idcuenta=c.idcuenta WHERE iddocumento=iddoc order by d.nlinea;
        end if;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spLiquidacion_Guardar`
--

DROP PROCEDURE IF EXISTS `spLiquidacion_Guardar`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spLiquidacion_Guardar`(IN docImpreso NVARCHAR(20),IN iduser INT,IN tc INT, IN idproveedor int, in procedencia varchar(45),in agencia decimal(12,4),in almacen decimal(12,4),in papeleria decimal(4,2),in transporte decimal(4,2),IN peso DECIMAL(12,4),in flete decimal(12,4),in seguro decimal(12,4),in gastos decimal(12,4),in tsim int,IN spe int,in iva int,  in iso int, IN totaldoc DECIMAL(12,4))
BEGIN
        DECLARE iddoc INT;
                 SELECT MAX(iddocumento)+1 FROM documentos INTO @iddoc;

                IF (@iddoc IS NULL) THEN
               SET @iddoc=1;
       END IF;

              INSERT INTO documentos (iddocumento,ndocimpreso,fechacreacion,idtipodoc,idusuario,idtipocambio,idpersona,anulado,total)
       VALUES(@iddoc,docImpreso,NOW(),7,iduser,tc,idproveedor,0,totaldoc);

               INSERT INTO liquidaciones VALUES(@iddoc,procedencia,agencia,almacen,papeleria,transporte,peso,flete,seguro,gastos);

                INSERT INTO costosxdocumento VALUES(@iddoc,tsim);
                INSERT INTO costosxdocumento VALUES(@iddoc,spe);

                IF iva IS NOT NULL THEN
          INSERT INTO costosxdocumento VALUES(@iddoc,iva);         END IF;
                IF iso IS NOT NULL THEN
          INSERT INTO costosxdocumento VALUES(@iddoc,iso);         END IF;



                 SELECT @iddoc;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spLiquidacion_Iniciar`
--

DROP PROCEDURE IF EXISTS `spLiquidacion_Iniciar`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spLiquidacion_Iniciar`()
BEGIN
    SELECT idbodega AS Id, nombrebodega AS Bodega FROM bodegas;

    SELECT idpersona AS Id,nombre AS Proveedor FROM personas WHERE tipopersona=2;

    SELECT CAST(idarticulo AS CHAR) AS Id, Descripcion AS 'Articulo',CAST( dai AS CHAR) AS dai,CAST( isc AS CHAR) AS isc,CAST(comision AS CHAR) AS comision FROM vw_articulosconcostosactuales;

    SELECT Codigo AS Id,Descripcion, idcuenta FROM cuentascontables c WHERE padre<>1;

    SELECT c.idcostoagregado,valorcosto,factorpeso,idtipocosto FROM costosagregados c left JOIN tsim t ON c.idcostoagregado=t.idtsim WHERE activo=1 AND idtipocosto in (1,4,5,6) ;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spmovimientocuentabanco`
--

DROP PROCEDURE IF EXISTS `spmovimientocuentabanco`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spmovimientocuentabanco`( IN idcuenta INT,IN fecha DATETIME)
BEGIN

      DECLARE saldoinicial DECIMAL(12,4);
      DECLARE iddoc  INTEGER;


		SELECT
        d.iddocumento,
        total as SaldoInicial
    FROM cuentasxdocumento cdoc
    JOIN documentos d ON d.iddocumento=cdoc.iddocumento
    WHERE cdoc.idcuenta=2 and d.idtipodoc=24
    ORDER BY d.iddocumento desc
    INTO @iddoc, @saldoinicial;

    SELECT * FROM documentos
    JOIN (SELECT @iddoc,@saldoinicial) saldos
   ;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spSalidasBodegaDetalladas`
--

DROP PROCEDURE IF EXISTS `spSalidasBodegaDetalladas`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`armonge-laptop.lan` PROCEDURE `spSalidasBodegaDetalladas`(in iddoc int)
BEGIN
       if iddoc is not null  then

	SELECT  
		d.ndocimpreso,
		d.fechacreacion,
		p.nombre AS Proveedor,
		d.observacion,
		SUM(axd.unidades * axd.costounit) AS subtotal,
		(SUM(axd.unidades * axd.costounit) * (ca.valorcosto / 100) ) AS IVA,
		(SUM(axd.unidades * axd.costounit) * 1+(ca.valorcosto / 100) ) AS total	
	FROM documentos d  
	JOIN personas p ON d.idpersona = p.idpersona  
	JOIN articulosxdocumento axd ON axd.iddocumento=d.iddocumento  
	JOIN articulos a ON a.idarticulo = axd.idarticulo  
	JOIN costosxdocumento cxd ON d.iddocumento = cxd.iddocumento  
	JOIN costosagregados ca ON cxd.idcostoagregado = ca.idcostoagregado  
	WHERE  d.iddocumento = iddoc; 
	


        SELECT 
		a.idarticulo AS id,  
		CONCAT(m.nombre,' ' , c.nombre, ' ' , subc.nombre) AS descripcion,  
		b.nombrebodega AS Bodega,
		axd.unidades AS Cantidad,   
		axd.costounit AS 'Precio',  
		(axd.unidades * axd.costounit) AS totalprod
	FROM documentos d  
	JOIN articulosxdocumento axd ON axd.iddocumento=d.iddocumento  
	JOIN articulos a ON a.idarticulo = axd.idarticulo  
	JOIN marcas m ON m.idmarca = a.idmarca  
	JOIN categorias subc ON a.idcategoria = subc.idcategoria  
	JOIN categorias c ON subc.padre = c. idcategoria  
	JOIN bodegas b ON axd.idbodega = b.idbodega  
	WHERE  d.iddocumento = iddoc;

 
        end if;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `spVercostoArticulo`
--

DROP PROCEDURE IF EXISTS `spVercostoArticulo`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `spVercostoArticulo`( IN idarticulo INT,IN idtc INT)
BEGIN

      DECLARE costo DECIMAL(12,4);
      DECLARE idtc  INTEGER;
	    DECLARE tasa DECIMAL(12,4);

		SELECT idtipocambio,tasa FROM documentos WHERE idtipocambio=idtc INTO @idtc, @tasa;
        SELECT SUM((unidades*costounit * @tasa))/SUM(unidades)  FROM articulosxdocumento a WHERE a.idarticulo=idarticulo INTO @costo;



        IF @costo IS NULL THEN
          SET @costo=0;
       END IF;

        SELECT @costo;


END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of procedure `sp_ArticulosProrrateados`
--

DROP PROCEDURE IF EXISTS `sp_ArticulosProrrateados`;

DELIMITER $$

/*!50003 SET @TEMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,STRICT_ALL_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,TRADITIONAL,NO_AUTO_CREATE_USER' */ $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_ArticulosProrrateados`()
BEGIN
  SELECT
a.idarticulo
,a.unidades
,a.costocompra
,@fob:=(a.unidades * a.costocompra) as fob
,@flete:=(l.fletetotal / f.fobt) * @fob as flete
,@seguro:=(l.segurototal / f.fobt) * @fob as seguro
,@ogastos:=(l.otrosgastos / f.fobt) * @fob as 'otros gastos'
,@cif:=(@fob+@flete+@seguro+@ogastos) as cif

,@impuesto:=(
    cal.dai+
    cal.isc+
    (costos.iso*@cif)+
    (costos.tsim * CEILING(l.peso/costos.factorpeso)/cift.total*@cif)+
    costos.spe/cift.total*@cif +
    (costos.iva*(@cif + cal.dai + cal.isc + (costos.tsim * CEILING(l.peso/costos.factorpeso)/cift.total*@cif))
    )) as impuesto

,cal.comision
,@agencia:=(l.totalagencia / cift.total) * @cif as agencia
,@almacen:=(l.totalalmacen / cift.total) * @cif as almacen
,@pap:=(l.porcentajepapeleria /100) * a.unidades as papeleria
,@trans:=(l.porcentajetransporte /100) * a.unidades as transporte
,@total:=@cif+@impuesto+cal.comision+@agencia+@almacen+@pap+@trans as total
,@total*tc.tasa as 'total C$'
,cift.total

from articulosxdocumento a
join liquidaciones l on l.iddocumento=a.iddocumento
join costosxarticuloliquidacion cal on cal.idarticuloxdocumento=a.idarticuloxdocumento
JOIN (SELECT SUM(unidades*costocompra) as fobt FROM articulosxdocumento where iddocumento=228 group by iddocumento) f
JOIN
(
SELECT
sum(if(c.idtipocosto=1,valorcosto,0))/100 as iva
,sum(if(c.idtipocosto=4,valorcosto,0)) as spe
,sum(if(c.idtipocosto=5,valorcosto,0)) as tsim
,sum(if(c.idtipocosto=5,factorpeso,0)) as factorpeso
,sum(if(c.idtipocosto=6,valorcosto,0))/100 as iso
FROM costosagregados c
left join tsim t on c.idcostoagregado=t.idtsim and c.idtipocosto in (1,4,5,6)
join costosxdocumento cd on c.idcostoagregado=cd.idcostoagregado where cd.iddocumento=228
) costos

JOIN documentos d on d.iddocumento=l.iddocumento
JOIN tiposcambio tc on tc.idtc=d.idtipocambio
join

(SELECT sum((a.unidades*a.costocompra) + (l.fletetotal+l.segurototal+l.otrosgastos) * ((a.unidades*a.costocompra)/f.fobt)) as total
from articulosxdocumento a
join liquidaciones l on l.iddocumento=a.iddocumento and l.iddocumento=228
JOIN (SELECT SUM(unidades*costocompra) as fobt FROM articulosxdocumento where iddocumento=228 group by iddocumento) f) cift

WHERE a.iddocumento=228
order by a.nlinea ;
END $$
/*!50003 SET SESSION SQL_MODE=@TEMP_SQL_MODE */  $$

DELIMITER ;

--
-- Definition of view `vw_articulosconcostosactuales`
--

DROP TABLE IF EXISTS `vw_articulosconcostosactuales`;
DROP VIEW IF EXISTS `vw_articulosconcostosactuales`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_articulosconcostosactuales` AS select `a`.`idarticulo` AS `idarticulo`,concat(`cat`.`nombre`,' ',`subcat`.`nombre`,' ',`m`.`nombre`) AS `descripcion`,sum(if((`ca`.`idtipocosto` = 3),`ca`.`valorcosto`,0)) AS `dai`,sum(if((`ca`.`idtipocosto` = 2),`ca`.`valorcosto`,0)) AS `isc`,sum(if((`ca`.`idtipocosto` = 7),`ca`.`valorcosto`,0)) AS `comision`,`a`.`ganancia` AS `ganancia`,`a`.`activo` AS `activo` from ((((`articulos` `a` join `categorias` `subcat` on((`a`.`idcategoria` = `subcat`.`idcategoria`))) join `categorias` `cat` on((`subcat`.`padre` = `cat`.`idcategoria`))) join `marcas` `m` on((`m`.`idmarca` = `a`.`idmarca`))) join `costosagregados` `ca` on((`ca`.`idarticulo` = `a`.`idarticulo`))) where (`ca`.`activo` = 1) group by `a`.`idarticulo`;

--
-- Definition of view `vw_articulosdescritos`
--

DROP TABLE IF EXISTS `vw_articulosdescritos`;
DROP VIEW IF EXISTS `vw_articulosdescritos`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_articulosdescritos` AS select `a`.`idarticulo` AS `idarticulo`,concat(`c`.`nombre`,' ',`sc`.`nombre`,' ',`m`.`nombre`) AS `descripcion`,`c`.`idcategoria` AS `idcategoria`,`c`.`nombre` AS `categorias`,`sc`.`idcategoria` AS `idsubcategoria`,`sc`.`nombre` AS `subcategoria`,`m`.`idmarca` AS `idmarca`,`m`.`nombre` AS `marcas`,`a`.`activo` AS `activo`,`a`.`ganancia` AS `ganancia` from (((`articulos` `a` join `marcas` `m` on((`a`.`idmarca` = `m`.`idmarca`))) join `categorias` `sc` on((`a`.`idcategoria` = `sc`.`idcategoria`))) join `categorias` `c` on((`c`.`idcategoria` = `sc`.`padre`)));

--
-- Definition of view `vw_articulosprorrateados`
--

DROP TABLE IF EXISTS `vw_articulosprorrateados`;
DROP VIEW IF EXISTS `vw_articulosprorrateados`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_articulosprorrateados` AS select `a`.`idarticulo` AS `idarticulo`,`a`.`unidades` AS `unidades`,`a`.`costocompra` AS `costocompra`,(`a`.`unidades` * `a`.`costocompra`) AS `fob`,((`l`.`fletetotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) AS `flete`,((`l`.`segurototal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) AS `seguro`,((`l`.`otrosgastostotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) AS `otros gastos`,((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) AS `cif`,(((((`cal`.`dai` + `cal`.`isc`) + ((`l`.`iso` * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`spe` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (`l`.`iva` * (((((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) + `cal`.`dai`) + `cal`.`isc`) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))))) AS `impuestos`,`cal`.`comision` AS `comision`,(((`l`.`agenciatotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)) AS `agencia`,(((`l`.`almacentotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)) AS `almacen`,(`l`.`tasapapeleria` * `a`.`unidades`) AS `papeleria`,(`l`.`tasatransporte` * `a`.`unidades`) AS `transporte`,`a`.`iddocumento` AS `iddocumento` from ((`articulosxdocumento` `a` join `vw_liquidacionescontodo` `l` on((`a`.`iddocumento` = `l`.`iddocumento`))) join `costosxarticuloliquidacion` `cal` on((`cal`.`idarticuloxdocumento` = `a`.`idarticuloxdocumento`)));

--
-- Definition of view `vw_costosdeldocumento`
--

DROP TABLE IF EXISTS `vw_costosdeldocumento`;
DROP VIEW IF EXISTS `vw_costosdeldocumento`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_costosdeldocumento` AS select `c`.`idcostoagregado` AS `idcostoagregado`,`tc`.`descripcion` AS `Descripcion`,`c`.`valorcosto` AS `valorcosto`,`cd`.`iddocumento` AS `iddocumento`,`td`.`descripcion` AS `TipoDoc`,`c`.`activo` AS `activo` from ((((`costosagregados` `c` join `costosxdocumento` `cd` on((`c`.`idcostoagregado` = `cd`.`idcostoagregado`))) join `tiposcosto` `tc` on((`c`.`idtipocosto` = `tc`.`idtipocosto`))) join `documentos` `d` on((`d`.`iddocumento` = `cd`.`iddocumento`))) join `tiposdoc` `td` on((`td`.`idtipodoc` = `d`.`idtipodoc`))) order by `cd`.`iddocumento`,`c`.`idcostoagregado`;

--
-- Definition of view `vw_liquidacioncontotales`
--

DROP TABLE IF EXISTS `vw_liquidacioncontotales`;
DROP VIEW IF EXISTS `vw_liquidacioncontotales`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_liquidacioncontotales` AS select `l`.`iddocumento` AS `iddocumento`,sum((`a`.`unidades` * `a`.`costocompra`)) AS `fobtotal`,`l`.`fletetotal` AS `fletetotal`,`l`.`segurototal` AS `segurototal`,`l`.`otrosgastos` AS `otrosgastostotal`,(((sum((`a`.`unidades` * `a`.`costocompra`)) + `l`.`fletetotal`) + `l`.`segurototal`) + `l`.`otrosgastos`) AS `ciftotal`,`l`.`peso` AS `pesototal`,`l`.`totalagencia` AS `agenciatotal`,`l`.`totalalmacen` AS `almacentotal`,(`l`.`porcentajepapeleria` / 100) AS `tasapapeleria`,(`l`.`porcentajetransporte` / 100) AS `tasatransporte`,`l`.`procedencia` AS `procedencia` from (`liquidaciones` `l` join `articulosxdocumento` `a` on((`l`.`iddocumento` = `a`.`iddocumento`))) group by `l`.`iddocumento`;

--
-- Definition of view `vw_liquidacionesconcostos`
--

DROP TABLE IF EXISTS `vw_liquidacionesconcostos`;
DROP VIEW IF EXISTS `vw_liquidacionesconcostos`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_liquidacionesconcostos` AS select `l`.`iddocumento` AS `iddocumento`,sum(if((`ca`.`idtipocosto` = 5),(`ca`.`valorcosto` * ceiling((`l`.`peso` / `t`.`factorpeso`))),0)) AS `tsimtotal`,(sum(if((`ca`.`idtipocosto` = 1),`ca`.`valorcosto`,0)) / 100) AS `iva`,sum(if((`ca`.`idtipocosto` = 4),`ca`.`valorcosto`,0)) AS `spe`,(sum(if((`ca`.`idtipocosto` = 6),`ca`.`valorcosto`,0)) / 100) AS `iso` from (((`liquidaciones` `l` join `costosxdocumento` `cd` on((`l`.`iddocumento` = `cd`.`iddocumento`))) join `costosagregados` `ca` on((`ca`.`idcostoagregado` = `cd`.`idcostoagregado`))) left join `tsim` `t` on((`t`.`idtsim` = `ca`.`idcostoagregado`))) group by `l`.`iddocumento`;

--
-- Definition of view `vw_liquidacionescontodo`
--

DROP TABLE IF EXISTS `vw_liquidacionescontodo`;
DROP VIEW IF EXISTS `vw_liquidacionescontodo`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_liquidacionescontodo` AS select `lt`.`iddocumento` AS `iddocumento`,`lt`.`fobtotal` AS `fobtotal`,`lt`.`fletetotal` AS `fletetotal`,`lt`.`segurototal` AS `segurototal`,`lt`.`otrosgastostotal` AS `otrosgastostotal`,`lt`.`ciftotal` AS `ciftotal`,`lt`.`agenciatotal` AS `agenciatotal`,`lt`.`almacentotal` AS `almacentotal`,`lc`.`tsimtotal` AS `tsimtotal`,`lt`.`tasapapeleria` AS `tasapapeleria`,`lt`.`tasatransporte` AS `tasatransporte`,`lc`.`iva` AS `iva`,`lc`.`spe` AS `spe`,`lc`.`iso` AS `iso`,`lt`.`pesototal` AS `pesototal`,`lt`.`procedencia` AS `procedencia` from (`vw_liquidacioncontotales` `lt` join `vw_liquidacionesconcostos` `lc` on((`lt`.`iddocumento` = `lc`.`iddocumento`)));

--
-- Definition of view `vw_liquidacionesguardadas`
--

DROP TABLE IF EXISTS `vw_liquidacionesguardadas`;
DROP VIEW IF EXISTS `vw_liquidacionesguardadas`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_liquidacionesguardadas` AS select `l`.`iddocumento` AS `iddocumento`,`d`.`ndocimpreso` AS `ndocimpreso`,`l`.`procedencia` AS `procedencia`,`l`.`totalagencia` AS `totalagencia`,`l`.`totalalmacen` AS `totalalmacen`,`l`.`porcentajepapeleria` AS `porcentajepapeleria`,`l`.`porcentajetransporte` AS `porcentajetransporte`,`l`.`peso` AS `peso`,`l`.`fletetotal` AS `fletetotal`,`l`.`segurototal` AS `segurototal`,`l`.`otrosgastos` AS `otrosgastos`,`d`.`idtipocambio` AS `tipocambio`,`tc`.`fecha` AS `fecha`,`tc`.`tasa` AS `tasa`,`p`.`idpersona` AS `idpersona`,`p`.`nombre` AS `Proveedor`,`d`.`anulado` AS `anulado` from ((((`liquidaciones` `l` join `documentos` `d` on((`l`.`iddocumento` = `d`.`iddocumento`))) join `tiposcambio` `tc` on((`d`.`idtipocambio` = `tc`.`idtc`))) join `personasxdocumento` `pd` on((`pd`.`iddocumento` = `d`.`iddocumento`))) join `personas` `p` on((`pd`.`idpersona` = `p`.`idpersona`)));

--
-- Definition of view `vw_saldofacturas`
--

DROP TABLE IF EXISTS `vw_saldofacturas`;
DROP VIEW IF EXISTS `vw_saldofacturas`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_saldofacturas` AS select `padre`.`iddocumento` AS `iddocumento`,cast(`padre`.`ndocimpreso` as signed) AS `ndocimpreso`,((`padre`.`total` - sum(if(isnull(`ph`.`monto`),0,`ph`.`monto`))) - sum(if((`hijo`.`idtipodoc` = 10),`hijo`.`total`,0))) AS `Saldo`,`pd`.`idpersona` AS `idpersona` from (((`documentos` `padre` join `personasxdocumento` `pd` on((`padre`.`iddocumento` = `pd`.`iddocumento`))) left join `docpadrehijos` `ph` on((`ph`.`idpadre` = `padre`.`iddocumento`))) left join `documentos` `hijo` on((`ph`.`idhijo` = `hijo`.`iddocumento`))) where ((`padre`.`idtipodoc` = 5) and ((`hijo`.`idtipodoc` = 18) or (`hijo`.`idtipodoc` = 10) or isnull(`hijo`.`idtipodoc`)) and (`padre`.`anulado` = 0)) group by `padre`.`iddocumento`;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
