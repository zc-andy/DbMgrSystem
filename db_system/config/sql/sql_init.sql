CREATE DATABASE IF NOT EXISTS `my_db`;

USE `my_db`; 
CREATE TABLE IF NOT EXISTS `all_table` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` text NOT NULL,
`happentime` datetime NOT NULL,
`overview` text NOT NULL,
`founder` text NOT NULL,
PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
