#initial patch

CREATE DATABASE `agile`;
USE `agile`;

CREATE TABLE `users` (
	`hiddenid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`id` BINARY(16) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`hiddenid`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `boards` (
	`hiddenid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`id` BINARY(16) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`hiddenid`),
	KEY `name` (`name`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `users_boards` (
	`user_id` BINARY(16) NOT NULL,
	`board_id` BINARY(16) NOT NULL,
	PRIMARY KEY (`user_id`, `board_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `stories` (
	`hiddenid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`id` BINARY(16) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	`description` VARCHAR(300),
	`estimate` DECIMAL(3, 1) NOT NULL,
	PRIMARY KEY (`hiddenid`),
	KEY `name` (`name`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `users_stories` (
	`user_id` BINARY(16) NOT NULL,
	`story_id` BINARY(16) NOT NULL,
	PRIMARY KEY (`user_id`, `story_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `tasks` (
	`hiddenid` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`id` BINARY(16) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	`description` VARCHAR(300),
	`estimate` DECIMAL(3, 1) NOT NULL,
	`completed` BOOLEAN NOT NULL DEFAULT FALSE
	`completion_date` DATETIME,
	PRIMARY KEY (`hiddenid`),
	KEY `name` (`name`),
	KEY `completed` (`completed`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `tasks_stories` (
	`task_id` BINARY(16) NOT NULL,
	`story_id` BINARY(16) NOT NULL,
	PRIMARY KEY (`task_id`, `story_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `users_tasks` (
	`user_id` BINARY(16) NOT NULL,
	`task_id` BINARY(16) NOT NULL,
	PRIMARY KEY (`user_id`, `task_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;

