create database varytech;
\c varytech

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password text NOT NULL
);

CREATE TABLE utilisateur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    password text NOT NULL,
    date_inscription TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    role_id INT REFERENCES role(id) ON DELETE SET NULL
);

CREATE TABLE type_sol (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE parcelle (
    id SERIAL PRIMARY KEY, 
    nom VARCHAR(100) UNIQUE NOT NULL,
    photo_a VARCHAR(100) NOT NULL,
    photo_e TEXT UNIQUE NOT NULL,
    superficie DOUBLE PRECISION NOT NULL, -- unité (ha, m2) à préciser
    type_sol_id INT REFERENCES type_sol(id) NOT NULL,
    humidite_moyenne DOUBLE PRECISION,
    temperature_moyenne DOUBLE PRECISION
);

create table unite(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE ressource (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prix NUMERIC(14,4) NOT NULL DEFAULT 0,
    unite_id BIGINT REFERENCES unite(id) NOT NULL
);

CREATE TABLE produit (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prix NUMERIC(14,4) NOT NULL DEFAULT 0
);

CREATE TABLE culture (
    id SERIAL PRIMARY KEY,
    produit_id BIGINT REFERENCES produit(id) ON DELETE SET NULL,
    parcelle_id BIGINT REFERENCES parcelle(id) ON DELETE SET NULL,
    photo_a VARCHAR(100) NOT NULL,
    photo_e TEXT UNIQUE NOT NULL,
    date_semis DATE NOT NULL,
    date_recolte_prevu DATE,
    date_recolte_reelle DATE,
    rendement_estime NUMERIC(14,4),
    rendement_reel NUMERIC(14,4),
    quantite_semee NUMERIC(14,4)
);

CREATE TABLE culture_ressource (
    id SERIAL PRIMARY KEY,
    culture_id BIGINT NOT NULL REFERENCES culture(id) ON DELETE CASCADE,
    ressource_id BIGINT NOT NULL REFERENCES ressource(id) ON DELETE RESTRICT,
    quantite_resource NUMERIC(14,4) NOT NULL
);

CREATE TABLE recolte (
    id SERIAL PRIMARY KEY,
    culture_id BIGINT REFERENCES culture(id) ON DELETE CASCADE,
    date_recolte DATE NOT NULL,
    quantite_recoltee FLOAT NOT NULL
);

-- CREATE TABLE meteo (
--     id SERIAL PRIMARY KEY,
--     date TIMESTAMP WITH TIME ZONE NOT NULL,
--     temperature_moyenne NUMERIC(6,3),
--     humidite_air NUMERIC(6,3),
--     precipitation NUMERIC(10,4),
--     vitesse_vent NUMERIC(8,3),
--     pression_atmospherique NUMERIC(10,3),
--     couverture_nuageuse NUMERIC(5,2), -- en %
--     description TEXT
-- );

-- CREATE TABLE recommandation_meteo (
--     id SERIAL PRIMARY KEY,
--     recommandation TEXT NOT NULL,
--     date_recommandation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
-- );

-- CREATE TABLE prediction_rendement (
--     id SERIAL PRIMARY KEY,
--     id_parcelle BIGINT REFERENCES parcelles(id) ON DELETE CASCADE,
--     rendement_predit NUMERIC(14,4)
-- );

-- CREATE TABLE agriculteurs (
--     id SERIAL PRIMARY KEY,
--     nom VARCHAR(200) NOT NULL,
--     photo TEXT -- chemin ou URL
-- );

-- CREATE TABLE forum (
--     id SERIAL PRIMARY KEY,
--     id_createur BIGINT REFERENCES users(id) ON DELETE SET NULL,
--     question TEXT NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
-- );

-- CREATE TABLE forum_reponse (
--     id SERIAL PRIMARY KEY,
--     id_forum BIGINT NOT NULL REFERENCES forum(id) ON DELETE CASCADE,
--     reponse TEXT NOT NULL,
--     id_repondeur BIGINT REFERENCES users(id) ON DELETE SET NULL,
--     created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
-- );

-- CREATE TABLE transporteurs (
--     id SERIAL PRIMARY KEY,
--     nom VARCHAR(200) NOT NULL
-- );

-- CREATE TABLE livraison (
--     id SERIAL PRIMARY KEY,
--     id_transporteur BIGINT REFERENCES transporteurs(id) ON DELETE SET NULL,
--     date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
-- );

-- CREATE TABLE livraison_detail (
--     id SERIAL PRIMARY KEY,
--     id_livraison BIGINT NOT NULL REFERENCES livraison(id) ON DELETE CASCADE,
--     id_recolte BIGINT REFERENCES cultures(id) ON DELETE SET NULL,
--     quantite NUMERIC(14,4) NOT NULL,
--     id_client BIGINT REFERENCES users(id) ON DELETE SET NULL
-- );

-- CREATE TABLE mouvement (
--     id SERIAL PRIMARY KEY,
--     id_produit BIGINT REFERENCES produits(id) ON DELETE SET NULL, -- anciennement id_plante
--     quantite_entrant NUMERIC(14,4) DEFAULT 0,
--     quantite_sortant NUMERIC(14,4) DEFAULT 0,
--     date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
-- );

-- -- Indexes utiles
-- CREATE INDEX idx_cultures_parcelle ON cultures(id_parcelle);
-- CREATE INDEX idx_meteo_date ON meteo(date);