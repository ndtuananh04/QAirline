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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'bahoang19052004@gmail.com','scrypt:32768:8:1$13OqDH6OztJoHsaK$481500f5be728620745b68b8424d66ce7f6113dc6333285f83677505c3e9acf956706925bc672f74d6d3d1ce1481a2271216c5f1007dfa1006bf38516bf0f0c4','customer'),(2,'admin@gmail.com','scrypt:32768:8:1$DdpECTqtw6LdYJNH$f237cef57a2f06776f68ceca80e02b88e12fc5980752d0292b9bf2fe4e3b8fe231632b902a87d31d7841f235692cc86293b3a8b0e1a4334eab79bc3d8698dfd6','admin'),(7,'admin1gmail.com','scrypt:32768:8:1$m4jTpGxxast2vSjY$ac57c1f7a1b8f32e3d517bdb2b1e1d75e24b72de6bf0656b2fd5027b1aee8e3466b2e5ad38d80eaf75eef12997d9fda7b770ba592f071fcb7344547978053186','customer'),(9,'admin2@gmail.com','scrypt:32768:8:1$HKfEa4c4EH5BQFdf$d20aeac01a9a1c7483a2c1fdd9b844f42f6b31ca45f34d7b3d752816f98c6945de4b2facc2ada5354c6bafc0194b11c09b180ac0137f99dd87fa07352b3817ad','admin'),(10,'admin3@gmail.com','scrypt:32768:8:1$nzpKNWZGFNRv2QOY$f1a05c39e4d2eec612cf710da171e8ebb1c684c131b95f80417aa8fdb5a30e5e966b6b8e7b515ab4543d3eb6686845a4b1a44a6470f6fa4fd21e4b36329cbb5a','admin'),(12,'admin4@gmail.com','scrypt:32768:8:1$bkxlwWb6Wob3RwMz$2da601e1089f36ec4bd2031a2ee0ff88e5199bb57efcb0b59e06b94c11daeabaeb9fa3cd91641ce9cbd3ef38b49a9aa8d8ba9ced97e9bc02d343b6d3095afcd3','admin'),(14,'bahoang@gmail.com','scrypt:32768:8:1$eJ1FlJRtp3eMTiDn$efc31941bcd797aca57a02e08c2b4e2b392154cfb22c77f3c84e66cbb7c3a7cb9808b46a9d9f6fd813f566bd5530c3b8501370774e22eb3545c6073b5612c932','customer'),(15,'admin6@gmail.com','scrypt:32768:8:1$PEYjg8I3N8cUb9Is$bdf930083f5201b7279a505bd2a26be531df1ed1e581ff15ca6745a18d857ee1d39b835d05f70c69f93ef3366cd598030030314b3f839514b22943bdb37f6551','customer'),(16,'admin1@gmail.com','scrypt:32768:8:1$hseCJSXLmJrtl6fR$8c7543a67f8ffc654c39aee870dbfa2c7491aa8af88147381426e35d2aa37b55d15e67a99c1412f2e38da60cb12a4f35b752ea026b93bbcc0ff9b3b6c403eb0c','customer'),(17,'user1@gmail.com','scrypt:32768:8:1$DkdSE7SqX5TOVBSL$1f211e0754de94ae7cf34959b523f5bbcc78ec0d0180788a0987a53eba4894887fc26b86348319d7481f66960798a3990caa493d13f2eef0b3d3c702e4293a63','customer');
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
  `name_airplane` varchar(10) NOT NULL,
  `capacity` int NOT NULL,
  `is_locked` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`airplane_id`),
  UNIQUE KEY `airline_number_UNIQUE` (`name_airplane`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airplanes`
--

LOCK TABLES `airplanes` WRITE;
/*!40000 ALTER TABLE `airplanes` DISABLE KEYS */;
INSERT INTO `airplanes` VALUES (1,'195QAL',18,0),(2,'204QAL',18,0),(3,'205QAL',18,0),(4,'123QAL',18,0),(5,'206QAL',18,0),(6,'207QAL',18,0);
/*!40000 ALTER TABLE `airplanes` ENABLE KEYS */;
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
  `reason` text NOT NULL,
  `cancellation_date` date NOT NULL,
  PRIMARY KEY (`cancellation_id`),
  KEY `fk_cancellations_ticket_id_idx` (`ticket_id`),
  CONSTRAINT `fk_cancellation_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellations`
--

LOCK TABLES `cancellations` WRITE;
/*!40000 ALTER TABLE `cancellations` DISABLE KEYS */;
INSERT INTO `cancellations` VALUES (1,60,'Tôi có việc bận','2024-12-10'),(2,60,'Tôi có việc bận','2024-12-10'),(3,58,'ddd','2024-12-12'),(4,64,'dddd','2024-12-12'),(5,61,'sssss','2024-12-12'),(6,59,'hello','2024-12-19'),(7,58,'Tôi không tam gia được','2024-12-19'),(8,61,'Tôi ','2024-12-20'),(9,71,'Tôi bận','2024-12-20'),(10,73,'Tôi muôn hủy vé\n','2024-12-21');
/*!40000 ALTER TABLE `cancellations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `flight_id` int NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(10) NOT NULL,
  `departure` varchar(60) NOT NULL,
  `code_departure` varchar(10) NOT NULL,
  `arrival` varchar(60) NOT NULL,
  `code_arrival` varchar(10) NOT NULL,
  `departure_time` date NOT NULL,
  `departure_hour_time` time NOT NULL,
  `arrival_hour_time` time NOT NULL,
  `boarding_time` time NOT NULL,
  `terminal` int NOT NULL,
  `status` enum('SCHEDULED','DELAYED','CANCELLED','FINISHED') NOT NULL,
  `airplane_id` int NOT NULL,
  `is_locked` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`flight_id`),
  KEY `fk_flights_airplanes_id_idx` (`airplane_id`),
  CONSTRAINT `fk_flights_airplanes_id` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights`
--

LOCK TABLES `flights` WRITE;
/*!40000 ALTER TABLE `flights` DISABLE KEYS */;
INSERT INTO `flights` VALUES (1,'195204QAL','Hà Nội','HAN','Tp. Hồ Chí Minh','SGN','2024-12-29','21:00:00','23:00:00','20:30:00',1,'FINISHED',1,0),(2,'123456QAL','Tp. Hồ Chí Minh','SGN','Hà Nội','HAN','2024-12-30','09:00:00','11:10:00','08:30:00',2,'SCHEDULED',1,0),(11,'195244QAL','Thanh Hóa','THD','Tp. Hồ Chí Minh','SGN','2025-01-15','13:00:00','15:20:00','12:30:00',1,'SCHEDULED',1,0),(12,'195208QAL','Thanh Hóa','THD','Tp. Hồ Chí Minh','SGN','2025-01-13','15:00:00','17:10:00','14:30:00',1,'SCHEDULED',1,0),(13,'195203QAL','Thanh Hóa','THD','Tp. Hồ Chí Minh','SGN','2024-12-18','15:00:00','17:10:00','14:30:00',1,'FINISHED',1,0),(14,'195207QAL','Thanh Hóa','THD','Tp. Hồ Chí Minh','SGN','2024-12-29','21:00:00','23:00:00','20:30:00',1,'DELAYED',1,0),(15,'195321QAL','Thanh Hóa','THD','Tp. Hồ Chí Minh','SGN','2025-01-30','06:00:00','08:20:00','05:30:00',1,'DELAYED',1,0),(16,'123321QAL','Tp. Hồ Chí Minh','SGN','Thanh Hóa','THD','2025-01-17','08:00:00','10:10:00','07:30:00',1,'SCHEDULED',2,0),(17,'123222QAL','Tp. Hồ Chí Minh','SGN','Hà Nội','HAN','2025-01-18','14:00:00','16:00:00','13:30:00',1,'CANCELLED',1,0),(18,'212212QAL','Thanh Hóa','THD','Nha Trang','CXR','2025-01-10','08:35:00','10:00:00','08:05:00',1,'SCHEDULED',1,0),(19,'195200QAL','Thanh Hóa','THD','Huế','HUI','2025-01-09','09:15:00','11:00:00','08:45:00',1,'SCHEDULED',1,0);
/*!40000 ALTER TABLE `flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(1024) NOT NULL,
  `block_1` text NOT NULL,
  `block_2` text,
  `block_3` text,
  `block_4` text,
  `block_5` text,
  `post_date` date NOT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,'Cập nhật chính sách hành lý ký gửi','Airline xin thông báo về việc cập nhật chính sách hành lý ký gửi, áp dụng từ ngày 01/01/2025. Quy định mới nhằm tối ưu hóa quy trình phục vụ và nâng cao trải nghiệm của quý khách khi sử dụng dịch vụ.','Theo chính sách mới, mức phí hành lý ký gửi sẽ được điều chỉnh linh hoạt tùy thuộc vào tuyến bay nội địa hoặc quốc tế, cũng như trọng lượng hành lý. Điều này giúp đảm bảo công bằng và thuận tiện cho tất cả hành khách.','Các loại hành lý đặc biệt, như thiết bị thể thao hoặc nhạc cụ, sẽ có chính sách cụ thể. Vui lòng kiểm tra chi tiết trước khi khởi hành để tránh phát sinh chi phí không mong muốn.','Để biết thêm thông tin, quý khách có thể truy cập mục \"Chính sách hành lý\" trên website chính thức của QAirline hoặc liên hệ tổng đài hỗ trợ 24/7.','QAirline cam kết mang lại dịch vụ vận chuyển hành lý an toàn, tiện lợi, và nhanh chóng cho mọi hành trình của quý khách.','2024-12-21'),(3,'Khuyến mãi Tết Nguyên Đán - Giảm đến 50%','Nhằm tri ân quý khách hàng nhân dịp Tết Nguyên Đán 2025, QAirline mang đến chương trình khuyến mãi đặc biệt với mức giảm giá lên đến 50% cho tất cả các tuyến bay nội địa và quốc tế.','Chương trình áp dụng cho các chuyến bay có ngày khởi hành từ 20/01/2025 đến 10/02/2025. Vé ưu đãi có giới hạn, vì vậy quý khách nên đặt vé sớm để đảm bảo chỗ ngồi phù hợp.','Ngoài ưu đãi giá vé, QAirline còn có chương trình tặng thêm hành lý ký gửi miễn phí cho một số tuyến bay được chọn. Đừng bỏ lỡ cơ hội này để tiết kiệm chi phí hành trình.','','','2024-12-21'),(4,'QAirline đạt giải thưởng “Hãng hàng không xuất sắc năm 2024”','QAirline tự hào thông báo đã được trao giải thưởng danh giá \"Hãng hàng không xuất sắc năm 2024\" tại lễ trao giải Hàng không Quốc tế, tổ chức tại Paris.','Giải thưởng này ghi nhận nỗ lực không ngừng của chúng tôi trong việc mang đến những trải nghiệm bay an toàn, tiện lợi và thoải mái nhất cho quý khách hàng.','Trong năm qua, QAirline đã đầu tư nâng cấp đội bay hiện đại, cải thiện chất lượng dịch vụ trên không và mặt đất, cũng như mở rộng các tuyến bay đến những điểm đến hấp dẫn.','Chúng tôi xin chân thành cảm ơn quý khách hàng đã luôn tin tưởng và đồng hành cùng QAirline. Đây chính là động lực để chúng tôi tiếp tục phấn đấu trong tương lai.','Với cam kết \"Chất lượng đi đầu, khách hàng là trọng tâm\", QAirline hứa hẹn sẽ mang đến những trải nghiệm ngày càng tốt hơn cho mọi chuyến đi của quý khách.','2024-12-21'),(5,'Ngày 5/10, đường bay thẳng đầu tiên và duy nhất giữa Việt Nam và thủ phủ bang Bayern, Munich','Ngày 5/10, đường bay thẳng đầu tiên và duy nhất giữa Việt Nam và thủ phủ bang Bayern, Munich, đã được QAirlines chính thức khai trương tại sân bay Nội Bài và sân bay quốc tế Munich.','Chuyến bay đầu tiên mang số hiệu VN35, có hành trình từ Hà Nội đến Munich, khởi hành 00:05 ngày 5/10. Vietnam Airlines trang trí đặc biệt các quầy phục vụ từ Nội Bài, tặng hoa chào đón tổ bay và tặng quà lưu niệm cho hành khách.','Ở chiều ngược lại, hãng long trọng tổ chức lễ cắt băng khai trương đường bay tại sân bay quốc tế Munich trong ngày 5/10. Tham dự buổi lễ có ông Nguyễn Hoàng Anh - Chủ tịch UBQLVNN tại Doanh nghiệp; ông Lưu Xuân Đồng - Tổng lãnh sự Việt Nam tại Frankfurt, Đức; ông Jost Lammers - Tổng Giám đốc sân bay Munich cùng đông đảo các đối tác, công ty du lịch và bạn hàng lớn của Vietnam Airlines.','Tại sự kiện, các đại biểu đã thực hiện nghi thức khai trương đường bay. Các lễ tân trong trang phục Bavaria truyền thống tặng quà cho hành khách và tặng hoa cho tổ bay. Chuyến bay được chào đón đặc biệt bằng nghi thức phun vòi rồng trước khi cất cánh vào lúc 13h35 (giờ địa phương).','Theo chia sẻ của ông Lê Đức Cảnh, Phó Tổng giám đốc Vietnam Airlines, việc mở đường bay thẳng đến Munich là cột mốc đặc biệt quan trọng trong hành trình mở rộng mạng đường bay quốc tế của hãng. Hai mươi năm trước, Vietnam Airlines bắt đầu khai thác đường bay đầu tiên giữa Việt Nam và Đức. Trong suốt 2 thập kỷ, Vietnam Airlines đã phục vụ hơn 3,1 triệu lượt hành khách với gần 14 nghìn chuyến bay. Việc khai trương đường bay thẳng từ Hà Nội và TP. Hồ Chí Minh đến Munich không chỉ mở ra những cơ hội mới cho du lịch và thương mại, mà còn góp phần thúc đẩy quan hệ hợp tác toàn diện giữa Việt Nam và Đức, đưa hai đất nước đến gần nhau hơn.','2024-12-10'),(11,'Lưu ý khi đặt vé trong mùa cao điểm','QAirline xin gửi đến quý khách một số lưu ý quan trọng khi đặt vé trong mùa cao điểm cuối năm, nhằm đảm bảo hành trình diễn ra thuận lợi và suôn sẻ.','Mùa cao điểm là thời gian lượng khách đặt vé tăng đột biến, vì vậy quý khách nên đặt vé sớm để tránh tình trạng hết chỗ. Hãy tham khảo lịch bay và giá vé trên website chính thức của QAirline.','Đảm bảo kiểm tra đầy đủ thông tin cá nhân, hành trình và các yêu cầu đặc biệt (nếu có) trước khi xác nhận đặt vé. Điều này giúp giảm thiểu rủi ro và phiền phức trong quá trình làm thủ tục.','Trong trường hợp cần thay đổi hoặc hủy vé, vui lòng liên hệ với tổng đài QAirline càng sớm càng tốt để được hỗ trợ và tránh mất phí không đáng có.','Chúng tôi luôn nỗ lực mang đến sự hài lòng và những trải nghiệm đáng nhớ cho mọi hành trình của quý khách. Chúc quý khách có chuyến đi an toàn và thú vị!','2024-12-21');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions`
--

DROP TABLE IF EXISTS `promotions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions` (
  `promotion_id` int NOT NULL AUTO_INCREMENT,
  `code_promotion` varchar(10) NOT NULL,
  `percent` int NOT NULL,
  PRIMARY KEY (`promotion_id`),
  UNIQUE KEY `code_promotion_UNIQUE` (`code_promotion`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions`
