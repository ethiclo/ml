DROP SCHEMA IF EXISTS ethiclo CASCADE;
CREATE SCHEMA ethiclo;
SET search_path TO ethiclo;

CREATE TABLE Shopper (
    email TEXT PRIMARY KEY,
    date_created DATE DEFAULT NOW()
);

CREATE TABLE Website (
    website_id SERIAL PRIMARY KEY,
    url TEXT,
    shopper TEXT NOT NULL REFERENCES Shopper(email),
    date_created DATE DEFAULT NOW()
);

CREATE TABLE Product (
   product_id SERIAL PRIMARY KEY,
   url TEXT,
   img_src TEXT,
   title VARCHAR(255),
   price FLOAT,
   brand VARCHAR(255),
   description TEXT,
   score FLOAT,
   date_created DATE DEFAULT NOW(),
   alt_to INTEGER,
   shopper TEXT NOT NULL REFERENCES Shopper(email)
)




