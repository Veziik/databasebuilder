#databasebuilder

Project for a database class where we had to catalog a filesystem or entire domain, usage below:


Executable files and usage are as follows:
singlefile.py <url/filepath> -- creates a .sql script from the metadata of a single file, local or otherwise
domainscraper.py <domain homepage> -- searches through all of a domain's files and produces a .sql script
directory.py <domain homepage> -- searches through all of a filesystem's files and produces a .sql script
mergescripts.py -- merges all .sql files in the scripts folder


The program creates a scripts folder for all of the sql scripts it generates and places them into that folder

