DROP SCHEMA IF EXISTS ethiclo CASCADE;
CREATE SCHEMA ethiclo;
SET search_path TO ethiclo;

CREATE TABLE user (
    user_id SERIAL,
    email TEXT,
    date_created DATE DEFAULT NOW(),
);

CREATE TABLE product (
   product_id SERIAL,
   url TEXT,
   img_src TEXT,
   title VARCHAR(255),
   price FLOAT,
   brand VARCHAR(255),
   description TEXT,
   score FLOAT,
   date_created DATE DEFAULT NOW(),
   alt_to SERIAL,
   FOREIGN KEY user REFERENCES user
)




