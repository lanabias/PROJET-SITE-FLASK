from ..app import app, db
from flask import render_template
from sqlalchemy import text
from ..models.nobility import CrrCarriere,IndIndividus,TypType6,RefDocuments

@app.route("/all_carrieres")
def all_carrieres():
    results = CrrCarriere.query.all()
    #print(results)
    for r in results:
        print(r )
        print(type(r))
        print(r.Individu_source_id)
        print(r.Individu_target_id)
        print(type(r.TYP_type_6))
    
    ''' donnees = []
    for carriere in CrrCarriere.query.all():
        donnees.append({
            "nomIndividu_1": "CrrCarriere.Individu_source_id",
            "nomIndividu_2":"CrrCarriere.Individu_target_id",
            "Element_de_carriere":"CrrCarriere.CRR_desc"
        })
    
    return render_template("pages/toutes_carrieres.html", donnees=donnees, sous_titre="Toutes les carrieres")'''
