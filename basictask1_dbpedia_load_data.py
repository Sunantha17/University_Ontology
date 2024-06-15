import rdflib
from SPARQLWrapper import SPARQLWrapper, RDFXML

# Read existing RDF data from the ontology file
existing_graph = rdflib.Graph()
existing_graph.parse("university_ontology.owl", format="xml")

# Set up the DBpedia SPARQL endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setReturnFormat(RDFXML)

# CONSTRUCT query to fetch data and build an RDF graph based on your ontology
sparql.setQuery("""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX ex: <http://www.semanticweb.org/sunanthakannan/ontologies/2024/3/university-ontology#>

CONSTRUCT {
   ?university rdf:type ex:University .
   ?university ex:name ?universityName .
   ?university ex:numberOfStudents ?numberOfStudents .
   ?university ex:abstract ?abstract .
   ?university ex:facultySize ?facultySize .

   ?university ex:hasPresident ?president .
   ?president  ex:isPresidentOf ?university .
   ?university ex:isLocatedIn ?state .
   ?university ex:isOfType ?type .
   ?university ex:hasChancellor ?chancellor .
   ?chancellor ex:chancellorOf ?university .

   ?chancellor rdf:type ex:Chancellor .
   ?chancellor ex:chancellorName ?chancellorName .
   ?chancellor ex:chancellorBirthDate ?chancellorBirthDate .
   ?chancellor ex:chancellorBirthPlace ?chancellorBirthPlace .

    ?state rdf:type ex:State .
    ?state ex:stateName ?stateName .
    ?state ex:capitalName ?capitalName .

    ?type rdf:type ex:TypeOfUniversity .
    ?type ex:typeLabel ?typeOfUniversity .

    ?president rdf:type ex:President .
    ?president ex:presidentLabel ?presidentLabel .
}

WHERE {
  ?university rdf:type dbo:University ;
              rdfs:label ?universityName ;
              dbo:chancellor ?chancellor ;
              dbo:state ?state ;
              dbo:president ?president ;
              dbo:type ?type .

  OPTIONAL { ?university dbo:numberOfStudents ?numberOfStudents. }
  OPTIONAL { ?university dbo:facultySize ?facultySize . }
  OPTIONAL { ?university dbo:abstract ?abstract . }

  ?chancellor rdfs:label ?chancellorName .
  OPTIONAL { ?chancellor dbp:birthDate ?chancellorBirthDate . }
  OPTIONAL { ?chancellor dbp:birthPlace ?chancellorBirthPlace . }

  ?state rdfs:label ?stateName .
  OPTIONAL { ?state dbp:capital ?capitalName . }

  ?president rdfs:label ?presidentLabel .

  ?type rdfs:label ?typeOfUniversity .

  FILTER (LANG(?chancellorName) = "en")
  FILTER (LANG(?universityName) = "en")
  FILTER (LANG(?abstract) = "en")
  FILTER (LANG(?typeOfUniversity) = "en")
  FILTER (LANG(?stateName) = "en")
  FILTER (LANG(?capitalName) = "en")
  FILTER (LANG(?presidentLabel) = "en")

}
LIMIT 100

""")

rdf_data = sparql.query().convert()


fetched_graph = rdflib.Graph()
fetched_graph.parse(data=rdf_data.serialize(format="xml"), format="xml")


merged_graph = existing_graph + fetched_graph


with open("dbpedia_loaded_university_ontology.owl", "wb") as rdf_file:
    rdf_file.write(merged_graph.serialize(format="xml").encode('utf-8'))