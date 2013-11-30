CREATE TABLE `invitations` (
	`id` BINARY(16) NOT NULL,
	`user_id` BINARY(16) NOT NULL,
	`board_id` BINARY(16) NOT NULL,
	`privileges` TINYINT NOT NULL DEFAULT 0, #0 will be admin
	`active` BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (`user_id`, `board_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;
