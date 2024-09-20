CREATE TABLE files (
    id SERIAL PRIMARY KEY, 
    filename VARCHAR(255), 
    importguid VARCHAR(255), 
    status VARCHAR(255), 
    textlayer TEXT
)