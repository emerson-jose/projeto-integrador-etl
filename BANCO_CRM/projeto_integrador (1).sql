CREATE DATABASE  IF NOT EXISTS `crm_vendas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `crm_vendas`;
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: crm_vendas
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contas`
--

DROP TABLE IF EXISTS `contas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `contas` (
  `conta` varchar(150) NOT NULL,
  `setor` varchar(100) DEFAULT NULL,
  `ano_fundacao` int(11) DEFAULT NULL,
  `receita` decimal(15,2) DEFAULT NULL,
  `funcionarios` int(11) DEFAULT NULL,
  `local_escritorio` varchar(100) DEFAULT NULL,
  `subsidiaria_de` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`conta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipes_vendas`
--

DROP TABLE IF EXISTS `equipes_vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipes_vendas` (
  `agente_vendas` varchar(100) NOT NULL,
  `gerente` varchar(100) DEFAULT NULL,
  `escritorio_regional` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`agente_vendas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metadados`
--

DROP TABLE IF EXISTS `metadados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `metadados` (
  `tabela` varchar(100) DEFAULT NULL,
  `campo` varchar(100) DEFAULT NULL,
  `descricao` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pipeline_vendas`
--

DROP TABLE IF EXISTS `pipeline_vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pipeline_vendas` (
  `id_oportunidade` varchar(50) NOT NULL,
  `agente_vendas` varchar(100) DEFAULT NULL,
  `produto` varchar(100) DEFAULT NULL,
  `conta` varchar(150) DEFAULT NULL,
  `fase_negociacao` varchar(50) DEFAULT NULL,
  `data_engajamento` date DEFAULT NULL,
  `data_fechamento` date DEFAULT NULL,
  `valor_fechamento` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`id_oportunidade`),
  KEY `fk_agente` (`agente_vendas`),
  KEY `fk_produto` (`produto`),
  KEY `fk_conta` (`conta`),
  CONSTRAINT `fk_agente` FOREIGN KEY (`agente_vendas`) REFERENCES `equipes_vendas` (`agente_vendas`) ON DELETE SET NULL,
  CONSTRAINT `fk_conta` FOREIGN KEY (`conta`) REFERENCES `contas` (`conta`) ON DELETE SET NULL,
  CONSTRAINT `fk_produto` FOREIGN KEY (`produto`) REFERENCES `produtos` (`produto`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `produto` varchar(100) NOT NULL,
  `serie` varchar(50) DEFAULT NULL,
  `preco_venda` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`produto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-06  0:42:19
