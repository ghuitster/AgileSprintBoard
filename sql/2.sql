ALTER TABLE `users`
ADD COLUMN `email` VARCHAR(100) NOT NULL,
ADD KEY `email` (`email`);

CREATE TABLE `users_openids` (
	`user_id` BINARY(16) NOT NULL,
	`openid` VARCHAR(200) NOT NULL,
	PRIMARY KEY (`user_id`, `openid`),
	KEY (`openid`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_general_ci;