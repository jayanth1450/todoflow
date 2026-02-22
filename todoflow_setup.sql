-- Create database
CREATE DATABASE IF NOT EXISTS todoflow;

-- Use the database
USE todoflow;

-- Create User table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    identity VARCHAR(50),
    gender VARCHAR(10),
    college VARCHAR(255),
    company VARCHAR(255),
    subscription_type VARCHAR(50) DEFAULT 'Free',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Task table
CREATE TABLE IF NOT EXISTS task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
