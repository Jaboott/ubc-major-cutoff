CREATE TABLE AdmissionStatus (
    Year INT,
    MaxGrade DOUBLE,
    MinGrade DOUBLE,
    InitialReject INT,
    FinalAdmit INT,
    ID INT,
    FOREIGN KEY (ID) REFERENCES Major(ID),
    PRIMARY KEY (Year, ID)
);

CREATE TABLE Major (
    Name VARCHAR(255),
    ID INT NOT NULL,
    type ENUM('Combined', 'Honours', 'Major') NOT NULL,
    PRIMARY KEY (ID)
);