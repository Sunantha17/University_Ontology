import rdflib

# Loaded the updated RDF graph
rdf_file = "university_ontology_populated_data.owl"
graph = rdflib.Graph()
graph.parse(rdf_file, format="xml")

# Defining a SPARQL query to check the integrated data
query = """
PREFIX ex: <http://www.semanticweb.org/sunanthakannan/ontologies/2024/3/university-ontology#>
SELECT ?university ?name ?numberOfStudents ?abstract ?facultySize ?address ?followers ?presidentName ?chancellorName
WHERE {
    ?university rdf:type ex:University ;
                ex:name ?name .

    OPTIONAL { ?university ex:numberOfStudents ?numberOfStudents . }
    OPTIONAL { ?university ex:abstract ?abstract . }
    OPTIONAL { ?university ex:facultySize ?facultySize . }
    OPTIONAL { ?university ex:address ?address . }
    OPTIONAL { ?university ex:numberOfSocialMediaFollowers ?followers . }

    OPTIONAL { 
        ?university ex:hasPresident ?president .
        ?president ex:presidentLabel ?presidentName .
    }

    OPTIONAL {
        ?university ex:hasChancellor ?chancellor .
        ?chancellor ex:chancellorLabel ?chancellorName .
    }
}
LIMIT 50
"""

# Executing the query
results = graph.query(query)
print(f"Total records found: {len(results)}")
for row in results:
    print("University URI:", row["university"])
    print("Name:", row["name"])
    print("Number of Students:", row.get("numberOfStudents", "Not provided"))
    print("Abstract:", row.get("abstract", "Not provided"))
    print("Faculty Size:", row.get("facultySize", "Not provided"))
    print("Address:", row.get("address", "Not provided"))
    print("Social Media Followers:", row.get("followers", "Not provided"))
    print("President Name:", row.get("presidentName", "Not provided"))
    print("Chancellor Name:", row.get("chancellorName", "Not provided"))
    print()
