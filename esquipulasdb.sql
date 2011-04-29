SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';



-- -----------------------------------------------------
-- Table `categorias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `categorias` ;

CREATE  TABLE IF NOT EXISTS `categorias` (
  `idcategoria` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la categoria' ,
  `nombre` VARCHAR(25) NOT NULL COMMENT 'El nombre de la categoria' ,
  `padre` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'El id de la categoria padre' ,
  PRIMARY KEY (`idcategoria`) ,
  CONSTRAINT `fk_catsubcategoria_catsubcategoria1`
    FOREIGN KEY (`padre` )
    REFERENCES `categorias` (`idcategoria` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 287
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_catsubcategoria_catsubcategoria1` ON `categorias` (`padre` ASC) ;


-- -----------------------------------------------------
-- Table `marcas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `marcas` ;

CREATE  TABLE IF NOT EXISTS `marcas` (
  `idmarca` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la marca' ,
  `nombre` VARCHAR(25) NOT NULL COMMENT 'El nombre de la marca' ,
  PRIMARY KEY (`idmarca`) )
ENGINE = InnoDB
AUTO_INCREMENT = 143
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `marcaunica` ON `marcas` (`nombre` ASC) ;


-- -----------------------------------------------------
-- Table `articulos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `articulos` ;

CREATE  TABLE IF NOT EXISTS `articulos` (
  `idarticulo` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `idmarca` INT(10) UNSIGNED NOT NULL ,
  `idcategoria` INT(10) UNSIGNED NOT NULL ,
  `ganancia` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '10' COMMENT 'El porcentaje de ganancia \nque se aplica a este\narticulo para obtener el \nprecio sugerido' ,
  `activo` TINYINT(1) UNSIGNED NOT NULL COMMENT 'Si un articulo\nse encuentra \nactivo o no' ,
  PRIMARY KEY USING BTREE (`idarticulo`) ,
  CONSTRAINT `fk_articulos_categoria1`
    FOREIGN KEY (`idcategoria` )
    REFERENCES `categorias` (`idcategoria` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulos_marca1`
    FOREIGN KEY (`idmarca` )
    REFERENCES `marcas` (`idmarca` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `uniqueproduct` ON `articulos` (`idmarca` ASC, `idcategoria` ASC) ;

CREATE UNIQUE INDEX `articulounico` ON `articulos` (`idmarca` ASC, `idcategoria` ASC) ;

CREATE INDEX `fk_articulos_marca1` ON `articulos` (`idmarca` ASC) ;

CREATE INDEX `fk_articulos_categoria1` ON `articulos` (`idcategoria` ASC) ;


-- -----------------------------------------------------
-- Table `modulos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modulos` ;

CREATE  TABLE IF NOT EXISTS `modulos` (
  `idmodulos` TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del modulo' ,
  `descripcion` VARCHAR(20) NOT NULL COMMENT 'El nombre del modulo' ,
  PRIMARY KEY (`idmodulos`) )
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `tiposdoc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tiposdoc` ;

CREATE  TABLE IF NOT EXISTS `tiposdoc` (
  `idtipodoc` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de costo' ,
  `codigodoc` VARCHAR(2) NOT NULL COMMENT 'El codigo del tipo de documento' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'La descripción del tipo de costo' ,
  `modulo` TINYINT(3) UNSIGNED NOT NULL COMMENT 'El modulo en el quee ste documento se utiliza' ,
  `seriedoc` MEDIUMINT UNSIGNED NULL ,
  PRIMARY KEY USING BTREE (`idtipodoc`) ,
  CONSTRAINT `fk_tipodoc_modulos1`
    FOREIGN KEY (`modulo` )
    REFERENCES `modulos` (`idmodulos` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_tipodoc_modulos1` ON `tiposdoc` (`modulo` ASC) ;


-- -----------------------------------------------------
-- Table `bodegas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bodegas` ;

CREATE  TABLE IF NOT EXISTS `bodegas` (
  `idbodega` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la bodega' ,
  `nombrebodega` VARCHAR(255) NOT NULL COMMENT 'El nombre de la bodega' ,
  PRIMARY KEY (`idbodega`) )
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `nombreunico` ON `bodegas` (`nombrebodega` ASC) ;


-- -----------------------------------------------------
-- Table `tiposcambio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tiposcambio` ;

CREATE  TABLE IF NOT EXISTS `tiposcambio` (
  `idtc` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de cambio' ,
  `tasa` DECIMAL(8,4) UNSIGNED NOT NULL COMMENT 'La tasa de cambio oficial' ,
  `fecha` DATE NOT NULL COMMENT 'La fecha para este tipo de cambio' ,
  `tasabanco` DECIMAL(8,4) NULL DEFAULT NULL COMMENT 'La tasa del banco, definida por el usuario' ,
  PRIMARY KEY (`idtc`) )
ENGINE = InnoDB
AUTO_INCREMENT = 213
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `fechaunica` ON `tiposcambio` (`fecha` ASC) ;


-- -----------------------------------------------------
-- Table `conceptos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `conceptos` ;

CREATE  TABLE IF NOT EXISTS `conceptos` (
  `idconcepto` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `descripcion` VARCHAR(100) NOT NULL ,
  `idtipodoc` INT(10) UNSIGNED NOT NULL ,
  PRIMARY KEY USING BTREE (`idconcepto`) ,
  CONSTRAINT `fk_conceptos_tiposdoc1`
    FOREIGN KEY (`idtipodoc` )
    REFERENCES `tiposdoc` (`idtipodoc` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_conceptos_tiposdoc1` ON `conceptos` (`idtipodoc` ASC) ;


-- -----------------------------------------------------
-- Table `cajas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cajas` ;

CREATE  TABLE IF NOT EXISTS `cajas` (
  `idcaja` TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la caja' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'El nombre de la caja' ,
  `activo` TINYINT(1)  NOT NULL DEFAULT 1 ,
  PRIMARY KEY (`idcaja`) )
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `estadosdocumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `estadosdocumento` ;

CREATE  TABLE IF NOT EXISTS `estadosdocumento` (
  `idestado` TINYINT NOT NULL ,
  `descripcion` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idestado`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `documentos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `documentos` ;

CREATE  TABLE IF NOT EXISTS `documentos` (
  `iddocumento` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del documento' ,
  `ndocimpreso` VARCHAR(20) NOT NULL COMMENT 'El numero de documento que el usuario ve' ,
  `total` DECIMAL(12,4) NOT NULL COMMENT 'total en cordobas de doc como factura, entrada, salida' ,
  `fechacreacion` DATETIME NOT NULL COMMENT 'La fecha y hora en la que se creo este documento' ,
  `idtipodoc` INT(10) UNSIGNED NOT NULL COMMENT 'El id del tipo de documento' ,
  `observacion` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Alguna observación que pueda tener el documento' ,
  `idtipocambio` MEDIUMINT(8) UNSIGNED NULL DEFAULT NULL COMMENT 'El id del tipo de cambio' ,
  `idbodega` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'El id de la bodega' ,
  `idconcepto` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'El concepto de este documento' ,
  `idcaja` TINYINT(3) UNSIGNED NULL ,
  `escontado` TINYINT(1)  NULL DEFAULT 1 COMMENT 'Si este documento es de contado o credito' ,
  `idestado` TINYINT NOT NULL DEFAULT 1 COMMENT 'Estado del documento, si esta pendiente , confirmado o anulado, por defecto esta 1 que es confirmado' ,
  `delbanco` VARCHAR(45) NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`iddocumento`) ,
  CONSTRAINT `FK_documentos_tiposdoc1`
    FOREIGN KEY (`idtipodoc` )
    REFERENCES `tiposdoc` (`idtipodoc` ),
  CONSTRAINT `fk_documentos_bodegas1`
    FOREIGN KEY (`idbodega` )
    REFERENCES `bodegas` (`idbodega` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_tiposcambio1`
    FOREIGN KEY (`idtipocambio` )
    REFERENCES `tiposcambio` (`idtc` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_conceptos1`
    FOREIGN KEY (`idconcepto` )
    REFERENCES `conceptos` (`idconcepto` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_cajas1`
    FOREIGN KEY (`idcaja` )
    REFERENCES `cajas` (`idcaja` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_estadosdocumento1`
    FOREIGN KEY (`idestado` )
    REFERENCES `estadosdocumento` (`idestado` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci
COMMENT = 'Entrada y Salida de dinero y productos';

CREATE INDEX `fk_documentos_tiposcambio1` USING BTREE ON `documentos` (`idtipocambio` ASC) ;

CREATE INDEX `fk_documentos_bodegas1` ON `documentos` (`idbodega` ASC) ;

CREATE INDEX `fk_documentos_tiposdoc1` ON `documentos` (`idtipodoc` ASC) ;

CREATE INDEX `fk_documento_conceptos1` USING BTREE ON `documentos` (`idconcepto` ASC) ;

CREATE INDEX `fk_documentos_conceptos1` ON `documentos` (`idconcepto` ASC) ;

CREATE INDEX `fk_documentos_cajas1` ON `documentos` (`idcaja` ASC) ;

CREATE INDEX `fk_documentos_estadosdocumento1` ON `documentos` (`idestado` ASC) ;


-- -----------------------------------------------------
-- Table `articulosxdocumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `articulosxdocumento` ;

CREATE  TABLE IF NOT EXISTS `articulosxdocumento` (
  `idarticuloxdocumento` INT(11) NOT NULL AUTO_INCREMENT ,
  `iddocumento` INT(10) UNSIGNED NOT NULL ,
  `idarticulo` INT(10) UNSIGNED NOT NULL COMMENT 'El id del articulo' ,
  `unidades` INT(11) NOT NULL COMMENT 'La cantidad de articulos\nen este documento' ,
  `costocompra` DECIMAL(12,4) NULL DEFAULT NULL COMMENT 'El costo de compra de este\narticulo' ,
  `costounit` DECIMAL(12,4) NULL DEFAULT NULL COMMENT 'El costo unitario para\neste articulo, sera en cordobas cuando se relacione a una factura y en dolares cuando se relacione a otro documento' ,
  `precioventa` DECIMAL(12,4) NULL DEFAULT NULL COMMENT 'El precio de venta de este articulo' ,
  `nlinea` SMALLINT(6) NULL COMMENT 'para ordenar en la interfaz grafica' ,
  `tccosto` MEDIUMINT(8) UNSIGNED NULL ,
  PRIMARY KEY (`idarticuloxdocumento`) ,
  CONSTRAINT `fk_articuloxdocumento_documentos1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` ),
  CONSTRAINT `fk_articulosxdocumento_articulos1`
    FOREIGN KEY (`idarticulo` )
    REFERENCES `articulos` (`idarticulo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulosxdocumento_tiposcambio1`
    FOREIGN KEY (`tccosto` )
    REFERENCES `tiposcambio` (`idtc` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 52
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `articuloxdoc` ON `articulosxdocumento` (`iddocumento` ASC, `idarticulo` ASC) ;

CREATE INDEX `fk_articuloxdocumento_articulos1` ON `articulosxdocumento` (`idarticulo` ASC) ;

CREATE INDEX `fk_articuloxdocumento_documento1` ON `articulosxdocumento` (`iddocumento` ASC) ;

CREATE INDEX `fk_articulosxdocumento_articulos1` ON `articulosxdocumento` (`idarticulo` ASC) ;

CREATE INDEX `fk_articulosxdocumento_tiposcambio1` ON `articulosxdocumento` (`tccosto` ASC) ;


-- -----------------------------------------------------
-- Table `bancos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bancos` ;

CREATE  TABLE IF NOT EXISTS `bancos` (
  `idbanco` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del banco' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'El nombre del banco' ,
  PRIMARY KEY (`idbanco`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `cuentascontables`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cuentascontables` ;

CREATE  TABLE IF NOT EXISTS `cuentascontables` (
  `idcuenta` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la cuenta contable' ,
  `padre` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'El id del padre de esta cuenta contable ' ,
  `codigo` VARCHAR(20) NOT NULL COMMENT 'El codigo contable' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'La descripción de esta cuenta' ,
  `esdebe` TINYINT(1) NOT NULL COMMENT 'Para definir si es activo, pasivo o capital' ,
  PRIMARY KEY (`idcuenta`) ,
  CONSTRAINT `fk_cuenta_cuenta1`
    FOREIGN KEY (`padre` )
    REFERENCES `cuentascontables` (`idcuenta` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 356
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci
COMMENT = 'Es un catalogo de cuentas';

CREATE INDEX `fk_cuenta_cuenta1` ON `cuentascontables` (`padre` ASC) ;


-- -----------------------------------------------------
-- Table `cierrescontables`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cierrescontables` ;

CREATE  TABLE IF NOT EXISTS `cierrescontables` (
  `idcierrecontable` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `idCuenta` INT(10) UNSIGNED NOT NULL ,
  `monto` DECIMAL(12,4) NOT NULL ,
  `fechacierre` DATETIME NOT NULL ,
  `esmensual` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idcierrecontable`) ,
  CONSTRAINT `fk_cierrecontable_cuentacontable1`
    FOREIGN KEY (`idCuenta` )
    REFERENCES `cuentascontables` (`idcuenta` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_cierrecontable_cuentacontable1` ON `cierrescontables` (`idCuenta` ASC) ;


-- -----------------------------------------------------
-- Table `tiposcosto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tiposcosto` ;

CREATE  TABLE IF NOT EXISTS `tiposcosto` (
  `idtipocosto` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de costo' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'La descripción del tipo de costo' ,
  `esporcentaje` TINYINT(1) NOT NULL COMMENT 'Si este costo es porcentaje o es un valor fijo' ,
  `cuentacontable` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'La cuenta contable del tipo de costo' ,
  PRIMARY KEY (`idtipocosto`) ,
  CONSTRAINT `FK_tipocosto_CuentaContable`
    FOREIGN KEY (`cuentacontable` )
    REFERENCES `cuentascontables` (`idcuenta` ))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `FK_tipocosto_CuentaContable` ON `tiposcosto` (`cuentacontable` ASC) ;


-- -----------------------------------------------------
-- Table `costosagregados`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `costosagregados` ;

CREATE  TABLE IF NOT EXISTS `costosagregados` (
  `idcostoagregado` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del costo agregado' ,
  `valorcosto` DECIMAL(8,2) NOT NULL COMMENT 'El valor del costo agregado' ,
  `fechaestablecido` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'La fecha en la que este costo agregado fue establecido' ,
  `activo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Si este costo esta activo o no' ,
  `idtipocosto` INT(10) UNSIGNED NOT NULL COMMENT 'El id del tipo de costo' ,
  `idarticulo` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'id del articulo cuando sea DAI, ISC o COMISION' ,
  PRIMARY KEY (`idcostoagregado`) ,
  CONSTRAINT `fk_costoagregado_articulos1`
    FOREIGN KEY (`idarticulo` )
    REFERENCES `articulos` (`idarticulo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_CostoAgregado_TipoCosto1`
    FOREIGN KEY (`idtipocosto` )
    REFERENCES `tiposcosto` (`idtipocosto` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 170
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_CostoAgregado_TipoCosto1` ON `costosagregados` (`idtipocosto` ASC) ;

CREATE INDEX `fk_costoagregado_articulos1` ON `costosagregados` (`idarticulo` ASC) ;


-- -----------------------------------------------------
-- Table `costosarticulo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `costosarticulo` ;

CREATE  TABLE IF NOT EXISTS `costosarticulo` (
  `idcostoarticulo` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del costoarticulo' ,
  `valor` DECIMAL(12,4) UNSIGNED NOT NULL COMMENT 'El valor del costo articulo' ,
  `idarticulo` INT(10) UNSIGNED NOT NULL COMMENT 'El id del articulo' ,
  `activo` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT 'Si este costo esta activo o no' ,
  `idtc` MEDIUMINT(8) UNSIGNED NOT NULL COMMENT 'El id del tipo de cambio' ,
  PRIMARY KEY (`idcostoarticulo`) ,
  CONSTRAINT `fk_costoarticulo_articulos1`
    FOREIGN KEY (`idarticulo` )
    REFERENCES `articulos` (`idarticulo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_costosarticulo_tiposcambio1`
    FOREIGN KEY (`idtc` )
    REFERENCES `tiposcambio` (`idtc` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_costoarticulo_articulos1` ON `costosarticulo` (`idarticulo` ASC) ;

CREATE INDEX `fk_costosarticulo_tiposcambio1` ON `costosarticulo` (`idtc` ASC) ;


-- -----------------------------------------------------
-- Table `costosxarticuloliquidacion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `costosxarticuloliquidacion` ;

CREATE  TABLE IF NOT EXISTS `costosxarticuloliquidacion` (
  `idarticuloxdocumento` INT(11) NOT NULL COMMENT 'El id del registro articuloxdodumento' ,
  `dai` DECIMAL(12,4) NOT NULL COMMENT 'El valor del costo DAI' ,
  `isc` DECIMAL(12,4) NOT NULL COMMENT 'El valor del costo ISC' ,
  `comision` DECIMAL(12,4) NOT NULL COMMENT 'El valor de la comisión' ,
  PRIMARY KEY (`idarticuloxdocumento`) ,
  CONSTRAINT `fk_table1_articuloxdocumento1`
    FOREIGN KEY (`idarticuloxdocumento` )
    REFERENCES `articulosxdocumento` (`idarticuloxdocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_table1_articuloxdocumento1` ON `costosxarticuloliquidacion` (`idarticuloxdocumento` ASC) ;


-- -----------------------------------------------------
-- Table `costosxdocumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `costosxdocumento` ;

CREATE  TABLE IF NOT EXISTS `costosxdocumento` (
  `iddocumento` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento' ,
  `idcostoagregado` INT(10) UNSIGNED NOT NULL COMMENT 'El id del costo agregado' ,
  PRIMARY KEY (`iddocumento`, `idcostoagregado`) ,
  CONSTRAINT `fk_documento_has_costoagregado_documento1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documento_has_costoagregado_costoagregado1`
    FOREIGN KEY (`idcostoagregado` )
    REFERENCES `costosagregados` (`idcostoagregado` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_documento_has_costoagregado_documento1` ON `costosxdocumento` (`iddocumento` ASC) ;

CREATE INDEX `fk_documento_has_costoagregado_costoagregado1` ON `costosxdocumento` (`idcostoagregado` ASC) ;


-- -----------------------------------------------------
-- Table `tiposmoneda`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tiposmoneda` ;

CREATE  TABLE IF NOT EXISTS `tiposmoneda` (
  `idtipomoneda` TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de moneda' ,
  `moneda` VARCHAR(45) NOT NULL COMMENT 'El nombre del tipo de moneda' ,
  `simbolo` VARCHAR(5) NOT NULL ,
  PRIMARY KEY (`idtipomoneda`) )
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `cuentasbancarias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cuentasbancarias` ;

CREATE  TABLE IF NOT EXISTS `cuentasbancarias` (
  `idcuentacontable` INT(10) UNSIGNED NOT NULL COMMENT 'El id de la cuenta contable' ,
  `idbanco` INT(10) UNSIGNED NOT NULL COMMENT 'El id del banco' ,
  `idtipomoneda` TINYINT(3) UNSIGNED NOT NULL COMMENT 'El id del tipo de moneda en esta cuenta bancaria' ,
  `ctabancaria` VARCHAR(45) NOT NULL COMMENT 'El numero de la cuenta bancaria' ,
  `fechacancelado` DATE NULL DEFAULT NULL COMMENT 'La fecha en que esta cuenta bancaria fue cerrada' ,
  `fechaapertura` DATE NOT NULL COMMENT 'La fecha en que esta cuenta bancaria fue cerrada' ,
  `seriedoc` INT(11)  NOT NULL DEFAULT 1 ,
  PRIMARY KEY (`idcuentacontable`) ,
  CONSTRAINT `fk_cuentabancaria_banco1`
    FOREIGN KEY (`idbanco` )
    REFERENCES `bancos` (`idbanco` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cuentabancaria_cuentacontable1`
    FOREIGN KEY (`idcuentacontable` )
    REFERENCES `cuentascontables` (`idcuenta` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cuentabancaria_tipomoneda1`
    FOREIGN KEY (`idtipomoneda` )
    REFERENCES `tiposmoneda` (`idtipomoneda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_cuentabancaria_banco1` ON `cuentasbancarias` (`idbanco` ASC) ;

CREATE INDEX `fk_cuentabancaria_cuentacontable1` ON `cuentasbancarias` (`idcuentacontable` ASC) ;

CREATE INDEX `fk_cuentabancaria_tipomoneda1` ON `cuentasbancarias` (`idtipomoneda` ASC) ;


-- -----------------------------------------------------
-- Table `cuentasxdocumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cuentasxdocumento` ;

CREATE  TABLE IF NOT EXISTS `cuentasxdocumento` (
  `iddocumento` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento' ,
  `idcuenta` INT(10) UNSIGNED NOT NULL COMMENT 'El id de la cuenta contable' ,
  `monto` DECIMAL(14,6) NOT NULL COMMENT 'El monto que se afecta en este movimiento' ,
  `nlinea` SMALLINT(6) NULL DEFAULT NULL COMMENT 'Para ordenarlo en la interfaz grafica' ,
  PRIMARY KEY (`iddocumento`, `idcuenta`) ,
  CONSTRAINT `fk_documentoxcuenta_documento1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Documento_has_cuenta_cuenta1`
    FOREIGN KEY (`idcuenta` )
    REFERENCES `cuentascontables` (`idcuenta` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_Documento_has_cuenta_cuenta1` ON `cuentasxdocumento` (`idcuenta` ASC) ;

CREATE INDEX `fk_documentoxcuenta_documento1` ON `cuentasxdocumento` (`iddocumento` ASC) ;


-- -----------------------------------------------------
-- Table `docpadrehijos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `docpadrehijos` ;

CREATE  TABLE IF NOT EXISTS `docpadrehijos` (
  `idpadre` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento padre' ,
  `idhijo` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento hijo' ,
  `monto` DECIMAL(12,4) UNSIGNED NULL DEFAULT NULL COMMENT 'El monto de esta relación' ,
  `nlinea` SMALLINT NULL COMMENT 'Numero de la linea para ordenarlo en la interfaz grafica\n' ,
  PRIMARY KEY USING BTREE (`idpadre`, `idhijo`) ,
  CONSTRAINT `fk_documento_has_documento_documento2`
    FOREIGN KEY (`idhijo` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documento_has_documento_documento1`
    FOREIGN KEY (`idpadre` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_documento_has_documento_documento1` USING BTREE ON `docpadrehijos` (`idpadre` ASC) ;

CREATE INDEX `fk_documento_has_documento_documento2` USING BTREE ON `docpadrehijos` (`idhijo` ASC) ;


-- -----------------------------------------------------
-- Table `liquidaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `liquidaciones` ;

CREATE  TABLE IF NOT EXISTS `liquidaciones` (
  `iddocumento` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del documento' ,
  `procedencia` VARCHAR(45) NOT NULL COMMENT 'El país de procedencia de la liquidación' ,
  `totalagencia` DECIMAL(12,4) NOT NULL COMMENT 'El total de agencia' ,
  `totalalmacen` DECIMAL(12,4) NOT NULL COMMENT 'El total de almacen' ,
  `porcentajepapeleria` DECIMAL(4,2) NOT NULL COMMENT 'El porcentaje papelería' ,
  `porcentajetransporte` DECIMAL(4,2) NOT NULL COMMENT 'El porcentaje transporte' ,
  `peso` DECIMAL(12,4) NOT NULL COMMENT 'El peso total ' ,
  `fletetotal` DECIMAL(12,4) NOT NULL COMMENT 'El flete total' ,
  `segurototal` DECIMAL(12,4) NOT NULL COMMENT 'El seguro total' ,
  `otrosgastos` DECIMAL(12,4) NOT NULL COMMENT 'El total de otros gastos del documento' ,
  PRIMARY KEY (`iddocumento`) ,
  CONSTRAINT `fk_liquidacion_documento1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 251
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_liquidacion_documento1` ON `liquidaciones` (`iddocumento` ASC) ;


-- -----------------------------------------------------
-- Table `tiposmovimientocaja`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tiposmovimientocaja` ;

CREATE  TABLE IF NOT EXISTS `tiposmovimientocaja` (
  `idtipomovimiento` TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id del tipo de pago' ,
  `descripcion` VARCHAR(45) NOT NULL COMMENT 'La descripción de este tipo de pago' ,
  PRIMARY KEY (`idtipomovimiento`) )
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `movimientoscaja`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `movimientoscaja` ;

CREATE  TABLE IF NOT EXISTS `movimientoscaja` (
  `iddocumento` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento recibo' ,
  `idtipomovimiento` TINYINT(3) UNSIGNED NOT NULL COMMENT 'El tipo de pago' ,
  `idtipomoneda` TINYINT(3) UNSIGNED NOT NULL COMMENT 'El id del tipo de moneda' ,
  `monto` DECIMAL(12,4) NOT NULL COMMENT 'El monto de este pago' ,
  `refexterna` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Referencia de los tipos de pago que no son efectivo. Ej. No. de minuta si es deposito' ,
  `idbanco` INT(10) UNSIGNED NULL ,
  `nlinea` SMALLINT NULL COMMENT 'Numero de la linea para ordenarlo en la interfaz grafica\n' ,
  PRIMARY KEY (`iddocumento`, `idtipomovimiento`, `idtipomoneda`) ,
  CONSTRAINT `fk_pago_documento1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pago_tipomoneda1`
    FOREIGN KEY (`idtipomoneda` )
    REFERENCES `tiposmoneda` (`idtipomoneda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pago_tipopago1`
    FOREIGN KEY (`idtipomovimiento` )
    REFERENCES `tiposmovimientocaja` (`idtipomovimiento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movimientoscaja_bancos1`
    FOREIGN KEY (`idbanco` )
    REFERENCES `bancos` (`idbanco` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_pago_tipopago1` ON `movimientoscaja` (`idtipomovimiento` ASC) ;

CREATE INDEX `fk_pago_tipomoneda1` ON `movimientoscaja` (`idtipomoneda` ASC) ;

CREATE INDEX `fk_pago_documento1` ON `movimientoscaja` (`iddocumento` ASC) ;

CREATE INDEX `fk_movimientoscaja_bancos1` ON `movimientoscaja` (`idbanco` ASC) ;


-- -----------------------------------------------------
-- Table `tipospersona`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tipospersona` ;

CREATE  TABLE IF NOT EXISTS `tipospersona` (
  `idtipopersona` TINYINT NOT NULL ,
  `descripcion` VARCHAR(45) NOT NULL ,
  `accion` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idtipopersona`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `personas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `personas` ;

CREATE  TABLE IF NOT EXISTS `personas` (
  `idpersona` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la persona' ,
  `nombre` VARCHAR(100) NOT NULL COMMENT 'El nombre de la persona' ,
  `fechaIngreso` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'La fecha de ingreso al sistema' ,
  `direccion` VARCHAR(200) NULL ,
  `telefono` VARCHAR(45) NULL DEFAULT NULL COMMENT 'El telefóno de la persona' ,
  `email` VARCHAR(45) NULL DEFAULT NULL COMMENT 'El e-mail de la persona' ,
  `ruc` VARCHAR(20) NULL DEFAULT NULL COMMENT 'EL numero de RUC de la persona\n' ,
  `activo` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Si una persona esta activa o no' ,
  `tipopersona` TINYINT NOT NULL COMMENT '1 cliente 2 proveedor, 3 vendedor, 4 usuario\n' ,
  `idcuenta` INT(10) UNSIGNED NULL COMMENT 'El id de la cuenta de esta persona' ,
  PRIMARY KEY (`idpersona`) ,
  CONSTRAINT `fk_personas_cuentascontables1`
    FOREIGN KEY (`idcuenta` )
    REFERENCES `cuentascontables` (`idcuenta` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_personas_tipospersona1`
    FOREIGN KEY (`tipopersona` )
    REFERENCES `tipospersona` (`idtipopersona` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 27
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `nombre_unico` USING BTREE ON `personas` (`nombre` ASC, `tipopersona` ASC) ;

CREATE INDEX `fk_personas_cuentascontables1` ON `personas` (`idcuenta` ASC) ;

CREATE INDEX `fk_personas_tipospersona1` ON `personas` (`tipopersona` ASC) ;


-- -----------------------------------------------------
-- Table `roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `roles` ;

CREATE  TABLE IF NOT EXISTS `roles` (
  `idrol` TINYINT UNSIGNED NOT NULL COMMENT 'El id del rol' ,
  `nombre` VARCHAR(40) NOT NULL COMMENT 'El nombre del rol,\nesto es usado por el \nsistema a nivel interno' ,
  `descripcion` VARCHAR(200) NOT NULL ,
  `idmodulo` TINYINT(3) UNSIGNED NOT NULL COMMENT 'El id del modulo al que sirve este rol' ,
  PRIMARY KEY (`idrol`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `tsim`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tsim` ;

CREATE  TABLE IF NOT EXISTS `tsim` (
  `idtsim` INT(10) UNSIGNED NOT NULL COMMENT 'El id del TSIM' ,
  `factorpeso` DECIMAL(10,4) NOT NULL COMMENT 'El factor peso de este TSIM' ,
  PRIMARY KEY (`idtsim`) ,
  CONSTRAINT `FK_tsim_1`
    FOREIGN KEY (`idtsim` )
    REFERENCES `costosagregados` (`idcostoagregado` ))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuarios` ;

CREATE  TABLE IF NOT EXISTS `usuarios` (
  `idusuario` INT UNSIGNED NOT NULL COMMENT 'El id del usuario' ,
  `username` VARCHAR(15) NOT NULL COMMENT 'El nombre de usuario' ,
  `password` VARCHAR(50) NOT NULL COMMENT 'La contraseña de este usuario' ,
  `estado` TINYINT(1) NOT NULL COMMENT 'El estado de este usuario, habilitado o deshabilitado' ,
  `tipousuario` TINYINT(2) NOT NULL COMMENT 'El tipo de usuario' ,
  PRIMARY KEY (`idusuario`) ,
  CONSTRAINT `fk_usuarios_personas1`
    FOREIGN KEY (`idusuario` )
    REFERENCES `personas` (`idpersona` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_usuarios_personas1` ON `usuarios` (`idusuario` ASC) ;


-- -----------------------------------------------------
-- Table `denominaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `denominaciones` ;

CREATE  TABLE IF NOT EXISTS `denominaciones` (
  `iddenominacion` INT NOT NULL ,
  `valor` FLOAT NOT NULL ,
  `activo` TINYINT(1)  NOT NULL ,
  `idtipomoneda` TINYINT(3) UNSIGNED NOT NULL ,
  PRIMARY KEY (`iddenominacion`) ,
  CONSTRAINT `fk_denominaciones_tiposmoneda1`
    FOREIGN KEY (`idtipomoneda` )
    REFERENCES `tiposmoneda` (`idtipomoneda` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_denominaciones_tiposmoneda1` ON `denominaciones` (`idtipomoneda` ASC) ;


-- -----------------------------------------------------
-- Table `lineasarqueo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `lineasarqueo` ;

CREATE  TABLE IF NOT EXISTS `lineasarqueo` (
  `idlineaarqueo` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'El id de la linea en el arqueo' ,
  `cantidad` SMALLINT UNSIGNED NOT NULL COMMENT 'Las unidades en esta linea' ,
  `iddocumento` INT(10) UNSIGNED NOT NULL COMMENT 'El id del documento' ,
  `iddenominacion` INT NOT NULL ,
  PRIMARY KEY (`idlineaarqueo`) ,
  CONSTRAINT `fk_lineasarqueo_documentos1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lineasarqueo_denominaciones1`
    FOREIGN KEY (`iddenominacion` )
    REFERENCES `denominaciones` (`iddenominacion` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_lineasarqueo_documentos1` ON `lineasarqueo` (`iddocumento` ASC) ;

CREATE INDEX `fk_lineasarqueo_denominaciones1` ON `lineasarqueo` (`iddenominacion` ASC) ;


-- -----------------------------------------------------
-- Table `personasxdocumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `personasxdocumento` ;

CREATE  TABLE IF NOT EXISTS `personasxdocumento` (
  `iddocumento` INT(10) UNSIGNED NOT NULL ,
  `idpersona` INT(10) UNSIGNED NOT NULL ,
  `idaccion` TINYINT NOT NULL ,
  PRIMARY KEY (`iddocumento`, `idpersona`, `idaccion`) ,
  CONSTRAINT `fk_documentos_has_personas_documentos1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentos_has_personas_personas1`
    FOREIGN KEY (`idpersona` )
    REFERENCES `personas` (`idpersona` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_personasxdocumento_tipospersona1`
    FOREIGN KEY (`idaccion` )
    REFERENCES `tipospersona` (`idtipopersona` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_documentos_has_personas_documentos1` ON `personasxdocumento` (`iddocumento` ASC) ;

CREATE INDEX `fk_documentos_has_personas_personas1` ON `personasxdocumento` (`idpersona` ASC) ;

CREATE INDEX `fk_personasxdocumento_tipospersona1` ON `personasxdocumento` (`idaccion` ASC) ;


-- -----------------------------------------------------
-- Table `usuarios_has_roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuarios_has_roles` ;

CREATE  TABLE IF NOT EXISTS `usuarios_has_roles` (
  `idusuario` INT UNSIGNED NOT NULL ,
  `idrol` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`idusuario`, `idrol`) ,
  CONSTRAINT `fk_usuarios_has_roles_usuarios1`
    FOREIGN KEY (`idusuario` )
    REFERENCES `usuarios` (`idusuario` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_roles_roles1`
    FOREIGN KEY (`idrol` )
    REFERENCES `roles` (`idrol` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_usuarios_has_roles_usuarios1` ON `usuarios_has_roles` (`idusuario` ASC) ;

CREATE INDEX `fk_usuarios_has_roles_roles1` ON `usuarios_has_roles` (`idrol` ASC) ;


-- -----------------------------------------------------
-- Table `conciliaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `conciliaciones` ;

CREATE  TABLE IF NOT EXISTS `conciliaciones` (
  `iddocumento` INT(10) UNSIGNED NOT NULL ,
  `saldobanco` DECIMAL(12,4) NOT NULL COMMENT 'Saldo de la final cuenta bancaria segun banco' ,
  `saldolibro` VARCHAR(45) NOT NULL COMMENT 'Saldo de la final cuenta bancaria segun banco' ,
  `fecha` DATE NOT NULL COMMENT 'Fecha para obtener mes y año de la conciliacion' ,
  `idcuentabancaria` INT(10) UNSIGNED NOT NULL COMMENT 'id de la cuenta que fue conciliada' ,
  PRIMARY KEY (`iddocumento`) ,
  CONSTRAINT `fk_conciliaciones_documentos1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conciliaciones_cuentasbancarias1`
    FOREIGN KEY (`idcuentabancaria` )
    REFERENCES `cuentasbancarias` (`idcuentacontable` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE UNIQUE INDEX `fechacuenta` ON `conciliaciones` (`idcuentabancaria` ASC, `fecha` ASC) ;

CREATE INDEX `fk_conciliaciones_documentos1` USING BTREE ON `conciliaciones` (`iddocumento` ASC) ;

CREATE INDEX `fk_conciliaciones_cuentasbancarias1` USING BTREE ON `conciliaciones` (`idcuentabancaria` ASC) ;


-- -----------------------------------------------------
-- Table `creditos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `creditos` ;

CREATE  TABLE IF NOT EXISTS `creditos` (
  `iddocumento` INT(10) UNSIGNED NOT NULL ,
  `fechatope` DATE NOT NULL ,
  `tasamulta` DECIMAL(12,4) NOT NULL ,
  `pagado` TINYINT(1)  NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`iddocumento`) ,
  CONSTRAINT `fk_creditos_documentos1`
    FOREIGN KEY (`iddocumento` )
    REFERENCES `documentos` (`iddocumento` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_creditos_documentos1` ON `creditos` (`iddocumento` ASC) ;


-- -----------------------------------------------------
-- Placeholder table for view `vw_articulosconcostosactuales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_articulosconcostosactuales` (`idarticulo` INT, `descripcion` INT, `dai` INT, `isc` INT, `comision` INT, `ganancia` INT, `activo` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_articulosdescritos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_articulosdescritos` (`idarticulo` INT, `descripcion` INT, `idcategoria` INT, `categorias` INT, `idsubcategoria` INT, `subcategoria` INT, `idmarca` INT, `marcas` INT, `activo` INT, `ganancia` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_costosdeldocumento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_costosdeldocumento` (`idcostoagregado` INT, `Descripcion` INT, `valorcosto` INT, `iddocumento` INT, `TipoDoc` INT, `activo` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_liquidacionesguardadas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_liquidacionesguardadas` (`iddocumento` INT, `ndocimpreso` INT, `procedencia` INT, `totalagencia` INT, `totalalmacen` INT, `porcentajepapeleria` INT, `porcentajetransporte` INT, `peso` INT, `fletetotal` INT, `segurototal` INT, `otrosgastos` INT, `tipocambio` INT, `fecha` INT, `tasa` INT, `idpersona` INT, `Proveedor` INT, `estado` INT, `bodega` INT, `totald` INT, `totalc` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_articulosprorrateados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_articulosprorrateados` (`idarticulo` INT, `unidades` INT, `costocompra` INT, `fob` INT, `flete` INT, `seguro` INT, `otrosgastos` INT, `cif` INT, `impuestos` INT, `comision` INT, `agencia` INT, `almacen` INT, `papeleria` INT, `transporte` INT, `iddocumento` INT, `costototal` INT, `costounit` INT, `nlinea` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_liquidacioncontotales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_liquidacioncontotales` (`iddocumento` INT, `unidadestotal` INT, `comisiontotal` INT, `fobtotal` INT, `fletetotal` INT, `segurototal` INT, `otrosgastostotal` INT, `ciftotal` INT, `impuestototal` INT, `pesototal` INT, `agenciatotal` INT, `almacentotal` INT, `papeleriatotal` INT, `transportetotal` INT, `tasapapeleria` INT, `tasatransporte` INT, `procedencia` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_liquidacionesconcostos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_liquidacionesconcostos` (`iddocumento` INT, `tsimtotal` INT, `iva` INT, `spe` INT, `iso` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_liquidacionescontodo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_liquidacionescontodo` (`iddocumento` INT, `fobtotal` INT, `fletetotal` INT, `segurototal` INT, `otrosgastostotal` INT, `ciftotal` INT, `agenciatotal` INT, `almacentotal` INT, `tsimtotal` INT, `tasapapeleria` INT, `tasatransporte` INT, `iva` INT, `spe` INT, `iso` INT, `pesototal` INT, `procedencia` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_saldofacturas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_saldofacturas` (`iddocumento` INT, `ndocimpreso` INT, `totalfacturado` INT, `saldo` INT, `totaldevolucion` INT, `totalabono` INT, `tasaiva` INT, `idpersona` INT, `nombre` INT, `idestado` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_cuentasbancarias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_cuentasbancarias` (`idcuenta` INT, `banco` INT, `ncuenta` INT, `moneda` INT, `codigocontable` INT, `cuentacontable` INT);

-- -----------------------------------------------------
-- Placeholder table for view `vw_articulosenbodegas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vw_articulosenbodegas` (`idarticulo` INT, `descripcion` INT, `precio` INT, `costodolar` INT, `costo` INT, `existencia` INT, `idbodega` INT);

-- -----------------------------------------------------
-- procedure spAgregarArticulos
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAgregarArticulos`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAgregarArticulos`(IN activo TINYINT,IN marca INTEGER, IN subcategoria INTEGER, IN dai INTEGER, IN isc INTEGER, IN comision INTEGER, IN tasaganancia INTEGER)
BEGIN

       START TRANSACTION;

            INSERT INTO articulos (activo,idmarca,idcategoria,ganancia) VALUES (activo,marca,subcategoria, tasaganancia);
            SET @ultimoarticulo := LAST_INSERT_ID();
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(dai,1,3,@ultimoarticulo);
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(comision,1,7,@ultimoarticulo);
            INSERT INTO costosagregados (valorcosto,activo,idtipocosto,idarticulo) VALUES(isc,1,2,@ultimoarticulo);

       COMMIT;

END
$$
DELIMITER ;



DELIMITER ;
-- -----------------------------------------------------
-- procedure spEntradasCompraDetalladas
-- -----------------------------------------------------


DROP procedure IF EXISTS `spEntradasCompraDetalladas`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spEntradasCompraDetalladas`(in iddoc int)
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
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spEntradasCompraDetalladasParaSalida
-- -----------------------------------------------------


DROP procedure IF EXISTS `spEntradasCompraDetalladasParaSalida`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spEntradasCompraDetalladasParaSalida`(in iddoc int)
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
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spLiquidacion_Abrir
-- -----------------------------------------------------


DROP procedure IF EXISTS `spLiquidacion_Abrir`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spLiquidacion_Abrir`(in iddoc int)
BEGIN
       if iddoc is not null then
        SELECT * FROM vw_liquidacionesguardadas v WHERE iddocumento=iddoc;

               SELECT c.idcostoagregado,ca.valorcosto, t.factorpeso,ca.idtipocosto FROM costosxdocumento c JOIN costosagregados ca ON c.idcostoagregado=ca.idcostoagregado left JOIN tsim t ON t.idtsim=c.idcostoagregado WHERE c.iddocumento=iddoc;

                SELECT v.idarticulo,v.descripcion,v.dai,v.isc,v.comision,a.unidades,a.costocompra AS punit,a.unidades*a.costocompra AS fob,v.comision*a.unidades AS comision, a.idbodega, b.nombrebodega FROM vw_articulosconcostosactuales v JOIN articulosxdocumento a ON v.idarticulo=a.idarticulo JOIN bodegas b ON b.idbodega=a.idbodega WHERE iddocumento=iddoc order by a.nlinea;

                SELECT c.codigo AS Cuenta,c.Descripcion,FORMAT(d.monto,4) AS 'Monto C$' FROM documentoxcuenta d JOIN cuentacontable c ON d.idcuenta=c.idcuenta WHERE iddocumento=iddoc order by d.nlinea;
        end if;
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spLiquidacion_Guardar
-- -----------------------------------------------------


DROP procedure IF EXISTS `spLiquidacion_Guardar`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spLiquidacion_Guardar`(IN docImpreso NVARCHAR(20),IN iduser INT,IN tc INT, IN idproveedor int, in procedencia varchar(45),in agencia decimal(12,4),in almacen decimal(12,4),in papeleria decimal(4,2),in transporte decimal(4,2),IN peso DECIMAL(12,4),in flete decimal(12,4),in seguro decimal(12,4),in gastos decimal(12,4),in tsim int,IN spe int,in iva int,  in iso int, IN totaldoc DECIMAL(12,4))
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
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spLiquidacion_Iniciar
-- -----------------------------------------------------


DROP procedure IF EXISTS `spLiquidacion_Iniciar`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spLiquidacion_Iniciar`()
BEGIN
    SELECT idbodega AS Id, nombrebodega AS Bodega FROM bodegas;

    SELECT idpersona AS Id,nombre AS Proveedor FROM personas WHERE tipopersona=2;

    SELECT CAST(idarticulo AS CHAR) AS Id, Descripcion AS 'Articulo',CAST( dai AS CHAR) AS dai,CAST( isc AS CHAR) AS isc,CAST(comision AS CHAR) AS comision FROM vw_articulosconcostosactuales;

    SELECT Codigo AS Id,Descripcion, idcuenta FROM cuentascontables c WHERE padre<>1;

    SELECT c.idcostoagregado,valorcosto,factorpeso,idtipocosto FROM costosagregados c left JOIN tsim t ON c.idcostoagregado=t.idtsim WHERE activo=1 AND idtipocosto in (1,4,5,6) ;
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spSalidasBodegaDetalladas
-- -----------------------------------------------------


DROP procedure IF EXISTS `spSalidasBodegaDetalladas`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spSalidasBodegaDetalladas`(in iddoc int)
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
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure sp_ArticulosProrrateados
-- -----------------------------------------------------


DROP procedure IF EXISTS `sp_ArticulosProrrateados`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `sp_ArticulosProrrateados`()
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
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spvercostoarticulo
-- -----------------------------------------------------


DROP procedure IF EXISTS `spvercostoarticulo`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spvercostoarticulo`( IN idarticulo INT,IN idtc INT)
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


END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spMovimientosCuentaBanco
-- -----------------------------------------------------


DROP procedure IF EXISTS `spMovimientosCuentaBanco`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spMovimientosCuentaBanco`( IN IDCUENTA INT,IN FECHA DATE)
BEGIN

      DECLARE saldo DECIMAL(12,4);
      DECLARE iddoc  INTEGER;

      -- OBTENER LA FECHA DEL MES ANTERIOR
      SELECT DATE_SUB(FECHA, INTERVAL DAY(FECHA) DAY) INTO @fecha;


      -- OBTENER EL SALDO DE LA CUENTA AL MES ANTERIOR Y EL IDDOCUMENTO
      SELECT
        d.iddocumento,
        d.total
      FROM documentos d
      JOIN tiposdoc td ON td.idtipodoc=d.idtipodoc
      JOIN cuentasxdocumento cd on cd.iddocumento=d.iddocumento AND cd.idcuenta=IDCUENTA
      WHERE d.idtipodoc=24
      AND d.fechacreacion =@fecha
      INTO @iddoc,@saldo
      ;

      -- SI IDDOC ES IGUAL A NULL EL SALDO INICIAL ES 0 PORQUE NO EXISTE UNA LIQUIDACION ANTERIOR.
      IF @iddoc IS NULL THEN
         SET @saldo=0.00;
      END IF;



      -- ELIMINA LA TABLA EN CASO QUE EXISTA
      DROP TEMPORARY TABLE IF EXISTS temp;

      -- CREA UNA TABLA TEMPORAL
      CREATE TEMPORARY TABLE temp (
        `iddocumento` int(10) unsigned NOT NULL,
        `concepto` varchar(50) NOT NULL,
        `monto` decimal(12,4) NULL,
        `fecha` date NOT NULL,
        `conciliado` tinyint(1) NOT NULL DEFAULT '0',
        PRIMARY KEY (`iddocumento`)
);

    -- INSERTA LA PRIMER LINEA QUE CONTIENE EL SALDO DEL MES ANTERIOR
    INSERT INTO temp VALUES(0,'Saldo del mes anterior',0.00,@fecha,0);

    -- INSERTAR MOVIMIENTOS DEL MES
    INSERT INTO temp
    SELECT
        d.iddocumento,
        CONCAT(td.descripcion,' ',d.ndocimpreso) as concepto,
        d.total,
        d.fechacreacion,
        IF(ph.idpadre IS NULL, 0,1) as conciliado
        FROM documentos d
        JOIN tiposdoc td ON td.idtipodoc=d.idtipodoc AND d.idtipodoc=24
        LEFT JOIN docpadrehijos ph ON ph.idhijo=d.iddocumento
        WHERE d.fechacreacion <=@fecha;

    --
    SELECT
      DATE_FORMAT(Fecha,'%d/%m/%y') as Fecha,
      Concepto,
      monto,
      @saldo:=monto + @saldo AS SALDO,
      Conciliado,
      iddocumento
    FROM TEMP;

      DROP TEMPORARY TABLE IF EXISTS temp;
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spMovimientoCuenta
-- -----------------------------------------------------


DROP procedure IF EXISTS `spMovimientoCuenta`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spMovimientoCuenta`(IN ID INT,IN FECHACONCI DATETIME)
BEGIN

      SELECT
       -- LAST_DAY(CURDATE() - INTERVAL 1 MONTH),
       -- LAST_DAY(CURDATE()),
        LAST_DAY(FECHACONCI - INTERVAL 1 MONTH),
        LAST_DAY(FECHACONCI)+ INTERVAL 1 DAY,
         0
      INTO
        @fechapasada,
        @fecha,
        @id
         ;


      SELECT
      SUM(monto)
      FROM cuentasxdocumento cd
      JOIN documentos d ON cd.iddocumento=d.iddocumento
      WHERE idcuenta=ID
      AND  d.fechacreacion <=@fechapasada
      INTO @saldo;

      IF @saldo IS NULL THEN
          SET @saldo=0;
      END IF;

      SET @monto=@saldo;

      DROP TEMPORARY TABLE IF EXISTS temp;
      CREATE TEMPORARY TABLE temp
      SELECT
        DATE_FORMAT(d.fechacreacion,'%d/%m/%y') as Fecha,
        CONCAT(td.codigodoc,' ',IF(d.idtipodoc=12,CONCAT('# ',d.ndocimpreso),DATE_FORMAT(IF(tc.fecha IS NULL,d.fechacreacion,tc.fecha),'%d/%m/%y'))) AS concepto,
        cd.monto,
        @saldo:=cd.monto+@saldo as saldo,
        IF(ph.idpadre IS NULL,0,1) as conciliado,
        d.iddocumento,
        CONCAT(td.descripcion,' ',IF(d.idtipodoc=12,CONCAT('# ',d.ndocimpreso),DATE_FORMAT(IF(tc.fecha IS NULL,d.fechacreacion,tc.fecha),'%d/%m/%y'))) AS concepto2,
        d.idtipodoc,
        @id:= @id + 1 as idmov
      FROM cuentasxdocumento cd
      JOIN cuentascontables c ON cd.idcuenta=c.idcuenta AND c.idcuenta=ID
      JOIN documentos d ON d.iddocumento  = cd.iddocumento
      JOIN tiposdoc td ON td.idtipodoc = d.idtipodoc
      LEFT JOIN tiposcambio tc ON tc.idtc = d.idtipocambio
      LEFT JOIN docpadrehijos ph ON ph.idhijo=d.iddocumento
      LEFT JOIN documentos padre ON padre.iddocumento=ph.idpadre AND padre.idtipodoc=24
      WHERE d.fechacreacion > @fechapasada AND d.fechacreacion< @fecha
      ORDER by d.fechacreacion
       ;


      INSERT INTO temp values (DATE_FORMAT(@fechapasada,'%d/%m/%y'),'Saldo del mes anterior',0,@monto,0,0,'Saldo Final del mes anterior',0,0);

      Select
      Fecha,
      Concepto,
      Monto,
      Saldo,
      Conciliado,
      idtipodoc,
      concepto2,
      iddocumento,
      idmov
      FROM temp
      ORDER BY idmov
       ;

      DROP TEMPORARY TABLE temp;


END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spBalance
-- -----------------------------------------------------


DROP procedure IF EXISTS `spBalance`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spBalance`(IN FECHA DATE)
BEGIN



    SET @CONT:=0;



    DROP TEMPORARY TABLE IF EXISTS temp;



    CREATE TEMPORARY TABLE temp

        SELECT

          cc.codigo,

          cc.descripcion,

          SUM(monto) as saldo,

          cc.esdebe,

          cc.padre,

          cc.idcuenta,

          0 as hijos

--          ,          @CONT:= @CONT+1 as cont

          FROM cuentasxdocumento cd

          JOIN cuentascontables cc ON cc.idcuenta = cd.idcuenta

          JOIN documentos d ON d.iddocumento = cd.iddocumento

          WHERE MONTH(d.fechacreacion)=MONTH(FECHA) AND YEAR(d.fechacreacion)=YEAR(FECHA)

          GROUP BY cd.idcuenta

;



    DROP TEMPORARY TABLE IF EXISTS temp2;

CREATE TEMPORARY TABLE temp2 select * from temp;

-- (

--      `codigo` varchar(20),

--  `descripcion` varchar(45),

--  `esdebe` tinyint(1),

--  `saldo` DECIMAL(12,4),

--  `padre` int(10),

--  `idcuenta` int(10)

--  );



    DROP TEMPORARY TABLE IF EXISTS resultados;

CREATE TEMPORARY TABLE resultados select * from temp;



 WHILE (SELECT COUNT(*) FROM temp2 WHERE padre>1)>0 DO

-- SELECT 5 INTO @C;

-- WHILE @C >0 DO



--  SELECT COUNT(*) FROM temp2 WHERE padre>1;

  DELETE FROM resultados;



  INSERT INTO resultados

  SELECT

          cc.codigo,

          cc.descripcion,

          0,

          cc.esdebe,

          cc.padre,

          cc.idcuenta,

          COUNT(cc.idcuenta)

-- ,          @CONT:= @CONT+1 as cont

  FROM cuentascontables cc

  JOIN temp2 t ON t.padre = cc.idcuenta

  WHERE t.padre>1

  GROUP BY cc.idcuenta

   ;



  delete from temp2;

  insert into temp2 SELECT * FROM resultados;

  insert into temp SELECT * FROM resultados;



--  SET @C = @C -1;

 END WHILE;



           select

          codigo,

          descripcion,

          IF(esdebe=1,1,IF(idcuenta BETWEEN 148 AND 168,2,0)),

          max(hijos) as nhijos,

          sum(saldo) as saldo,

          padre,

          idcuenta

-- ,          cont

 from temp group by idcuenta  order by idcuenta;



  DROP TEMPORARY TABLE temp;

  DROP TEMPORARY TABLE temp2;

  DROP TEMPORARY TABLE resultados;

END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spEstadoResultado
-- -----------------------------------------------------


DROP procedure IF EXISTS `spEstadoResultado`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spEstadoResultado`(IN FECHA DATE)
BEGIN





    SET @totalBruto:=0;



    DROP TEMPORARY TABLE IF EXISTS temp;



    CREATE TEMPORARY TABLE temp

SELECT

          cc.codigo,

          cc.descripcion,

          SUM(IFNULL(cd.monto,0)) as saldo,



          @totalBruto:=@totalBruto+ IFNULL(cd.monto,0) as total,

          cc.esdebe,

          cc.padre,

          cc.idcuenta,

          IF(

          cc.idcuenta = 173,

          1

          ,2) as orden

FROM cuentascontables cc

LEFT JOIN cuentasxdocumento cd ON cc.idcuenta = cd.idcuenta

LEFT JOIN documentos d ON d.iddocumento = cd.iddocumento

WHERE MONTH(d.fechacreacion) = MONTH(FECHA) AND YEAR(d.fechacreacion)=YEAR(FECHA)

 AND

-- WHERE

cc.idcuenta IN (173,182)

GROUP BY cc.idcuenta

;





 INSERT INTO temp VALUES('',IF(@totalBruto>=0,'UTILIDAD BRUTA','PERDIDA BRUTA'),@totalBruto,@totalBruto,1,1,0,3);

 INSERT INTO temp VALUES('','',@totalBruto,@totalBruto,1,1,1,4);





 SET @totalOperacion:=0;

 INSERT INTO temp

SELECT

          cc.codigo,

          cc.descripcion,

          SUM(IFNULL(cd.monto,0)) as saldo,

          @totalOperacion:=@totalOperacion+ SUM(IFNULL(cd.monto,0)) as total,

          cc.esdebe,

          cc.padre,

          cc.idcuenta,

          IF(

          cc.idcuenta = 180,

          5

          ,IF(

          cc.idcuenta = 248,

          6

          ,IF(

          cc.idcuenta = 184,

          7

          ,IF(

          cc.idcuenta = 314,

          8

          ,IF(

          cc.idcuenta = 327,

          9

          ,IF(

          cc.idcuenta = 323,

          10

          ,0

          )))))) as orden

FROM cuentascontables cc

LEFT JOIN cuentasxdocumento cd ON cc.idcuenta = cd.idcuenta

LEFT JOIN documentos d ON d.iddocumento = cd.iddocumento

WHERE MONTH(d.fechacreacion) = MONTH(FECHA) AND YEAR(d.fechacreacion)=YEAR(FECHA)

 AND

cc.idcuenta IN (180,248,184,314,327,323)

GROUP BY cc.idcuenta

;



INSERT INTO temp VALUES('',IF(@totalOperacion>=0,'UTILIDAD OPERATIVA','PERDIDA OPERATIVA'),@totalOperacion,@totalOperacion,1,1,0,11);

SET @total:=@totalBruto+@totalOperacion;

INSERT INTO temp VALUES('',IF(@total>=0,'UTILIDAD NETA ANTES DEL IR','PERDIDA NETA'),@total,@total,1,1,0,12);



SELECT

         Codigo,

         Descripcion,

         IF(padre=1,'',saldo) as Saldo,

         IF(idcuenta=0,total,'') as Total

--         ,

--         esdebe,

--         padre,

--         idcuenta

 ,          orden

 from temp

 ORDER BY orden

 ;

   DROP TEMPORARY TABLE temp;



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spConsecutivo
-- -----------------------------------------------------


DROP procedure IF EXISTS `spConsecutivo`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spConsecutivo`(IN TIPODOC INTEGER,IN CUENTA INTEGER)
BEGIN



        IF TIPODOC=12 THEN

              SELECT

                    IF(seriedoc>MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED)),seriedoc,MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED))+1) as actual

              FROM cuentasbancarias c

              LEFT JOIN cuentasxdocumento cxd ON cxd.idcuenta=c.idcuentacontable

              LEFT JOIN documentos d ON cxd.iddocumento=d.iddocumento AND d.idtipodoc=12

              WHERE idcuentacontable=CUENTA

              ;

        ELSE

          SELECT IF(IFNULL(seriedoc,1)>MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED)),IFNULL(seriedoc,1),MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED))+1) as actual FROM tiposdoc t

          LEFT JOIN documentos d ON d.idtipodoc=t.idtipodoc

          WHERE t.idtipodoc=TIPODOC

          ;

        END IF;



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spTotalesSesion
-- -----------------------------------------------------


DROP procedure IF EXISTS `spTotalesSesion`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spTotalesSesion`(IN IDSESION INT)

BEGIN



  SELECT

      p.idtipomovimiento,

      tp.descripcion,

      p.idtipomoneda,

      tm.moneda,

      tm.simbolo,

--      p.monto,

 SUM(IFNULL(p.monto,d.total)) as Total

  FROM documentos d

  JOIN movimientoscaja p ON d.iddocumento = p.iddocumento

  JOIN tiposmovimientocaja tp ON p.idtipomovimiento = tp.idtipomovimiento

  JOIN tiposmoneda tm ON p.idtipomoneda = tm.idtipomoneda

  LEFT JOIN docpadrehijos ph ON ph.idhijo = d.iddocumento

  WHERE (d.iddocumento = IDSESION OR ph.idpadre= IDSESION)

  GROUP BY p.idtipomoneda,p.idtipomovimiento

  ;



END;


$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- function fnConsecutivo
-- -----------------------------------------------------


DROP function IF EXISTS `fnConsecutivo`;

DELIMITER $$

DELIMITER $$
CREATE FUNCTION `fnConsecutivo`(TIPODOC INTEGER,CUENTA INTEGER) RETURNS int(11)

NOT DETERMINISTIC 

READS SQL DATA
BEGIN





        IF TIPODOC=12 THEN

              SELECT

                    IF(seriedoc>MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED)),seriedoc,MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED))+1) as actual

              FROM cuentasbancarias c

              LEFT JOIN cuentasxdocumento cxd ON cxd.idcuenta=c.idcuentacontable

              LEFT JOIN documentos d ON cxd.iddocumento=d.iddocumento AND d.idtipodoc=12

              AND d.idestado <>3

              WHERE idcuentacontable=CUENTA



              INTO @number;

        ELSE

          SELECT IF(IFNULL(seriedoc,1)>MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED)),IFNULL(seriedoc,1),MAX(CAST( IFNULL(ndocimpreso,0) AS SIGNED))+1) as actual FROM tiposdoc t

          LEFT JOIN documentos d ON d.idtipodoc=t.idtipodoc

          AND d.idestado <>3

          WHERE t.idtipodoc=TIPODOC



          INTO @number

          ;

        END IF;



        RETURN @number;

END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spAutorizarFactura
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAutorizarFactura`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAutorizarFactura`(

IDFACTURA INT,

IDGERENTE INT,

ACCIONAUTORIZAR INT,

CONFIRMADO INT,

VENTASNETAS INT,

CXCCLIENTE INT,

INVENTARIO INT,

COSTOSVENTAS INT,

IMPUESTOSXPAGAR INT

)
BEGIN



-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

 DECLARE EXIT HANDLER FOR SQLEXCEPTION

  BEGIN

      ROLLBACK;

      CALL RaiseException();

  END;



      START TRANSACTION;

      -- OBTENGO EL ESTADO ACTUAL DEL DOCUMENTO

          SELECT idestado FROM documentos WHERE iddocumento = IDFACTURA INTO @estado;



     -- VERIFICO QUE NO ESTE CONFIRMADO.

     IF @estado = CONFIRMADO THEN



        SELECT FALSE;



      ELSE
      
      
      -- OBTENGO EL CONSECUTIVO, EL TOTAL , EL SUBTOTAL, EL IVA, Y EL TOTAL COSTO



        SELECT



            fnconsecutivo(idtipodoc,NULL),



            total * tc.tasa as total,



            ROUND((total/(1 + (IFNULL(ca.valorcosto,0)/100)))*tc.tasa,4) as subtotal,



            ROUND((



            total - (total/(1 + (IFNULL(ca.valorcosto,0)/100)))



            )*tc.tasa,4) as totaliva,



            ROUND(SUM(-ad.unidades * ad.costounit),4) as totalcosto

        FROM documentos d

        JOIN tiposcambio tc ON tc.idtc = d.idtipocambio

        JOIN articulosxdocumento ad ON ad.iddocumento = IDFACTURA
        
        LEFT JOIN costosxdocumento cd ON cd.iddocumento = IDFACTURA

        LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado

        WHERE d.iddocumento = IDFACTURA

        INTO

        @numero,

        @total,

        @subtotal,

        @iva,

        @costo

         ;



        -- LE PASO EL ESTADO A CONFIRMAOD Y LE PONGO EL CONSECUTIVO QUE LE CORRESPONDE

        UPDATE documentos SET idestado=CONFIRMADO,ndocimpreso = @numero WHERE iddocumento = IDFACTURA;



        -- INSERTO LA RELACION DE LA FACTURA CON LA PERSONA QUE LA AUTORIZA

        INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDFACTURA,ACCIONAUTORIZAR);



        -- INSERTO LA RELACION DE LAS CUENTAS CONTABLES CON LA FACTURA

        INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto) VALUES

        (IDFACTURA,VENTASNETAS,-@subtotal),

        (IDFACTURA,CXCCLIENTE,@total),

        (IDFACTURA,INVENTARIO,-@costo),

        (IDFACTURA,COSTOSVENTAS,@costo)

        ;



        -- SOLO SI TIENE IVA INSERTO EL REGISTRO

        IF @iva >0 then

                INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto) VALUES

                (IDFACTURA,IMPUESTOSXPAGAR,-@iva);

        END IF;



    COMMIT;

    SELECT TRUE;

   END IF;



END

$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spEliminarFactura
-- -----------------------------------------------------


DROP procedure IF EXISTS `spEliminarFactura`;

DELIMITER $$

DELIMITER $$
 
CREATE PROCEDURE `spEliminarFactura`(IN iddoc INT)
BEGIN
       START TRANSACTION;

         DELETE FROM personasxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM costosxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM articulosxdocumento WHERE iddocumento=iddoc;
	    DELETE FROM docpadrehijos WHERE idhijo=iddoc;
	    DELETE FROM creditos WHERE iddocumento=iddoc LIMIT 1;
         DELETE FROM documentos WHERE iddocumento=iddoc LIMIT 1;
		
       COMMIT;

END 

$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- function fnImpuestos
-- -----------------------------------------------------


DROP function IF EXISTS `fnImpuestos`;

DELIMITER $$

DELIMITER $$
CREATE FUNCTION `fnImpuestos`(IDLIQ INT,CIFTOTAL DECIMAL(12,4),CIFPARCIAL DECIMAL(12,4),DAI DECIMAL(12,4),ISC DECIMAL(12,4)) RETURNS decimal(12,4)

NOT DETERMINISTIC 

READS SQL DATA
BEGIN

      DECLARE imp DECIMAL(12,4);

      SET @imp = 0;



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

      WHERE l.iddocumento = IDLIQ

      INTO @iva,@spe,@iso,@tsim,@factorpeso,@peso

      ;



      SET @factorcif = (CIFPARCIAL/CIFTOTAL);

-- RETURN @factorcif;

      SET @tsim = IFNULL((CEIL(@peso/@factorpeso) * @tsim * @factorcif) ,0) ;

-- RETURN @tsim;

-- RETURN CEIL(@peso/@factorpeso);

--  RETURN @tsim;

      SET @spe = IFNULL(@spe * @factorcif,0);

      SET @iso = IFNULL(@iso * CIFPARCIAL,0);

--       RETURN @;

      SET @iva = IFNULL((CIFPARCIAL + DAI + ISC + @tsim) * @iva,0);

      SET @imp =  IFNULL(@iva +  @spe + @tsim + @iso +  DAI + ISC,0) ;



      RETURN ROUND(@imp,4);



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spAutorizarAnulacionFactura
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAutorizarAnulacionFactura`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAutorizarAnulacionFactura`(

IDFACTURA INT,

IDGERENTE INT,

TIPOANULACION INT,

TIPOFACTURA INT,

TIPORECIBO INT,

TIPOKARDEX INT,

PENDIENTEANULAR INT,

CONFIRMADO INT,

ANULADO INT,

ACCIONAUTORIZAR INT

)

BEGIN

-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

 DECLARE EXIT HANDLER FOR SQLEXCEPTION

  BEGIN

      ROLLBACK;

      CALL RAISE_EXCEPTION();

  END;



-- INICIO TRANSACCION

    START TRANSACTION;



-- OBTENGO EL ID DE LA FACTURA QUE FUE ANULADA

      SELECT

          fac.ndocimpreso,

          fac.idestado AS anulacionEstado,

          fac.idtipodoc ,

          SUM(IF(hijo.idtipodoc = TIPOANULACION,hijo.iddocumento,0)) AS anulacionId,

          SUM(IF(hijo.idtipodoc = TIPOKARDEX,hijo.iddocumento,0)) AS kardexId,

          fac.escontado AS facturaContado

      FROM documentos fac

      JOIN docpadrehijos ph ON ph.idpadre = fac.iddocumento

      JOIN documentos hijo ON ph.idhijo = hijo.iddocumento AND hijo.idtipodoc in (TIPOANULACION,TIPOKARDEX)

       WHERE

      -- fac.idtipodoc =5

       --  AND

         fac.iddocumento = IDFACTURA

    INTO

    @nfactura,

    @anulEstado,

    @tipo,

    @anulacion,

    @kardex,

    @esContado

     ;



    SELECT

        rec.iddocumento,

        COUNT(iddocumento) as nrecibo

    FROM documentos rec

    JOIN  docpadrehijos ph ON ph.idhijo = rec.iddocumento

    AND rec.idtipodoc=TIPORECIBO

    AND ph.idpadre =IDFACTURA

    INTO

    @recibo,

    @nrec

    ;





  IF @tipo <> TIPOFACTURA OR (@anulEstado <> PENDIENTEANULAR) OR (@esContado = 0 AND (@nrec > 0)) THEN



      SELECT FALSE;



  ELSE



-- OBTENGO EL ID DEL RECIBO EN CASO DE QUE LA FACTURA FUERA AL CONTADO O HALLA SIDO PAGADA POR UN RECIBO





-- INSERTO LA RELACION DE LA ANULACION CON LA PERSONA QUE LA AUTORIZA

    INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,@anulacion,ACCIONAUTORIZAR);



-- REVIERTO LAS CUENTAS CONTABLES DE LA FACTURA, RELACIONANDOLAS CON LA ANULACION

    INSERT INTO cuentasxdocumento

      SELECT

         @anulacion,

         cxd.idcuenta,

         SUM(-cxd.monto) AS monto,

         nlinea

         FROM documentos doc

         JOIN cuentasxdocumento cxd ON  cxd.iddocumento = doc.iddocumento AND cxd.iddocumento IN (IDFACTURA,@recibo)

         GROUP BY cxd.idcuenta

         HAVING SUM(-cxd.monto)<>0

         ;



    IF @kardex != 0 THEN



        INSERT INTO articulosxdocumento(iddocumento,idarticulo,unidades,costocompra,costounit,precioventa,nlinea)

        SELECT @anulacion,idarticulo,-unidades,costocompra,costounit,precioventa,nlinea

        FROM articulosxdocumento

        WHERE iddocumento = IDFACTURA;



    END IF;



    -- VERIFICO SI HAY RECIBO

    IF @recibo is not null then



-- INSERTO LA RELACION ENTRE EL RECIBO Y  LA ANULACION, LA ANULACION ES EL HIJO.

      INSERT INTO docpadrehijos(idpadre,idhijo) VALUES

      (@recibo,@anulacion)

       ;



-- ACTUALIZO EL ESTADO DEL RECIBO A ANULADO

      UPDATE documentos SET idestado = ANULADO where iddocumento = @recibo LIMIT 1;

   END IF;



-- ACTUALIZO EL ESTADO DE LA FACTURA A ANULADO

      UPDATE documentos SET idestado = ANULADO where iddocumento = IDFACTURA LIMIT 1;



-- ACTUALIZO EL ESTADO DE LA ANULACION Y LO PASO A CONFIRMADO, Y LE PONGO EL NUMERO DE LA FACTURA EN NDOCIMPRESO

    UPDATE documentos SET idestado = CONFIRMADO, ndocimpreso =@nfactura WHERE iddocumento = @anulacion LIMIT 1;





    COMMIT;

    SELECT TRUE;

   END IF;

END

$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spAutorizarDevolucion
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAutorizarDevolucion`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAutorizarDevolucion`(

IDNC INT,

IDGERENTE INT,

AUTORIZAR INT,

TIPONC INT,

TIPOFACTURA INT,

TIPOCIERRE INT,

TIPORECIBO INT,

CONFIRMADO INT,

PENDIENTE INT,

VENTAS INT,

COSTOVENTA INT,

IVAXPAGAR INT,

RETENCIONPAGADA INT,

CAJA INT,

INVENTARIO INT





)
BEGIN



--  DECLARE EXIT HANDLER FOR SQLEXCEPTION

--  BEGIN

--      ROLLBACK;

--      SELECT False;

--  END;





    START TRANSACTION;





SELECT

-- *

fnConsecutivo(TIPONC,null) as ndocimpreso,

fac.iddocumento as idfactura,

-- ROUND(dev.total * tc.tasa,4) as 'totaldev C$',

ROUND((dev.total * tc.tasa) / (1 + (ca.valorcosto/100)),4) as 'subtotal dev',

ca.valorcosto as 'tasaIVA',

 tc.tasa,

-- phrec.monto,0)) as 'total abono'

dev.total 'totaldev $',

-- (SUM(IFNULL(phrec.monto,0)) - SUM(IFNULL(phrecdev.monto,0))) as totalabonos,

-- -- SUM(IFNULL(phrec.monto,0)) as abono,

-- SUM(IFNULL(phrecdev.monto,0)) as abonosdevueltos,

(

(dev.total <= (SUM(IFNULL(phrec.monto,0)) - SUM(IFNULL(phrecdev.monto,0)))) AND

dev.idestado IN (PENDIENTE))



 AS aceptable,

IF(cierre.iddocumento IS NULL,0,1) AS cerrado



FROM documentos dev



JOIN docpadrehijos ph ON ph.idhijo = dev.iddocumento

JOIN documentos fac ON ph.idpadre = fac.iddocumento AND fac.idtipodoc = TIPOFACTURA



LEFT JOIN docpadrehijos phcierre ON phcierre.idpadre = fac.iddocumento

LEFT JOIN documentos cierre ON phcierre.idhijo = cierre.iddocumento AND cierre.idtipodoc = TIPOCIERRE





LEFT JOIN docpadrehijos phrec ON phrec.idpadre = fac.iddocumento

LEFT JOIN documentos rec ON phrec.idhijo = rec.iddocumento AND rec.idtipodoc = TIPORECIBO



LEFT JOIN docpadrehijos phrecdev ON phrecdev.idpadre = rec.iddocumento

LEFT JOIN documentos recdev ON phrecdev.idhijo = recdev.iddocumento AND recdev.idtipodoc=TIPONC





JOIN tiposcambio tc on tc.idtc = fac.idtipocambio

LEFT JOIN costosxdocumento cd ON cd.iddocumento = fac.iddocumento

LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado

WHERE

dev.iddocumento =IDNC

    INTO

    @numeroNC,

    @idfactura,

    @subtotal,

    @tasaIVA,

    @tasa,

    @totaldev,

    @aceptable,

    @cerrado

     ;



IF @aceptable <> 1 OR @cerrado =1 THEN

  SELECT FALSE;



ELSE



SET @totalret:=0;



DROP TEMPORARY TABLE IF EXISTS devolucionxabono;

CREATE TEMPORARY TABLE devolucionxabono

SELECT

rec.iddocumento as idrecibo,

phrec.monto as totalabono,

SUM(

IFNULL(phrecdev.monto,0)

) as totaldevuelto,



phrec.monto - SUM(IFNULL(phrecdev.monto,0)) as saldoactual,



@totaldev as totaldev,

ROUND(

IF(

IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),

IFNULL(@totaldev,0),

phrec.monto - SUM(IFNULL(phrecdev.monto,0))

) ,4) as devparcial,

ROUND(

IF(

IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),

IFNULL(@totaldev,0),

phrec.monto - SUM(IFNULL(phrecdev.monto,0))

) /

(

(100 + @tasaIVA)/

ca.valorcosto

)

,4) as retencionparcial,

(

@totalret:=

@totalret +

ROUND(

IF(

IFNULL(@totaldev,0) <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),

IFNULL(@totaldev,0),

phrec.monto - SUM(IFNULL(phrecdev.monto,0))

) /

(

(100 + @tasaIVA)/

ca.valorcosto

)

,4)

)as sumaret,

(

@totaldev:=

ROUND(

@totaldev -

IF(

@totaldev <= phrec.monto - SUM(IFNULL(phrecdev.monto,0)),

@totaldev,

phrec.monto - SUM(IFNULL(phrecdev.monto,0))

)

,4)

) AS devrestante

FROM

docpadrehijos phrec

JOIN documentos rec ON phrec.idhijo =rec.iddocumento AND rec.idtipodoc = TIPORECIBO

LEFT JOIN docpadrehijos phrecdev ON phrecdev.idpadre = rec.iddocumento

LEFT JOIN documentos recdev ON phrecdev.idhijo = recdev.iddocumento AND recdev.idtipodoc = TIPONC

LEFT JOIN costosxdocumento cd ON cd.iddocumento = rec.iddocumento

LEFT JOIN costosagregados ca ON ca.idcostoagregado = cd.idcostoagregado

WHERE phrec.idpadre = @idfactura

GROUP BY rec.iddocumento

;



-- INSERTAR LA RELACION CON LOS recibos

INSERT INTO docpadrehijos(idpadre,idhijo,monto)

SELECT

idrecibo,

IDNC,

devparcial

FROM devolucionxabono

WHERE devparcial <> 0

;



IF @cerrado = 1 THEN

  SET @totalret:= 0;

  SET @totalIVA:= 0;

ELSE

  SET @totalret:= @totalret * @tasa;

  SET @totalIVA:= @subtotal * ROUND(@tasaIVA/100,4);

END IF;







select SUM(ROUND(unidades * costounit,4)) from articulosxdocumento WHERE iddocumento = IDNC INTO @totalcosto;











INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)

VALUES (IDNC,VENTAS,@subtotal),

(IDNC,CAJA,-(@subtotal + @totalIVA - @totalret))

;



IF @totalIVA >0 THEN

  INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)

  VALUES (IDNC,IVAXPAGAR,@totalIVA);

END IF;





IF @totalret >0 THEN

  INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)

  VALUES (IDNC,RETENCIONPAGADA,-@totalret);

END IF;





-- Revertir el costo de venta

INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto)

VALUES (IDNC,INVENTARIO,@totalcosto),

(IDNC,COSTOVENTA,-@totalcosto)

;





INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDGERENTE,IDNC,AUTORIZAR);



UPDATE documentos SET idestado = CONFIRMADO, ndocimpreso =@numeroNC where iddocumento = IDNC LIMIT 1;









     COMMIT;

     SELECT TRUE;

END IF;



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spDenegarAnulacion
-- -----------------------------------------------------


DROP procedure IF EXISTS `spDenegarAnulacion`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spDenegarAnulacion` (IN IDDOC INTEGER, IN ESTADO INTEGER,IN ANULACION INTEGER)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE
 DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      SELECT False;
  END;

START TRANSACTION;

SET @anulacion := (SELECT d.iddocumento FROM documentos d join docpadrehijos dh on d.iddocumento=dh.idhijo where dh.idpadre=IDDOC and d.idtipodoc=ANULACION);
	IF @anulacion>0 THEN
	
	UPDATE documentos d SET idestado=ESTADO where iddocumento=IDDOC LIMIT 1;
	delete from docpadrehijos where idhijo=@anulacion;
	delete from personasxdocumento where iddocumento=@anulacion;
	delete from documentos where iddocumento=@anulacion;

	ELSE

	SELECT FALSE;

  	END IF;
COMMIT;

END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- function fnFacturaAnulable
-- -----------------------------------------------------


DROP function IF EXISTS `fnFacturaAnulable`;

DELIMITER $$

DELIMITER $$
CREATE FUNCTION `fnFacturaAnulable`(

IDFACTURA INT,

TIPOFACTURA INT,

TIPORECIBO INT,

TIPONC INT,

CONFIRMADO INT,

PENDIENTEAUTORIZACION INT

) RETURNS tinyint(4)

NOT DETERMINISTIC 

READS SQL DATA
BEGIN



RETURN (SELECT

IF(fac.idestado in (CONFIRMADO,PENDIENTEAUTORIZACION),

IF(

-- Si la factura es de hoy verificar el estado

DATE(fac.fechacreacion) = DATE(NOW()),



-- si el estado es confirmado o pendiente de credito verificar si es al credito y tiene abonos

IF(

(fac.escontado=1) OR (SUM(IF(hijo.idtipodoc=TIPORECIBO,1,0))=0),



 -- si no tiene abonos o es al contado verificar si tiene devoluciones

IF(

SUM(IF(hijo.idtipodoc=TIPONC,1,0))=0,

-- Si cumple todas las condiciones devolver 1 que significa que se puede anular

1

-- si la factura tiene devoluciones devolver 5

,

5)

-- si la factura es al credito y tiene abono devolver 4

,

4)

,

-- Si la factura no tiene el estado confirmado o pendiente de autorizacion  retornar 3

3)

,

-- Si la factura no es de hoy retorna 2

2) as anulable

FROM documentos fac

LEFT JOIN docpadrehijos ph ON ph.idpadre = fac.iddocumento

LEFT JOIN documentos hijo ON ph.idhijo = hijo.iddocumento AND hijo.idtipodoc in (TIPORECIBO,TIPONC)

where fac.idtipodoc =TIPOFACTURA  and fac.iddocumento = IDFACTURA);



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spAutorizarCheque
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAutorizarCheque`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAutorizarCheque` (IN USERAUTORIZA INTEGER, IN IDCHEQUE INTEGER, IN IDACCION INTEGER, IN CUENTABANCARIA INTEGER, IN TIPODOC INTEGER, IN CONFIRMADO INTEGER)
BEGIN

-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

 DECLARE EXIT HANDLER FOR SQLEXCEPTION

  BEGIN

      ROLLBACK;

      SELECT False;

  END;



      START TRANSACTION;

      -- OBTENGO EL ESTADO ACTUAL DEL DOCUMENTO

          SELECT idestado FROM documentos WHERE iddocumento = IDCHEQUE INTO @estado;



     -- VERIFICO QUE NO ESTE CONFIRMADO.

     IF @estado = CONFIRMADO THEN

        SELECT FALSE;



      ELSE

	

	SELECT fnconsecutivo(TIPODOC,CUENTABANCARIA) INTO @numero;

	

	        -- LE PASO EL ESTADO A CONFIRMADO Y LE PONGO EL CONSECUTIVO QUE LE CORRESPONDE

        	UPDATE documentos SET idestado=CONFIRMADO,ndocimpreso = @numero WHERE iddocumento = IDCHEQUE LIMIT 1;



		INSERT INTO personasxdocumento (idpersona,iddocumento,idaccion) VALUES (USERAUTORIZA,IDCHEQUE,IDACCION);

	

		SELECT TRUE;

		COMMIT;

	END IF;
END

$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spAutorizarAnulacionCheque
-- -----------------------------------------------------


DROP procedure IF EXISTS `spAutorizarAnulacionCheque`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spAutorizarAnulacionCheque` (IN IDCHEQUE INTEGER,IN IDCUENTABANCARIA INTEGER,IN CONFIRMADO INTEGER, IN NDOCIMPRESO INTEGER, IN ACCIONAUTORIZAR INTEGER,IN TIPOANULACION INTEGER, IN IDAUTORIZA INTEGER)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

 DECLARE EXIT HANDLER FOR SQLEXCEPTION

  BEGIN

      ROLLBACK;

      SELECT False;

  END;



      START TRANSACTION;

      -- OBTENGO EL ESTADO ACTUAL DEL DOCUMENTO

          SELECT idestado FROM documentos WHERE iddocumento = IDCHEQUE INTO @estado;



     -- VERIFICO QUE NO ESTE CONFIRMADO.

     IF @estado = CONFIRMADO THEN



        SELECT FALSE;

	ROLLBACK;



      ELSE                               



	SET @IDANULACION := (SELECT an.iddocumento FROM documentos an JOIN docpadrehijos ph ON an.iddocumento = ph.idhijo AND ph.idpadre =IDCHEQUE AND an.idtipodoc=TIPOANULACION);



        -- LE PASO EL ESTADO A CONFIRMAOD Y LE PONGO EL CONSECUTIVO QUE LE CORRESPONDE

        UPDATE documentos SET idestado=CONFIRMADO,ndocimpreso = NDOCIMPRESO WHERE iddocumento = IDCHEQUE LIMIT 1;



        -- INSERTO LA RELACION DE LA ANULACION DE CHEQUE CON LA PERSONA QUE LA AUTORIZA

        INSERT INTO personasxdocumento(idpersona, iddocumento,idaccion) VALUES (IDAUTORIZA,IDCHEQUE,ACCIONAUTORIZAR);

	INSERT INTO cuentasxdocumento 

		SELECT

				@IDANULACION,

		            c.idcuenta,

		            -c.monto as Monto,

			    nlinea

	        FROM cuentasxdocumento c 

	        JOIN documentos d ON c.iddocumento = d.iddocumento

	        JOIN cuentascontables cc ON cc.idcuenta = c.idcuenta

        	WHERE d.iddocumento = IDCHEQUE

       		ORDER BY nlinea;

    COMMIT;

    SELECT TRUE;

   END IF;
END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure spCierreMensual
-- -----------------------------------------------------


DROP procedure IF EXISTS `spCierreMensual`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `spCierreMensual`(

IN IDCIERRE INTEGER,

IN MES INTEGER,

IN ESTADO INTEGER,

IN ANO INTEGER,

IN INGRESOSXVENTA INTEGER,

IN OTROSINGRESOS INTEGER,

IN COSTOSGASTOSOPERACIONES INTEGER,

IN GASTOSXVENTAS INTEGER,

IN GASTOS INTEGER,

IN GASTOSFINANCIEROS INTEGER,

IN PRODUCTOSFINANCIEROS INTEGER,

IN OTROSGASTOS INTEGER,

IN PERDIDASGANANCIAS INTEGER)

BEGIN

    -- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

    DECLARE EXIT HANDLER FOR SQLEXCEPTION

    BEGIN

        ROLLBACK;

       CALL RAISE_EXCEPTION();

    END;



    START TRANSACTION;



        SET @concierre := (

            SELECT d.iddocumento

            FROM documentos d

            WHERE d.idtipodoc=IDCIERRE

            AND MONTH(fechacreacion)=MES

            AND YEAR(d.fechacreacion)=ANO

        );

        IF @concierre is null THEN



            -- Determina el montototal de las cuentas de resultado

            SET @MONTOCUENTAS := (

                SELECT SUM(IFNULL(monto,0)) monto

                FROM cuentascontables cc

                JOIN cuentascontables ccc ON ccc.codigo LIKE CONCAT(SUBSTR(cc.codigo,1,5),'%')

                LEFT JOIN cuentasxdocumento cxd ON ccc.idcuenta = cxd.idcuenta

                JOIN documentos d on d.iddocumento=cxd.iddocumento

                wHERE cc.idcuenta IN (

                    INGRESOSXVENTA,

                    COSTOSGASTOSOPERACIONES,

                    GASTOSXVENTAS,

                    GASTOS,

                    GASTOSFINANCIEROS,

                    PRODUCTOSFINANCIEROS,

                    OTROSGASTOS

                )

                AND MONTH(d.fechacreacion)=MES

                AND YEAR(d.fechacreacion)=ANO

            );



            SELECT fnconsecutivo(IDCIERRE,NULL) INTO @NUMERO;

            INSERT INTO documentos (NDOCIMPRESO,TOTAL,IDTIPODOC,IDESTADO,FECHACREACION)

            VALUES(@NUMERO,@MONTOCUENTAS,IDCIERRE,ESTADO,NOW());

            SET @NDOCCIERRE := LAST_INSERT_ID();

            -- CIERRA TODAS LAS CUENTAS DE RESULTADOS

            -- Inserta los movimientos con saldo invertido para convertir el saldo de las cuentas

            -- a CERO y estas a su vez son asignadas al documento cierre que se crea en este procedimiento



            INSERT into cuentasxdocumento

            SELECT

                @NDOCCIERRE,

                ccc.idcuenta,

                SUM(IFNULL(monto*-1,0)) monto

                ,NULL

            FROM cuentascontables cc

            JOIN cuentascontables ccc ON ccc.codigo LIKE CONCAT(SUBSTR(cc.codigo,1,3),'%')

            LEFT JOIN cuentasxdocumento cxd ON ccc.idcuenta = cxd.idcuenta

            JOIN documentos d on d.iddocumento=cxd.iddocumento

            wHERE cc.idcuenta IN (INGRESOSXVENTA,

            OTROSINGRESOS,

            COSTOSGASTOSOPERACIONES,

            GASTOSXVENTAS,

            GASTOS,

            GASTOSFINANCIEROS,

            PRODUCTOSFINANCIEROS,

            OTROSGASTOS)

            AND MONTH(d.fechacreacion)=MES AND YEAR(d.fechacreacion)=ANO and CONCAT(SUBSTR(ccc.codigo,5,3))!='000'

            GROUP BY ccc.idcuenta

            HAVING monto!=0;



            -- Inserta docpadrehijos de todos los docs a este cierre

            INSERT INTO docpadrehijos

            SELECT

                @NDOCCIERRE,

                iddocumento,

                NULL,

                NULL

            FROM documentos d

            JOIN estadosdocumento estados ON estados.idestado=d.idestado

            JOIN tiposdoc td ON d.idtipodoc=td.idtipodoc

            WHERE MONTH(fechacreacion)=MES

            AND YEAR(d.fechacreacion)=ANO

            AND d.idtipodoc!=22;



            -- Inserta el total de los movimientos de las cuentascontables en perdidas y ganancias

            INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto,nlinea)

            VALUES(@NDOCCIERRE,PERDIDASGANANCIAS,@MONTOCUENTAS,null);



            IF @MONTOCUENTAS > 0 THEN



                SET @IR:= @MONTOCUENTAS * 0.01;

                -- INSERTA EL IR EN PERDIDAS Y GANANCIAS CUANDO EL SALDO ES MAYOR QUE O, ES DECIR CON UTILIDADES

                INSERT INTO cuentasxdocumento(iddocumento,idcuenta,monto,nlinea)

                VALUES (@NDOCCIERRE,PERDIDASGANANCIAS,@IR,null);



            END IF;



            COMMIT;

            SELECT TRUE;



    ELSE

        ROLLBACK;

        CALL RAISE_EXCEPTION();

    END IF;



END
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- procedure SpEliminarCheque
-- -----------------------------------------------------


DROP procedure IF EXISTS `SpEliminarCheque`;

DELIMITER $$

DELIMITER $$
CREATE PROCEDURE `SpEliminarCheque`(IN ANULACION INTEGER, IN ANULADO INTEGER,IN IDCHEQUE INTEGER, IN IDRETENCION INTEGER)
BEGIN
-- DECLARO UN ERROR HANDLER QUE HARA UN ROLLBACK EN CASO DE ERROR Y RETORNARA FALSE

-- DECLARE EXIT HANDLER FOR SQLEXCEPTION
 -- BEGIN

--      ROLLBACK;

--      CALL RAISE_EXCEPTION();

-- END;



-- INICIO TRANSACCION

    START TRANSACTION;

    -- Inserto cuentas contables con signo invertido para cancelar movimientos del cheque
    INSERT INTO cuentasxdocumento

      SELECT

         ANULACION,

         cxd.idcuenta,

         SUM(-cxd.monto) AS monto,

         nlinea

         FROM documentos doc

                  JOIN cuentasxdocumento cxd ON  cxd.iddocumento = doc.iddocumento AND cxd.iddocumento=ANULACION

         GROUP BY cxd.idcuenta

         HAVING SUM(-cxd.monto)<>0;

      -- Cambio el estado del cheque a Anulado
        UPDATE documentos set idestado=ANULADO where iddocumento=IDCHEQUE;

      -- Obtengo el IDHIJO que equivale a la retencion
        SELECT idhijo FROM docpadrehijos join tiposdoc td on td.idtipodoc=IDRETENCION WHERE idpadre=IDCHEQUE limit 1 into @idhijo;

      -- Cambio el estado de la retencion a Anulado
        UPDATE documentos set idestado=ANULADO where iddocumento=@idhijo;

       COMMIT;

END 
$$
DELIMITER ;
DELIMITER ;
-- -----------------------------------------------------
-- View `vw_articulosconcostosactuales`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_articulosconcostosactuales` ;
DROP TABLE IF EXISTS `vw_articulosconcostosactuales`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_articulosconcostosactuales` AS select `a`.`idarticulo` AS `idarticulo`,concat(`cat`.`nombre`,' ',`subcat`.`nombre`,' ',`m`.`nombre`) AS `descripcion`,sum(if((`ca`.`idtipocosto` = 3),`ca`.`valorcosto`,0)) AS `dai`,sum(if((`ca`.`idtipocosto` = 2),`ca`.`valorcosto`,0)) AS `isc`,sum(if((`ca`.`idtipocosto` = 7),`ca`.`valorcosto`,0)) AS `comision`,`a`.`ganancia` AS `ganancia`,`a`.`activo` AS `activo` from ((((`articulos` `a` join `categorias` `subcat` on((`a`.`idcategoria` = `subcat`.`idcategoria`))) join `categorias` `cat` on((`subcat`.`padre` = `cat`.`idcategoria`))) join `marcas` `m` on((`m`.`idmarca` = `a`.`idmarca`))) join `costosagregados` `ca` on((`ca`.`idarticulo` = `a`.`idarticulo`))) where (`ca`.`activo` = 1) group by `a`.`idarticulo`;

-- -----------------------------------------------------
-- View `vw_articulosdescritos`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_articulosdescritos` ;
DROP TABLE IF EXISTS `vw_articulosdescritos`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_articulosdescritos` AS select `a`.`idarticulo` AS `idarticulo`,concat(`c`.`nombre`,' ',`sc`.`nombre`,' ',`m`.`nombre`) AS `descripcion`,`c`.`idcategoria` AS `idcategoria`,`c`.`nombre` AS `categorias`,`sc`.`idcategoria` AS `idsubcategoria`,`sc`.`nombre` AS `subcategoria`,`m`.`idmarca` AS `idmarca`,`m`.`nombre` AS `marcas`,`a`.`activo` AS `activo`,`a`.`ganancia` AS `ganancia` from (((`articulos` `a` join `marcas` `m` on((`a`.`idmarca` = `m`.`idmarca`))) join `categorias` `sc` on((`a`.`idcategoria` = `sc`.`idcategoria`))) join `categorias` `c` on((`c`.`idcategoria` = `sc`.`padre`)));

-- -----------------------------------------------------
-- View `vw_costosdeldocumento`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_costosdeldocumento` ;
DROP TABLE IF EXISTS `vw_costosdeldocumento`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_costosdeldocumento` AS select `c`.`idcostoagregado` AS `idcostoagregado`,`tc`.`descripcion` AS `Descripcion`,`c`.`valorcosto` AS `valorcosto`,`cd`.`iddocumento` AS `iddocumento`,`td`.`descripcion` AS `TipoDoc`,`c`.`activo` AS `activo` from ((((`costosagregados` `c` join `costosxdocumento` `cd` on((`c`.`idcostoagregado` = `cd`.`idcostoagregado`))) join `tiposcosto` `tc` on((`c`.`idtipocosto` = `tc`.`idtipocosto`))) join `documentos` `d` on((`d`.`iddocumento` = `cd`.`iddocumento`))) join `tiposdoc` `td` on((`td`.`idtipodoc` = `d`.`idtipodoc`))) order by `cd`.`iddocumento`,`c`.`idcostoagregado`;

-- -----------------------------------------------------
-- View `vw_liquidacionesguardadas`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_liquidacionesguardadas` ;
DROP TABLE IF EXISTS `vw_liquidacionesguardadas`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_liquidacionesguardadas` AS select `l`.`iddocumento` AS `iddocumento`,`d`.`ndocimpreso` AS `ndocimpreso`,`l`.`procedencia` AS `procedencia`,`l`.`totalagencia` AS `totalagencia`,`l`.`totalalmacen` AS `totalalmacen`,`l`.`porcentajepapeleria` AS `porcentajepapeleria`,`l`.`porcentajetransporte` AS `porcentajetransporte`,`l`.`peso` AS `peso`,`l`.`fletetotal` AS `fletetotal`,`l`.`segurototal` AS `segurototal`,`l`.`otrosgastos` AS `otrosgastos`,`d`.`idtipocambio` AS `tipocambio`,`tc`.`fecha` AS `fecha`,`tc`.`tasa` AS `tasa`,`p`.`idpersona` AS `idpersona`,`p`.`nombre` AS `Proveedor`,`d`.`idestado` AS `estado`,`b`.`nombrebodega` AS `bodega`,`d`.`total` AS `totald`,(`d`.`total` * `tc`.`tasa`) AS `totalc` from (((((`liquidaciones` `l` join `documentos` `d` on((`l`.`iddocumento` = `d`.`iddocumento`))) join `tiposcambio` `tc` on((`d`.`idtipocambio` = `tc`.`idtc`))) join `personasxdocumento` `pd` on((`pd`.`iddocumento` = `d`.`iddocumento`))) join `personas` `p` on(((`pd`.`idpersona` = `p`.`idpersona`) and (`p`.`tipopersona` = 2)))) join `bodegas` `b` on((`b`.`idbodega` = `d`.`idbodega`)));

-- -----------------------------------------------------
-- View `vw_articulosprorrateados`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_articulosprorrateados` ;
DROP TABLE IF EXISTS `vw_articulosprorrateados`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_articulosprorrateados` AS select `a`.`idarticulo` AS `idarticulo`,`a`.`unidades` AS `unidades`,`a`.`costocompra` AS `costocompra`,(`a`.`unidades` * `a`.`costocompra`) AS `fob`,round(((`l`.`fletetotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `flete`,round(((`l`.`segurototal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `seguro`,round(((`l`.`otrosgastostotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `otrosgastos`,round(((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `cif`,round((((((`cal`.`dai` + `cal`.`isc`) + ((`l`.`iso` * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (((`l`.`spe` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))) + (`l`.`iva` * (((((`l`.`ciftotal` / `l`.`fobtotal`) * (`a`.`unidades` * `a`.`costocompra`)) + `cal`.`dai`) + `cal`.`isc`) + (((`l`.`tsimtotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`))))),4) AS `impuestos`,`cal`.`comision` AS `comision`,round((((`l`.`agenciatotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `agencia`,round((((`l`.`almacentotal` / `l`.`ciftotal`) * (`l`.`ciftotal` / `l`.`fobtotal`)) * (`a`.`unidades` * `a`.`costocompra`)),4) AS `almacen`,round((`l`.`tasapapeleria` * `a`.`unidades`),4) AS `papeleria`,round((`l`.`tasatransporte` * `a`.`unidades`),4) AS `transporte`,`a`.`iddocumento` AS `iddocumento`,(`a`.`costounit` * `a`.`unidades`) AS `costototal`,`a`.`costounit` AS `costounit`,`a`.`nlinea` AS `nlinea` from ((`articulosxdocumento` `a` join `vw_liquidacionescontodo` `l` on((`a`.`iddocumento` = `l`.`iddocumento`))) join `costosxarticuloliquidacion` `cal` on((`cal`.`idarticuloxdocumento` = `a`.`idarticuloxdocumento`)));

-- -----------------------------------------------------
-- View `vw_liquidacioncontotales`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_liquidacioncontotales` ;
DROP TABLE IF EXISTS `vw_liquidacioncontotales`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_liquidacioncontotales` AS select `l`.`iddocumento` AS `iddocumento`,sum(`a`.`unidades`) AS `unidadestotal`,sum(`cal`.`comision`) AS `comisiontotal`,sum((`a`.`unidades` * `a`.`costocompra`)) AS `fobtotal`,`l`.`fletetotal` AS `fletetotal`,`l`.`segurototal` AS `segurototal`,`l`.`otrosgastos` AS `otrosgastostotal`,(((sum((`a`.`unidades` * `a`.`costocompra`)) + `l`.`fletetotal`) + `l`.`segurototal`) + `l`.`otrosgastos`) AS `ciftotal`,`FNIMPUESTOS`(`l`.`iddocumento`,(((sum((`a`.`unidades` * `a`.`costocompra`)) + `l`.`fletetotal`) + `l`.`segurototal`) + `l`.`otrosgastos`),(((sum((`a`.`unidades` * `a`.`costocompra`)) + `l`.`fletetotal`) + `l`.`segurototal`) + `l`.`otrosgastos`),sum(`cal`.`dai`),sum(`cal`.`isc`)) AS `impuestototal`,`l`.`peso` AS `pesototal`,`l`.`totalagencia` AS `agenciatotal`,`l`.`totalalmacen` AS `almacentotal`,round(((`l`.`porcentajepapeleria` / 100) * sum(`a`.`unidades`)),4) AS `papeleriatotal`,round(((`l`.`porcentajetransporte` / 100) * sum(`a`.`unidades`)),4) AS `transportetotal`,(`l`.`porcentajepapeleria` / 100) AS `tasapapeleria`,(`l`.`porcentajetransporte` / 100) AS `tasatransporte`,`l`.`procedencia` AS `procedencia` from (((`liquidaciones` `l` join `articulosxdocumento` `a` on((`l`.`iddocumento` = `a`.`iddocumento`))) join `costosxarticuloliquidacion` `cal` on((`a`.`idarticuloxdocumento` = `cal`.`idarticuloxdocumento`))) join `vw_liquidacionesconcostos` `lcc` on((`lcc`.`iddocumento` = `l`.`iddocumento`))) group by `l`.`iddocumento`;

-- -----------------------------------------------------
-- View `vw_liquidacionesconcostos`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_liquidacionesconcostos` ;
DROP TABLE IF EXISTS `vw_liquidacionesconcostos`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_liquidacionesconcostos` AS select `l`.`iddocumento` AS `iddocumento`,sum(if((`ca`.`idtipocosto` = 5),(`ca`.`valorcosto` * ceiling((`l`.`peso` / `t`.`factorpeso`))),0)) AS `tsimtotal`,(sum(if((`ca`.`idtipocosto` = 1),`ca`.`valorcosto`,0)) / 100) AS `iva`,sum(if((`ca`.`idtipocosto` = 4),`ca`.`valorcosto`,0)) AS `spe`,(sum(if((`ca`.`idtipocosto` = 6),`ca`.`valorcosto`,0)) / 100) AS `iso` from (((`liquidaciones` `l` join `costosxdocumento` `cd` on((`l`.`iddocumento` = `cd`.`iddocumento`))) join `costosagregados` `ca` on((`ca`.`idcostoagregado` = `cd`.`idcostoagregado`))) left join `tsim` `t` on((`t`.`idtsim` = `ca`.`idcostoagregado`))) group by `l`.`iddocumento`;

-- -----------------------------------------------------
-- View `vw_liquidacionescontodo`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_liquidacionescontodo` ;
DROP TABLE IF EXISTS `vw_liquidacionescontodo`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_liquidacionescontodo` AS select `lt`.`iddocumento` AS `iddocumento`,`lt`.`fobtotal` AS `fobtotal`,`lt`.`fletetotal` AS `fletetotal`,`lt`.`segurototal` AS `segurototal`,`lt`.`otrosgastostotal` AS `otrosgastostotal`,`lt`.`ciftotal` AS `ciftotal`,`lt`.`agenciatotal` AS `agenciatotal`,`lt`.`almacentotal` AS `almacentotal`,`lc`.`tsimtotal` AS `tsimtotal`,`lt`.`tasapapeleria` AS `tasapapeleria`,`lt`.`tasatransporte` AS `tasatransporte`,`lc`.`iva` AS `iva`,`lc`.`spe` AS `spe`,`lc`.`iso` AS `iso`,`lt`.`pesototal` AS `pesototal`,`lt`.`procedencia` AS `procedencia` from (`vw_liquidacioncontotales` `lt` join `vw_liquidacionesconcostos` `lc` on((`lt`.`iddocumento` = `lc`.`iddocumento`)));

-- -----------------------------------------------------
-- View `vw_saldofacturas`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_saldofacturas` ;
DROP TABLE IF EXISTS `vw_saldofacturas`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_saldofacturas` AS select `fac`.`iddocumento` AS `iddocumento`,`fac`.`ndocimpreso` AS `ndocimpreso`,`fac`.`total` AS `totalfacturado`,((`fac`.`total` - sum(if((`otros`.`idtipodoc` = 10),`otros`.`total`,0))) - sum(if((`otros`.`idtipodoc` = 18),`ph`.`monto`,0))) AS `saldo`,sum(if((`otros`.`idtipodoc` = 10),`otros`.`total`,0)) AS `totaldevolucion`,sum(if((`otros`.`idtipodoc` = 18),`ph`.`monto`,0)) AS `totalabono`,`ca`.`valorcosto` AS `tasaiva`,`p`.`idpersona` AS `idpersona`,`p`.`nombre` AS `nombre`,`fac`.`idestado` AS `idestado` from ((((((`documentos` `fac` join `personasxdocumento` `pxd` on(((`pxd`.`iddocumento` = `fac`.`iddocumento`) and (`pxd`.`idaccion` = 1)))) join `personas` `p` on((`p`.`idpersona` = `pxd`.`idpersona`))) left join `costosxdocumento` `cd` on((`cd`.`iddocumento` = `fac`.`iddocumento`))) left join `costosagregados` `ca` on((`ca`.`idcostoagregado` = `cd`.`idcostoagregado`))) left join `docpadrehijos` `ph` on((`ph`.`idpadre` = `fac`.`iddocumento`))) left join `documentos` `otros` on(((`ph`.`idhijo` = `otros`.`iddocumento`) and (`otros`.`idestado` = 1)))) where (`fac`.`idtipodoc` = 5) group by `fac`.`iddocumento`;

-- -----------------------------------------------------
-- View `vw_cuentasbancarias`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_cuentasbancarias` ;
DROP TABLE IF EXISTS `vw_cuentasbancarias`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_cuentasbancarias` AS select `cc`.`idcuenta` AS `idcuenta`,`b`.`descripcion` AS `banco`,`c`.`ctabancaria` AS `ncuenta`,`tp`.`simbolo` AS `moneda`,`cc`.`codigo` AS `codigocontable`,`cc`.`descripcion` AS `cuentacontable` from (((`cuentasbancarias` `c` join `bancos` `b` on((`b`.`idbanco` = `c`.`idbanco`))) join `tiposmoneda` `tp` on((`tp`.`idtipomoneda` = `c`.`idtipomoneda`))) join `cuentascontables` `cc` on((`cc`.`idcuenta` = `c`.`idcuentacontable`)));

-- -----------------------------------------------------
-- View `vw_articulosenbodegas`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `vw_articulosenbodegas` ;
DROP TABLE IF EXISTS `vw_articulosenbodegas`;

CREATE  OR REPLACE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vw_articulosenbodegas` AS select `axd`.`idarticulo` AS `idarticulo`,`a`.`descripcion` AS `descripcion`,(`c`.`valor` * (1 + (`a`.`ganancia` / 100))) AS `precio`,`c`.`valor` AS `costodolar`,(`c`.`valor` * `tc`.`tasa`) AS `costo`,sum(if(((`axd`.`unidades` > 0) and isnull(`kardex`.`iddocumento`) and (`d`.`idtipodoc` <> 27)),0,`axd`.`unidades`)) AS `existencia`,`d`.`idbodega` AS `idbodega` from ((((((`articulosxdocumento` `axd` join `vw_articulosdescritos` `a` on((`a`.`idarticulo` = `axd`.`idarticulo`))) join `costosarticulo` `c` on(((`a`.`idarticulo` = `c`.`idarticulo`) and (`c`.`activo` = 1)))) join `tiposcambio` `tc` on((`tc`.`idtc` = `c`.`idtc`))) join `documentos` `d` on((`d`.`iddocumento` = `axd`.`iddocumento`))) left join `docpadrehijos` `ph` on((`ph`.`idpadre` = `axd`.`iddocumento`))) left join `documentos` `kardex` on(((`ph`.`idhijo` = `kardex`.`iddocumento`) and (`kardex`.`idtipodoc` = 27)))) group by `axd`.`idarticulo`,`d`.`idbodega`;


DELIMITER $$


DROP TRIGGER IF EXISTS `tr_promediarcosto` $$





CREATE

TRIGGER `tr_promediarcosto`
AFTER INSERT ON `articulosxdocumento`
FOR EACH ROW
BEGIN



      DECLARE costo DECIMAL(12,4);

      DECLARE idtc  INTEGER;

	DECLARE tasa DECIMAL(12,4);







      IF (select IF(idtipodoc in (21,7),1,0) from documentos where iddocumento = NEW.iddocumento) = 1 AND NEW.unidades>0 THEN



		SELECT idtipocambio,tc.tasa FROM documentos d



    JOIN tiposcambio tc ON tc.idtc=d.idtipocambio



    WHERE iddocumento = NEW.iddocumento INTO @idtc, @tasa;


      IF @tasa IS NULL THEN

          SET NEW='La tasa del tipo de cambio para calcular el costo promedio no puede ser null';

      END IF;



	SELECT sum(unidades * (costounit / IF(a.tccosto IS NULL,1,tc.tasa)))/sum(unidades) FROM articulosxdocumento a 
	LEFT JOIN tiposcambio tc ON tc.idtc = a.tccosto
	WHERE a.idarticulo = NEW.idarticulo 
	
	INTO @costo;



        IF @costo IS NULL THEN

          SET @costo=NEW.costounit;

    --    ELSE

  --        SET @costo=@costo/@tasa;

       END IF;



        UPDATE costosarticulo SET activo=0 WHERE idarticulo=NEW.idarticulo AND activo=1;



        INSERT INTO costosarticulo (valor,idarticulo,idtc) VALUES (@costo,NEW.idarticulo,@idtc);



      END IF;



END$$


DELIMITER ;

DELIMITER $$


DROP TRIGGER IF EXISTS `tr_validarnombrebodega` $$





CREATE

TRIGGER `tr_validarnombrebodega`
BEFORE INSERT ON `bodegas`
FOR EACH ROW
BEGIN



    IF NEW.nombrebodega ='' THEN

       SET NEW = NULL;

    END IF;



END$$


DELIMITER ;

DELIMITER $$


DROP TRIGGER IF EXISTS `tr_checkCuentaPadre` $$



CREATE

TRIGGER `tr_checkCuentaPadre`
BEFORE INSERT ON `cuentascontables`
FOR EACH ROW
BEGIN







  IF NEW.padre IS NOT NULL AND NEW.padre <>1 THEN



        SET @codHijo:=REPLACE(NEW.codigo,' 000','');



        SELECT LEFT(@codHijo,CHAR_LENGTH(@codHijo)-4) INTO @codHijo;







        SELECT REPLACE(codigo,' 000','')



        FROM cuentascontables cc



        where cc.idcuenta = NEW.padre



        into @cod;



    IF @cod NOT LIKE @codHijo THEN



      SET NEW = NULL;



    END IF;







  END IF;







END$$


DELIMITER ;

DELIMITER $$


DROP TRIGGER IF EXISTS `tr_checkNivelCuentaUpdate` $$







CREATE

TRIGGER `tr_checkNivelCuentaUpdate`
BEFORE UPDATE ON `cuentasxdocumento`
FOR EACH ROW
BEGIN

  SELECT padre.padre

  FROM cuentascontables hijo

  JOIN cuentascontables padre ON hijo.padre=padre.idcuenta

  where hijo.idcuenta = NEW.idcuenta

  into @padre;



    IF @padre=1 OR (@padre IS NULL) THEN

      SET  NEW=NULL;

    END IF;

END$$



DROP TRIGGER IF EXISTS `tr_checkNivelCuenta` $$







CREATE

TRIGGER `tr_checkNivelCuenta`
BEFORE INSERT ON `cuentasxdocumento`
FOR EACH ROW
BEGIN
    
    IF NEW.monto = 0 THEN
        SET NEW= 'NO SE PUEDE INSERTAR UN MOVIMIENTO CON MONTO 0';
    END IF;

  SELECT padre.padre

  FROM cuentascontables hijo

  JOIN cuentascontables padre ON hijo.padre=padre.idcuenta

  where hijo.idcuenta = NEW.idcuenta

  into @padre;

    IF @padre=1 OR (@padre IS NULL) THEN

      SET  NEW='NO SE PUEDE INSERTAR EN LAS CUENTAS CONTABLES DE NIVEL 1 o 2';

    END IF;
END$$


DELIMITER ;

DELIMITER $$


DROP TRIGGER IF EXISTS `tr_checkndoc_update` $$







CREATE

TRIGGER `tr_checkndoc_update`
BEFORE UPDATE ON `documentos`
FOR EACH ROW
BEGIN

      DECLARE id int;



     IF NEW.idestado = 3 THEN

        SET NEW.ndocimpreso = 'S/N';

    ELSE
        IF OLD.ndocimpreso <> NEW.ndocimpreso THEN
            IF NEW.idtipodoc NOT IN (12,7) THEN

                SELECT iddocumento FROM documentos where ndocimpreso=NEW.ndocimpreso AND idtipodoc=NEW.idtipodoc AND idestado <>3 LIMIT 1    into id;

            END IF;



            IF id IS NOT NULL THEN

                SET  NEW='NO SE PUEDE INSERTAR UN NUMERO DE DOCUMENTO REPETIDO';

            END IF;

        END IF;



    END IF;

END$$



DROP TRIGGER IF EXISTS `tr_checkndoc_insert` $$







CREATE

TRIGGER `tr_checkndoc_insert`
BEFORE INSERT ON `documentos`
FOR EACH ROW
BEGIN

      DECLARE id int;  



     IF NEW.idestado = 3 THEN



        SET NEW.ndocimpreso = 'S/N';



    ELSE



        IF NEW.idtipodoc NOT IN (12,7) THEN

            SELECT iddocumento FROM documentos where ndocimpreso=NEW.ndocimpreso AND idtipodoc=NEW.idtipodoc AND idestado<>3 LIMIT 1    into id;

        END IF;



        IF id IS NOT NULL THEN

            SET  NEW='NO SE PUEDE INSERTAR UN NUMERO DE DOCUMENTO REPETIDO';

        END IF;



    END IF;



END$$


DELIMITER ;

DELIMITER $$


DROP TRIGGER IF EXISTS `tr_validarnombre` $$





CREATE

TRIGGER `tr_validarnombre`
BEFORE INSERT ON `personas`
FOR EACH ROW
BEGIN



    IF NEW.nombre ='' THEN

       SET NEW = NULL;

    END IF;



END$$


DELIMITER ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `categorias`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('1', '\\\"BATERIAS\\\"', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('2', 'FRICCIONES*', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('3', 'NEUMATICOS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('4', 'VARIOS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('5', 'VALVULAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('6', 'GATOS DE CHASSIS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('7', 'RINES PARA AUTO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('8', 'GATOS DE 3/4 TONELAD', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('9', 'RINES PARA CAMIONETA', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('10', 'PULIDORAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('11', 'FORRO DE TIMON', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('12', 'FORRO DE ASIENTO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('13', 'MOFLE', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('14', 'EXTENCION P/MUFLER', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('15', 'ROCIADORES', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('16', 'LLANTAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('17', 'ALFOMBRAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('18', 'SPOILER', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('19', 'CORTINA DE CARRO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('20', 'COPAS PARA AUTO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('21', 'COPAS P/LLANTAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('22', 'LAMPARA', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('23', 'TELEFONO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('24', 'COJIN DE CARRO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('25', 'MANUBRIO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('26', 'KIT', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('27', 'DISCO DE FRENO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('28', 'MARCO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('29', 'CONO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('30', 'GAMUSA', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('31', 'TAPAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('32', 'ACCESORIOS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('33', 'T.V', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('34', 'TRIANGULO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('35', 'CORTINA', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('36', 'LUZ', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('37', 'BASE', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('38', 'ADAPTADOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('39', 'TIMON DE AUTO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('40', 'ESPEJOS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('41', 'RADIO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('42', 'REPRODUCTOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('43', 'MUFFLER', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('44', 'LIMPIA PARA BRISA', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('45', 'BOCINAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('46', 'CABLE', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('47', 'MONITOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('48', 'ANTENAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('49', 'AMPLIFICADOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('50', 'ECUALIZADOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('51', 'MODULADOR', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('52', 'D.V.D', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('53', 'SUB-WOOFER', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('54', 'TWEETERS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('55', 'ALARMAS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('56', 'KIT DE CIERRE', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('57', 'MOTOR DS-2.1', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('58', 'MODULO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('59', 'RELAY', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('60', 'SOCKET', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('61', 'AIRE', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('62', 'TUBOS', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('63', 'PALANCAS DE CAMBIO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('64', 'tv 21 Pulg', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('65', '11-22.5MOD', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('66', '11R22.5MOD66', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('67', '11R24.5', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('68', '175-70R13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('69', '185 R 14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('70', '185-70R 13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('71', '195 R 14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('72', '195 R 15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('73', '205-70 R 14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('74', '205R16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('75', '31x10.50 R 15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('76', '5-50-13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('77', '6-50-14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('78', '7-00-16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('79', '7-50-16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('80', '8-19.5', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('81', '235/75R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('82', '750R16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('83', '305-45 R22', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('84', '18570R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('85', '10-00-200 T212', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('86', '1000-20 T101 RANGER', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('87', '5-00-12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('88', '20560R13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('89', '5-50-14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('90', '825 15 14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('91', '700 12 14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('92', '600 9 10', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('93', '155-R12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('94', '15.5 X 38', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('95', '205/50R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('96', '60014', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('97', '60013', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('98', '285/50R20', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('99', '195/50R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('100', '70015', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('101', '305-40 X 22', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('102', '26570R16 KUMHO', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('103', '14.9 x 24', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('104', '30X9.50R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('105', '215/75R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('106', '215 40 R17', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('107', '10-00-20', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('108', '185/60R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('109', '10 50 R 15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('110', '750 15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('111', '700 15 12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('112', '205 40 R 17', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('113', '19570R14 KUMHO', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('114', '265 75 16 W', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('115', '309 50 R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('116', '18-4-30-12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('117', '23-1-30-8', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('118', '1300-24-12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('119', 'TT TR270 18.4-30.8', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('120', 'TS19 15.5 38.8', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('121', '7-50-20 TS 23', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('122', '19570R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('123', '16580R13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('124', '215/60R16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('125', '155/70R13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('126', '215/70R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('127', '175/65R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('128', '11R22.5 REENCAUCHE', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('129', '650-10-10', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('130', '600-9-10', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('131', '215-R14 SUMITOMO', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('132', '175 65 R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('133', '175-70R14', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('134', '700 R 16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('135', 'LLANTA 825X16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('136', '215-65R16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('137', '185-60R15 NEXEN', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('141', '750-15-12', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('142', '26570SR16', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('143', '31-10.50R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('144', '30-9.50R15', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('145', '18565R14 KUMHO', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('146', '16570R13', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('147', '9-00-20', '1');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('148', 'BATERIA  1111MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('149', 'BATERIA  1150MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('150', 'BATERIA  N-120', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('151', 'BATERIA  N-150', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('152', 'BATERIA  N-200', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('153', 'BATERIA  N-40', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('154', 'BATERIA 75 AMPERIO', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('155', 'BATERIA NX110MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('156', 'BATERIA N-200', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('157', 'BATERIA N-180 CHARGE', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('158', 'BATERIA N 40 Z 35AMP', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('159', 'BATERIA 30H 100AM', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('160', '31T 670/AMP', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('161', '31P 670/AMP', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('162', 'N-X 120 MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('163', 'BATERIA N-42-550', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('164', 'BATERIA G-27 (N-70)', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('165', 'BATERIA G-31 (30HP)', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('166', 'BATERIA G-22F ( N50)', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('167', 'BATERIA G-24 (N-50)', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('168', 'BATERIA N 40 L', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('169', 'NS70MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('170', 'K42R5MF', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('171', 'BATERIA  N-50', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('172', 'BATERIA  N-70', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('173', 'BATERIA N-200', '2');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('174', 'FRICCION', '3');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('175', 'BATERIA 42-550', '3');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('176', 'BATERIA N-701', '3');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('177', 'FRICCION KORENA ', '3');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('178', 'NEUMATICOS', '4');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('179', 'VALVULAS', '5');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('180', 'VARIOS2', '6');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('181', '25110', '7');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('182', '26110', '7');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('183', 'GATOS DE TALLER', '7');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('184', '3/4 DE TONELADA', '7');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('185', '229.5', '8');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('186', '3/4 DE TONELADA', '9');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('187', 'RINES 20x8.56x5.5 CH', '10');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('188', 'RINES 17*7', '10');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('189', 'RINES 15*7', '10');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('190', 'RINES 13*5.5', '10');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('191', 'RINES 15x7.54/100 HB', '10');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('192', 'S/N', '11');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('193', 'FORRO DE TIMON CUERI', '12');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('194', 'FORRO PARA TIMON', '12');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('195', 'FORRO DE TIMON GRIS', '12');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('196', 'FORRO MASAGE TOYOTA', '12');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('197', 'FORRO DE TIMON NEGRO', '12');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('198', 'FORRO PARA ASIENTO', '13');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('199', 'FORRO GRIS P/ASIENTO', '13');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('200', 'FORRO AUTO GRIS', '13');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('201', 'MOFLE MUFLER', '14');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('202', 'EXTENSION PARA MUFLE', '15');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('203', 'ROCIADORES PARABRISA', '16');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('204', 'ALFOMBRAS DE CAUCHO', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('205', 'ALFOMBRAS AUTO NEGRO', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('206', 'ALFOMBRAS GRIS', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('207', 'ALFOMBRA AZUL', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('208', 'ALFOMBRA CHOCOLATE', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('209', 'ALFOMBRAS NEGRO', '17');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('210', 'COLA DE PATO SPOILER', '18');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('211', 'CORTINA DE PALMERA', '19');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('212', 'CORTINA PLASTICA', '19');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('213', 'COPAS CROMADA AZUL', '20');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('214', 'COPAS CROMADA NEGRA', '20');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('215', 'COPAS CROMADA ROJA', '20');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('216', 'COPAS PARA LLANTAS', '21');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('217', 'COPAS P/LLANTAS 13', '21');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('218', 'COPAS P/LLANTAS 13 P', '21');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('219', 'COPAS P/LLANTAS 14 P', '21');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('220', 'LAMPARA ORIENTAL', '22');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('221', 'LAMPARA DE INTERIOR', '22');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('222', 'LAMPARA DE TECHO', '22');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('223', 'LAMPARA HALOGENO', '22');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('224', 'TELEFONO ANTIGUO', '23');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('225', 'COJIN PARA CARRO', '24');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('226', 'MANUBRIO PALAN. DE C', '25');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('227', 'KIT DE ACCESORIOS', '26');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('228', 'DISCO DE FRENOS', '27');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('229', 'MARCO P/PLACA', '28');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('230', 'CONO HIEDRA', '29');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('231', 'GAMUSA ACC.', '30');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('232', 'TAPAS P/TANQUE', '31');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('233', 'ACCESORIOS', '32');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('234', 'TVD P/AUTO', '33');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('235', 'TRIANGULO REFLECTIVO', '34');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('236', 'CORTINA FRONTAL', '35');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('237', 'LUZ PARA BUMPER', '36');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('238', 'BASE DE TIMON', '37');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('239', 'ADAPTADOR PARA TIMON', '38');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('240', 'TIMON DE AUTO', '39');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('241', 'TIMON STEERING WHEEL', '39');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('242', 'ESPEJOS P/AUTO', '40');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('243', 'RADIO P/AUTO', '41');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('244', 'REPRODUCTOR DE DVD', '42');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('245', 'MUFFLER METALICO', '43');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('246', 'LIMPIA PARA BRISA', '44');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('247', 'BOCINAS 240W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('248', 'BOCINAS 460W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('249', 'BOCINAS TSP-1066', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('250', 'BOCINAS SILVER POINT', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('251', 'BOCINAS SPEAKERS BOX', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('252', 'BOCINAS 440W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('253', 'BOCINAS 1000W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('254', 'BOCINAS 300W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('255', 'BOCINAS 160W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('256', 'BOCINAS 220W', '45');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('257', 'CABLE PARA AMP.', '46');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('258', 'MONITOR LCD', '47');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('259', 'ANTENA P/AUTO', '48');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('260', 'AMPLIFICADOR', '49');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('261', 'ECUALIZADOR', '50');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('262', 'MODULADOR', '51');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('263', 'D.V.D', '52');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('264', 'SUBWOOFER P/AUTOS', '53');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('265', 'TWEETERS P/AUTOS', '54');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('266', 'K-9 MUNDIAL SS', '55');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('267', 'REVOLUTION', '55');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('268', 'KIT DE CIERRE CENTRA', '56');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('269', 'MOTOR DS 2.1', '57');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('270', 'MODULO MUNDIAL 3', '58');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('271', 'RELAY 20/30', '59');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('272', 'SOCKET', '60');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('273', 'AIRE SPLIT', '61');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('274', 'TUBOS PARA BJO BASS', '62');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('275', 'PALANCAS DE CAMBIO', '63');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('276', 'TV 21 PULG.', '64');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('280', 'LAST', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('281', 'PEDRO', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('282', 'Sillas', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('283', 'Llantas Reencauchadas', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('284', 'Condensador', NULL);
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('285', 'Sub', '284');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('286', 'VARIOSLAST', '4');
INSERT INTO `categorias` (`idcategoria`, `nombre`, `padre`) VALUES ('287', 'VAL', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `modulos`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('1', 'Compras');
INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('2', 'Caja');
INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('3', 'Contabilidad');
INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('4', 'Inventario');
INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('5', 'Administracion');
INSERT INTO `modulos` (`idmodulos`, `descripcion`) VALUES ('6', 'Reportes');

COMMIT;

-- -----------------------------------------------------
-- Data for table `tiposdoc`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('1', 'AE', 'AJUSTE DE ENTRADA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('2', 'AF', 'ANULACION DE FACTURA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('3', 'AS', 'AJUSTE DE SALIDA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('4', 'EM', 'AJUSTE DE MONTO DE ENTRADA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('5', 'FA', 'FACTURA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('6', 'DT', 'DEPOSITO EN TRANSITO', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('7', 'LI', 'LIQUIDACION', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('8', 'MS', 'AJUSTE DE MONTO DE SALIDA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('9', 'SI', 'SALDO INICIAL', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('10', 'NC', 'NOTA DE CREDITO', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('11', 'ND', 'NOTAS DE DEBITOS', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('12', 'CK', 'CHEQUES ', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('13', 'DP', 'DEPOSITOS', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('14', 'DV', 'DEVOLUCIONES', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('15', 'AC', 'AJUSTE DE CREDITO', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('16', 'AD', 'AJUSTE DE DEBITO', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('17', 'CS', 'CIERRE DE SESION', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('18', 'RC', 'RECIBO', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('19', 'IR', 'CONSTANCIA DE RETENCION', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('20', 'IS', 'INICIO DE SESION', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('21', 'EC', 'ENTRADA DE COMPRAS LOCALES A BODEGA', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('22', 'CA', 'APERTURA DE CAJA', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('23', 'AR', 'ARQUEO', '2', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('24', 'AC', 'AJUSTE CONTABLE', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('25', 'CB', 'CONCILIACION BANCARIA', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('26', 'ER', 'ERROR BANCO', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('27', 'KX', 'KARDEX', '1', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('28', 'CM', 'CIERRE MENSUAL', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('29', 'CA', 'CIERRE ANUAL', '3', NULL);
INSERT INTO `tiposdoc` (`idtipodoc`, `codigodoc`, `descripcion`, `modulo`, `seriedoc`) VALUES ('30', 'AB', 'AJUSTE DE BODEGA', '1', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `bodegas`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('1', 'ESQUIPULAS');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('2', 'UNITRANSPORT');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('3', 'COLÓN');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('4', 'COOSPETECS');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('5', '15 DE OCTUBRE');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('6', 'LA GALLERA');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('7', 'EFUERZO Y UNIDAD');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('8', 'MONIMBO');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('9', '15 DE JULIO');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('10', 'FERNANDINA');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('11', 'LA GRAN SULTANA');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('12', 'J. R. GARCIA');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('13', '30 DE AGOSTO');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('14', 'DIVINO NIÑO');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('15', 'JOSE SHENDELL');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('16', 'COOTRACARI');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('17', 'COOGRANT');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('18', 'COOTRABO');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('19', 'COOTAXCAPA');
INSERT INTO `bodegas` (`idbodega`, `nombrebodega`) VALUES ('20', 'SAN RAMON');

COMMIT;

-- -----------------------------------------------------
-- Data for table `conceptos`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('1', 'Abono al Saldo Pendiente', '18');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('2', 'Cancelación Saldo de Factura', '18');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('3', 'Préstamo del Banco', '25');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('4', 'Multa por cheques sin fondo', '25');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('5', 'Abono de un cliente', '18');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('6', 'Cobro por servicios bancarios', '25');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('7', 'Abono a préstamo', '25');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('8', 'Salida por productos en mal estado', '27');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('9', 'Salida por robo', '27');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('10', 'Servicio Eléctrico', '30');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('11', 'Servicio de Agua Potable', '30');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('12', 'Servicio de Teléfono', '30');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('14', 'Otros Gastos', '30');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('15', 'Papeleria', '30');
INSERT INTO `conceptos` (`idconcepto`, `descripcion`, `idtipodoc`) VALUES ('16', 'Vale', '30');

COMMIT;

-- -----------------------------------------------------
-- Data for table `cajas`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `cajas` (`idcaja`, `descripcion`, `activo`) VALUES ('1', 'Caja 1', 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `estadosdocumento`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `estadosdocumento` (`idestado`, `descripcion`) VALUES ('1', 'CONFIRMADO');
INSERT INTO `estadosdocumento` (`idestado`, `descripcion`) VALUES ('2', 'ANULADO');
INSERT INTO `estadosdocumento` (`idestado`, `descripcion`) VALUES ('3', 'CREDITO PENDIENTE');
INSERT INTO `estadosdocumento` (`idestado`, `descripcion`) VALUES ('4', 'INCOMPLETO');
INSERT INTO `estadosdocumento` (`idestado`, `descripcion`) VALUES ('5', 'ANULACION PENDIENTE');

COMMIT;

-- -----------------------------------------------------
-- Data for table `bancos`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `bancos` (`idbanco`, `descripcion`) VALUES ('1', 'BAC');
INSERT INTO `bancos` (`idbanco`, `descripcion`) VALUES ('2', 'BANCENTRO');

COMMIT;

-- -----------------------------------------------------
-- Data for table `cuentascontables`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('1', NULL, '---', 'ES UNA CLASIFICACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('2', '1', '', 'ACTIVO CORRIENTE', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('3', '2', '110 000 000 000 000', 'ACTIVOS CORRIENTES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('4', '3', '110 001 000 000 000', 'CYB Caja', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('5', '4', '110 001 001 000 000', 'CYB Caja General', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('6', '4', '110 001 002 000 000', 'CYB Caja Chica', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('7', '4', '110 001 003 000 000', 'CYB Banco de Moneda Nacional', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('8', '7', '110 001 003 001 000', 'BMN Bancentro 240-201-518', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('9', '7', '110 001 003 002 000', 'BMN BAC 004-13116-5', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('10', '4', '110 001 004 000 000', 'CYB Banco de Moneda Extranjero', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('11', '10', '110 001 004 001 000', 'BME Bancentro 241-200-825', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('12', '4', '110 001 005 000 000', 'C Efectivo en Caja', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('13', '3', '110 002 000 000 000', 'CUENTAS Y DOCUMENTOS POR COBRAR', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('14', '13', '110 002 001 000 000', 'CDC Cuentas por Cobrar Clientes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('15', '13', '110 002 002 000 000', 'CDC Estimacion para Cuentas Incb Clientes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('16', '13', '110 002 003 000 000', 'CDC Documentos por Cobrar', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('17', '13', '110 002 004 000 000', 'CDC Estimacion para Cuentas Incob Doc x Co', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('18', '13', '110 002 005 000 000', 'CDC Cuentas por Liquidar', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('19', '13', '110 002 006 000 000', 'CDC Cuentas por Cobrar Empleados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('20', '13', '110 002 007 000 000', 'CDC Otras Cuentas por Cobrar', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('21', '3', '110 003 000 000 000', 'INVENTARIOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('22', '21', '110 003 001 000 000', 'INV Inventario de Bodega', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('23', '21', '110 003 002 000 000', 'INV Mercaderia en Transito', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('24', '21', '110 003 003 000 000', 'INV Piezas y Repuestos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('25', '21', '110 003 004 000 000', 'INV Herramientas y Utiles', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('26', '21', '110 003 005 000 000', 'INV Materiales de Oficinas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('27', '21', '110 003 006 000 000', 'INV Otros', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('28', '3', '110 004 000 000 000', 'ANTICIPO A JUSTIFICAR', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('29', '28', '110 004 001 000 000', 'AJ Anticipo para Compras y Gastos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('30', '28', '110 004 002 000 000', 'AJ Otros', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('31', '3', '110 005 000 000 000', 'PAGOS ANTICIPADOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('32', '31', '110 005 001 000 000', 'PA Anticipos a Contrtista', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('33', '31', '110 005 002 000 000', 'PA Anticipos a Proveedores', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('34', '31', '110 005 003 000 000', 'PA Impuestos  Anticipados (IVA)', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('35', '31', '110 005 004 000 000', 'PA Impuestos Anticipados (IR)', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('36', '31', '110 005 005 000 000', 'PA Otros', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('37', '31', '110 005 006 000 000', 'PA Saldos Iniciales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('38', '31', '110 005 007 000 000', 'PA ANTICIPOS DE ARRIENDOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('39', '38', '110 005 007 001 000', 'PA ANTICIPOS DE ARRIENDOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('40', '1', '', 'ACTIVO FIJOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('41', '40', '120 000 000 000 000', 'PROPIEDAD PLANTAS Y EQUIPOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('42', '41', '120 001 000 000 000', 'PPE Terrenos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('43', '41', '120 002 000 000 000', 'PPE Edificios', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('44', '41', '120 003 000 000 000', 'PPE Mobiliario y Equipo de Oficina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('45', '44', '120 003 001 000 000', 'MEO Puertas ,  Ventanas, etc.', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('46', '44', '120 003 002 000 000', 'MEO Sillas, Escritorios, Maq Escrib, etc', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('47', '44', '120 003 003 000 000', 'MEO Fotocopiadora', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('48', '41', '120 004 000 000 000', 'PPE Equipo de Computacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('49', '41', '120 005 000 000 000', 'PPE Equipo Rodante', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('50', '41', '120 006 000 000 000', 'PPE Vehiculos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('51', '41', '120 007 000 000 000', 'PPE Equipo de Comunicacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('52', '41', '120 008 000 000 000', 'PPE Radio Wolkie Toki, Telefonos,etc', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('53', '41', '120 009 000 000 000', 'PPE Otros Activos Fijos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('54', '40', '130 000 000 000 000', 'DEPRECIACION ACUMULADA', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('55', '54', '130 001 000 000 000', 'DA Depreciacion Acumulada de Edificios', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('56', '54', '130 002 000 000 000', 'DA Dep Acum de Mob y Equipo de Oficina', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('57', '54', '130 003 000 000 000', 'DA Dep Acum de Equipo de Computacion', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('58', '54', '130 004 000 000 000', 'DA Dep de  Equipo Rodante', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('59', '54', '130 005 000 000 000', 'DA Dep Acum de Comunicacion', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('60', '54', '130 006 000 000 000', 'DA Dep  Acum de Otros Activos', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('61', '54', '130 007 000 000 000', 'DA Saldos Iniciales', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('62', '1', '', 'ACTIVOS DIFERIDOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('63', '62', '140 000 000 000 000', 'ACTIVOS DIFERIDOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('64', '63', '140 001 000 000 000', 'AD Gastos de Constitucion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('65', '63', '140 002 000 000 000', 'AD Gastos de Organizacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('66', '63', '140 003 000 000 000', 'AD Gastos de Instalacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('67', '63', '140 004 000 000 000', 'AD Mejoras en Propiedades Arrendadas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('68', '63', '140 005 000 000 000', 'AD Remodelaciones de Oficinas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('69', '63', '140 006 000 000 000', 'AD Primas de Seguros y Finanzas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('70', '1', '', 'OTROS ACTIVOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('71', '70', '150 000 000 000 000', 'OTROS ACTIVOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('72', '71', '150 001 000 000 000', 'OA Reparaciones Capitalizables', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('73', '71', '150 002 000 000 000', 'OA Marcas y Patentes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('74', '71', '150 003 000 000 000', 'OA Depositos en Garantias', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('75', '1', '', 'PASIVO CORRIENTE', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('76', '75', '210 000 000 000 000', 'PASIVO CIRCULANTE', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('77', '76', '210 001 000 000 000', 'PC Proveedores', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('78', '77', '210 001 001 000 000', 'P  Proveedores Locales', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('79', '78', '210 001 001 001 000', 'PL GRUPO Q', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('80', '78', '210 001 001 002 000', 'PL COTARSA', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('81', '77', '210 001 002 000 000', 'P Proveedores del Exterio', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('82', '81', '210 001 002 001 000', 'PE N VISION', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('83', '81', '210 001 002 002 000', 'PE  NSC LOGISTICS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('84', '81', '210 001 002 003 000', 'PE GRUPO HUANG', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('85', '81', '210 001 002 004 000', 'PE TRIANGLE PANAMA', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('86', '81', '210 001 002 005 000', 'PE SUOTH DADE EEUU', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('87', '81', '210 001 002 006 000', 'PE GEDEON', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('88', '81', '210 001 002 007 000', 'PE STEPHANIE TIRES EEUU', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('89', '81', '210 001 002 008 000', 'PE PUENTE INVENTARIO-PROVEEDORES', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('90', '81', '210 001 002 009 000', 'PE Saldo Inicial', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('91', '81', '210 001 002 010 000', 'PE Puente Inv. Proveedores en Efectivo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('92', '81', '210 001 002 011 000', 'PE Puente Inv. Proveedores en Consignacion', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('93', '81', '210 001 002 012 000', 'PE MT - C S', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('94', '81', '210 001 002 013 000', 'PE ABC TORE GROUP INC', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('95', '81', '210 001 002 014 000', 'PL Reyoli Tires', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('96', '81', '210 001 002 015 000', 'ANTON IMPORTADORA Y EXPORTADORA', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('97', '81', '210 001 002 016 000', 'PE AUDIO CENTRO INTERNACIONAL, S.A ACISA', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('98', '81', '210 001 002 017 000', 'LUCY TIRES INC', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('99', '81', '210 001 002 018 000', 'PE MASTER TIRES & RUBBER, S.A.', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('100', '81', '210 001 002 019 000', 'PE MURESSA INTERTRADE, S.A.', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('101', '81', '210 001 002 020 000', 'MULTILLANTAS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('102', '76', '210 002 000 000 000', 'ACREEDORES DIVERSOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('103', '102', '210 002 001 000 000', 'AD Alquileres y Arriendos', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('104', '102', '210 002 002 000 000', 'AD Otros', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('105', '102', '210 002 003 000 000', 'AD Saldo Inicial', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('106', '76', '210 003 000 000 000', 'PRESTAMOS BANCARIOS A CORTO PLAZO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('107', '106', '210 003 001 000 000', 'PBCP Prestamos Bancarios para Operaciones', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('108', '106', '210 003 002 000 000', 'PBCP Prestamos para Inversiones', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('109', '76', '210 004 000 000 000', 'INTERESES ACUMULADOS POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('110', '109', '210 004 001 000 000', 'IAP Intereses por Prestamos para Operacion', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('111', '109', '210 004 002 000 000', 'IAP Intereses por Prest para Inversion', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('112', '109', '210 004 003 000 000', 'IAP Intereses Moratorios', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('113', '76', '210 005 000 000 000', 'PRESTACIONES SOCIALES POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('114', '113', '210 005 001 000 000', 'PSP Vacaciones', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('115', '113', '210 005 002 000 000', 'PSP Aguinaldo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('116', '113', '210 005 003 000 000', 'PSP Indemnizacion  por Ley', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('117', '113', '210 005 004 000 000', 'PSP Saldo Inicial', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('118', '76', '210 006 000 000 000', 'RETENCIONES POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('119', '118', '210 006 001 000 000', 'RP IR en la Fuente por Pagar 2%', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('120', '118', '210 006 002 000 000', 'RP Retenciones a Empleados (IR)', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('121', '118', '210 006 003 000 000', 'RP Cuota al INSS Empleados', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('122', '118', '210 006 004 000 000', 'RP Otras Retenciones', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('123', '118', '210 006 005 000 000', 'IP RETENCION EN LA FUENTE SER. PROF(10%)', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('124', '118', '210 006 006 000 000', 'RP Saldo Inicial', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('125', '76', '210 007 000 000 000', 'GASTOS ACUMULADOS POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('126', '125', '210 007 001 000 000', 'GAP Reembolsos de Caja Chica', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('127', '125', '210 007 002 000 000', 'SERVICIOS PUBLICOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('128', '127', '210 007 002 001 000', 'SP ENACAL', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('129', '127', '210 007 002 002 000', 'SP DISSUR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('130', '127', '210 007 002 003 000', 'SP ENITEL', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('131', '76', '210 008 000 000 000', 'IMPUESTOS Y APORTES POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('132', '131', '210 008 001 000 000', 'IMPUESTO POR PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('133', '132', '210 008 001 001 000', 'IP IVA por Pagar', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('134', '132', '210 008 001 002 000', 'IP  IR Anual', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('135', '131', '210 008 002 000 000', 'APORTES A PAGAR', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('136', '135', '210 008 002 001 000', 'AP Aportes Patronal al INSS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('137', '135', '210 008 002 002 000', 'AP Aportes de 2% al INATEC', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('138', '135', '210 008 002 003 000', 'AP Aportes del 1%  de Alcaldia', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('139', '135', '210 008 002 004 000', 'AP Otros Aportes por Pagar', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('140', '135', '210 008 002 005 000', 'IP Saldo Inicial', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('141', '76', '210 009 000 000 000', 'PASIVO A LARGO PLAZO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('142', '141', '210 009 001 000 000', 'PLP Cuentas por Pagar a Largo Plazo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('143', '142', '210 009 001 001 000', 'CPLA Prestamos Bancarios a Largo Plazo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('144', '76', '210 010 000 000 000', 'PASIVOS DIFERIDOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('145', '144', '210 010 001 000 000', 'PA Creditos  Diferidos', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('146', '145', '210 010 001 001 000', 'PD Cobros Anticipados', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('147', '76', '210 011 000 000 000', 'OTROS PASIVOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('148', '1', '', 'CAPITAL', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('149', '148', '300 000 000 000 000', 'CUENTAS DE CAPITAL CONTABLE', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('150', '148', '310 000 000 000 000', 'CUENTAS DE CAPITAL CONTABLE', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('151', '150', '310 001 000 000 000', 'CAPITAL CONTRIBUIDO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('152', '151', '310 001 001 000 000', 'CC Capital Social Autorizado', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('153', '151', '310 001 002 000 000', 'CC Aporte para Fut Aumento de Cpital', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('154', '151', '310 001 003 000 000', 'CC Donaciones', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('155', '150', '310 002 000 000 000', 'RESERVAS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('156', '155', '310 002 001 000 000', 'R Reserva Legal', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('157', '155', '310 002 002 000 000', 'R Rerservas Eventuales', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('158', '148', '320 000 000 000 000', 'CAPITAL  GANADO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('159', '158', '320 001 000 000 000', 'CAPITAL', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('160', '159', '320 001 001 000 000', 'CG Utilidades y/o Perdidas Acumuladas', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('161', '159', '320 001 002 000 000', 'CG Ajuste por Revaluacion de Activo Fijo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('162', '159', '320 001 003 000 000', 'CG Utilidades y/o Perdidas Netas del Ejerc', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('163', '159', '320 001 004 000 000', 'CG Ajuste a Periodos Anteriores', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('164', '159', '320 001 005 000 000', 'CG Ajuste por Deslizamiento Monetaria', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('165', '159', '320 001 006 000 000', 'CG Utilidad del Ejercicio PF 2003-2004', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('166', '159', '320 001 007 000 000', 'CG Utilidad del Ejercicio PF 2004-2005', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('167', '159', '320 001 008 000 000', 'CG Utilidad del Ejerecicio PF 2005-2006', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('168', '148', '999 000 000 000 000', 'SUPERÁVIT O (DÉFICIT) DEL PERÍODO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('169', '1', '', 'INGRESOS CORRIENTES', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('170', '169', '410 000 000 000 000', 'INGRESOS POR VENTAS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('171', '170', '410 001 000 000 000', 'IG. Ventas Brutas', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('172', '170', '410 002 000 000 000', 'IG. Devoluciones y Rebajas sobre Ventas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('173', '170', '410 003 000 000 000', 'IG. Ventas Netas', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('174', '1', '', 'OTROS INGRESOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('175', '174', '420 000 000 000 000', 'OTROS INGRESOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('176', '175', '420 001 000 000 000', 'OI. Saldos Iniciales', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('177', '175', '420 002 000 000 000', 'OI. Ajuste de Precisión - Dólar', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('178', '175', '420 003 000 000 000', 'DESCUENTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('179', '178', '420 003 001 000 000', 'Devoluciones y Rebajas sobre Compras', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('180', '1', '', 'GASTOS DE OPERACIONES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('181', '180', '510 000 000 000 000', 'COSTOS Y GASTOS DE OPERACIONES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('182', '181', '510 001 000 000 000', 'Costos de Ventas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('183', '180', '610 000 000 000 000', 'GASTOS DE VENTAS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('184', '183', '610 001 000 000 000', 'GASTOS DE VENTAS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('185', '184', '610 001 001 000 000', 'GASTOS DE PERSONAL', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('186', '185', '610 001 001 001 000', 'GP Salario Personal de Venta', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('187', '185', '610 001 001 002 000', 'GP Viatico de Alimentacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('188', '185', '610 001 001 003 000', 'GP Viaticos (Alojamiento , Transpoprte, et', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('189', '185', '610 001 001 004 000', 'GP Horas Extras', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('190', '185', '610 001 001 005 000', 'GP Incentivos  Bonificaciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('191', '185', '610 001 001 006 000', 'GP Comisiones Sobre Venta', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('192', '185', '610 001 001 007 000', 'GV Vacaciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('193', '185', '610 001 001 008 000', 'GP  Aguinaldo', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('194', '185', '610 001 001 009 000', 'GP Indemnizacion por Ley', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('195', '185', '610 001 001 010 000', 'GP Utiles y Suministros de Cafeteria', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('196', '185', '610 001 001 011 000', 'GP Uniformes y Equipos de Seguridad', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('197', '185', '610 001 001 012 000', 'GPP Medicina y Suministros Clinicaos Medic', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('198', '185', '610 001 001 013 000', 'GP Productos y Obsequios al Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('199', '185', '610 001 001 014 000', 'GP Reuniones y Celebraciones al Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('200', '185', '610 001 001 015 000', 'GP Gastos Navideños', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('201', '185', '610 001 001 016 000', 'GP Otros Gastos del Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('202', '185', '610 001 001 017 000', 'GP Aporte Patronal al INSS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('203', '185', '610 001 001 018 000', 'GP Otras Prestaciones Sociales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('204', '185', '610 001 001 019 000', 'GP Gastos de Representacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('205', '185', '610 001 001 020 000', 'GP Gastos de Capacitacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('206', '185', '610 001 001 021 000', 'GP. Saldos Iniciales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('207', '184', '610 001 002 000 000', 'MATERIALES Y SUMINISTROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('208', '207', '610 001 002 001 000', 'MS Baterias, Llantas, Neumaticos, Rines', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('209', '207', '610 001 002 002 000', 'MS Piezas de Repuestos y Accesorios', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('210', '207', '610 001 002 003 000', 'MS Herramientas y utiles', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('211', '207', '610 001 002 004 000', 'MS Materiales para Aseo y Limpieza', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('212', '207', '610 001 002 005 000', 'MS Materiales y Utiles de Oficina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('213', '207', '610 001 002 006 000', 'MS Materiales para Aseo y Limpieza de Vehi', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('214', '207', '610 001 002 007 000', 'MS Otros Materiales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('215', '207', '610 001 002 008 000', 'GV. Gastos por Oferta', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('216', '184', '610 001 003 000 000', 'COMBUSTIBLES Y LUBRICANTES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('217', '216', '610 001 003 001 000', 'CL Dissel y Gasolina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('218', '216', '610 001 003 002 000', 'CL Aceites y Lubricantes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('219', '216', '610 001 003 003 000', 'CL Otros Combustibles y Lubricantes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('220', '184', '610 001 004 000 000', 'SERVICIOS COMPRADOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('221', '220', '610 001 004 001 000', 'SC Agua, Luz, Telefono y Correos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('222', '220', '610 001 004 002 000', 'SC Fletes y  Acarreos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('223', '220', '610 001 004 003 000', 'SC Servicios Comerciales y Bancarios', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('224', '220', '610 001 004 004 000', 'SC Publicidad y Propaganda', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('225', '220', '610 001 004 005 000', 'SC Alquileres y Arriendos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('226', '220', '610 001 004 006 000', 'SC Servicios y Mant de Equipos de Oficina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('227', '220', '610 001 004 007 000', 'SC Servicios y Mantenimiento de  Edificio', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('228', '220', '610 001 004 008 000', 'SC Servicios y Mantenimiento de Equipo Rod', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('229', '220', '610 001 004 009 000', 'SC Servicios de Fotocopias', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('230', '220', '610 001 004 010 000', 'SC Suscripciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('231', '220', '610 001 004 011 000', 'SC Poliza  de Seguro', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('232', '220', '610 001 004 012 000', 'SC Otros Servicios Comprados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('233', '220', '610 001 004 013 000', 'SC Servicios Profesionales y Tecnicos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('234', '220', '610 001 004 014 000', 'SC Servicios Prestados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('235', '220', '610 001 004 015 000', 'SC Impuestos y Contribuciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('236', '184', '610 001 005 000 000', 'GASTOS DE INSTALACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('237', '184', '610 001 006 000 000', 'MEJORAS EN PROPIEDADES ARRENDADAS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('238', '184', '610 001 007 000 000', 'DEPRECIACIONES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('239', '238', '610 001 007 001 000', 'D Depreciacion  Acumulada de  Edificio', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('240', '238', '610 001 007 002 000', 'D Dep Acum de Prop Planta y Equipo', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('241', '238', '610 001 007 003 000', 'D Dep. Acum. de Equipo Rodante', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('242', '238', '610 001 007 004 000', 'D Dep. Acum de Comunicacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('243', '238', '610 001 007 005 000', 'D Dep Acum de Otros Activos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('244', '184', '610 001 008 000 000', 'ESTIMACIONES DE COBRO DUDOSO', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('245', '244', '610 001 008 001 000', 'ECD Est. de Cobros Dudoso Cliente', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('246', '244', '610 001 008 002 000', 'ECD Est de Cobros Dudoso Doc por Cobrar', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('247', '1', '', 'GASTOS DE ADMINISTRACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('248', '247', '620 000 000 000 000', 'GASTOS DE ADMINISTRACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('249', '248', '620 001 000 000 000', 'GASTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('250', '249', '620 001 001 000 000', 'GA Gastos del Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('251', '250', '620 001 001 001 000', 'GP Salario Personal de Administracion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('252', '250', '620 001 001 002 000', 'GP Viaticos de Alimentacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('253', '250', '620 001 001 003 000', 'GP Viaticos (Alojamiento, Transporte ,etc)', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('254', '250', '620 001 001 004 000', 'GP Horas Extras', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('255', '250', '620 001 001 005 000', 'GP Incentivos, Bonificaciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('256', '250', '620 001 001 006 000', 'GP Comisiones Sobre Ventas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('257', '250', '620 001 001 007 000', 'GP  Vacaciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('258', '250', '620 001 001 008 000', 'GP Aguinaldo', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('259', '250', '620 001 001 009 000', 'GP Indemnizacion por Ley', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('260', '250', '620 001 001 010 000', 'GP Utiles y Suministros de Cafeteria', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('261', '250', '620 001 001 011 000', 'GP Uniforme & Equipo de Seguridad', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('262', '250', '620 001 001 012 000', 'GP Medicina y Suministros Clinica Medica', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('263', '250', '620 001 001 013 000', 'GP Productos y Obsequios al Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('264', '250', '620 001 001 014 000', 'GP Reuniones y Celebraciones al Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('265', '250', '620 001 001 015 000', 'GP Gastos Navideños', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('266', '250', '620 001 001 016 000', 'GP Otros Gastos del Personal', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('267', '250', '620 001 001 017 000', 'GP Aportes Patronal al INSS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('268', '250', '620 001 001 018 000', 'GP Gastos de Capacitacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('269', '250', '620 001 001 019 000', 'GP Gastos de Representacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('270', '250', '620 001 001 020 000', 'GP Otras Prestaciones Sociales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('271', '250', '620 001 001 021 000', 'GP. Saldos Iniciales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('272', '249', '620 001 002 000 000', 'MATERIALES Y SUMINISTROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('273', '272', '620 001 002 001 000', 'MS Baterias, Llantas, Neumaticos, Rines', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('274', '272', '620 001 002 002 000', 'MS Pieza de Pespuestos y Accesorios', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('275', '272', '620 001 002 003 000', 'MS Herramientas y Utiles', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('276', '272', '620 001 002 004 000', 'MS Materiales para Aseo y Limpieza', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('277', '272', '620 001 002 005 000', 'MS Materiales y Utiles de Oficina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('278', '272', '620 001 002 006 000', 'MS Materiales para Aseo y Limpieza de Vehi', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('279', '272', '620 001 002 007 000', 'MS Otros Materiales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('280', '249', '620 001 003 000 000', 'COMBUSTIBLES Y LUBRICANTES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('281', '280', '620 001 003 001 000', 'CL Diessel y Gasolina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('282', '280', '620 001 003 002 000', 'CL Aceites y Lubricantes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('283', '280', '620 001 003 003 000', 'CL Otros Combustibles y Lubricantes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('284', '249', '620 001 004 000 000', 'SERVICIOS COMPRADOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('285', '284', '620 001 004 001 000', 'SC Agua, Luz, Teléfono, Correos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('286', '284', '620 001 004 002 000', 'SC Fletes y Acarreos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('287', '284', '620 001 004 003 000', 'SC Servicios Comerciales y Bancarios', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('288', '284', '620 001 004 004 000', 'SC Publicidad y Promocion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('289', '284', '620 001 004 005 000', 'SC Alquileres y Arriendos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('290', '284', '620 001 004 006 000', 'SC Servicios y Mant de Equip de Oficina', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('291', '284', '620 001 004 007 000', 'SC Servicios y Mantenimiento de Edificio', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('292', '284', '620 001 004 008 000', 'SC Servicio y Mantenimiento de Eqp Rodante', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('293', '284', '620 001 004 009 000', 'SC Servicios de Fotocopias', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('294', '284', '620 001 004 010 000', 'SC Suscripciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('295', '284', '620 001 004 011 000', 'SC Poliza de Seguros', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('296', '284', '620 001 004 012 000', 'SC Otros Servicios Comprados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('297', '284', '620 001 004 013 000', 'SC Servicios Profesionales y Tecnicos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('298', '284', '620 001 004 014 000', 'SC Servicios Prestados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('299', '284', '620 001 004 015 000', 'SC Impuestos y Contribuciones (ALMA)', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('300', '249', '620 001 005 000 000', 'GASTOS DE INSTALACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('301', '249', '620 001 006 000 000', 'MEJORAS EN PROPIEDADES ARRENDADAS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('302', '249', '620 001 007 000 000', 'DEPRECIACIONES', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('303', '302', '620 001 007 001 000', 'D Depreciaciones Acumuladas de Edificio', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('304', '302', '620 001 007 002 000', 'D Depreciacion Acumulada de Prop  Plat y E', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('305', '302', '620 001 007 003 000', 'D Dep Acumulada de Equipo Rodante', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('306', '302', '620 001 007 004 000', 'D Depreciacion  Acumulada de Comunicacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('307', '302', '620 001 007 005 000', 'D Depreciacion Acumulada de Otros Activos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('308', '249', '620 001 008 000 000', 'ESTIMACIONES DE COBROS DUDOSOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('309', '308', '620 001 008 001 000', 'ECD Estrimaciones de Cobro Dudoso Cliente', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('310', '308', '620 001 008 002 000', 'ECD Est de Cobr Dudoso Doc por Cobrar', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('311', '249', '620 001 009 000 000', 'GASTOS DE ORGANIZACION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('312', '249', '620 001 010 000 000', 'GASTOS DE CONSTITUCION', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('313', '1', '', 'GASTOS FINANCIEROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('314', '313', '630 000 000 000 000', 'GASTOS FINANCIEROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('315', '314', '630 001 000 000 000', 'GASTOS FINANCIEROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('316', '315', '630 001 001 000 000', 'GF Pago de Interes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('317', '315', '630 001 002 000 000', 'GF GF Descuentos Concedidos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('318', '315', '630 001 003 000 000', 'GF Comisiones Bancarias', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('319', '315', '630 001 004 000 000', 'GF Otros Gastos Financieros', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('320', '315', '630 001 005 000 000', 'GF. Saldos Iniciales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('321', '1', '', 'PRODUCTOS FINANCIEROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('322', '321', '640 000 000 000 000', 'PRODUCTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('323', '322', '640 001 000 000 000', 'PRODUCTOS FINANCIEROS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('324', '323', '640 001 001 000 000', 'PF Cobro de Intereses', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('325', '323', '640 001 002 000 000', 'PF Descuentos Obtenidos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('326', '1', '', 'OTROS GASTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('327', '326', '650 000 000 000 000', 'OTROS GASTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('328', '327', '650 001 000 000 000', 'OTROS GASTOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('329', '328', '650 001 001 000 000', 'OG Gastos de Atencion Social', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('330', '328', '650 001 002 000 000', 'OG Perdida por Baja de Activos Fijos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('331', '328', '650 001 003 000 000', 'OG Multas , Indemnizacion y Compensaciones', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('332', '328', '650 001 004 000 000', 'OG Gastos de Representacion', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('333', '328', '650 001 005 000 000', 'OG Faltantes o Sobrantes', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('334', '328', '650 001 006 000 000', 'OG Robos o Perdidas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('335', '328', '650 001 007 000 000', 'OG Otros Gastos no Especificados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('336', '328', '650 001 008 000 000', 'OG. Saldos Iniciales', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('337', '328', '650 001 009 000 000', 'OG Ajuste por Precision - Córdobas', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('338', '1', '', 'CUENTAS DE ORDEN DEUDORA', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('339', '338', '810 000 000 000 000', 'CUENTAS DE ORDEN DEUDORA', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('340', '339', '810 001 000 000 000', 'SERVICIOS PROFESIONALES Y TECNICOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('341', '340', '810 001 004 000 000', 'SERVICIOS PROFESIONALES Y TECNICOS', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('342', '341', '810 001 004 013 000', 'Servicios profesionales y Tecnicos', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('343', '341', '810 001 004 014 000', 'Servicios Prestados', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('344', '339', '810 005 000 000 000', 'ANTICIPO DE ARRIENDO', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('345', '344', '810 005 007 000 000', 'ANTICIPO DE ARRIENDO', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('346', '345', '810 005 007 001 000', 'Antiicpo de Arriendo', '1');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('347', '1', '', 'CUENTA DE ORDEN ACREEDORAS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('348', '347', '910 000 000 000 000', 'CUENTAS DE ORDEN ACREEDORAS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('349', '348', '910 001 000 000 000', 'SERVICIOS PROFESIONALES Y TECNICOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('350', '349', '910 001 004 000 000', 'SERVICIOS PROFESIONALES Y TECNICOS', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('351', '350', '910 001 004 013 000', 'Servicios Profesionales y Tecnicos', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('352', '350', '910 001 004 014 000', 'Servicios Prestados', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('353', '348', '910 005 000 000 000', 'ANTICIPO DE ARRIENDO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('354', '353', '910 005 007 000 000', 'ANTICIPO DE ARRIENDO', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('355', '354', '910 005 007 001 000', 'Anticipo de Arriendo', '0');
INSERT INTO `cuentascontables` (`idcuenta`, `padre`, `codigo`, `descripcion`, `esdebe`) VALUES ('356', '175', '420 004 000 000 000', 'Otros Ingresos no Especificados', '0');

COMMIT;

-- -----------------------------------------------------
-- Data for table `tiposcosto`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('1', 'IVA', '1', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('2', 'ISC', '1', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('3', 'DAI', '1', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('4', 'SPE', '0', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('5', 'TSIM', '0', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('6', 'ISO', '1', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('7', 'Comisión', '0', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('8', 'RETENCION EN LA FUENTE', '1', NULL);
INSERT INTO `tiposcosto` (`idtipocosto`, `descripcion`, `esporcentaje`, `cuentacontable`) VALUES ('9', 'RETENCION  POR SERVICIOS PROFESIONALES', '1', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `costosagregados`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('1', '15', '20100809', '1', '1', NULL);
INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('2', '2', '20100809', '1', '8', NULL);
INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('3', '10', '20100809', '1', '9', NULL);
INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('4', '35', '20100809', '1', '6', NULL);
INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('5', '0.5', '20100809', '1', '5', NULL);
INSERT INTO `costosagregados` (`idcostoagregado`, `valorcosto`, `fechaestablecido`, `activo`, `idtipocosto`, `idarticulo`) VALUES ('6', '5', '20100809', '1', '4', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `tiposmoneda`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tiposmoneda` (`idtipomoneda`, `moneda`, `simbolo`) VALUES ('1', 'CORDOBAS', 'C$');
INSERT INTO `tiposmoneda` (`idtipomoneda`, `moneda`, `simbolo`) VALUES ('2', 'DOLARES', 'US$');

COMMIT;

-- -----------------------------------------------------
-- Data for table `cuentasbancarias`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `cuentasbancarias` (`idcuentacontable`, `idbanco`, `idtipomoneda`, `ctabancaria`, `fechacancelado`, `fechaapertura`, `seriedoc`) VALUES ('9', '1', '1', '004-13116-5', NULL, '20100704', 1);
INSERT INTO `cuentasbancarias` (`idcuentacontable`, `idbanco`, `idtipomoneda`, `ctabancaria`, `fechacancelado`, `fechaapertura`, `seriedoc`) VALUES ('8', '2', '1', ' 240-201-518', NULL, '20100704', 1);
INSERT INTO `cuentasbancarias` (`idcuentacontable`, `idbanco`, `idtipomoneda`, `ctabancaria`, `fechacancelado`, `fechaapertura`, `seriedoc`) VALUES ('11', '2', '2', '241-200-825', NULL, '20100704', 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `tiposmovimientocaja`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tiposmovimientocaja` (`idtipomovimiento`, `descripcion`) VALUES ('1', 'Efectivo');
INSERT INTO `tiposmovimientocaja` (`idtipomovimiento`, `descripcion`) VALUES ('2', 'Cheque');
INSERT INTO `tiposmovimientocaja` (`idtipomovimiento`, `descripcion`) VALUES ('3', 'Deposito');
INSERT INTO `tiposmovimientocaja` (`idtipomovimiento`, `descripcion`) VALUES ('4', 'Transferencia');
INSERT INTO `tiposmovimientocaja` (`idtipomovimiento`, `descripcion`) VALUES ('5', 'Tarjeta');

COMMIT;

-- -----------------------------------------------------
-- Data for table `tipospersona`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('1', 'Cliente', 'Comprar');
INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('2', 'Proveedor', 'Abastecer');
INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('3', 'Vendedor', 'Vender');
INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('4', 'Usuario', 'Crear');
INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('5', 'Supervisor', 'Autorizar');
INSERT INTO `tipospersona` (`idtipopersona`, `descripcion`, `accion`) VALUES ('6', 'Contador', 'Contabilizar');

COMMIT;

-- -----------------------------------------------------
-- Data for table `personas`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `personas` (`idpersona`, `nombre`, `fechaIngreso`, `direccion`, `telefono`, `email`, `ruc`, `activo`, `tipopersona`, `idcuenta`) VALUES ('1', 'Administrador', CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, '1', '4', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `roles`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('1', 'root', 'Administrador del Sistema', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('2', 'gerencia', 'Gerencia Esquipulas', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('3', 'caja', 'Usuario de Caja', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('4', 'inventario', 'Usuario de Inventario', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('5', 'contabilidad', 'Usuario de Contabilidad', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('6', 'inventariorep', 'Reportes de Inventario', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('7', 'contabilidadrep', 'Reportes de Contabilidad', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('8', 'ventasrep', 'Reportes de Ventas', '0');
INSERT INTO `roles` (`idrol`, `nombre`, `descripcion`, `idmodulo`) VALUES ('9', 'kardex', 'Usuario de Bodega', '0');

COMMIT;

-- -----------------------------------------------------
-- Data for table `tsim`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `tsim` (`idtsim`, `factorpeso`) VALUES ('5', '1000');

COMMIT;

-- -----------------------------------------------------
-- Data for table `usuarios`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `usuarios` (`idusuario`, `username`, `password`, `estado`, `tipousuario`) VALUES ('1', 'root', '39db306abbac01aae3fe6c00c7f53da6bd78cd1b', '1', '1');

COMMIT;

-- -----------------------------------------------------
-- Data for table `denominaciones`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('1', '500', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('2', '200', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('3', '100', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('4', '50', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('5', '20', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('6', '10', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('8', '5', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('9', '1', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('10', '0.5', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('11', '0.25', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('12', '0.10', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('13', '0.05', 1, '1');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('14', '100', 1, '2');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('15', '50', 1, '2');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('16', '20', 1, '2');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('17', '10', 1, '2');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('18', '5', 1, '2');
INSERT INTO `denominaciones` (`iddenominacion`, `valor`, `activo`, `idtipomoneda`) VALUES ('19', '1', 1, '2');

COMMIT;

-- -----------------------------------------------------
-- Data for table `usuarios_has_roles`
-- -----------------------------------------------------
SET AUTOCOMMIT=0;

INSERT INTO `usuarios_has_roles` (`idusuario`, `idrol`) VALUES ('1', '1');

COMMIT;