--

LOCK TABLES `promotions` WRITE;
/*!40000 ALTER TABLE `promotions` DISABLE KEYS */;
INSERT INTO `promotions` VALUES (1,'QALKM195',20),(3,'QALKM209',20);
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
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revoked_tokens`
--

LOCK TABLES `revoked_tokens` WRITE;
/*!40000 ALTER TABLE `revoked_tokens` DISABLE KEYS */;
INSERT INTO `revoked_tokens` VALUES (1,'fd2bd3d7-dca8-43d0-a3d5-a4879671b90a'),(2,'10ddf932-f284-4579-ae65-345a1bbec9ec'),(3,'a1358505-7865-4bee-8313-55de080a8574'),(4,'01ac813d-e0cc-438d-894d-e75948ef2af5'),(5,'6ece930f-a64c-426d-9aa5-4ea3287959de'),(6,'2c9e985c-e610-4cc8-b5d9-3179116ec545'),(7,'9ce50232-3f84-48b8-88f3-a639fe5fb765'),(8,'b6de9c9e-cf6b-4011-bb11-772e17f7a3fa'),(9,'c9d24672-f9e4-4237-adf5-976800b7812b'),(10,'176f7dbf-f653-4851-abad-d3441d4c54ee'),(11,'5241a743-4597-410a-bcf1-ac0dbf8fbfe6'),(12,'973a3577-c4cd-4c55-9a6e-6047199979de'),(13,'b75caa07-d48c-4e4a-9b89-0731f6cb9df1'),(14,'f9a1f1d7-7d65-499a-b5a6-1b9198d9540e'),(15,'28d7b631-eef0-4324-919c-425e8cae8e3b'),(16,'288fc5cb-4025-48b7-bf2e-5f3e14cbf98a'),(17,'0f323696-876a-4cfe-bd34-4ba8aeb5273f'),(18,'78d820f0-7c19-4823-b8e6-5db6060017b0'),(19,'7fd2233b-41d8-4101-bd54-fbfb660cab37'),(20,'35eca9cd-d0ef-48b3-8c22-1cc6800f33c2'),(21,'26932f44-93f1-4fb3-9119-4de5b6fa2c92'),(22,'6d098fdf-80dd-4520-aa8a-11757eca46ae'),(23,'c80d5f1c-dbb6-4b39-ab34-0ccfda46fc83'),(24,'3f95217f-b605-4a2c-9ce7-989bb131a0c8'),(25,'ca71fe4b-2868-42ac-8532-124ca82dc2d4'),(26,'77921fc4-2d6e-4620-b3a9-bb92e1e3094a'),(27,'223c3a5b-01af-4405-9e57-e93c455c6948'),(28,'6328a6a6-5ccc-44e0-9d0e-db9cd3948aed'),(29,'003481eb-e660-45cc-bf67-049763833bb9'),(30,'b46c0a4f-1b80-4944-aac1-15f834abd02c'),(31,'b306c9e1-a60b-493d-9312-4e0b42c286aa'),(32,'bc4c5072-a0a7-4b61-9be3-8158ba6d5813'),(33,'b4e76ad5-0ad0-4d19-9000-7059ffcf288c'),(34,'e4c0b4a1-92dc-43d0-aaa1-638dcd0fb718'),(35,'156c3763-6128-4a5e-811d-eff28eabefeb'),(36,'99c01249-975b-4604-9d03-dd283818aba3'),(37,'f035253a-24b0-4a1d-ab20-3368f929282e'),(38,'1bca3199-f605-4eda-84b1-d87655e20ef9'),(39,'5ce99537-9f73-4c83-b0ff-c81ce60a208c'),(40,'8a8f27d8-e96a-4802-97cc-0c46815300b0'),(41,'832fb963-a59a-4bb9-8ea3-e4bdfc95d612'),(42,'3ea756e3-8c3b-463c-8167-463252f998bf'),(43,'dd804463-c959-43e7-8110-0af8d5ea37b4'),(44,'684deab7-1304-4024-be41-fc9f67f8bd43'),(45,'8e9214a3-cbc1-40db-ad9d-7b2dfc64024e'),(46,'5c986056-fbf7-4e3c-a51e-9cb40e26a618'),(47,'5e77f3a6-e30b-41fd-9da5-e6d08f99a82a'),(48,'902f1d63-079b-421a-a7bd-4e6f45190e10'),(49,'bd3d583e-eaf7-4800-8ab8-83e3fcbb09dc'),(50,'74762cfd-aa64-4a98-8091-9f1ff2da5acd'),(51,'751d604c-daed-4662-b04e-d5bd9a9e46fa'),(52,'add0e508-5a1a-45d4-8f7b-185e8431c2ef'),(53,'3100cb58-56a2-4d1f-9f50-a690ff4975a0'),(54,'8a52b682-3bcc-4761-b148-b40c47b1c26f'),(55,'cc1b988b-385b-496a-b1ef-d222e96effe0'),(56,'9c087bfa-b5b8-4bbd-9e52-5d4f44a1ae44'),(57,'1e8dd58f-0440-4462-a539-c6c481db32ca'),(58,'cb2c42b5-a5c8-401a-bea4-2062743d81c9'),(59,'8600c349-8396-4d29-ae56-2425d81744b2'),(60,'b9bed28d-7eb7-448c-a8a4-97e1a69b471a'),(61,'75712084-c33c-459a-9b8a-2faf34c00bcd'),(62,'70b32f0c-397f-4cd2-9937-470475fcbd90'),(63,'e7a26b2c-6a0b-474c-9990-017a19c93919'),(64,'2ee38c45-2016-4c84-8c32-c6997d139a98'),(65,'9d39f884-ea08-4676-9284-1c9aa290ce26'),(66,'5bf1d76b-58ca-4db4-82b4-308c834afeb1'),(67,'caf37b5b-c696-41cd-be6b-a7f918c66f5a'),(68,'14b91f33-9b72-4873-9da2-74994b0f590b'),(69,'525e233e-821b-4708-9d2e-253e6fbfdf4c'),(70,'42c3f702-6e42-4237-8fbf-9eae73c077f8'),(71,'7eeeb633-d389-4e96-a33e-6c7502153705'),(72,'0ff47ffd-03d3-482d-9328-9c0895987f06'),(73,'73cdcc44-e603-4db3-aa41-b6dafc43d012'),(74,'fe1f444a-7940-49dd-b5f1-10a7b62d4796'),(75,'2de75791-80f5-43d0-9f37-e31ba98d9817'),(76,'72bf41ac-4036-442b-a5b9-369e0778dc23'),(77,'392f5672-ebcd-44ca-b789-e4391e4fdb5c'),(78,'2e4f2793-2268-4c82-8ca5-94a293db3903'),(79,'1f40d291-6a6c-419e-9480-9df25273ba02'),(80,'c2b06187-a41c-469d-b51a-7fbe46859d59'),(81,'7411d2a9-cbdb-4786-b3d8-bbd89d3e535a'),(82,'b1ba8dc6-cd42-4268-a81f-33faccef2e66'),(83,'af866df1-1046-464f-8599-e549d564d82b'),(84,'3339a331-dbcc-4641-ae9e-fb07fa396395');
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
  `seat_number` varchar(10) NOT NULL,
  `seat_class` enum('ECONOMY','BUSINESS','SKYBOSS') NOT NULL,
  `price` decimal(10,0) NOT NULL,
  PRIMARY KEY (`seat_id`),
  KEY `fk_seats_airplanes_id_idx` (`airplane_id`),
  CONSTRAINT `fk_seats_airplanes_id` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES (1,1,'1A','BUSINESS',2000000),(2,1,'1B','BUSINESS',2000000),(3,1,'1C','BUSINESS',2000000),(4,1,'2A','SKYBOSS',1300000),(5,1,'2B','SKYBOSS',1300000),(6,1,'2C','SKYBOSS',1300000),(7,1,'3A','ECONOMY',800000),(8,1,'3B','ECONOMY',800000),(9,1,'3C','ECONOMY',800000),(13,1,'3D','ECONOMY',800000),(14,1,'3E','ECONOMY',800000),(15,1,'3F','ECONOMY',800000),(16,1,'2D','SKYBOSS',1300000),(17,1,'2E','SKYBOSS',1300000),(18,1,'2F','SKYBOSS',1300000),(19,1,'1D','BUSINESS',2000000),(20,1,'1E','BUSINESS',2000000),(21,1,'1F','BUSINESS',2000000);
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_user`
--

