/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: db    Database: proyecto_qchicharron
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_usuario_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `administrador_administrador`
--

DROP TABLE IF EXISTS `administrador_administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador_administrador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nivel_prioridad` int NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `administrador_admini_usuario_id_bcb4b843_fk_usuario_u` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador_administrador`
--

LOCK TABLES `administrador_administrador` WRITE;
/*!40000 ALTER TABLE `administrador_administrador` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `administrador_administrador` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add site',6,'add_site'),
(22,'Can change site',6,'change_site'),
(23,'Can delete site',6,'delete_site'),
(24,'Can view site',6,'view_site'),
(25,'Can add email address',7,'add_emailaddress'),
(26,'Can change email address',7,'change_emailaddress'),
(27,'Can delete email address',7,'delete_emailaddress'),
(28,'Can view email address',7,'view_emailaddress'),
(29,'Can add email confirmation',8,'add_emailconfirmation'),
(30,'Can change email confirmation',8,'change_emailconfirmation'),
(31,'Can delete email confirmation',8,'delete_emailconfirmation'),
(32,'Can view email confirmation',8,'view_emailconfirmation'),
(33,'Can add social account',9,'add_socialaccount'),
(34,'Can change social account',9,'change_socialaccount'),
(35,'Can delete social account',9,'delete_socialaccount'),
(36,'Can view social account',9,'view_socialaccount'),
(37,'Can add social application',10,'add_socialapp'),
(38,'Can change social application',10,'change_socialapp'),
(39,'Can delete social application',10,'delete_socialapp'),
(40,'Can view social application',10,'view_socialapp'),
(41,'Can add social application token',11,'add_socialtoken'),
(42,'Can change social application token',11,'change_socialtoken'),
(43,'Can delete social application token',11,'delete_socialtoken'),
(44,'Can view social application token',11,'view_socialtoken'),
(45,'Can add captcha store',12,'add_captchastore'),
(46,'Can change captcha store',12,'change_captchastore'),
(47,'Can delete captcha store',12,'delete_captchastore'),
(48,'Can view captcha store',12,'view_captchastore'),
(49,'Can add administrador',13,'add_administrador'),
(50,'Can change administrador',13,'change_administrador'),
(51,'Can delete administrador',13,'delete_administrador'),
(52,'Can view administrador',13,'view_administrador'),
(53,'Can add Categoría',14,'add_categoria'),
(54,'Can change Categoría',14,'change_categoria'),
(55,'Can delete Categoría',14,'delete_categoria'),
(56,'Can view Categoría',14,'view_categoria'),
(57,'Can add compra',15,'add_compra'),
(58,'Can change compra',15,'change_compra'),
(59,'Can delete compra',15,'delete_compra'),
(60,'Can view compra',15,'view_compra'),
(61,'Can add empleado',16,'add_empleado'),
(62,'Can change empleado',16,'change_empleado'),
(63,'Can delete empleado',16,'delete_empleado'),
(64,'Can view empleado',16,'view_empleado'),
(65,'Can add informe',17,'add_informe'),
(66,'Can change informe',17,'change_informe'),
(67,'Can delete informe',17,'delete_informe'),
(68,'Can view informe',17,'view_informe'),
(69,'Can add marca',18,'add_marca'),
(70,'Can change marca',18,'change_marca'),
(71,'Can delete marca',18,'delete_marca'),
(72,'Can view marca',18,'view_marca'),
(73,'Can add Menú',19,'add_menu'),
(74,'Can change Menú',19,'change_menu'),
(75,'Can delete Menú',19,'delete_menu'),
(76,'Can view Menú',19,'view_menu'),
(77,'Can add Producto del Menú',20,'add_menuproducto'),
(78,'Can change Producto del Menú',20,'change_menuproducto'),
(79,'Can delete Producto del Menú',20,'delete_menuproducto'),
(80,'Can view Producto del Menú',20,'view_menuproducto'),
(81,'Can add Pedido',21,'add_pedido'),
(82,'Can change Pedido',21,'change_pedido'),
(83,'Can delete Pedido',21,'delete_pedido'),
(84,'Can view Pedido',21,'view_pedido'),
(85,'Can add Item del Pedido',22,'add_pedidoitem'),
(86,'Can change Item del Pedido',22,'change_pedidoitem'),
(87,'Can delete Item del Pedido',22,'delete_pedidoitem'),
(88,'Can view Item del Pedido',22,'view_pedidoitem'),
(89,'Can add mesa',23,'add_mesa'),
(90,'Can change mesa',23,'change_mesa'),
(91,'Can delete mesa',23,'delete_mesa'),
(92,'Can view mesa',23,'view_mesa'),
(93,'Can add Nómina',24,'add_nomina'),
(94,'Can change Nómina',24,'change_nomina'),
(95,'Can delete Nómina',24,'delete_nomina'),
(96,'Can view Nómina',24,'view_nomina'),
(97,'Can add pedido',25,'add_pedido'),
(98,'Can change pedido',25,'change_pedido'),
(99,'Can delete pedido',25,'delete_pedido'),
(100,'Can view pedido',25,'view_pedido'),
(101,'Can add pedido detalle',26,'add_pedidodetalle'),
(102,'Can change pedido detalle',26,'change_pedidodetalle'),
(103,'Can delete pedido detalle',26,'delete_pedidodetalle'),
(104,'Can view pedido detalle',26,'view_pedidodetalle'),
(105,'Can add plato',27,'add_plato'),
(106,'Can change plato',27,'change_plato'),
(107,'Can delete plato',27,'delete_plato'),
(108,'Can view plato',27,'view_plato'),
(109,'Can add plato producto',28,'add_platoproducto'),
(110,'Can change plato producto',28,'change_platoproducto'),
(111,'Can delete plato producto',28,'delete_platoproducto'),
(112,'Can view plato producto',28,'view_platoproducto'),
(113,'Can add producto',29,'add_producto'),
(114,'Can change producto',29,'change_producto'),
(115,'Can delete producto',29,'delete_producto'),
(116,'Can view producto',29,'view_producto'),
(117,'Can add proveedor',30,'add_proveedor'),
(118,'Can change proveedor',30,'change_proveedor'),
(119,'Can delete proveedor',30,'delete_proveedor'),
(120,'Can view proveedor',30,'view_proveedor'),
(121,'Can add unidad',31,'add_unidad'),
(122,'Can change unidad',31,'change_unidad'),
(123,'Can delete unidad',31,'delete_unidad'),
(124,'Can view unidad',31,'view_unidad'),
(125,'Can add usuario',32,'add_usuario'),
(126,'Can change usuario',32,'change_usuario'),
(127,'Can delete usuario',32,'delete_usuario'),
(128,'Can view usuario',32,'view_usuario'),
(129,'Can add venta',33,'add_venta'),
(130,'Can change venta',33,'change_venta'),
(131,'Can delete venta',33,'delete_venta'),
(132,'Can view venta',33,'view_venta'),
(133,'Can add venta item',34,'add_ventaitem'),
(134,'Can change venta item',34,'change_ventaitem'),
(135,'Can delete venta item',34,'delete_ventaitem'),
(136,'Can view venta item',34,'view_ventaitem'),
(137,'Can add Inventario Diario',35,'add_inventariodiario'),
(138,'Can change Inventario Diario',35,'change_inventariodiario'),
(139,'Can delete Inventario Diario',35,'delete_inventariodiario'),
(140,'Can view Inventario Diario',35,'view_inventariodiario'),
(141,'Can add Historial de Stock',36,'add_historialstock'),
(142,'Can change Historial de Stock',36,'change_historialstock'),
(143,'Can delete Historial de Stock',36,'delete_historialstock'),
(144,'Can view Historial de Stock',36,'view_historialstock'),
(145,'Can add Movimiento de Inventario',37,'add_movimientoinventario'),
(146,'Can change Movimiento de Inventario',37,'change_movimientoinventario'),
(147,'Can delete Movimiento de Inventario',37,'delete_movimientoinventario'),
(148,'Can view Movimiento de Inventario',37,'view_movimientoinventario');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `captcha_captchastore` (
  `id` int NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `categoria_categoria`
--

DROP TABLE IF EXISTS `categoria_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_categoria`
--

LOCK TABLES `categoria_categoria` WRITE;
/*!40000 ALTER TABLE `categoria_categoria` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `categoria_categoria` VALUES
(1,'Bebidas','fjdhasd');
/*!40000 ALTER TABLE `categoria_categoria` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `compra_compra`
--

DROP TABLE IF EXISTS `compra_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra_compra` (
  `id_factura` varchar(20) NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` date NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `producto_id` bigint NOT NULL,
  `proveedor_id` bigint DEFAULT NULL,
  `unidad_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id_factura`),
  KEY `compra_compra_producto_id_5b80cdab_fk_producto_producto_id` (`producto_id`),
  KEY `compra_compra_proveedor_id_5eb5faf5_fk_proveedor_proveedor_id` (`proveedor_id`),
  KEY `compra_compra_unidad_id_00a2d0ff_fk_unidad_unidad_id` (`unidad_id`),
  CONSTRAINT `compra_compra_producto_id_5b80cdab_fk_producto_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`),
  CONSTRAINT `compra_compra_proveedor_id_5eb5faf5_fk_proveedor_proveedor_id` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor_proveedor` (`id`),
  CONSTRAINT `compra_compra_unidad_id_00a2d0ff_fk_unidad_unidad_id` FOREIGN KEY (`unidad_id`) REFERENCES `unidad_unidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra_compra`
--

LOCK TABLES `compra_compra` WRITE;
/*!40000 ALTER TABLE `compra_compra` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `compra_compra` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_usuario_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(7,'account','emailaddress'),
(8,'account','emailconfirmation'),
(1,'admin','logentry'),
(13,'administrador','administrador'),
(3,'auth','group'),
(2,'auth','permission'),
(12,'captcha','captchastore'),
(14,'categoria','categoria'),
(15,'compra','compra'),
(4,'contenttypes','contenttype'),
(16,'empleado','empleado'),
(17,'informe','informe'),
(36,'inventario','historialstock'),
(35,'inventario','inventariodiario'),
(37,'inventario','movimientoinventario'),
(18,'marca','marca'),
(19,'menu','menu'),
(20,'menu','menuproducto'),
(21,'menu','pedido'),
(22,'menu','pedidoitem'),
(23,'mesa','mesa'),
(24,'nomina','nomina'),
(25,'pedido','pedido'),
(26,'pedido','pedidodetalle'),
(27,'plato','plato'),
(28,'plato','platoproducto'),
(29,'producto','producto'),
(30,'proveedor','proveedor'),
(5,'sessions','session'),
(6,'sites','site'),
(9,'socialaccount','socialaccount'),
(10,'socialaccount','socialapp'),
(11,'socialaccount','socialtoken'),
(31,'unidad','unidad'),
(32,'usuario','usuario'),
(33,'venta','venta'),
(34,'venta','ventaitem');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-02-24 01:16:33.850901'),
(2,'contenttypes','0002_remove_content_type_name','2026-02-24 01:16:34.619533'),
(3,'auth','0001_initial','2026-02-24 01:16:36.449495'),
(4,'auth','0002_alter_permission_name_max_length','2026-02-24 01:16:36.448204'),
(5,'auth','0003_alter_user_email_max_length','2026-02-24 01:16:36.496267'),
(6,'auth','0004_alter_user_username_opts','2026-02-24 01:16:36.546773'),
(7,'auth','0005_alter_user_last_login_null','2026-02-24 01:16:36.578568'),
(8,'auth','0006_require_contenttypes_0002','2026-02-24 01:16:36.601622'),
(9,'auth','0007_alter_validators_add_error_messages','2026-02-24 01:16:36.635141'),
(10,'auth','0008_alter_user_username_max_length','2026-02-24 01:16:36.667319'),
(11,'auth','0009_alter_user_last_name_max_length','2026-02-24 01:16:36.698467'),
(12,'auth','0010_alter_group_name_max_length','2026-02-24 01:16:36.774149'),
(13,'auth','0011_update_proxy_permissions','2026-02-24 01:16:36.812874'),
(14,'auth','0012_alter_user_first_name_max_length','2026-02-24 01:16:36.851283'),
(15,'usuario','0001_initial','2026-02-24 01:16:39.045236'),
(16,'account','0001_initial','2026-02-24 01:16:40.154328'),
(17,'account','0002_email_max_length','2026-02-24 01:16:40.238410'),
(18,'account','0003_alter_emailaddress_create_unique_verified_email','2026-02-24 01:16:40.419595'),
(19,'account','0004_alter_emailaddress_drop_unique_email','2026-02-24 01:16:40.611190'),
(20,'account','0005_emailaddress_idx_upper_email','2026-02-24 01:16:40.796077'),
(21,'account','0006_emailaddress_lower','2026-02-24 01:16:40.837792'),
(22,'account','0007_emailaddress_idx_email','2026-02-24 01:16:41.153880'),
(23,'account','0008_emailaddress_unique_primary_email_fixup','2026-02-24 01:16:41.225003'),
(24,'account','0009_emailaddress_unique_primary_email','2026-02-24 01:16:41.258882'),
(25,'admin','0001_initial','2026-02-24 01:16:42.062591'),
(26,'admin','0002_logentry_remove_auto_add','2026-02-24 01:16:42.099763'),
(27,'admin','0003_logentry_add_action_flag_choices','2026-02-24 01:16:42.132624'),
(28,'administrador','0001_initial','2026-02-24 01:16:42.278522'),
(29,'administrador','0002_initial','2026-02-24 01:16:42.874004'),
(30,'captcha','0001_initial','2026-02-24 01:16:43.098467'),
(31,'captcha','0002_alter_captchastore_id','2026-02-24 01:16:43.121117'),
(32,'categoria','0001_initial','2026-02-24 01:16:43.373633'),
(33,'unidad','0001_initial','2026-02-24 01:16:43.581130'),
(34,'proveedor','0001_initial','2026-02-24 01:16:43.830216'),
(35,'marca','0001_initial','2026-02-24 01:16:44.149963'),
(36,'producto','0001_initial','2026-02-24 01:16:46.460711'),
(37,'compra','0001_initial','2026-02-24 01:16:47.781462'),
(38,'empleado','0001_initial','2026-02-24 01:16:47.942873'),
(39,'empleado','0002_initial','2026-02-24 01:16:48.313006'),
(40,'informe','0001_initial','2026-02-24 01:16:48.455339'),
(41,'informe','0002_initial','2026-02-24 01:16:48.854749'),
(42,'inventario','0001_initial','2026-02-24 01:16:50.632170'),
(43,'mesa','0001_initial','2026-02-24 01:16:50.941151'),
(44,'menu','0001_initial','2026-02-24 01:16:54.811843'),
(45,'nomina','0001_initial','2026-02-24 01:16:55.092732'),
(46,'nomina','0002_initial','2026-02-24 01:16:56.242177'),
(47,'pedido','0001_initial','2026-02-24 01:16:58.129630'),
(48,'plato','0001_initial','2026-02-24 01:17:01.832413'),
(49,'sessions','0001_initial','2026-02-24 01:17:02.251366'),
(50,'sites','0001_initial','2026-02-24 01:17:02.583379'),
(51,'sites','0002_alter_domain_unique','2026-02-24 01:17:02.738176'),
(52,'socialaccount','0001_initial','2026-02-24 01:17:10.503543'),
(53,'socialaccount','0002_token_max_lengths','2026-02-24 01:17:10.960348'),
(54,'socialaccount','0003_extra_data_default_dict','2026-02-24 01:17:11.036858'),
(55,'socialaccount','0004_app_provider_id_settings','2026-02-24 01:17:12.042940'),
(56,'socialaccount','0005_socialtoken_nullable_app','2026-02-24 01:17:13.760076'),
(57,'socialaccount','0006_alter_socialaccount_extra_data','2026-02-24 01:17:14.572985'),
(58,'venta','0001_initial','2026-02-24 01:17:16.384646');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('n18zp09mirlj6tmt9tudgy325jsszti9','.eJxVjM0KgkAURt9l1iHT_KjTLilcRBQEgSu5d-ZOWqHi6Kbo3dNoUdvvnO88WQnjUJVjoL6sHVuxJVv8bgj2Rs0M3BWaSxvZthn6GqNZib40RPvW0T37un-BCkI1vbVA60QsATRHrbU3CUqMPVdKCGkN6dQLA-ScSpXVJEkKbr23xhBqY6do-4mGAQaagrjLID-eTUcPKbsai1N-KDYJpOtKbTl7vQG1LEdh:1vusDX:C5NefwDQ2ZjgTZuR_wRb7FknJulpHhc1zOMnXULvwK0','2026-03-10 13:12:47.048348');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_site` VALUES
(1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `empleado_empleado`
--

DROP TABLE IF EXISTS `empleado_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado_empleado` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_ingreso` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `empleado_empleado_usuario_id_f52cee6d_fk_usuario_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado_empleado`
--

LOCK TABLES `empleado_empleado` WRITE;
/*!40000 ALTER TABLE `empleado_empleado` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `empleado_empleado` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `informe_informe`
--

DROP TABLE IF EXISTS `informe_informe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `informe_informe` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `creado_por_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `informe_informe_creado_por_id_c0405267_fk_usuario_usuario_id` (`creado_por_id`),
  CONSTRAINT `informe_informe_creado_por_id_c0405267_fk_usuario_usuario_id` FOREIGN KEY (`creado_por_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informe_informe`
--

LOCK TABLES `informe_informe` WRITE;
/*!40000 ALTER TABLE `informe_informe` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `informe_informe` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `inventario_historialstock`
--

DROP TABLE IF EXISTS `inventario_historialstock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_historialstock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` varchar(20) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `stock_anterior` decimal(10,2) NOT NULL,
  `stock_nuevo` decimal(10,2) NOT NULL,
  `referencia` varchar(200) DEFAULT NULL,
  `observaciones` longtext,
  `fecha` datetime(6) NOT NULL,
  `usuario` varchar(100) DEFAULT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_historial_producto_id_0641ce94_fk_producto_` (`producto_id`),
  CONSTRAINT `inventario_historial_producto_id_0641ce94_fk_producto_` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_historialstock`
--

LOCK TABLES `inventario_historialstock` WRITE;
/*!40000 ALTER TABLE `inventario_historialstock` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `inventario_historialstock` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `inventario_inventariodiario`
--

DROP TABLE IF EXISTS `inventario_inventariodiario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_inventariodiario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `fecha_apertura` datetime(6) NOT NULL,
  `fecha_cierre` datetime(6) DEFAULT NULL,
  `numero` int unsigned NOT NULL,
  `estado` varchar(20) NOT NULL,
  `observaciones` longtext,
  PRIMARY KEY (`id`),
  CONSTRAINT `inventario_inventariodiario_chk_1` CHECK ((`numero` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_inventariodiario`
--

LOCK TABLES `inventario_inventariodiario` WRITE;
/*!40000 ALTER TABLE `inventario_inventariodiario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `inventario_inventariodiario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `inventario_movimientoinventario`
--

DROP TABLE IF EXISTS `inventario_movimientoinventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_movimientoinventario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_control` varchar(10) NOT NULL,
  `inventario_inicial` decimal(10,2) NOT NULL,
  `consumo_automatico` decimal(10,2) NOT NULL,
  `inventario_final` decimal(10,2) DEFAULT NULL,
  `ajuste_manual` decimal(10,2) NOT NULL,
  `motivo_ajuste` varchar(200) DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `inventario_diario_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventario_movimientoinv_inventario_diario_id_pro_44e120fd_uniq` (`inventario_diario_id`,`producto_id`),
  KEY `inventario_movimient_producto_id_cec1a696_fk_producto_` (`producto_id`),
  CONSTRAINT `inventario_movimient_inventario_diario_id_8d145b6e_fk_inventari` FOREIGN KEY (`inventario_diario_id`) REFERENCES `inventario_inventariodiario` (`id`),
  CONSTRAINT `inventario_movimient_producto_id_cec1a696_fk_producto_` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_movimientoinventario`
--

LOCK TABLES `inventario_movimientoinventario` WRITE;
/*!40000 ALTER TABLE `inventario_movimientoinventario` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `inventario_movimientoinventario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `marca_marca`
--

DROP TABLE IF EXISTS `marca_marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `marca_marca` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext,
  `pais_origen` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marca_marca`
--

LOCK TABLES `marca_marca` WRITE;
/*!40000 ALTER TABLE `marca_marca` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `marca_marca` VALUES
(1,'Coca-cola','jhkdan','Colombia');
/*!40000 ALTER TABLE `marca_marca` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `menu_menu`
--

DROP TABLE IF EXISTS `menu_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext,
  `precio_base` decimal(10,2) NOT NULL,
  `descuento` decimal(5,2) NOT NULL,
  `disponible` tinyint(1) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `categoria_menu_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_menu_categoria_menu_id_cfc2a071_fk_categoria_categoria_id` (`categoria_menu_id`),
  CONSTRAINT `menu_menu_categoria_menu_id_cfc2a071_fk_categoria_categoria_id` FOREIGN KEY (`categoria_menu_id`) REFERENCES `categoria_categoria` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_menu`
--

LOCK TABLES `menu_menu` WRITE;
/*!40000 ALTER TABLE `menu_menu` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `menu_menu` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `menu_menuproducto`
--

DROP TABLE IF EXISTS `menu_menuproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_menuproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` decimal(10,2) NOT NULL,
  `orden` int unsigned NOT NULL,
  `fecha_agregado` datetime(6) NOT NULL,
  `menu_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_menuproducto_menu_id_producto_id_480dd1a8_uniq` (`menu_id`,`producto_id`),
  KEY `menu_menuproducto_producto_id_b1dc5fca_fk_producto_producto_id` (`producto_id`),
  CONSTRAINT `menu_menuproducto_menu_id_6d53d861_fk_menu_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu_menu` (`id`),
  CONSTRAINT `menu_menuproducto_producto_id_b1dc5fca_fk_producto_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`),
  CONSTRAINT `menu_menuproducto_chk_1` CHECK ((`orden` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_menuproducto`
--

LOCK TABLES `menu_menuproducto` WRITE;
/*!40000 ALTER TABLE `menu_menuproducto` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `menu_menuproducto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `menu_pedido`
--

DROP TABLE IF EXISTS `menu_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_pedido` varchar(20) NOT NULL,
  `cliente_nombre` varchar(200) NOT NULL,
  `tipo_pedido` varchar(10) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `observaciones` longtext,
  `subtotal` decimal(10,2) NOT NULL,
  `descuento_total` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `mesa_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `menu_pedido_mesa_id_444855fe_fk_mesa_mesa_id` (`mesa_id`),
  CONSTRAINT `menu_pedido_mesa_id_444855fe_fk_mesa_mesa_id` FOREIGN KEY (`mesa_id`) REFERENCES `mesa_mesa` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_pedido`
--

LOCK TABLES `menu_pedido` WRITE;
/*!40000 ALTER TABLE `menu_pedido` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `menu_pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `menu_pedidoitem`
--

DROP TABLE IF EXISTS `menu_pedidoitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_pedidoitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_temporal` varchar(200) DEFAULT NULL,
  `cantidad` int unsigned NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento_aplicado` decimal(5,2) NOT NULL,
  `observaciones` longtext,
  `menu_id` bigint DEFAULT NULL,
  `pedido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_pedidoitem_menu_id_bc2be4b2_fk_menu_menu_id` (`menu_id`),
  KEY `menu_pedidoitem_pedido_id_90adfbf0_fk_menu_pedido_id` (`pedido_id`),
  CONSTRAINT `menu_pedidoitem_menu_id_bc2be4b2_fk_menu_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu_menu` (`id`),
  CONSTRAINT `menu_pedidoitem_pedido_id_90adfbf0_fk_menu_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `menu_pedido` (`id`),
  CONSTRAINT `menu_pedidoitem_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_pedidoitem`
--

LOCK TABLES `menu_pedidoitem` WRITE;
/*!40000 ALTER TABLE `menu_pedidoitem` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `menu_pedidoitem` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `mesa_mesa`
--

DROP TABLE IF EXISTS `mesa_mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesa_mesa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `capacidad` int NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `numero` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesa_mesa`
--

LOCK TABLES `mesa_mesa` WRITE;
/*!40000 ALTER TABLE `mesa_mesa` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `mesa_mesa` VALUES
(1,4,'Afuera','M-001');
/*!40000 ALTER TABLE `mesa_mesa` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `nomina_nomina`
--

DROP TABLE IF EXISTS `nomina_nomina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `nomina_nomina` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_pago` varchar(10) NOT NULL,
  `valor_unitario` decimal(10,2) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `fecha_pago` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `observaciones` longtext,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `creado_por_id` bigint DEFAULT NULL,
  `empleado_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `nomina_nomina_creado_por_id_bea130a1_fk_usuario_usuario_id` (`creado_por_id`),
  KEY `nomina_nomina_empleado_id_9920664e_fk_usuario_usuario_id` (`empleado_id`),
  CONSTRAINT `nomina_nomina_creado_por_id_bea130a1_fk_usuario_usuario_id` FOREIGN KEY (`creado_por_id`) REFERENCES `usuario_usuario` (`id`),
  CONSTRAINT `nomina_nomina_empleado_id_9920664e_fk_usuario_usuario_id` FOREIGN KEY (`empleado_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nomina_nomina`
--

LOCK TABLES `nomina_nomina` WRITE;
/*!40000 ALTER TABLE `nomina_nomina` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `nomina_nomina` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pedido_pedido`
--

DROP TABLE IF EXISTS `pedido_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mesa` varchar(10) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_pedido`
--

LOCK TABLES `pedido_pedido` WRITE;
/*!40000 ALTER TABLE `pedido_pedido` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pedido_pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pedido_pedidodetalle`
--

DROP TABLE IF EXISTS `pedido_pedidodetalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_pedidodetalle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int unsigned NOT NULL,
  `menu_id` bigint NOT NULL,
  `pedido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_pedidodetalle_menu_id_c50b0ae1_fk_menu_menu_id` (`menu_id`),
  KEY `pedido_pedidodetalle_pedido_id_95a54780_fk_pedido_pedido_id` (`pedido_id`),
  CONSTRAINT `pedido_pedidodetalle_menu_id_c50b0ae1_fk_menu_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu_menu` (`id`),
  CONSTRAINT `pedido_pedidodetalle_pedido_id_95a54780_fk_pedido_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `pedido_pedido` (`id`),
  CONSTRAINT `pedido_pedidodetalle_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_pedidodetalle`
--

LOCK TABLES `pedido_pedidodetalle` WRITE;
/*!40000 ALTER TABLE `pedido_pedidodetalle` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pedido_pedidodetalle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `plato_plato`
--

DROP TABLE IF EXISTS `plato_plato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `plato_plato` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `producto_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `plato_plato_producto_id_d9c46a7c_fk_producto_producto_id` (`producto_id`),
  CONSTRAINT `plato_plato_producto_id_d9c46a7c_fk_producto_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plato_plato`
--

LOCK TABLES `plato_plato` WRITE;
/*!40000 ALTER TABLE `plato_plato` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `plato_plato` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `plato_platoproducto`
--

DROP TABLE IF EXISTS `plato_platoproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `plato_platoproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` decimal(10,2) NOT NULL,
  `plato_id` bigint NOT NULL,
  `producto_id` bigint NOT NULL,
  `unidad_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `plato_platoproducto_plato_id_410f88db_fk_plato_plato_id` (`plato_id`),
  KEY `plato_platoproducto_producto_id_e682a507_fk_producto_producto_id` (`producto_id`),
  KEY `plato_platoproducto_unidad_id_39bea6c3_fk_unidad_unidad_id` (`unidad_id`),
  CONSTRAINT `plato_platoproducto_plato_id_410f88db_fk_plato_plato_id` FOREIGN KEY (`plato_id`) REFERENCES `plato_plato` (`id`),
  CONSTRAINT `plato_platoproducto_producto_id_e682a507_fk_producto_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto_producto` (`id`),
  CONSTRAINT `plato_platoproducto_unidad_id_39bea6c3_fk_unidad_unidad_id` FOREIGN KEY (`unidad_id`) REFERENCES `unidad_unidad` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plato_platoproducto`
--

LOCK TABLES `plato_platoproducto` WRITE;
/*!40000 ALTER TABLE `plato_platoproducto` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `plato_platoproducto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `producto_producto`
--

DROP TABLE IF EXISTS `producto_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `tipo_uso` varchar(20) NOT NULL,
  `stock` decimal(8,2) DEFAULT NULL,
  `area_preparacion` varchar(20) NOT NULL,
  `disponible` tinyint(1) NOT NULL,
  `categoria_id` bigint NOT NULL,
  `marca_id` bigint NOT NULL,
  `proveedor_id` bigint NOT NULL,
  `unidad_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_producto_categoria_id_873c058f_fk_categoria` (`categoria_id`),
  KEY `producto_producto_marca_id_3e6157bc_fk_marca_marca_id` (`marca_id`),
  KEY `producto_producto_proveedor_id_95d96f92_fk_proveedor` (`proveedor_id`),
  KEY `producto_producto_unidad_id_c304c409_fk_unidad_unidad_id` (`unidad_id`),
  CONSTRAINT `producto_producto_categoria_id_873c058f_fk_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria_categoria` (`id`),
  CONSTRAINT `producto_producto_marca_id_3e6157bc_fk_marca_marca_id` FOREIGN KEY (`marca_id`) REFERENCES `marca_marca` (`id`),
  CONSTRAINT `producto_producto_proveedor_id_95d96f92_fk_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor_proveedor` (`id`),
  CONSTRAINT `producto_producto_unidad_id_c304c409_fk_unidad_unidad_id` FOREIGN KEY (`unidad_id`) REFERENCES `unidad_unidad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_producto`
--

LOCK TABLES `producto_producto` WRITE;
/*!40000 ALTER TABLE `producto_producto` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `producto_producto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `proveedor_proveedor`
--

DROP TABLE IF EXISTS `proveedor_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor_proveedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nit` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit` (`nit`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor_proveedor`
--

LOCK TABLES `proveedor_proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor_proveedor` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `proveedor_proveedor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_social_user_id_8146e70c_fk_usuario_u` (`user_id`),
  CONSTRAINT `socialaccount_social_user_id_8146e70c_fk_usuario_u` FOREIGN KEY (`user_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `unidad_unidad`
--

DROP TABLE IF EXISTS `unidad_unidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad_unidad` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `tipo` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_unidad`
--

LOCK TABLES `unidad_unidad` WRITE;
/*!40000 ALTER TABLE `unidad_unidad` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `unidad_unidad` VALUES
(1,'Ml(mililitros)','jhfkalsf','unidad');
/*!40000 ALTER TABLE `unidad_unidad` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario`
--

DROP TABLE IF EXISTS `usuario_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cedula` varchar(20) DEFAULT NULL,
  `cargo` varchar(50) NOT NULL,
  `numero_celular` varchar(20) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `cedula` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario`
--

LOCK TABLES `usuario_usuario` WRITE;
/*!40000 ALTER TABLE `usuario_usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `usuario_usuario` VALUES
(1,'pbkdf2_sha256$1000000$xewwfS0KO9i1tAzKu3kqfZ$FE7QnI+wBrhVeYIzt5jxgYJGMmwGX49TseDVM7edMB0=','2026-02-24 01:22:58.236641',1,'','',1,1,'2026-02-24 01:18:21.057492','',NULL,'operador',NULL,'activo','puertobotiadavidalejandro@gmail.com');
/*!40000 ALTER TABLE `usuario_usuario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario_groups`
--

DROP TABLE IF EXISTS `usuario_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_usuario_groups_usuario_id_group_id_a4cfb0b8_uniq` (`usuario_id`,`group_id`),
  KEY `usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id` (`group_id`),
  CONSTRAINT `usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `usuario_usuario_groups_usuario_id_62de76a1_fk_usuario_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario_groups`
--

LOCK TABLES `usuario_usuario_groups` WRITE;
/*!40000 ALTER TABLE `usuario_usuario_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `usuario_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario_usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuario_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_usuario_user_per_usuario_id_permission_id_c0a85055_uniq` (`usuario_id`,`permission_id`),
  KEY `usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `usuario_usuario_user_usuario_id_5969a193_fk_usuario_u` FOREIGN KEY (`usuario_id`) REFERENCES `usuario_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_usuario_user_permissions`
--

LOCK TABLES `usuario_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `usuario_usuario_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `usuario_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `venta_venta`
--

DROP TABLE IF EXISTS `venta_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_venta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `metodo_pago` varchar(20) DEFAULT NULL,
  `numero_factura` varchar(20) NOT NULL,
  `cliente_nombre` varchar(200) NOT NULL,
  `tipo_pedido` varchar(10) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `descuento_total` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_venta` datetime(6) NOT NULL,
  `estado` varchar(15) NOT NULL,
  `mesa_id` bigint DEFAULT NULL,
  `pedido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_factura` (`numero_factura`),
  UNIQUE KEY `pedido_id` (`pedido_id`),
  KEY `venta_venta_mesa_id_f715a839_fk_mesa_mesa_id` (`mesa_id`),
  CONSTRAINT `venta_venta_mesa_id_f715a839_fk_mesa_mesa_id` FOREIGN KEY (`mesa_id`) REFERENCES `mesa_mesa` (`id`),
  CONSTRAINT `venta_venta_pedido_id_c502ac80_fk_menu_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `menu_pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_venta`
--

LOCK TABLES `venta_venta` WRITE;
/*!40000 ALTER TABLE `venta_venta` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `venta_venta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `venta_ventaitem`
--

DROP TABLE IF EXISTS `venta_ventaitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_ventaitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `venta_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_ventaitem_venta_id_69715c0c_fk_venta_venta_id` (`venta_id`),
  CONSTRAINT `venta_ventaitem_venta_id_69715c0c_fk_venta_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `venta_venta` (`id`),
  CONSTRAINT `venta_ventaitem_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_ventaitem`
--

LOCK TABLES `venta_ventaitem` WRITE;
/*!40000 ALTER TABLE `venta_ventaitem` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `venta_ventaitem` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-02-24 14:34:06
