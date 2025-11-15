insert into role (nom) values ('CLIENT'), 
                                ('AGRICULTEUR');

insert into admin (username, password) values ('admin', 'admin');

insert into type_sol(nom) values ('Argileux'), 
                                 ('Sableux'), 
                                 ('Limonneux'), 
                                 ('Tourbeux'), 
                                 ('Calcaire'), 
                                 ('Silty-loam / limono-argileux'), 
                                 ('Laterite / sols tropicaux');

INSERT INTO unite (nom) VALUES('kg'),
                                ('g'),
                                ('L'),
                                ('mL'),
                                ('m'),
                                ('cm'),
                                ('mm'),
                                ('ha'),
                                ('m2'),
                                ('pc'),
                                ('t'),
                                ('bag'),
                                ('sack'),
                                ('unit'),
                                ('h');

insert into ressource (nom, prix, unite_id) values ('Eau', 2500, 3),
                                                    ('Engrais NPK', 5000, 1),
                                                    ('Semence Maïs', 1200, 1),
                                                    ('Pesticide ABC', 100000, 3),
                                                    ('Binette', 60000, 14);

insert into produit (nom, prix) values ('Riz', 2500),
                                        ('Maïs', 2000),
                                        ('Manioc', 1800),
                                        ('Tomate', 3000),
                                        ('Mangue', 5000);

INSERT INTO alerte_culture (produit_id, temperature_min, temperature_max, humidite_min, humidite_max, vitesse_vent)
VALUES
-- Riz
(1, 20.0, 35.0, 60.0, 90.0, 15.0),
-- Maïs
(2, 18.0, 32.0, 50.0, 85.0, 12.0),
-- Manioc
(3, 22.0, 38.0, 55.0, 80.0, 10.0),
-- Tomate
(4, 15.0, 30.0, 60.0, 90.0, 8.0),
-- Mangue
(5, 24.0, 36.0, 50.0, 85.0, 20.0);