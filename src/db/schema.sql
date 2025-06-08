CREATE TYPE major_type AS ENUM('Major', 'Combined_Major', 'Honours', 'Combined_Honours');

-- There is instances such as "Chemical Biology" where the major id is different between the google sheet and their website
CREATE TABLE IF NOT EXISTS majors (
    uid SERIAL,
    name VARCHAR(255),
    id INT NOT NULL,
    type major_type NOT NULL,
    note TEXT,
    PRIMARY KEY (uid),
    UNIQUE(name, type)
);

CREATE TABLE IF NOT EXISTS admission_statistics (
    year INT,
    max_grade NUMERIC,
    min_grade NUMERIC,
    initial_reject INT,
    final_admit INT,
    uid INT,
    domestic BOOLEAN,
    FOREIGN KEY (uid) REFERENCES majors(uid) ON DELETE CASCADE,
    PRIMARY KEY (year, uid, domestic)
);

CREATE TABLE IF NOT EXISTS meta_data (
    id SERIAL,
    check_sum VARCHAR(64),
    success BOOLEAN,
    last_updated TIMESTAMP,
    PRIMARY KEY (id)
);