from ..app import app, db
from flask import render_template
from sqlalchemy import text
from ..models.nobility import CrrCarriere,IndIndividus,TypType6,RefDocuments

@app.route("/all_carrieres")
def all_carrieres():
    results = CrrCarriere.query.all()

    donnees = []
    
    for r in results: 
        donnees = []
        for carriere in results:
            #Récupération des individus associés dans une relation de carrière
            individu_1 = IndIndividus.query.get(carriere.IND_id_1)
            individu_2 = IndIndividus.query.get(carriere.IND_id_2)

            # Construction des données
            donnees.append({
              "nomIndividu_1": individu_1.IND_lignage if individu_1 else "Inconnu",
              "nomIndividu_2": individu_2.IND_lignage if individu_2 else "Inconnu",
             "Element_de_carriere": carriere.CRR_desc
            })
    
    return render_template("pages/toutes_carrieres.html", donnees=donnees, sous_titre="Toutes les carrieres")
