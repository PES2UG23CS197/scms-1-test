DROP DATABASE IF EXISTS scms1;
CREATE DATABASE scms1;
USE scms1;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'User') NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Products (
    sku VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    threshold INT DEFAULT 10
) ENGINE=InnoDB;

CREATE TABLE Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL,
    quantity INT DEFAULT 0,
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    customer_name VARCHAR(100),
    status ENUM('Pending', 'Processed') DEFAULT 'Pending',
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

CREATE TABLE Logistics (
    logistics_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    transport_cost DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

CREATE TABLE Routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    cost DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE DemandForecast (
    forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL,
    forecast_value INT NOT NULL,
    forecast_date DATE NOT NULL,
    FOREIGN KEY (sku) REFERENCES Products(sku)
) ENGINE=InnoDB;

CREATE TABLE Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    generated_by VARCHAR(50) NOT NULL,
    summary TEXT
) ENGINE=InnoDB;

CREATE TABLE Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
) ENGINE=InnoDB;

-- Sample Users
INSERT INTO Users (username, password, role) VALUES
('admin1', 'adminpass123', 'Admin'),
('user1', 'userpass123', 'User');

-- Sample Products
INSERT INTO Products (sku, name, description, threshold) VALUES
('SKU001', 'Laptop', 'High-performance laptop', 5),
('SKU002', 'Smartphone', 'Latest model smartphone', 10),
('SKU003', 'Router', 'Dual-band WiFi router', 8);

-- Sample Inventory
INSERT INTO Inventory (sku, location, quantity) VALUES
('SKU001', 'Warehouse A', 20),
('SKU002', 'Warehouse B', 15),
('SKU003', 'Warehouse A', 5);

-- Sample Queries
SELECT * FROM Products;
SELECT * FROM Inventory;
SELECT * FROM Users;
