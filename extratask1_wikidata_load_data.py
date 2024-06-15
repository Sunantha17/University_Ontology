# Now passing DBPedia Loaded Ontology into SPARQL query to merge another external source data from Wikidata

import rdflib
from SPARQLWrapper import SPARQLWrapper, RDFXML

# Reading existing dbpedia loaded RDF data from the ontology file
existing_graph = rdflib.Graph()
existing_graph.parse("dbpedia_loaded_university_ontology.owl", format="xml")

# Setting up the Wikidata SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(RDFXML)

# CONSTRUCT query to fetch data and build an RDF graph based on your ontology
# Included address and number of social media followers field while populating data from wikidata which is not present in DBpedia
sparql.setQuery("""
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX ex: <http://www.semanticweb.org/sunanthakannan/ontologies/2024/3/university-ontology#>

CONSTRUCT {
  ?university rdf:type ex:University.
  ?university ex:name ?universityName.
  ?university ex:numberOfStudents ?numberOfStudents.
  ?university ex:abstract ?abstract.
  ?university ex:facultySize ?facultySize.
  ?university ex:address ?address. 
  ?university ex:numberOfSocialMediaFollowers ?followers.

  ?university ex:hasPresident ?president.
  ?president ex:isPresident ?university.
  ?university ex:hasChancellor ?chancellor.
  ?chancellor ex:chancellorOf ?university.
  ?university ex:isLocatedIn ?location.
  ?university ex:isOfType ?type.


  ?president rdf:type ex:President.
  ?president ex:presidentLabel ?presidentName.

  ?chancellor rdf:type ex:Chancellor.
  ?chancellor ex:chancellorLabel ?chancellorName.
  ?chancellor ex:chancellorBirthDate ?chancellorBirthDate.
  ?chancellor ex:chancellorBirthPlace ?chancellorBirthPlace.

  ?location rdf:type ex:State.
  ?location ex:stateName ?stateName.
  ?location ex:capitalName ?capitalName.

  ?type rdf:type ex:TypeOfUniversity.
  ?type ex:typeLabel ?typeLabel.


}
WHERE {
  ?university wdt:P31 wd:Q3918; # Wikidata item for "university"
  OPTIONAL { ?university rdfs:label ?universityName FILTER (LANG(?universityName) = "en") }
  OPTIONAL { ?university wdt:P2196 ?numberOfStudents }
  OPTIONAL { ?university schema:description ?abstract FILTER (LANG(?abstract) = "en") }
  OPTIONAL { ?university wdt:P3342 ?facultySize }
  OPTIONAL { ?university wdt:P6375 ?address }
  OPTIONAL { ?university wdt:P8687 ?followers }

  OPTIONAL {
    ?university wdt:P35 ?president .
    ?president rdfs:label ?presidentName FILTER (LANG(?presidentName) = "en")
  }

  OPTIONAL {
    ?university wdt:P35 ?chancellor .
    ?chancellor rdfs:label ?chancellorName FILTER (LANG(?chancellorName) = "en")
    OPTIONAL { ?chancellor wdt:P569 ?chancellorBirthDate }
    OPTIONAL { ?chancellor wdt:P19 ?chancellorBirthPlace FILTER (LANG(?chancellorBirthPlace) = "en") }
  }

  OPTIONAL {
    ?university wdt:P131 ?location .
    ?location wdt:P1448 ?stateName FILTER (LANG(?stateName) = "en")
    OPTIONAL {
      ?location wdt:P36 ?capital .
      ?capital rdfs:label ?capitalName FILTER (LANG(?capitalName) = "en")
    }
  }

  OPTIONAL {
    ?university wdt:P31 ?typeEntity .
    ?typeEntity rdfs:label ?typeLabel FILTER (LANG(?typeLabel) = "en")
  }


}
LIMIT 100

""")

rdf_data = sparql.query().convert()
fetched_graph = rdflib.Graph()
fetched_graph.parse(data=rdf_data.serialize(format="xml"), format="xml")

# Merge the existing graph and fetched graph
merged_graph = existing_graph + fetched_graph

# Serialize and save the merged graph to a file
with open("university_ontology_populated_data.owl", "wb") as rdf_file:
  rdf_file.write(merged_graph.serialize(format="xml").encode('utf-8'))