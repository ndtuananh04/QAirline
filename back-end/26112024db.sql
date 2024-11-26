-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: qairline
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(60) NOT NULL,
  `password` text NOT NULL,
  `role` enum('customer','admin') NOT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'hoang195@gmail.com','hoang190504@','customer'),(2,'user1@gmail.com','hoang19504@@','customer'),(3,'user2@gmail.com','scrypt:32768:8:1$Q7TTzldaPyN6GC39$0279cebebaa79bb776798f589f8062e2d45b7d9a515dc38191425679731f82abbd59007054e500279f800a8e52d0a2380b52f391d1be0190e5abbf352c43c38c','customer'),(4,'user3@gmail.com','scrypt:32768:8:1$TCWGiYgOu0BtuqTm$e5eb837d821998a26f3a480cd5a228d9d3c3687126628686de1aafca25d4ce91c12fbab054ed356df9825823ab1edf291ac58fb9f47c11e332f98949458a5d30','customer'),(5,'user4@gmail.com','scrypt:32768:8:1$4vwSpUAKIxDpR2Vf$8d0ed472fe4834ef94fb1c2f73bffcb85390cfd13c014084d833fd0a631a4c82970eadf2e599156ae0cd32f94df86ee5179739e6914461760cfb3a355b548d70','customer'),(6,'user5@gmail.com','scrypt:32768:8:1$hx6WnKWs64MOXeG9$8789b1486086afc22a94350a006730625a8c3960ec00f58ab09d5f973d7f58d06d63596dde15d3555fd0e559fd85bff841e992f0e5a1e5fcc6422f13d3d00737','customer'),(7,'user6@gmail.com','scrypt:32768:8:1$rIZlBenWTo0bpGfq$d75626c0035961cd01a3ee7f8021bc2a9afa443e6dbeca9b3bbd4b8247387878e3c36ee4c910982492b124df7363ac2629d986704d480fd271d0de089e94f64b','customer'),(8,'user7@gmail.com','scrypt:32768:8:1$7LO9BD2bssuBrMDu$27a363ba42a3c23c7bf1be2516ca4b5d7be63e92d26ce3bfc2f93bf5f7a153fd997225343b417259742db0299b9a1207d4b1c5e2c5ac54b8930f464906bee26b','customer'),(9,'user8@gmail.com','scrypt:32768:8:1$cdbTMYON5fzRC4SE$960ad52c756b9e6ea5b75834647513076c9bb53fd1bf93e53707e87878b7383b76755481a04effe9f2975309fa1448fe9fe535f11b4dbbf8cd1088958b8a4773','customer'),(10,'user9@gmail.com','scrypt:32768:8:1$tPFCn1nRQAbddpi0$95ff30e67b7fa6eb54c49191e7d04966214fc0df1043363776d1ee60a66179e27625c74b4fa2f8bac4ae45209b9b605f250214d89a432dd7fda6dc18ff6757dd','customer'),(11,'user10@gmail.com','scrypt:32768:8:1$EO4Q6NKLYe3kuQ3q$eb14e3b5f51183037d49efe18c52e118e094fbf11510b54e83e2683da389f8fcc3aa652cba8e2daec68e99c2c28a092d373d197debb6c9bc531ae8e133825fb1','customer'),(12,'user11@gmail.com','scrypt:32768:8:1$La4ucgV7oBZMxo8j$bc8214c5010eabce48b79afef764e21acbb8b51a66f50e64f06633332897b96202ca206489b72393eea85dc1d0ff6e9b53f8628f24c5cc0b7a7ba205c5b395c1','customer'),(13,'user12@gmail.com','scrypt:32768:8:1$K2xhyW04ODp76Mxm$56757f52a51f6e0f8b90735faaeef66c123cc917171784e995d754fdc85d407b5a686ac9319ec003aef67d60e01739d17f32acb66c8381d933a2733d62e524eb','customer'),(14,'user13@gmail.com','scrypt:32768:8:1$g9zaxFOx6EVIo7Sk$4edd8b7e4b8fb4d2690a73293e3be3f307f8a8717eab4b467d4e0dceaae7c8d957d59341b37b065a6a03847b547bfe7f6b8c3b4b151dbe11216db822126aa0d8','customer'),(15,'user14@gmail.com','scrypt:32768:8:1$drjXNEwNAuabJP7y$065a6e82bb625c6a0c0fec7bb6c3654f3c252917d74d00c21c6f737953f8dd358a5ed1fbf21931ac67c89f71d1851e9336c02caca6a0cf01a58b9c204668c219','customer'),(16,'admin1@gmail.com','scrypt:32768:8:1$7NbdzwrAwvuLYMXe$ab3844ba7e29eb88c5bd4eabb6df9f6dd71925c3c3e7182a4c3650abaf4dcf39c74d70e44cece4ae46c945583cd25b5c490414663156dbab5e66cb4dc714c03d','admin'),(17,'admin2@gmail.com','scrypt:32768:8:1$BMKlZGqLPMRit90j$10a28326daa2aba0c0691767b884942c98230a2081a8b279a8bb28c92975115684106f3989435bb33634b412293d28c08a9b42e88432f454ba1e65364fa0ce2b','admin'),(18,'admin3@gmail.com','scrypt:32768:8:1$46ETspihwNxFuEUx$bf161fc6b0b19b8cffeb4eceb1fadf0eb59a39a055f55cc88e1553934833525e15bb413f4857cee5d41e8be6269b3c19c614d109a6fdc21fd5016575e39a94a0','admin'),(19,'admin4@gmail.com','scrypt:32768:8:1$fndw0jhaAVVbKK9R$6186d4ac39ee458a6c28e9655f89f3a78f51f87d7ac9e129c346315f0ca32d85b9eb695971590cfb4cd60d7c01ac08ef04119abba5b3b342e1a4882189411038','admin');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airplanes`
--

DROP TABLE IF EXISTS `airplanes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airplanes` (
  `airplane_id` int NOT NULL AUTO_INCREMENT,
  `name_airplane` varchar(45) NOT NULL,
  `capacity` int NOT NULL,
  `is_locked` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`airplane_id`),
  UNIQUE KEY `airline_number_UNIQUE` (`name_airplane`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airplanes`
