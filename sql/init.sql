CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(10) NOT NULL,
    location VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    air_quality DECIMAL(5,2) NOT NULL,
    timestamp DATETIME NOT NULL
);
