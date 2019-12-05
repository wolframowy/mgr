db.hmdb_metabolite.update({"spectra.spectrum":{$exists:true}},{$pull:{"spectra.spectrum":{"type":/^.*\:\:(?!MsMs).*$/}}},{multi:true})
db.hmdb_metabolite.createIndex( { id: 1 }, { name: "Primary key" } )
db.hmdb_spectra.createIndex( { id: 1 }, { name: "Primary key" } )

