
CREATE TABLE IF NOT EXISTS cetac_user (
    id SERIAL,
    first_lastname VARCHAR(30),
    second_lastname VARCHAR(30),
    firstname VARCHAR(30),
    gender VARCHAR(10),
    marital_status VARCHAR(10),
    phone VARCHAR(10),
    cellphone VARCHAR(10),
    birth_date DATE,
    birth_place VARCHAR(20),
    occupation VARCHAR(20),
    religion VARCHAR(20),
    zip_code INT,
    street VARCHAR(20),
    address_number INT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user_child(
    id SERIAL,
    first_lastname VARCHAR(30),
    second_lastname VARCHAR(30),
    firstname VARCHAR(30),
    birth_date DATE,
    gender VARCHAR(10),
    mother_id INT,
    father_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (mother_id) REFERENCES cetac_user(id),
    FOREIGN KEY (father_id) REFERENCES cetac_user(id)
);

-- Using SHA256 to hash passwords and a 16 char SALT suffix value
CREATE TABLE IF NOT EXISTS cetac_staff (
    id SERIAL,
    first_lastname VARCHAR(30),
    second_lastname VARCHAR(30),
    firstname VARCHAR(30),
    access_level VARCHAR(15) CHECK (access_level IN ('thanatologist', 'admin_support', 'admin')),
    username VARCHAR(30),
    password CHAR(64),
    salt CHAR(16),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cetac_record (
    id SERIAL,
    ekr TEXT,
    staff_id INT,
    user_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (staff_id) REFERENCES cetac_staff(id),
    FOREIGN KEY (user_id) REFERENCES cetac_user(id)
);

CREATE TABLE IF NOT EXISTS cetac_session (
    id SERIAL,
    tool VARCHAR(50),
    intervention_type VARCHAR(50),
    session_number INT,
    evaluation TEXT,
    session_date DATE,
    motive TEXT,
    recovery_fee REAL,
    record_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (record_id) REFERENCES cetac_record(id)
);

-- Insert sample information into the DB
INSERT INTO cetac_user (
    first_lastname,
    second_lastname,
    firstname,
    gender,
    marital_status,
    phone,
    cellphone,
    birth_date,
    birth_place,
    occupation,
    religion,
    zip_code,
    street,
    address_number
) VALUES (
    'Gabián',
    'Pérez',
    'Santiago',
    'Hombre',
    'Soltero',
    '5236433261',
    '5936393441',
    '1978-06-30',
    'CDMX',
    'Estudiante',
    'Budista',
    09855,
    'Calle X',
    32
);

INSERT INTO user_child (
    first_lastname,
    second_lastname,
    firstname,
    birth_date,
    gender,
    father_id
) VALUES (
    'Roberto',
    'Pérez',
    'Nogales',
    '2004-04-26',
    'Hombre',
    1
);

-- Sample passwords are the same as usernames.
INSERT INTO cetac_staff (
    first_lastname,
    second_lastname,
    firstname,
    access_level,
    username,
    password,
    salt
) VALUES (
    'Jiménez',
    'Urgell',
    'Diego Enrique',
    'thanatologist',
    'diego.urgell',
    'd7ae5c9d3ae39533baac510171f889e5fc255e5f05ff45a200ca1a13ba4c3339',
    'a1b2c3d4e5f6g7h8'
);

INSERT INTO cetac_staff (
    first_lastname,
    second_lastname,
    firstname,
    access_level,
    username,
    password,
    salt
) VALUES (
    'Zepeda',
    'Ceballos',
    'Iñigo Enrique',
    'admin',
    'inigo.zepeda',
    '00d4159b5d106c9d058f2e04c6ca7ec42ba36546a468c07330b7c8d70fc5f768',
    'b2c3d4e5f6g7h8i9'
);

INSERT INTO cetac_staff (
    first_lastname,
    second_lastname,
    firstname,
    access_level,
    username,
    password,
    salt
) VALUES (
    'Hernández',
    'Bravo',
    'Manuel Alejandro',
    'admin_support',
    'manuel.hernandez',
    'db124066384060b7c132c51e3606338811a99912761eaf973dea64c4f1214c1a',
    'c3d4e5f6g7h8i9j0'
);

INSERT INTO cetac_record (
    ekr,
    staff_id,
    user_id
) VALUES (
    'Expendiente de prueba jskjsksj',
    1,
    1
);

INSERT INTO cetac_session (
    tool,
    intervention_type,
    session_number,
    evaluation,
    session_date,
    motive,
    recovery_fee,
    record_id
) VALUES (
    'Sesión Individual',
    'Acompañamiento',
    1,
    'Prueba exitosa',
    '2021-09-25',
    'Sesión de Prueba',
    250.0,
    1
);

CREATE USER username WITH PASSWORD 'password' VALID UNTIL 'infinity';

GRANT SELECT, INSERT, UPDATE, DELETE
ON cetac_staff, cetac_session, cetac_record, cetac_user, user_child
TO username;
