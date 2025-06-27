/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - landslide
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`landslide` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `landslide`;

/*Table structure for table `authority` */

DROP TABLE IF EXISTS `authority`;

CREATE TABLE `authority` (
  `authority_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `authority_name` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`authority_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `authority` */

insert  into `authority`(`authority_id`,`login_id`,`authority_name`,`district`,`place`,`phone`,`email`,`status`) values 
(1,2,'tinu','tsr','sdfgh','7894561237','tinu@gmail.com','Active');

/*Table structure for table `authority_land_slide_report` */

DROP TABLE IF EXISTS `authority_land_slide_report`;

CREATE TABLE `authority_land_slide_report` (
  `authority_report_id` int(11) NOT NULL AUTO_INCREMENT,
  `authority_id` int(11) DEFAULT NULL,
  `place_name` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`authority_report_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `authority_land_slide_report` */

insert  into `authority_land_slide_report`(`authority_report_id`,`authority_id`,`place_name`,`latitude`,`longitude`,`date`,`time`,`status`) values 
(1,1,'Jawahar Nagar, Kozhikode, Kerala, 673006, India','10.880397570633699','78.32548141479492','2025-02-12','11:20','Pending');

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaints_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `reply` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`complaints_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `complaints` */

insert  into `complaints`(`complaints_id`,`sender_id`,`title`,`description`,`reply`,`date`) values 
(1,'2','sam','sd','ok fine','2025-02-12 15:41:15'),
(2,'3','fff','gre','hi','2025-02-12 15:41:08'),
(3,'3','hi','asas','NA','2025-02-12 16:43:18'),
(4,'3','cds','dsx','NA','2025-02-12 16:43:46'),
(5,'1','sdfghjk','qwertyuio','NA','2025-02-19 09:32:16');

/*Table structure for table `emergency_notification` */

DROP TABLE IF EXISTS `emergency_notification`;

CREATE TABLE `emergency_notification` (
  `emergency_notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`emergency_notification_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `emergency_notification` */

insert  into `emergency_notification`(`emergency_notification_id`,`title`,`description`,`date`,`status`) values 
(1,'dfghj','zxcvbnm,','2025-02-19 09:15:04','Inactive');

/*Table structure for table `family_friends_number` */

DROP TABLE IF EXISTS `family_friends_number`;

CREATE TABLE `family_friends_number` (
  `family_friend_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`family_friend_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `family_friends_number` */

/*Table structure for table `helpline_number` */

DROP TABLE IF EXISTS `helpline_number`;

CREATE TABLE `helpline_number` (
  `helpline_number_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`helpline_number_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `helpline_number` */

insert  into `helpline_number`(`helpline_number_id`,`name`,`number`) values 
(1,'tinu','7945612378'),
(2,'police','100'),
(4,'fire','101');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `usertype` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'tinu','tinu','authority');

/*Table structure for table `predict_landslide` */

DROP TABLE IF EXISTS `predict_landslide`;

CREATE TABLE `predict_landslide` (
  `predict_landslide_id` int(11) NOT NULL AUTO_INCREMENT,
  `authority_id` int(11) NOT NULL,
  `location_name` text NOT NULL,
  `latitude` varchar(50) NOT NULL,
  `longitude` varchar(50) NOT NULL,
  `temperature` varchar(50) NOT NULL,
  `humidity` varchar(50) NOT NULL,
  `precipitation` varchar(50) NOT NULL,
  `dew_point` varchar(50) NOT NULL,
  `wind_speed` varchar(50) NOT NULL,
  `elevation` varchar(50) NOT NULL,
  `soil_moisture` varchar(50) NOT NULL,
  `date_time` varchar(225) NOT NULL,
  `result` text NOT NULL,
  PRIMARY KEY (`predict_landslide_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `predict_landslide` */

insert  into `predict_landslide`(`predict_landslide_id`,`authority_id`,`location_name`,`latitude`,`longitude`,`temperature`,`humidity`,`precipitation`,`dew_point`,`wind_speed`,`elevation`,`soil_moisture`,`date_time`,`result`) values 
(4,3,'Jawahar Nagar, Kozhikode, Kerala, 673006, India','10.880397570633699','78.32548141479492','29.5','71','111','22.6','5.8','11','99','2025-02-13 09:44:16','Low');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(255) DEFAULT NULL,
  `lname` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`district`,`place`,`phone`,`email`,`latitude`,`longitude`) values 
(1,5,'us','er','ekm','ekm','9632580741','us@g.com',NULL,NULL);

/*Table structure for table `user_land_slide_report` */

DROP TABLE IF EXISTS `user_land_slide_report`;

CREATE TABLE `user_land_slide_report` (
  `user_report_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_report_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `user_land_slide_report` */

insert  into `user_land_slide_report`(`user_report_id`,`user_id`,`place`,`latitude`,`longitude`,`date`,`time`,`status`) values 
(1,1,'ekm','345','555','2025-02-12','10:30','Verified');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
