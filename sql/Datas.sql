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