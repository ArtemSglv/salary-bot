CREATE TABLE `users` (
  `user_id` int PRIMARY KEY,
  `name` varchar(255),
  `salary` double
);

CREATE TABLE `progress` (
  `work_day` date PRIMARY KEY,
  `user_id` int,
  `number_of_hours` double,
  `comment` varchar(255)
);

CREATE TABLE `configurations` (
  `config_id` int PRIMARY KEY AUTO_INCREMENT,
  `salary_day` int,
  `advance_payment` int,
  `tax` double,
  `working_day` int
);

ALTER TABLE `progress` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
