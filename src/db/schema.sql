-- CREATE TYPE major_type AS ENUM('Major', 'Combined Major', 'Honours', 'Combined Honours');

CREATE TABLE IF NOT EXISTS majors (
    name VARCHAR(255),
    id INT NOT NULL,
    type major_type NOT NULL,
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
    success Boolean,
    last_updated TIMESTAMP,
    PRIMARY KEY (id)
);