CREATE DATABASE `sfadmin`;

USE `sfadmin`;


CREATE TABLE `admin_users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(100),
  `password` VARCHAR(100),
  `created_date` DATETIME DEFAULT CURRENT_TIMESTAMP
);
