CREATE TABLE cities (
        id UUID NOT NULL,
        name VARCHAR(65) NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL,
        PRIMARY KEY (id)
);