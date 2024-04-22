-- MariaDB dump 10.19-11.3.2-MariaDB, for osx10.18 (arm64)
--
-- Host: localhost    Database: milestone3
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Alias`
--

DROP TABLE IF EXISTS `Alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Alias` (
  `Alias_ID` int NOT NULL,
  `Criminal_ID` int DEFAULT NULL,
  `Alias` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Alias_ID`),
  KEY `Criminal_ID` (`Criminal_ID`),
  CONSTRAINT `alias_ibfk_1` FOREIGN KEY (`Criminal_ID`) REFERENCES `Criminals` (`Criminal_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Alias`
--

LOCK TABLES `Alias` WRITE;
/*!40000 ALTER TABLE `Alias` DISABLE KEYS */;
INSERT INTO `Alias` VALUES
(1,1,'A Crimmy'),
(2,2,'B Bully'),
(3,3,'C Cutter'),
(4,4,'D Duff'),
(5,5,'E Electric'),
(6,6,'F Flapper'),
(7,7,'G Gutter'),
(8,8,'H Heater'),
(9,9,'I Icker'),
(10,10,'J Jolt');
/*!40000 ALTER TABLE `Alias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Appeals`
--

DROP TABLE IF EXISTS `Appeals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Appeals` (
  `Appeal_ID` int NOT NULL,
  `Crime_ID` int DEFAULT NULL,
  `Filing_date` date DEFAULT NULL,
  `Hearing_date` date DEFAULT NULL,
  `Status` enum('P','A','D') NOT NULL,
  PRIMARY KEY (`Appeal_ID`),
  KEY `Crime_ID` (`Crime_ID`),
  CONSTRAINT `appeals_ibfk_1` FOREIGN KEY (`Crime_ID`) REFERENCES `Crimes` (`Crime_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Appeals`
--

LOCK TABLES `Appeals` WRITE;
/*!40000 ALTER TABLE `Appeals` DISABLE KEYS */;
INSERT INTO `Appeals` VALUES
(1,1,'2000-01-10','2000-01-15','P'),
(2,2,'2002-01-10','2002-01-15','A'),
(3,3,'2003-01-10','2003-01-15','D'),
(4,4,'2004-01-10','2004-01-15','P'),
(5,5,'2005-01-10','2005-01-15','A'),
(6,6,'2006-01-10','2006-01-15','P'),
(7,7,'2007-01-10','2007-01-15','A'),
(8,8,'2008-01-10','2008-01-15','D'),
(9,9,'2009-01-10','2009-01-15','P'),
(10,10,'2010-01-10','2010-01-15','A');
/*!40000 ALTER TABLE `Appeals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Crime_charges`
--

DROP TABLE IF EXISTS `Crime_charges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Crime_charges` (
  `Charge_ID` int NOT NULL,
  `Crime_ID` int DEFAULT NULL,
  `Crime_code` int DEFAULT NULL,
  `Charge_status` enum('PD','GL','NG') DEFAULT NULL,
  `Fine_amount` int DEFAULT NULL,
  `Court_fee` int DEFAULT NULL,
  `Amount_paid` int DEFAULT NULL,
  `Pay_due_date` date DEFAULT NULL,
  PRIMARY KEY (`Charge_ID`),
  KEY `Crime_ID` (`Crime_ID`),
  KEY `Crime_code` (`Crime_code`),
  CONSTRAINT `crime_charges_ibfk_1` FOREIGN KEY (`Crime_ID`) REFERENCES `Crimes` (`Crime_ID`),
  CONSTRAINT `crime_charges_ibfk_2` FOREIGN KEY (`Crime_code`) REFERENCES `Crime_codes` (`Crime_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Crime_charges`
--

LOCK TABLES `Crime_charges` WRITE;
/*!40000 ALTER TABLE `Crime_charges` DISABLE KEYS */;
INSERT INTO `Crime_charges` VALUES
(1,1,1,'PD',10,20,15,'2005-01-01'),
(2,2,2,'GL',5,2,3,'2005-01-02'),
(3,3,3,'NG',20,20,17,'2008-01-03'),
(4,4,4,'PD',25,20,20,'2009-01-04'),
(5,5,5,'GL',15,20,22,'2010-01-05'),
(6,6,6,'NG',35,20,30,'2011-01-06'),
(7,7,7,'PD',50,20,40,'2012-01-07'),
(8,8,8,'GL',25,20,35,'2013-01-08'),
(9,9,9,'NG',80,20,70,'2014-01-09'),
(10,10,1,'PD',55,20,60,'2015-01-10');
/*!40000 ALTER TABLE `Crime_charges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Crime_codes`
--

DROP TABLE IF EXISTS `Crime_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Crime_codes` (
  `Crime_code` int NOT NULL,
  `Code_description` varchar(30) NOT NULL,
  PRIMARY KEY (`Crime_code`),
  UNIQUE KEY `Code_description` (`Code_description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Crime_codes`
--

LOCK TABLES `Crime_codes` WRITE;
/*!40000 ALTER TABLE `Crime_codes` DISABLE KEYS */;
INSERT INTO `Crime_codes` VALUES
(10,'Currency'),
(9,'Domestic'),
(6,'Drugs'),
(4,'Fraud'),
(5,'Identity'),
(8,'Murder'),
(7,'Smuggling'),
(3,'Theft'),
(2,'Vandalism'),
(1,'Violence');
/*!40000 ALTER TABLE `Crime_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Crime_officers`
--

DROP TABLE IF EXISTS `Crime_officers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Crime_officers` (
  `Crime_ID` int NOT NULL,
  `Officer_ID` int NOT NULL,
  PRIMARY KEY (`Crime_ID`,`Officer_ID`),
  KEY `Officer_ID` (`Officer_ID`),
  CONSTRAINT `crime_officers_ibfk_1` FOREIGN KEY (`Crime_ID`) REFERENCES `Crimes` (`Crime_ID`),
  CONSTRAINT `crime_officers_ibfk_2` FOREIGN KEY (`Officer_ID`) REFERENCES `Officers` (`Officer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Crime_officers`
--

LOCK TABLES `Crime_officers` WRITE;
/*!40000 ALTER TABLE `Crime_officers` DISABLE KEYS */;
INSERT INTO `Crime_officers` VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);
/*!40000 ALTER TABLE `Crime_officers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Crimes`
--

DROP TABLE IF EXISTS `Crimes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Crimes` (
  `Crime_ID` int NOT NULL,
  `Criminal_ID` int DEFAULT NULL,
  `Appeal_cut_date` date DEFAULT NULL,
  `Classification` enum('U','F','M','O') NOT NULL,
  `Date_charged` date DEFAULT NULL,
  `Hearing_date` date DEFAULT NULL,
  `Status` enum('CL','CA','IA') NOT NULL,
  PRIMARY KEY (`Crime_ID`),
  CONSTRAINT `crimes_chk_1` CHECK ((`Hearing_Date` > `Date_charged`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Crimes`
--

LOCK TABLES `Crimes` WRITE;
/*!40000 ALTER TABLE `Crimes` DISABLE KEYS */;
INSERT INTO `Crimes` VALUES
(1,1,'2000-02-15','U','2000-01-01','2000-02-01','CL'),
(2,2,'2002-02-15','F','2001-01-01','2002-02-01','CA'),
(3,3,'2003-02-15','M','2002-01-01','2003-02-01','IA'),
(4,4,'2004-02-15','O','2003-01-01','2004-02-01','CL'),
(5,5,'2005-02-15','U','2004-01-01','2005-02-01','CA'),
(6,6,'2006-02-15','F','2005-01-01','2006-02-01','IA'),
(7,7,'2007-02-15','M','2006-01-01','2007-02-01','CL'),
(8,8,'2008-02-15','O','2007-01-01','2008-02-01','CA'),
(9,9,'2009-02-15','U','2008-01-01','2009-02-01','IA'),
(10,10,'2010-02-15','F','2009-01-01','2010-02-01','CL');
/*!40000 ALTER TABLE `Crimes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Criminals`
--

DROP TABLE IF EXISTS `Criminals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Criminals` (
  `Criminal_ID` int NOT NULL,
  `Last` varchar(15) DEFAULT NULL,
  `First` varchar(10) DEFAULT NULL,
  `Street` varchar(30) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `State` char(2) DEFAULT NULL,
  `Zip` char(5) DEFAULT NULL,
  `Phone` char(10) DEFAULT NULL,
  `V_status` enum('N','Y') DEFAULT NULL,
  `P_status` enum('N','Y') DEFAULT NULL,
  PRIMARY KEY (`Criminal_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Criminals`
--

LOCK TABLES `Criminals` WRITE;
/*!40000 ALTER TABLE `Criminals` DISABLE KEYS */;
INSERT INTO `Criminals` VALUES
(1,'Alba','Andy','Apple Street','Apple City','AS','1234A','0123456789','N','N'),
(2,'Ball','Bryan','Banana Street','Banana City','BS','1234B','120394890','N','N'),
(3,'Cat','Cathy','Citrus Street','Citrus City','CS','1234C','128340189','N','N'),
(4,'Dot','Daniel','Date Street','Date City','DS','1234D','123478010','N','Y'),
(5,'Elephant','Ellie','Eggplant Street','Eggplant City','ES','1234E','098765938','Y','Y'),
(6,'Furt','Frank','Fig Street','Fig City','FS','1234F','876456092','N','N'),
(7,'Gurt','Greg','Ginger Street','Ginger City','GS','1234G','285730283','Y','N'),
(8,'Hurt','Helen','Honeydew Street','Honeydew City','HS','1234H','768463879','Y','N'),
(9,'Iyball','Irene','Icecream Street','Icecream City','IS','1234I','768475678','N','Y'),
(10,'Jill','Jack','Jackfruit Street','Jackfruit City','JS','1234J','647586930','Y','Y');
/*!40000 ALTER TABLE `Criminals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Logs`
--

DROP TABLE IF EXISTS `Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Logs` (
  `query_run` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Logs`
--

LOCK TABLES `Logs` WRITE;
/*!40000 ALTER TABLE `Logs` DISABLE KEYS */;
INSERT INTO `Logs` VALUES
('2024-04-21 at 2024-04-21 19:20:22.089603 executed SELECT * From Criminals'),
('2024-04-21 at 2024-04-21 19:20:37.284663 executed UPDATE Officers SET First = Andy WHERE Officer_ID = 1'),
('2024-04-21 at 2024-04-21 19:27:27.020373 executed UPDATE Officers SET Last = Alexis WHERE Officer_ID = 1');
/*!40000 ALTER TABLE `Logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Officers`
--

DROP TABLE IF EXISTS `Officers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Officers` (
  `Officer_ID` int NOT NULL,
  `Last` varchar(15) DEFAULT NULL,
  `First` varchar(10) DEFAULT NULL,
  `Precinct` char(4) NOT NULL,
  `Badge` varchar(14) DEFAULT NULL,
  `Phone` char(10) DEFAULT NULL,
  `Status` enum('A','I') NOT NULL,
  PRIMARY KEY (`Officer_ID`),
  UNIQUE KEY `Badge` (`Badge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Officers`
--

LOCK TABLES `Officers` WRITE;
/*!40000 ALTER TABLE `Officers` DISABLE KEYS */;
INSERT INTO `Officers` VALUES
(1,'Alexis','Andy','1212','11111111111111','1222222221','A'),
(2,'Baxter','Brandy','1212','22222222222222','1222222222','A'),
(3,'Candle','Carl','3434','33333333333333','1222222223','A'),
(4,'Doozer','Debbie','3434','44444444444444','1222222224','A'),
(5,'Eman','Emmanuel','5678','55555555555555','1222222225','A'),
(6,'Foodle','Francy','5678','66666666666666','1222222226','A'),
(7,'Gerble','Gerard','5678','77777777777777','1222222227','A'),
(8,'Hamson','Hillary','5678','88888888888888','1222222228','I'),
(9,'Ifoa','Indira','9100','99999999999999','1222222229','I'),
(10,'Jort','Jack','9100','10101010101010','1222222210','I');
/*!40000 ALTER TABLE `Officers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prob_officer`
--

DROP TABLE IF EXISTS `Prob_officer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Prob_officer` (
  `Prob_ID` int NOT NULL,
  `Last` varchar(15) DEFAULT NULL,
  `First` varchar(10) DEFAULT NULL,
  `Street` varchar(30) DEFAULT NULL,
  `City` varchar(20) DEFAULT NULL,
  `State` char(2) DEFAULT NULL,
  `Zip` char(5) DEFAULT NULL,
  `Phone` char(10) DEFAULT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `Status` enum('A','I') NOT NULL,
  PRIMARY KEY (`Prob_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prob_officer`
--

LOCK TABLES `Prob_officer` WRITE;
/*!40000 ALTER TABLE `Prob_officer` DISABLE KEYS */;
INSERT INTO `Prob_officer` VALUES
(1,'Alding','Andy','Acop Street','Acop City','AS','1234A','123456789','ac@gmail.com','A'),
(2,'Baker','Brad','Bcop Street','Bcop City','BS','1234B','103456789','bc@gmail.com','I'),
(3,'Cap','Cassie','Ccop Street','Ccop City','CS','1234C','113456789','cc@gmail.com','A'),
(4,'Dartk','Derek','Dcop Street','Dcop City','DS','1234D','123456789','dc@gmail.com','I'),
(5,'Eller','Elsie','Ecop Street','Ecop City','ES','1234E','133456789','ec@gmail.com','A'),
(6,'Farsy','Fernando','Fcop Street','Fcop City','FS','1234F','143456789','fc@gmail.com','I'),
(7,'Gerdle','George','Gcop Street','Gcop City','GS','1234G','153456789','gc@gmail.com','A'),
(8,'Helper','Harry','Hcop Street','Hcop City','HS','1234H','163456789','hc@gmail.com','I'),
(9,'Imani','Iman','Icop Street','Icop City','IS','1234I','123451789','ic@gmail.com','A'),
(10,'Josle','Jessica','Jcop Street','Jcop City','JS','1234J','123256789','jc@gmail.com','I');
/*!40000 ALTER TABLE `Prob_officer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sentences`
--

DROP TABLE IF EXISTS `Sentences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sentences` (
  `Sentence_ID` int NOT NULL,
  `Criminal_ID` int DEFAULT NULL,
  `Type` enum('J','H','P') DEFAULT NULL,
  `Prob_ID` int DEFAULT NULL,
  `Start_date` date DEFAULT NULL,
  `End_date` date DEFAULT NULL,
  `Violations` int NOT NULL,
  PRIMARY KEY (`Sentence_ID`),
  KEY `Criminal_ID` (`Criminal_ID`),
  KEY `Prob_ID` (`Prob_ID`),
  CONSTRAINT `sentences_ibfk_1` FOREIGN KEY (`Criminal_ID`) REFERENCES `Criminals` (`Criminal_ID`),
  CONSTRAINT `sentences_ibfk_2` FOREIGN KEY (`Prob_ID`) REFERENCES `Prob_officer` (`Prob_ID`),
  CONSTRAINT `sentences_chk_1` CHECK ((`End_date` > `Start_date`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sentences`
--

LOCK TABLES `Sentences` WRITE;
/*!40000 ALTER TABLE `Sentences` DISABLE KEYS */;
INSERT INTO `Sentences` VALUES
(1,1,'J',1,'2003-01-01','2005-01-01',1),
(2,2,'H',1,'2004-01-01','2005-01-01',1),
(3,3,'P',1,'2005-01-01','2006-01-01',1),
(4,4,'J',1,'2006-01-01','2011-01-01',1),
(5,5,'H',1,'2005-01-01','2007-01-01',1),
(6,6,'P',1,'2007-01-01','2009-01-01',1),
(7,7,'J',1,'2009-01-01','2014-01-01',1),
(8,8,'H',1,'2005-01-01','2008-01-01',1),
(9,9,'P',1,'2011-01-01','2015-01-01',1),
(10,10,'J',1,'2010-01-01','2020-01-01',1);
/*!40000 ALTER TABLE `Sentences` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-21 22:10:10
