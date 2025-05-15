-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: helldivers2_test
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `biomes`
--

DROP TABLE IF EXISTS `biomes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `biomes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `slug` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campaigns`
--

DROP TABLE IF EXISTS `campaigns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campaigns` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `planet_index` int NOT NULL,
  `biome_id` int DEFAULT NULL,
  `faction_id` int DEFAULT NULL,
  `defense` tinyint(1) DEFAULT NULL,
  `expire_datetime` datetime DEFAULT NULL,
  `health` int DEFAULT NULL,
  `max_health` int DEFAULT NULL,
  `percentage` float DEFAULT NULL,
  `players` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `biome_id` (`biome_id`),
  KEY `faction_id` (`faction_id`),
  CONSTRAINT `campaigns_ibfk_1` FOREIGN KEY (`biome_id`) REFERENCES `biomes` (`id`),
  CONSTRAINT `campaigns_ibfk_2` FOREIGN KEY (`faction_id`) REFERENCES `factions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `environmentals`
--

DROP TABLE IF EXISTS `environmentals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environmentals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `factions`
--

DROP TABLE IF EXISTS `factions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `home_worlds`
--

DROP TABLE IF EXISTS `home_worlds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `home_worlds` (
  `war_id` int NOT NULL,
  `faction_id` int NOT NULL,
  `planet_id` int NOT NULL,
  PRIMARY KEY (`war_id`,`faction_id`,`planet_id`),
  KEY `faction_id` (`faction_id`),
  KEY `planet_id` (`planet_id`),
  CONSTRAINT `home_worlds_ibfk_1` FOREIGN KEY (`war_id`) REFERENCES `war_info` (`war_id`),
  CONSTRAINT `home_worlds_ibfk_2` FOREIGN KEY (`faction_id`) REFERENCES `factions` (`id`),
  CONSTRAINT `home_worlds_ibfk_3` FOREIGN KEY (`planet_id`) REFERENCES `planets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `major_orders`
--

DROP TABLE IF EXISTS `major_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `major_orders` (
  `id32` bigint NOT NULL,
  `expires_in` int DEFAULT NULL,
  `expiry_time` datetime DEFAULT NULL,
  `progress` json DEFAULT NULL,
  `flags` int DEFAULT NULL,
  `override_brief` text,
  `override_title` varchar(255) DEFAULT NULL,
  `reward` json DEFAULT NULL,
  `rewards` json DEFAULT NULL,
  `task_description` text,
  `tasks` json DEFAULT NULL,
  `order_type` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id32`),
  KEY `idx_expiry_time` (`expiry_time`),
  KEY `idx_order_type` (`order_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` int NOT NULL,
  `published` datetime NOT NULL,
  `type` varchar(100) NOT NULL,
  `tagIds` json NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `planet_environmentals`
--

DROP TABLE IF EXISTS `planet_environmentals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planet_environmentals` (
  `planet_id` int NOT NULL,
  `environmental_id` int NOT NULL,
  PRIMARY KEY (`planet_id`,`environmental_id`),
  KEY `environmental_id` (`environmental_id`),
  CONSTRAINT `planet_environmentals_ibfk_1` FOREIGN KEY (`planet_id`) REFERENCES `planets` (`id`),
  CONSTRAINT `planet_environmentals_ibfk_2` FOREIGN KEY (`environmental_id`) REFERENCES `environmentals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `planet_history`
--

DROP TABLE IF EXISTS `planet_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planet_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `planet_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  `current_health` bigint DEFAULT NULL,
  `max_health` bigint DEFAULT NULL,
  `player_count` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `planet_id` (`planet_id`),
  CONSTRAINT `planet_history_ibfk_1` FOREIGN KEY (`planet_id`) REFERENCES `planets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `planet_infos`
--

DROP TABLE IF EXISTS `planet_infos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planet_infos` (
  `war_id` int NOT NULL,
  `planet_id` int NOT NULL,
  `position_x` float DEFAULT NULL,
  `position_y` float DEFAULT NULL,
  `waypoints` json DEFAULT NULL,
  `sector` int DEFAULT NULL,
  `max_health` bigint DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT NULL,
  `initial_faction_id` int DEFAULT NULL,
  PRIMARY KEY (`war_id`,`planet_id`),
  KEY `planet_id` (`planet_id`),
  KEY `initial_faction_id` (`initial_faction_id`),
  CONSTRAINT `planet_infos_ibfk_1` FOREIGN KEY (`war_id`) REFERENCES `war_info` (`war_id`),
  CONSTRAINT `planet_infos_ibfk_2` FOREIGN KEY (`planet_id`) REFERENCES `planets` (`id`),
  CONSTRAINT `planet_infos_ibfk_3` FOREIGN KEY (`initial_faction_id`) REFERENCES `factions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `planet_status`
--

DROP TABLE IF EXISTS `planet_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planet_status` (
  `war_id` int NOT NULL,
  `planet_index` int NOT NULL,
  `owner` int DEFAULT NULL,
  `health` bigint DEFAULT NULL,
  `regen_per_second` float DEFAULT NULL,
  `players` int DEFAULT NULL,
  `position_x` float DEFAULT NULL,
  `position_y` float DEFAULT NULL,
  PRIMARY KEY (`war_id`,`planet_index`),
  CONSTRAINT `planet_status_ibfk_1` FOREIGN KEY (`war_id`) REFERENCES `war_status` (`war_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `planets`
--

DROP TABLE IF EXISTS `planets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `biome_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `biome_id` (`biome_id`),
  CONSTRAINT `planets_ibfk_1` FOREIGN KEY (`biome_id`) REFERENCES `biomes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `war_info`
--

DROP TABLE IF EXISTS `war_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `war_info` (
  `war_id` int NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `layout_version` int DEFAULT NULL,
  `minimum_client_version` varchar(20) DEFAULT NULL,
  `capital_infos` json DEFAULT NULL,
  `planet_permanent_effects` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`war_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `war_status`
--

DROP TABLE IF EXISTS `war_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `war_status` (
  `war_id` int NOT NULL,
  `time` datetime NOT NULL,
  `impact_multiplier` float DEFAULT NULL,
  `story_beat_id32` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`war_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15 15:33:54
