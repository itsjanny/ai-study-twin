-- =========================================================
-- AI Study Twin — Complete MySQL Relational Database Schema
-- =========================================================

CREATE DATABASE IF NOT EXISTS `aistudytwin` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `aistudytwin`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(255) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Student Profiles Table
CREATE TABLE IF NOT EXISTS `student_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `college` VARCHAR(255) DEFAULT 'State University',
    `course` VARCHAR(255) DEFAULT 'Computer Science & Engineering',
    `semester` VARCHAR(50) DEFAULT 'Semester 4',
    `learning_goals` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Subjects Table
CREATE TABLE IF NOT EXISTS `subjects` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `code` VARCHAR(50) NOT NULL,
    `description` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Topics Table
CREATE TABLE IF NOT EXISTS `topics` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `subject_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `difficulty_level` INT DEFAULT 3,
    `importance_weight` FLOAT DEFAULT 1.0,
    `prerequisite_topic_id` INT DEFAULT NULL,
    FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`prerequisite_topic_id`) REFERENCES `topics`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Questions Table
CREATE TABLE IF NOT EXISTS `questions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `topic_id` INT NOT NULL,
    `question_text` TEXT NOT NULL,
    `option_a` TEXT NOT NULL,
    `option_b` TEXT NOT NULL,
    `option_c` TEXT NOT NULL,
    `option_d` TEXT NOT NULL,
    `correct_option` VARCHAR(10) NOT NULL,
    `explanation` TEXT NOT NULL,
    `sub_concept` VARCHAR(255) DEFAULT NULL,
    `difficulty` INT DEFAULT 3,
    FOREIGN KEY (`topic_id`) REFERENCES `topics`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Topic Performance Table
CREATE TABLE IF NOT EXISTS `topic_performance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `topic_id` INT NOT NULL,
    `quiz_attempts` INT DEFAULT 0,
    `correct_answers` INT DEFAULT 0,
    `total_questions` INT DEFAULT 0,
    `accuracy` FLOAT DEFAULT 0.0,
    `recent_score` FLOAT DEFAULT 0.0,
    `avg_score` FLOAT DEFAULT 0.0,
    `difficulty_level` INT DEFAULT 3,
    `last_studied_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `revision_count` INT DEFAULT 0,
    `weakness_score` FLOAT DEFAULT 50.0,
    `confidence_score` FLOAT DEFAULT 50.0,
    `status_label` VARCHAR(50) DEFAULT 'Average',
    FOREIGN KEY (`student_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`topic_id`) REFERENCES `topics`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Quiz Attempts Table
CREATE TABLE IF NOT EXISTS `quiz_attempts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `subject_id` INT NOT NULL,
    `topic_id` INT DEFAULT NULL,
    `predicted_score` FLOAT DEFAULT 70.0,
    `actual_score` FLOAT DEFAULT 0.0,
    `score_diff` FLOAT DEFAULT 0.0,
    `total_questions` INT DEFAULT 5,
    `correct_answers` INT DEFAULT 0,
    `time_taken_seconds` INT DEFAULT 120,
    `completed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`topic_id`) REFERENCES `topics`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Quiz Answers Table
CREATE TABLE IF NOT EXISTS `quiz_answers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `quiz_attempt_id` INT NOT NULL,
    `question_id` INT NOT NULL,
    `selected_option` VARCHAR(10) NOT NULL,
    `is_correct` TINYINT(1) NOT NULL,
    FOREIGN KEY (`quiz_attempt_id`) REFERENCES `quiz_attempts`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`question_id`) REFERENCES `questions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Recommendations Table
CREATE TABLE IF NOT EXISTS `recommendations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `topic_id` INT NOT NULL,
    `priority_rank` INT DEFAULT 1,
    `priority_score` FLOAT DEFAULT 80.0,
    `reason` TEXT NOT NULL,
    `revision_required` VARCHAR(50) DEFAULT 'High',
    `recommended_duration_min` INT DEFAULT 30,
    `status` VARCHAR(50) DEFAULT 'Active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`topic_id`) REFERENCES `topics`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. ML Predictions Log Table
CREATE TABLE IF NOT EXISTS `predictions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `topic_id` INT DEFAULT NULL,
    `predicted_score` FLOAT NOT NULL,
    `actual_score` FLOAT DEFAULT NULL,
    `features_json` TEXT,
    `model_version` VARCHAR(50) DEFAULT 'v1.0.0-rf',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`topic_id`) REFERENCES `topics`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. User Detailed Activity Telemetry Logs Table
CREATE TABLE IF NOT EXISTS `user_activity_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT DEFAULT NULL,
    `action_type` VARCHAR(100) NOT NULL,
    `endpoint` VARCHAR(255) DEFAULT NULL,
    `ip_address` VARCHAR(50) DEFAULT NULL,
    `user_agent` TEXT DEFAULT NULL,
    `details_json` TEXT DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_activity_user_id` (`user_id`),
    INDEX `idx_activity_action` (`action_type`),
    INDEX `idx_activity_timestamp` (`created_at`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. User Active Sessions Table
CREATE TABLE IF NOT EXISTS `user_sessions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `session_token` VARCHAR(255) NOT NULL UNIQUE,
    `ip_address` VARCHAR(50) DEFAULT NULL,
    `user_agent` TEXT DEFAULT NULL,
    `login_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `last_activity_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `is_active` TINYINT(1) DEFAULT 1,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
