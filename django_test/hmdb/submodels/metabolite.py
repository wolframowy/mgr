from djongo import models

"""*********************************
    Embedded and abstract models
*********************************"""


class SecondaryAccession(models.Model):

    accession = models.ListField('Accession')

    class Meta:
        abstract = True


class SynonymArray(models.Model):

    synonym = models.ListField('Synonym')

    class Meta:
        abstract = True


class AlternativeParents(models.Model):

    alternative_parent = models.ListField('Alternative Parent')

    class Meta:
        abstract = True


class SubstituentArray(models.Model):

    substituent = models.ListField('Substituent')

    class Meta:
        abstract = True


class ExternalDescriptorsArray(models.Model):

    external_descriptor = models.ListField('External descriptor')

    class Meta:
        abstract = True


class Taxonomy(models.Model):

    description = models.TextField('Description', max_length=1000)
    direct_parent = models.TextField('Direct parent', max_length=100)
    kingdom = models.TextField('Kingdom', max_length=100)
    super_class = models.TextField('Super class', max_length=100)
    main_class = models.TextField('Class', max_length=100)
    sub_class = models.TextField('Sub class', max_length=100)
    molecular_framework = models.TextField('Molecular framework', max_length=100)
    alternative_parents = models.EmbeddedModelField(
        model_container=AlternativeParents
    )
    substituents = models.EmbeddedModelField(
        model_container=SubstituentArray
    )
    external_descriptors = models.EmbeddedModelField(
        model_container=ExternalDescriptorsArray
    )

    class Meta:
        abstract = True


"""
    FOR TIME BEING ONTOLOGY IS OUT OF DATA. 
    REASON IS THAT THERE WAS CIRCULAR REFERENCE WHICH DJONGO DOESN'T SUPPORT
    
"""

# # Due to cross reference with OntologyRoot class is described here, and it's attribute is added later on
# class Descendant(models.Model):
#
#     descendant = models.ArrayModelField(
#         model_container=OntologyRoot
#     )
#
#     class Meta:
#         abstract = True
#
#
# class OntologyRoot(models.Model):
#
#     term = models.TextField('Term', max_length=100)
#     definition = models.TextField('Definition', max_length=1000)
#     parent_id = models.PositiveIntegerField('Parent ID')
#     level = models.PositiveSmallIntegerField('Level')
#     type = models.TextField('Type', max_length=50)
#     synonyms = models.TextField('Synonyms', max_length=50)
#     descendants = models.EmbeddedModelField(
#         model_container=Descendant
#     )
#
#     class Meta:
#         abstract = True
#
#
# class Ontology(models.Model):
#     root = models.ArrayModelField(
#         model_container=OntologyRoot
#     )
#
#     class Meta:
#         abstract = True


class Property(models.Model):

    kind = models.TextField('Kind', max_length=50)
    # value is a text field, because it's values sometimes contains symbol of unit of measurement
    value = models.TextField('Value', max_length=100)
    source = models.TextField('Source', max_length=100)

    class Meta:
        abstract = True


class PropertyArray(models.Model):

    property = models.ArrayModelField(
        model_container=Property
    )

    class Meta:
        abstract = True


class Spectrum(models.Model):

    type = models.TextField('Type', max_length=100)
    spectrum_id = models.PositiveIntegerField('Spectrum ID')

    class Meta:
        abstract = True


class SpectrumArray(models.Model):

    spectrum = models.ArrayModelField(
        model_container=Spectrum
    )

    class Meta:
        abstract = True


class Cellular(models.Model):

    cellular = models.ListField('Callular location')

    class Meta:
        abstract = True


class Biospecimen(models.Model):

    biospecimen = models.ListField('Biospecimen location')

    class Meta:
        abstract = True


class Tissue(models.Model):

    tissue = models.ListField('Tissue location')

    class Meta:
        abstract = True


class Pathway(models.Model):

    pathway = models.ListField('Pathway')

    class Meta:
        abstract = True


class BiologicalProperties(models.Model):

    cellular_locations = models.EmbeddedModelField(
        model_container=Cellular
    )
    biospecimen_locations = models.EmbeddedModelField(
        model_container=Biospecimen
    )
    tissue_locations = models.EmbeddedModelField(
        model_container=Tissue
    )
    pathways = models.EmbeddedModelField(
        model_container=Pathway
    )

    class Meta:
        abstract = True


class Reference(models.Model):

    reference_text = models.TextField('Reference text', max_length=1000)
    pubmed_id = models.IntegerField()

    class Meta:
        abstract = True


class ReferenceArray(models.Model):

    reference = models.ArrayModelField(
        model_container=Reference
    )

    class Meta:
        abstract = True


class Concentration(models.Model):

    biospecimen = models.TextField('Biospecimen', max_length=50)
    concentration_value = models.TextField('Concentration value', max_length=20)
    concentration_units = models.TextField('Concentration unit', max_length=10)
    subject_age = models.TextField('Subject Age', max_length=50)
    subject_sex = models.TextField('Subject Sex', max_length=20)
    subject_condition = models.TextField('Subject condition', max_length=50)
    subject_information = models.TextField('Subject information', max_length=50)
    comment = models.TextField('Comment', max_length=1000)
    references = models.EmbeddedModelField(
        model_container=ReferenceArray
    )

    class Meta:
        abstract = True


class Concentrations(models.Model):

    concentration = models.ArrayModelField(
        model_container=Concentration
    )

    class Meta:
        abstract = True


class Disease(models.Model):

    name = models.TextField('Name', max_length=200)
    omim_id = models.PositiveIntegerField('Omim ID', max_length=20)
    references = models.EmbeddedModelField(
        model_container=ReferenceArray
    )

    class Meta:
        abstract = True


