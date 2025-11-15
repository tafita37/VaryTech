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

CREATE TABLE alerte_culture (
    id BIGSERIAL PRIMARY KEY,
    produit_id INT REFERENCES produit(id) NOT NULL,
    temperature_min FLOAT,
    temperature_max FLOAT,
    humidite_min FLOAT,
    humidite_max FLOAT,
    vitesse_vent FLOAT
);

CREATE TABLE alerte_recolte (
    id BIGSERIAL PRIMARY KEY,
    culture_id INT REFERENCES culture(id) NOT NULL,
    temperature_min FLOAT,
    temperature_max FLOAT,
    humidite_min FLOAT,
    humidite_max FLOAT,
    vitesse_vent FLOAT
);