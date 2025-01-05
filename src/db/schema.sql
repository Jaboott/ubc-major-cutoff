-- uncomment for initial db setup --
-- CREATE TYPE major_type AS ENUM('Combined', 'Honours', 'Major');

CREATE TABLE IF NOT EXISTS majors (
    name VARCHAR(255),
    id INT NOT NULL,
    type  major_type NOT NULL,
    PRIMARY KEY (id, type)
);

CREATE TABLE IF NOT EXISTS admission_statistics (
    year INT,
    max_grade NUMERIC,
    min_grade NUMERIC,
    initial_reject INT,
    final_admit INT,
    id INT,
    type major_type NOT NULL,
    FOREIGN KEY (id, type) REFERENCES majors(id, type),
    PRIMARY KEY (year, id, type)
);

CREATE TABLE IF NOT EXISTS meta_data (
    id SERIAL,
    check_sum VARCHAR(64),
    last_updated TIMESTAMP,
    PRIMARY KEY (id)
);