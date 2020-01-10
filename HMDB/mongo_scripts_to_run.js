db.hmdb_metabolite.update({"spectra.spectrum":{$exists:true}},{$pull:{"spectra.spectrum":{"type":/^.*\:\:(?!MsMs).*$/}}},{multi:true})
db.hmdb_metabolite.createIndex( { id: 1 }, { name: "Primary key" } )
db.hmdb_spectra.createIndex( { id: 1 }, { name: "Primary key" } )
db.hmdb_metabolite.distinct('biological_properties.biospecimen_locations.biospecimen').forEach(function(elem){db.hmdb_biolocation.insert({name: elem})})
db.sequence.replaceOne({_id: 'hmdb_met_names_seq'},{_id: 'hmdb_met_names_seq', value: 1},{upsert:true})
db.hmdb_metabolite.aggregate([
	{$sort: {name: 1}},
	{$project: {met_id: "$id", name: 1, super_class: "$taxonomy.super_class",
				main_class: "$taxonomy.main_class", sub_class: "$taxonomy.sub_class",
				biospecimen_locations: "$biological_properties.biospecimen_locations.biospecimen",
				monisotopic_molecular_weight: {$toDouble: "$monisotopic_molecular_weight"}}},
	{$out: "hmdb_met_names"}
	],
	{allowDiskUse: true}
)
db.hmdb_met_names.find().forEach(function (row){
	var id = db.sequence.findAndModify({query:{_id: 'hmdb_met_names_seq'},
		update:	{$inc: {value:1}},
		new:true})
	db.hmdb_met_names.update({_id: row._id},
		{$set: {"id": id.value}})
})
db.hmdb_met_names.createIndex( { name: 1 }, { name: "Primary key" } )