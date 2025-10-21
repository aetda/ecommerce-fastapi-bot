CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  price FLOAT,
  description VARCHAR(255),
  category VARCHAR(50)
);

INSERT INTO products (name, price, description, category)
VALUES
('Lenovo Laptop', 299000, 'Powerful laptop for work', 'Laptops'),
('Samsung Phone', 199000, 'New Galaxy smartphone', 'Phones'),
('Sony Headphones', 49900, 'Wireless with noise cancellation', 'Accessories'),
('Apple MacBook Pro', 450000, 'High-performance laptop for professionals', 'Laptops'),
('iPhone 15', 250000, 'Latest Apple smartphone', 'Phones'),
('Bose Headphones', 55000, 'Noise-cancelling over-ear headphones', 'Accessories'),
('Dell XPS 13', 320000, 'Compact and powerful ultrabook', 'Laptops'),
('Google Pixel 8', 180000, 'Smartphone with excellent camera', 'Phones'),
('Logitech Mouse', 12000, 'Wireless ergonomic mouse', 'Accessories'),
('HP Pavilion Laptop', 210000, 'Reliable laptop for everyday use', 'Laptops'),
('OnePlus 12', 160000, 'Fast and smooth Android smartphone', 'Phones'),
('JBL Speaker', 25000, 'Portable Bluetooth speaker', 'Accessories');