DROP TABLE IF EXISTS `ticket_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_user` (
  `ticket_user_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `identification` varchar(20) NOT NULL,
  `family_name` varchar(60) NOT NULL,
  `given_name` varchar(45) NOT NULL,
  `gender` enum('male','female') NOT NULL,
  `nationality` varchar(60) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(20) NOT NULL,
  `email` varchar(60) NOT NULL,
  PRIMARY KEY (`ticket_user_id`),
  KEY `fk_to_tickets_idx` (`ticket_id`),
  CONSTRAINT `fk_to_tickets` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`ticket_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_user`
--

LOCK TABLES `ticket_user` WRITE;
/*!40000 ALTER TABLE `ticket_user` DISABLE KEYS */;
INSERT INTO `ticket_user` VALUES (1,58,'038204014543','LE','BA HOANG ','male','VIET NAM','2004-05-19','0836425093','hoang123@gmail.com'),(2,59,'038204014543','LE','BA HOANG ','male','VIET NAM','2004-05-19','0836425093','hoang123@gmail.com'),(3,60,'012345654322','NGUYEN','TUAN ANH','male','VIET NAM','2024-12-04','09999999555','bahoang19052004@gmail.com'),(4,61,'012345654322','NGUYEN','TUAN ANH','male','VIET NAM','2024-12-04','09999999555','bahoang19052004@gmail.com'),(5,62,'012345654321','LE','BA HOANG ','female','VIET NAM','2024-12-22','09999999942','bahoang19052004@gmail.com'),(6,63,'012345654321','LE','BA HOANG ','female','VIET NAM','2024-12-22','09999999942','bahoang19052004@gmail.com'),(7,64,'012345654322','LE','BA PHI','male','VIET NAM','2024-12-10','0836425093','nghiamata777@gmail.com'),(8,65,'012345654322','LE','BA PHI','male','VIET NAM','2024-12-10','0836425093','nghiamata777@gmail.com'),(9,66,'012345654321','LE THI','MAI LINH','female','VIET NAM','2004-02-19','0836425093','admin@gmail.com'),(10,67,'012345654321','LE THI','MAI LINH','female','VIET NAM','2004-02-19','0836425093','admin@gmail.com'),(11,68,'098214514528','LE','LINH','male','VIET NAM','2004-03-19','0987654322','bahoang@gmail.com'),(12,69,'012345654321','LE','MAI LINH','female','VIET NAM','2024-12-05','09999999999','bahoang19052004@gmail.com'),(13,70,'012345654321','LE','MAI LINH','female','VIET NAM','2024-12-05','09999999999','bahoang19052004@gmail.com'),(14,71,'012345654320','LE','BA HOANG ','male','VIET NAM','2024-12-06','0987654322','bahoang19052004@gmail.com'),(15,72,'012345654321','A','A','male','VIET NAM','2024-12-20','0123456780','user1@gmail.com'),(16,73,'012345654321','B','B','male','VIET NAM','2024-12-12','0123456780','user1@gmail.com'),(17,74,'012345654321','C','C','male','VIET NAM','2024-12-13','0123456780','user1@gmail.com');
/*!40000 ALTER TABLE `ticket_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `flight_id` int NOT NULL,
  `ticket_number` varchar(20) NOT NULL,
  `seat_class` enum('business','skyboss','economy') NOT NULL,
  `seat_number` varchar(10) DEFAULT NULL,
  `booking_time` date NOT NULL,
  `status` enum('scheduled','cancelled') NOT NULL,
  PRIMARY KEY (`ticket_id`),
  UNIQUE KEY `ticket_number_UNIQUE` (`ticket_number`),
  KEY `fk_ticket_flight_id_idx` (`flight_id`),
  KEY `fk_ticket_user_id` (`account_id`),
  CONSTRAINT `fk_ticket_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ticket_user_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (58,1,1,'4QUKMJQ5','business','1B','2024-12-10','cancelled'),(59,1,2,'9CDKE7U9','skyboss','2B','2024-12-10','cancelled'),(60,1,1,'V4SHPU56','business','1B','2024-12-10','scheduled'),(61,1,2,'KQXJ84OS','skyboss','3E','2024-12-10','cancelled'),(62,1,1,'NDVSHYLP','business',NULL,'2024-12-11','scheduled'),(63,1,2,'1TMXOS3V','business',NULL,'2024-12-11','scheduled'),(64,1,1,'4IWLO3SH','business',NULL,'2024-12-12','scheduled'),(65,1,2,'BJGGGANV','skyboss',NULL,'2024-12-12','scheduled'),(66,1,1,'8ZTR2T2B','business',NULL,'2024-12-19','scheduled'),(67,1,2,'POYTA1TL','business',NULL,'2024-12-19','scheduled'),(68,14,1,'IFVCY1B0','business','1A','2024-12-19','scheduled'),(69,14,1,'SB6BURYH','economy',NULL,'2024-12-19','scheduled'),(70,14,2,'CNU8CEP3','skyboss',NULL,'2024-12-19','scheduled'),(71,16,1,'A3AHC1ZG','business','3A','2024-12-20','cancelled'),(72,17,18,'KWTGHS3X','business','1A','2024-12-21','scheduled'),(73,17,18,'LEDNX93A','business',NULL,'2024-12-21','cancelled'),(74,17,18,'4ODY2I2S','business',NULL,'2024-12-21','scheduled');
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
  `phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `identification_UNIQUE` (`identification`),
  KEY `fk_user_information_account_id` (`account_id`),
  CONSTRAINT `fk_user_information_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES (1,1,'038204014528','LE','BA HOANG','male','VIET NAM','2004-05-19','0836425093'),(2,2,'999999999999','LE','BA HOANG','male','VIET NAM','2024-12-26','9999999999'),(4,14,'098214514528','LE ','LINH','male','VIET NAM','2004-03-19','0987654542'),(5,16,'038204012345','LE','BA HOANGGG','male','VIET NAM','2025-01-04','0999889833'),(6,17,'012345654226','LE','BA HOANG','male','VIET NAM','2024-12-19','0123456780');
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

-- Dump completed on 2024-12-21 16:14:15
