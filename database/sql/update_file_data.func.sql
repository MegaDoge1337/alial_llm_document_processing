UPDATE filesdata 
SET docnumber = '@DOCNUMBER',
docdate = '@DOCDATE',
executor = '@EXECUTOR',
sum = '@SUM'
WHERE fileid = @FILEID;