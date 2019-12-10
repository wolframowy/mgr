db.hmdb_metabolite.update({"spectra.spectrum":{$exists:true}},{$pull:{"spectra.spectrum":{"type":/^.*\:\:(?!MsMs).*$/}}},{multi:true})
db.hmdb_metabolite.createIndex( { id: 1 }, { name: "Primary key" } )
db.hmdb_spectra.createIndex( { id: 1 }, { name: "Primary key" } )
db.sequence.replaceOne({_id: 'hmdb_met_names_seq'},{_id: 'hmdb_met_names_seq', value: 1},{upsert:true})
db.hmdb_metabolite.aggregate([{$sort: {name: 1}},{$project: {met_id: "$id", name: 1}},{$out: "hmdb_met_names"}])
db.hmdb_met_names.find().forEach(function (row){
	var id = db.sequence.findAndModify({query:{_id: 'hmdb_met_names_seq'},
		update:	{$inc: {value:1}},
		new:true})
	db.hmdb_met_names.update({_id: row._id},
		{$set: {"id": id.value}})
})