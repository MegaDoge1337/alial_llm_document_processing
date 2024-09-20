CREATE TABLE filesdata (
    id SERIAL PRIMARY KEY, 
    fileid INTEGER, 
    doctype INTEGER, 
    docnumber VARCHAR(255), 
    docdate VARCHAR(255), 
    executor VARCHAR(255), 
    sum VARCHAR(255), 
    CONSTRAINT fk_files 
    FOREIGN KEY (fileid) 
    REFERENCES files(id) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
    CONSTRAINT fk_doctypes 
    FOREIGN KEY (doctype) 
    REFERENCES doctypes(id) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE
)