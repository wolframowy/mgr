mongoimport --db hmdb --collection hmdb_spectra --file hmdb_all_spectra.json --jsonArray
mongoimport --db hmdb --collection hmdb_metabolite --file hmdb_metabolites.json --jsonArray
powershell.exe -executionpolicy bypass mongo hmdb mongo_scripts_to_run.js