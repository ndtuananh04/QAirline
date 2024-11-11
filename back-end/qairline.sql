-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema qairline
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema qairline
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `qairline` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4 ;
USE `qairline` ;

-- -----------------------------------------------------
-- Table `qairline`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`account` (
  `account_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(60) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  `role_id` ENUM('customer', 'admin') NOT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`airplanes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`airplanes` (
  `airplane_id` VARCHAR(60) NOT NULL,
  `model` VARCHAR(60) NOT NULL,
  `capacity` INT NOT NULL,
  `seat_info` TEXT NOT NULL,
  PRIMARY KEY (`airplane_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`flights`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`flights` (
  `flight_id` VARCHAR(45) NOT NULL,
  `airplane_id` VARCHAR(60) NOT NULL,
  `flight_number` VARCHAR(45) NOT NULL,
  `origin` VARCHAR(50) NOT NULL,
  `destination` VARCHAR(60) NOT NULL,
  `departure_time` DATETIME NOT NULL,
  `arrival_time` DATETIME NOT NULL,
  `status` ENUM('scheduled', 'delayed', 'cancelled') NOT NULL,
  PRIMARY KEY (`flight_id`),
  INDEX `fk_flights_airplane_id_idx` (`airplane_id` ASC) VISIBLE,
  CONSTRAINT `fk_flights_airplane_id`
    FOREIGN KEY (`airplane_id`)
    REFERENCES `qairline`.`airplanes` (`airplane_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`ticket` (
  `ticket_id` VARCHAR(45) NOT NULL,
  `flight_id` VARCHAR(45) NOT NULL,
  `account_id` INT NOT NULL,
  `seat_number` VARCHAR(45) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `class` ENUM('economy', 'business', 'first') NOT NULL,
  `status` ENUM('booked', 'checked_in', 'cancelled') NOT NULL,
  `booking_date` DATETIME NOT NULL,
  PRIMARY KEY (`ticket_id`),
  UNIQUE INDEX `flight_id_UNIQUE` (`flight_id` ASC) VISIBLE,
  INDEX `fk_ticket_user_id_idx` (`account_id` ASC) VISIBLE,
  INDEX `fk_ticket_flight_id_idx` (`flight_id` ASC) VISIBLE,
  CONSTRAINT `fk_ticket_flight_id`
    FOREIGN KEY (`flight_id`)
    REFERENCES `qairline`.`flights` (`flight_id`),
  CONSTRAINT `fk_ticket_user_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `qairline`.`account` (`account_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`booking_histories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`booking_histories` (
  `history_id` INT NOT NULL AUTO_INCREMENT,
  `ticket_id` VARCHAR(45) NOT NULL,
  `action` ENUM('booked', 'cancelled', 'modified') NOT NULL,
  `action_date` DATETIME NOT NULL,
  PRIMARY KEY (`history_id`),
  INDEX `fk_booking_ticket_id_idx` (`ticket_id` ASC) VISIBLE,
  CONSTRAINT `fk_booking_ticket_id`
    FOREIGN KEY (`ticket_id`)
    REFERENCES `qairline`.`ticket` (`ticket_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`cancellations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`cancellations` (
  `cancellation_id` INT NOT NULL AUTO_INCREMENT,
  `ticket_id` VARCHAR(45) NOT NULL,
  `cancellationscol` INT NOT NULL,
  `reason` TEXT NULL DEFAULT NULL,
  `cancellation_date` DATETIME NOT NULL,
  PRIMARY KEY (`cancellation_id`),
  INDEX `fk_cancellations_ticket_id_idx` (`ticket_id` ASC) VISIBLE,
  CONSTRAINT `fk_cancellations_ticket_id`
    FOREIGN KEY (`ticket_id`)
    REFERENCES `qairline`.`ticket` (`ticket_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`customer_support_tickets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`customer_support_tickets` (
  `ticket_id` VARCHAR(45) NOT NULL,
  `subject` VARCHAR(100) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `status` ENUM('open', 'in progress', 'closed') NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`ticket_id`),
  CONSTRAINT `fk_support_ticket_id`
    FOREIGN KEY (`ticket_id`)
    REFERENCES `qairline`.`ticket` (`ticket_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`fligt_delay`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`fligt_delay` (
  `delay_id` INT NOT NULL AUTO_INCREMENT,
  `flight_id` VARCHAR(45) NOT NULL,
  `new_departure_time` DATETIME NOT NULL,
  PRIMARY KEY (`delay_id`),
  INDEX `fk_delay_flight_id_idx` (`flight_id` ASC) VISIBLE,
  CONSTRAINT `fk_delay_flight_id`
    FOREIGN KEY (`flight_id`)
    REFERENCES `qairline`.`flights` (`flight_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`logs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`logs` (
  `log_id` INT NOT NULL AUTO_INCREMENT,
  `action` TEXT NOT NULL,
  `action_date` DATETIME NOT NULL,
  PRIMARY KEY (`log_id`),
  CONSTRAINT `fk_logs_user_id`
    FOREIGN KEY (`log_id`)
    REFERENCES `qairline`.`account` (`account_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`payments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`payments` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `ticket_id` VARCHAR(45) NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `payment_date` DATETIME NOT NULL,
  `status` ENUM('completed', 'pending', 'failed') NOT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `fk_payments_ticket_id_idx` (`ticket_id` ASC) VISIBLE,
  CONSTRAINT `fk_payments_ticket_id`
    FOREIGN KEY (`ticket_id`)
    REFERENCES `qairline`.`ticket` (`ticket_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`promotions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`promotions` (
  `promotion_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  PRIMARY KEY (`promotion_id`),
  CONSTRAINT `fk_promotions_user_id`
    FOREIGN KEY (`promotion_id`)
    REFERENCES `qairline`.`account` (`account_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`seats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`seats` (
  `seat_id` INT NOT NULL AUTO_INCREMENT,
  `airplane_id` VARCHAR(60) NOT NULL,
  `seat_number` VARCHAR(45) NOT NULL,
  `class` ENUM('economy', 'business', 'first') NOT NULL,
  `status` ENUM('available', 'reserved') NOT NULL,
  PRIMARY KEY (`seat_id`),
  INDEX `fk_seats_airplanes_id_idx` (`airplane_id` ASC) VISIBLE,
  CONSTRAINT `fk_seats_airplanes_id`
    FOREIGN KEY (`airplane_id`)
    REFERENCES `qairline`.`airplanes` (`airplane_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


-- -----------------------------------------------------
-- Table `qairline`.`user_information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `qairline`.`user_information` (
  `identification` INT NOT NULL,
  `family_name` VARCHAR(60) NOT NULL,
  `given_name` VARCHAR(60) NOT NULL,
  `title` VARCHAR(60) NOT NULL,
  `nationality` VARCHAR(60) NOT NULL,
  `date_of_birth` DATETIME NOT NULL,
  `phone_number` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`identification`),
  UNIQUE INDEX `identification_UNIQUE` (`identification` ASC) VISIBLE,
  CONSTRAINT `fk_user_information_account_id`
    FOREIGN KEY (`identification`)
    REFERENCES `qairline`.`account` (`account_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
