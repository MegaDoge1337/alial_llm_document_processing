CREATE TABLE documentsets (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(255) NOT NULL, 
    importguid VARCHAR(255) NOT NULL
)