<a name="ds-genericmetadatajson"> </a>

# Generic Geographic data for Uralic languages as CLDF dataset derived from Rantanen et al. "Geographical database of the Uralic languages"

**CLDF Metadata**: [Generic-metadata.json](./Generic-metadata.json)

This dataset provides geographic point coordinates as well as speaker areas as GeoJSON MultiPolygons in WGS84 for Uralic languages. It has been derived from the "Geographic database of the Uralic languages".

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Rantanen, Timo, Vesakoski, Outi, Ylikoski, Jussi, & Tolvanen, Harri. (2021). Geographical database of the Uralic languages (Version v1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4784188
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Generic](http://cldf.clld.org/v1.0/terms.rdf#Generic)
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/cldf-datasets/rantanenurageo
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/cldf-datasets/rantanenurageo/tree/24f8708">cldf-datasets/rantanenurageo 24f8708</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v4.4">Glottolog v4.4</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.8.5</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | rantanenurageo
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 154


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal` | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
`Branch` | `string` | 
`Language` | `string` | 
`Dialect` | `string` | 

## <a name="table-areascsv"></a>Table [areas.csv](./areas.csv)

Speaker areas are provided as GeoJSON MultiPolygons. Since these may be big (bigger than Python's default size limit for columns in CSV files, for example), this data is provided in a separate table to allow reading of the other language metadata without worrying about this.

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 127


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
`SpeakerArea` | `json` | Speaker area of the variety or language in the traditional time period.

