PRAGMA foreign_keys = ON;

-- ============================
-- CATEGORIES (5)
-- ============================
INSERT INTO Category (name, description) VALUES
('Électronique', 'Appareils et accessoires'),
('Maison', 'Objets pour la maison'),
('Sport', 'Équipements sportifs'),
('Beauté', 'Produits de soin'),
('Alimentation', 'Produits alimentaires');

-- ============================
-- PRODUCTS (20)
-- ============================
INSERT INTO Product (name, description, price, stock, category_id) VALUES
('Smartphone X1', 'Téléphone performant', 699, 15, 1),
('Casque Bluetooth', 'Casque sans fil', 89, 30, 1),
('Lampe LED', 'Lampe économique', 25, 40, 2),
('Aspirateur Turbo', 'Aspirateur puissant', 149, 10, 2),
('Tapis de Yoga', 'Tapis antidérapant', 29, 50, 3),
('Haltères 10kg', 'Paire de haltères', 45, 20, 3),
('Crème hydratante', 'Crème visage', 19, 60, 4),
('Shampoing Bio', 'Shampoing naturel', 12, 80, 4),
('Pâtes complètes', '500g', 2.5, 100, 5),
('Huile d’olive', 'Extra vierge', 7.9, 70, 5),
('Chargeur USB-C', 'Charge rapide', 15, 25, 1),
('Enceinte portable', 'Bluetooth', 59, 18, 1),
('Coussin décoratif', 'Coussin doux', 14, 35, 2),
('Bougie parfumée', 'Vanille', 9, 50, 2),
('Ballon de foot', 'Taille 5', 22, 40, 3),
('Raquette de tennis', 'Graphite', 89, 12, 3),
('Mascara Volume', 'Longue tenue', 17, 55, 4),
('Gel douche', 'Aloe vera', 6, 90, 4),
('Riz basmati', '1kg', 3.2, 120, 5),
('Chocolat noir', '70%', 2.8, 80, 5);

-- ============================
-- CUSTOMERS (12)
-- ============================
INSERT INTO Customer (first_name, last_name, email, city, created_at) VALUES
('Alice', 'Martin', 'alice.martin@example.com', 'Lille', '2026-01-10'),
('Bob', 'Durand', 'bob.durand@example.com', 'Paris', '2026-02-14'),
('Claire', 'Petit', 'claire.petit@example.com', 'Lyon', '2026-03-01'),
('David', 'Morel', 'david.morel@example.com', 'Marseille', '2026-03-22'),
('Emma', 'Bernard', 'emma.bernard@example.com', 'Nice', '2026-04-05'),
('François', 'Lambert', 'francois.lambert@example.com', 'Toulouse', '2026-04-18'),
('Gina', 'Rossi', 'gina.rossi@example.com', 'Lille', '2026-05-02'),
('Hugo', 'Leclerc', 'hugo.leclerc@example.com', 'Paris', '2026-05-20'),
('Inès', 'Robert', 'ines.robert@example.com', 'Lyon', '2026-06-01'),
('Julien', 'Fabre', 'julien.fabre@example.com', 'Nice', '2026-06-15'),
('Karim', 'Belaid', 'karim.belaid@example.com', 'Marseille', '2026-07-01'),
('Laura', 'Gomez', 'laura.gomez@example.com', 'Toulouse', '2026-07-10');

-- ============================
-- ORDERS (25)
-- ============================
INSERT INTO CustomerOrder (customer_id, order_date, status) VALUES
(1, '2026-07-01', 'Payée'),
(2, '2026-07-02', 'Livrée'),
(3, '2026-07-03', 'En cours'),
(4, '2026-07-04', 'Payée'),
(5, '2026-07-05', 'Livrée'),
(6, '2026-07-06', 'En cours'),
(7, '2026-07-07', 'Payée'),
(8, '2026-07-08', 'Livrée'),
(9, '2026-07-09', 'Payée'),
(10, '2026-07-10', 'En cours'),
(11, '2026-07-11', 'Livrée'),
(12, '2026-07-12', 'Payée'),
(1, '2026-07-13', 'Payée'),
(2, '2026-07-14', 'Livrée'),
(3, '2026-07-15', 'En cours'),
(4, '2026-07-16', 'Payée'),
(5, '2026-07-17', 'Livrée'),
(6, '2026-07-18', 'En cours'),
(7, '2026-07-19', 'Payée'),
(8, '2026-07-20', 'Livrée'),
(9, '2026-07-21', 'Payée'),
(10, '2026-07-22', 'En cours'),
(11, '2026-07-23', 'Livrée'),
(12, '2026-07-24', 'Payée'),
(1, '2026-07-25', 'Payée');

-- ============================
-- ORDER ITEMS (50)
-- ============================
INSERT INTO OrderItem (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 699),
(1, 9, 3, 2.5),
(2, 2, 1, 89),
(2, 10, 2, 7.9),
(3, 5, 2, 29),
(3, 6, 1, 45),
(4, 3, 1, 25),
(4, 11, 1, 15),
(5, 7, 2, 19),
(5, 8, 1, 12),
(6, 12, 1, 59),
(6, 14, 2, 9),
(7, 15, 1, 22),
(7, 16, 1, 89),
(8, 17, 2, 17),
(8, 18, 3, 6),
(9, 19, 2, 3.2),
(9, 20, 4, 2.8),
(10, 4, 1, 149),
(10, 13, 2, 14),
(11, 5, 1, 29),
(11, 6, 2, 45),
(12, 1, 1, 699),
(12, 2, 1, 89),
(13, 3, 2, 25),
(13, 4, 1, 149),
(14, 7, 1, 19),
(14, 8, 2, 12),
(15, 9, 5, 2.5),
(15, 10, 1, 7.9),
(16, 11, 1, 15),
(16, 12, 1, 59),
(17, 13, 2, 14),
(17, 14, 1, 9),
(18, 15, 1, 22),
(18, 16, 1, 89),
(19, 17, 2, 17),
(19, 18, 1, 6),
(20, 19, 3, 3.2),
(20, 20, 2, 2.8),
(21, 1, 1, 699),
(21, 5, 2, 29),
(22, 6, 1, 45),
(22, 7, 1, 19),
(23, 8, 2, 12),
(23, 9, 4, 2.5),
(24, 10, 1, 7.9),
(24, 11, 1, 15),
(25, 12, 1, 59),
(25, 13, 2, 14);