class Diseases(models.Model):

    disease = models.ArrayModelField(
        model_container=Disease
    )

    class Meta:
        abstract = True


class Protein(models.Model):

    protein_accession = models.TextField('Protein accession', max_length=20)
    name = models.TextField('Name', max_length=50)
    uniprot_id = models.TextField('Uniprot ID', max_length=20)
    gene_name = models.TextField('Gene name', max_length=20)
    protein_type = models.TextField('Protein type', max_length=20)

    class Meta:
        abstract = True


class ProteinAssociations(models.Model):

    protein = models.ArrayModelField(
        model_container=Protein
    )

    class Meta:
        abstract = True


class Identifier(models.Model):

    name = models.TextField('Name', max_length=50)
    id = models.PositiveIntegerField('ID', max_length=20)

    class Meta:
        abstract = True


class ExternalLinks(models.Model):

    identifier = models.ArrayModelField(
        model_container=Identifier
    )

    class Meta:
        abstract = True


"""*********************************
    Main model
*********************************"""


class Metabolite(models.Model):

    version = models.TextField('Version', max_length=10)
    creation_date = models.DateTimeField('Creation date')
    update_date = models.DateTimeField('Update date')
    accession = models.TextField('Accession', max_length=20)
    secondary_accessions = models.EmbeddedModelField(
        model_container=SecondaryAccession, blank=True
    )
    name = models.TextField('Name', max_length=100)
    cs_description = models.TextField('CS description', max_length=1000)
    description = models.TextField('Description', max_length=1000)
    synonyms = models.EmbeddedModelField(
        model_container=SynonymArray, blank=True
    )
    chemical_formula = models.TextField('Chemical Formula', max_length=100)
    average_molecular_weight = models.FloatField('Average molecular weight')
    monisotopic_molecular_weight = models.FloatField('Monisotopic molecular weight')
    iupac_name = models.TextField('Iupac name', max_length=50)
    traditional_iupac = models.TextField('Traditional iupac name', max_length=50)
    cas_registry_number = models.TextField('Cas registry number', max_length=20)
    smiles = models.TextField('Smiles', max_length=50)
    inchi = models.TextField('Inchi', max_length=100)
    inchikey = models.TextField('Inchi Key', max_length=100)
    taxonomy = models.EmbeddedModelField(
        model_container=Taxonomy, blank=True
    )
    # Otology omited for time being as djongo doesn't work with circular reference
    # ontology = models.EmbeddedModelField(
    #     model_container=Ontology
    # )
    state = models.TextField('State', max_length=20)
    experimental_properties = models.EmbeddedModelField(
        model_container=PropertyArray, blank=True
    )
    predicted_properties = models.EmbeddedModelField(
        model_container=PropertyArray, blank=True
    )
    spectra = models.EmbeddedModelField(
        model_container=SpectrumArray, blank=True
    )
    biological_properties = models.EmbeddedModelField(
        model_container=BiologicalProperties, blank=True
    )
    normal_concentrations = models.EmbeddedModelField(
        model_container=Concentrations, blank=True
    )
    abnormal_concentrations = models.EmbeddedModelField(
        model_container=Concentrations, blank=True
    )
    diseases = models.EmbeddedModelField(
        model_container=Diseases, blank=True
    )
    kegg_id = models.TextField('Kegg ID', max_length=20)
    chebi_id = models.PositiveIntegerField('Chebi ID')
    chemspider_id = models.PositiveIntegerField('Chemspider ID')
    pubchem_compound_id = models.PositiveIntegerField('Pubchem compoud ID' )
    foodb_id = models.PositiveIntegerField('Foodb ID')
    drugbank_id = models.PositiveIntegerField('Drugbank ID')
    phenol_explorer_compound_id = models.PositiveIntegerField('Phenol explorer compound ID')
    meta_cyc_id = models.TextField('Meta cyc ID', max_length=20)
    wikipedia_id = models.TextField('Wikipedia ID', max_length=100)
    knapsack_id = models.TextField('Knapsack ID', max_length=20)
    bigg_id = models.PositiveIntegerField('Bigg ID')
    metlin_id = models.PositiveIntegerField('Metlin ID')
    pdb_id = models.TextField('PDB ID', max_length=20)
    synthesis_reference = models.TextField('Synthesis reference', max_length=1000)
    general_references = models.EmbeddedModelField(
        model_container=ReferenceArray, blank=True
    )
    protein_associations = models.EmbeddedModelField(
        model_container=ProteinAssociations, blank=True
    )

    biocyc_id = models.TextField('Biocyc_id', max_length=50, blank=True)
    biospecimen_locations = models.EmbeddedModelField(
        model_container=Biospecimen, blank=True
    )
    cellular_locations = models.EmbeddedModelField(
        model_container=Cellular, blank=True
    )
    tissue_locations = models.EmbeddedModelField(
        model_container=Tissue, blank=True
    )
    pathways = models.EmbeddedModelField(
        model_container=Pathway, blank=True
    )
    drugbank_metabolite_id = models.TextField('Drugbank metabolite ID', max_length=50)
    external_links = models.EmbeddedModelField(
        model_container=ExternalLinks, blank=True
    )
    # Het_id is null everywhere
    het_id = models.PositiveIntegerField('Het ID')
    # metagene is null everywhere
    # metagene = models.

    nugowiki = models.PositiveIntegerField('Nugowiki')

    # phenol_explorer_metabolite_id is null everywhere
    # phenol_explorer_metabolite_id = models.

    status = models.TextField('Status', max_length=50)
    wikipidia = models.TextField('Wikipidia', max_length=100)

    def __str__(self):
        return "Metabolite"
