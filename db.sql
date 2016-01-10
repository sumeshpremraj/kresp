# Sequel Pro SQL dump
# Version 4499
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.6.25)
# Database: kresp
# Generation Time: 2016-01-07 15:15:14 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table content
# ------------------------------------------------------------
DROP DATABASE IF EXISTS `kresp`;
CREATE Database `kresp`;
use kresp;
grant all on `kresp`.* to 'kresp'@'localhost' identified by '';

CREATE TABLE IF NOT EXISTS `content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `link` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `publish_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`category_id`) REFERENCES categories(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `categories` (`id`, `category_name`)
VALUES
  (1, 'sports'),
  (2, 'science');

CREATE TABLE IF NOT EXISTS `category_mapping` (
  `category_id` int(11) NOT NULL,
  `feed_url` varchar(200) NOT NULL,
  `site_name` varchar(200) NOT NULL,
  `last_updated` datetime DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `category_mapping_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `category_mapping` (`category_id`, `feed_url`, `site_name`)
VALUES
  (1, 'http://feeds.bbci.co.uk/sport/0/football/rss.xml', 'BBC - Football'),
  (2, 'https://www.brainpickings.org/feed/', 'Brainpickings');

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_id` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `kindle_id` varchar(200) NOT NULL,
  `category_ids` varchar(200) NOT NULL,
  `last_sent_date` datetime DEFAULT NULL,
  `frequency` int(11) DEFAULT NULL,
  `active` boolean not null default 1,
  `providers_list` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into user(email_id,password,password_hash,kindle_id,category_ids,frequency,providers_list) values('sumeshpremraj@gmail.com','blah','$6$rounds=677265$FIToeCcwbytFeanm$mle89QD/AAoDbBMlN7DlEZwTDjqMLDq0R2q7XxcyzQEFqlgu8/sdy4Cf9Ghng9zfXA2jj2Ylx3rHAggKnBohG0','sumeshpremraj@kindle.com','1,2',1,'1,2');
INSERT INTO `user` (`email_id`,`password`,`password_hash`,`kindle_id`, `category_ids`, `last_sent_date`, `frequency`,providers_list) VALUES ('kindlefellastest@gmail.com','test','$6$rounds=609132$zF18uPsrtxxCTdyc$dcp8SH6Kw2suxTr1oYdmMlgxzc1cD3LdLXF6NMf9mzIwwFIgEUs7vRb8x9r2Qz.6/RtSCNa.rypEL4uf2ziUZ.','sumeshpremraj@kindle.com', '1,2', NULL, 1,'1,2');

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

