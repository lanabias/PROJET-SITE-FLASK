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

            #Récupération de la référence de la relation

            reference=RefDocuments.query.get(carriere.REF_id)

            #Récupération du type de relation
            type_relation=TypType6.query.get(carriere.TYP_type_6)


            # Construction des données
            if reference is not None:
              donnees.append({
                "nomIndividu_1": f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu",
                "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
                "Element_de_carriere": carriere.CRR_desc,
                "Référence_carriere": reference.REF_desc,
                "Type_carriere_groupe":f"{type_relation.TYP_groupes} e{type_relation.TYP_sous_groupes}",
                "Type_carriere_libelle":type_relation.TYP_lib
              })

            else:
            # Gérer le cas où la référence est manquante
              donnees.append({
                "nomIndividu_1": f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu",
                "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
                "Element_de_carriere": carriere.CRR_desc,
                "Référence_carriere": "Référence manquante",
                "Type_carriere_groupe":f"{type_relation.TYP_groupes} {type_relation.TYP_sous_groupes}",
                "Type_carriere_libelle":type_relation.TYP_lib
            })
    
    return render_template("pages/toutes_carrieres.html", donnees=donnees, sous_titre="Toutes les carrieres")