--

LOCK TABLES `airplanes` WRITE;
/*!40000 ALTER TABLE `airplanes` DISABLE KEYS */;
INSERT INTO `airplanes` VALUES (1,'123456A',200,0),(2,'123456B',250,0),(3,'123456C',200,0),(4,'123456D',300,0);
/*!40000 ALTER TABLE `airplanes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking_histories`
--

DROP TABLE IF EXISTS `booking_histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking_histories` (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `action` enum('booked','cancelled','modified') NOT NULL,
  `action_date` datetime NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `fk_booking_ticket_id_idx` (`ticket_id`),
  CONSTRAINT `fk_booking_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_histories`
--

LOCK TABLES `booking_histories` WRITE;
/*!40000 ALTER TABLE `booking_histories` DISABLE KEYS */;
/*!40000 ALTER TABLE `booking_histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cancellations`
--

DROP TABLE IF EXISTS `cancellations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancellations` (
  `cancellation_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `cancellationscol` int NOT NULL,
  `reason` text,
  `cancellation_date` datetime NOT NULL,
  PRIMARY KEY (`cancellation_id`),
  KEY `fk_cancellations_ticket_id_idx` (`ticket_id`),
  CONSTRAINT `fk_cancellation_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellations`
--

LOCK TABLES `cancellations` WRITE;
/*!40000 ALTER TABLE `cancellations` DISABLE KEYS */;
/*!40000 ALTER TABLE `cancellations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_delay`
--

DROP TABLE IF EXISTS `flight_delay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_delay` (
  `delay_id` int NOT NULL AUTO_INCREMENT,
  `flight_id` int NOT NULL,
  `new_departure_time` datetime DEFAULT NULL,
  PRIMARY KEY (`delay_id`),
  KEY `fk_delay_flight_id_idx` (`flight_id`),
  CONSTRAINT `fk_delay_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_delay`
--

LOCK TABLES `flight_delay` WRITE;
/*!40000 ALTER TABLE `flight_delay` DISABLE KEYS */;
/*!40000 ALTER TABLE `flight_delay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `flight_id` int NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(45) NOT NULL,
  `departure` varchar(60) NOT NULL,
  `code_departure` varchar(10) NOT NULL,
  `arrival` varchar(60) NOT NULL,
  `code_arrival` varchar(10) NOT NULL,
  `departure_time` date NOT NULL,
  `departure_hour_time` time NOT NULL,
  `arrival_hour_time` time NOT NULL,
  `terminal` int NOT NULL,
  `status` enum('SCHEDULED','DELAYED','CANCELLED') NOT NULL,
  `available_seats` int NOT NULL,
  `airplane_id` int NOT NULL,
  PRIMARY KEY (`flight_id`),
  KEY `fk_flights_airplanes_id_idx` (`airplane_id`),
  CONSTRAINT `fk_flights_airplanes_id` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights`
--

LOCK TABLES `flights` WRITE;
/*!40000 ALTER TABLE `flights` DISABLE KEYS */;
INSERT INTO `flights` VALUES (1,'195204QAL','Ha Noi','HAN','Ho Chi Minh','SGN','2024-11-26','07:00:00','09:00:00',1,'SCHEDULED',100,1),(2,'123456QAL','Thanh Hoa','THD','Nha Trang','CXR','2024-12-12','08:00:00','10:00:00',1,'SCHEDULED',100,3),(3,'123321QAL','Ha Noi','HAN','Thanh Hoa','THD','2024-11-28','11:00:00','15:00:00',1,'SCHEDULED',200,1),(4,'123432QAL','Hue','HUI','Ho Chi Minh','SGN','2024-10-19','19:00:00','23:00:00',1,'CANCELLED',50,4),(5,'204195QAL','Ha Noi','HAN','Ho Chi Minh','SGN','2024-11-26','19:00:00','21:00:00',1,'SCHEDULED',200,2);
/*!40000 ALTER TABLE `flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions`
--

DROP TABLE IF EXISTS `promotions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions` (
  `promotion_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  PRIMARY KEY (`promotion_id`),
  CONSTRAINT `fk_promotions_user_id` FOREIGN KEY (`promotion_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions`
--

LOCK TABLES `promotions` WRITE;
/*!40000 ALTER TABLE `promotions` DISABLE KEYS */;
INSERT INTO `promotions` VALUES (1,'1','Hello','2004-05-19 00:00:00','2004-05-21 00:00:00');
/*!40000 ALTER TABLE `promotions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revoked_tokens`
--

DROP TABLE IF EXISTS `revoked_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `revoked_tokens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jti` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revoked_tokens`
--

LOCK TABLES `revoked_tokens` WRITE;
/*!40000 ALTER TABLE `revoked_tokens` DISABLE KEYS */;
INSERT INTO `revoked_tokens` VALUES (1,'fde00b35-ed97-40c8-ba98-011060c7b7bc');
/*!40000 ALTER TABLE `revoked_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seats`
--

DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
  `seat_id` int NOT NULL AUTO_INCREMENT,
  `airplane_id` int NOT NULL,
  `seat_number` varchar(45) NOT NULL,
  `seat_class` enum('ECONOMY','BUSINESS','SKYBOSS') NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `seat_info` text,
  PRIMARY KEY (`seat_id`),
  KEY `fk_seats_airplanes_id_idx` (`airplane_id`),
  CONSTRAINT `fk_seats_airplanes_id` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES (1,1,'1A','BUSINESS',100.00,NULL),(2,1,'1B','BUSINESS',100.00,NULL),(3,1,'1C','BUSINESS',100.00,NULL),(4,1,'50A','ECONOMY',10.00,NULL),(5,1,'50B','ECONOMY',10.00,NULL),(6,1,'50C','ECONOMY',10.00,NULL),(7,1,'1A','BUSINESS',100.00,NULL),(8,1,'50A','ECONOMY',10.00,NULL),(9,1,'20A','SKYBOSS',50.00,NULL),(10,1,'20B','SKYBOSS',50.00,NULL),(11,2,'1A','BUSINESS',100.00,NULL),(12,2,'50A','ECONOMY',10.00,NULL);
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `ticket_number` varchar(45) NOT NULL,
  `flight_id` int NOT NULL,
  `seat_number` varchar(45) DEFAULT NULL,
  `ticket_class` enum('economy','bussiness') NOT NULL,
  `booking_time` datetime DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  UNIQUE KEY `flight_id_UNIQUE` (`flight_id`),
  KEY `fk_ticket_flight_id_idx` (`flight_id`),
  CONSTRAINT `fk_ticket_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`),
  CONSTRAINT `fk_ticket_user_id` FOREIGN KEY (`ticket_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_info` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `identification` varchar(20) NOT NULL,
  `family_name` varchar(60) NOT NULL,
  `given_name` varchar(60) NOT NULL,
  `gender` enum('male','female') NOT NULL,
  `nationality` varchar(60) NOT NULL,
  `date_of_birth` date NOT NULL,
  `phone_number` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `identification_UNIQUE` (`identification`),
  KEY `fk_user_information_account_id` (`account_id`),
  CONSTRAINT `fk_user_information_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES (1,12,'38204014528','Le Ba','Hoang','male','Viet Nam','2004-05-19','0836425093'),(2,13,'38204014529','Le Ba','Hoang','male','Viet Nam','2004-05-19','0836425094'),(3,14,'38204014527','Le Ba','Hoang','male','Viet Nam','2004-05-19','0836425095'),(4,15,'38204014522','Le Ba','Hoang','male','Viet Nam','2004-05-19','0836425090');
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-26 14:36:50
