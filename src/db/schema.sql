-- CREATE TYPE major_type AS ENUM('Major', 'Combined_Major', 'Honours', 'Combined_Honours');

CREATE TABLE IF NOT EXISTS majors (
    name VARCHAR(255),
    id INT NOT NULL,
    type major_type NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(name, type)
);

CREATE TABLE IF NOT EXISTS admission_statistics (
    year INT,
    max_grade NUMERIC,
    min_grade NUMERIC,
    initial_reject INT,
    final_admit INT,
    id INT,
    domestic BOOLEAN,
    FOREIGN KEY (id) REFERENCES majors(id) ON DELETE CASCADE,
    PRIMARY KEY (year, id, domestic)
);

CREATE TABLE IF NOT EXISTS meta_data (
    id SERIAL,
    check_sum VARCHAR(64),
    success BOOLEAN,
    last_updated TIMESTAMP,
    PRIMARY KEY (id)
);