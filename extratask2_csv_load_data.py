import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# Define your ontology namespace
univ_ont = Namespace("http://www.semanticweb.org/sunanthakannan/ontologies/2024/3/university-ontology#")

# Load the CSV file
with open('university_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    g = Graph()

    for row in reader:
        # Create a new URI for each university
        university_uri = univ_ont[f"university/{row['name'].replace(' ', '_')}"]
        g.add((university_uri, RDF.type, univ_ont.University))
        g.add((university_uri, univ_ont.name, Literal(row['name'])))
        g.add((university_uri, univ_ont.abstract, Literal(row['abstract'])))
        g.add((university_uri, univ_ont.address, Literal(row['address'])))
        g.add((university_uri, univ_ont.numberOfStudents, Literal(row['numberOfStudents'], datatype=XSD.integer)))
        g.add((university_uri, univ_ont.numberOfSocialMediaFollowers, Literal(row['numberOfSocialMediaFollowers'], datatype=XSD.integer)))
        g.add((university_uri, univ_ont.facultySize, Literal(row['facultySize'], datatype=XSD.integer)))

        # President information
        president_uri = univ_ont[f"president/{row['presidentLabel'].replace(' ', '_')}"]
        g.add((president_uri, RDF.type, univ_ont.President))
        g.add((president_uri, univ_ont.presidentName, Literal(row['presidentLabel'])))
        g.add((university_uri, univ_ont.hasPresident, president_uri))

        # Chancellor information
        chancellor_uri = univ_ont[f"chancellor/{row['chancellorName'].replace(' ', '_')}"]
        g.add((chancellor_uri, RDF.type, univ_ont.Chancellor))
        g.add((chancellor_uri, univ_ont.chancellorName, Literal(row['chancellorName'])))
        g.add((chancellor_uri, univ_ont.chancellorBirthDate, Literal(row['chancellorBirthDate'], datatype=XSD.date)))
        g.add((chancellor_uri, univ_ont.chancellorBirthPlace, Literal(row['chancellorBirthPlace'])))
        g.add((university_uri, univ_ont.hasChancellor, chancellor_uri))

        # Location information
        state_uri = univ_ont[f"state/{row['stateName'].replace(' ', '_')}"]
        g.add((state_uri, RDF.type, univ_ont.State))
        g.add((state_uri, univ_ont.stateName, Literal(row['stateName'])))
        g.add((state_uri, univ_ont.capitalName, Literal(row['capitalName'])))
        g.add((university_uri, univ_ont.isLocatedIn, state_uri))

        # University Type
        type_uri = univ_ont[f"type/{row['typeLabel'].replace(' ', '_')}"]
        g.add((type_uri, RDF.type, univ_ont.TypeOfUniversity))
        g.add((type_uri, univ_ont.typeLabel, Literal(row['typeLabel'])))
        g.add((university_uri, univ_ont.isOfType, type_uri))

    # Save the RDF data to a file
    g.serialize(destination="university_populated_data.rdf", format="xml")
    print("RDF data generated and saved to 'university_populated_data.rdf'")
