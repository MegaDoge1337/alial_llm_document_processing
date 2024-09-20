CREATE TABLE prompts (
    id SERIAL PRIMARY KEY, 
    version INTEGER, 
    optype VARCHAR(255), 
    doctype INTEGER, 
    content TEXT,
    CONSTRAINT fk_doctypes 
    FOREIGN KEY (doctype) 
    REFERENCES doctypes(id) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE
)