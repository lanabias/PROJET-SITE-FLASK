from ..app import app, db
from flask import render_template,request,flash,redirect, url_for
from sqlalchemy import text,or_,and_
from ..models.nobility import CrrCarriere,IndIndividus,TypType6,RefDocuments
from ..models.formulaire import Recherche

@app.route("/")
def accueil():
    return redirect(url_for("all_individus"))


@app.route("/all_individus")
def all_individus():
  results=IndIndividus.query.all()

  donnees=[]
  for individu in results:
    #Récupération des individus de la liste
      individu_1=IndIndividus.query.get(individu.IND_id)  
    #Construction de la liste des individus de la base de données avec leurs attributs
      donnees.append({
        "identifindividu":individu_1.IND_id,
        "nomindividu": f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu"
      })
  return render_template("pages/individus.html", donnees=donnees, sous_titre="Tous les individus")


@app.route("/individus/<int:id_individu>")
def un_individu(id_individu):
  '''individu_1=IndIndividus.query.filter(IndIndividus.IND_id == id_individu)'''
  #Récupération de l'enregistrement des données sur l'identité de l'individu identifié par son identité
  individu_1 = IndIndividus.query.get(id_individu)
  
  carrieres_sortantes=[]
  
  relations_carrieres_sortantes=individu_1.relation_carriere_sortante.all()

  if relations_carrieres_sortantes:
    for carriere in relations_carrieres_sortantes:
      print(type(carriere))  # Vérifiez si c'est un objet ou un dictionnaire
      #Récupération de l'enregistrement du chef de faction qui est à l'autre bout de la relation de carrière avec individu_1
      individu_2 = IndIndividus.query.get(carriere.IND_id_2)

      #Récupération de l'enregistrement du type de relation de carrière
      type_relation = TypType6.query.get(carriere.TYP_type_6)

      #Récupération de la référence de la relation
      reference=RefDocuments.query.get(carriere.REF_id)
      
      # Construction des données
      if reference is not None:
        carrieres_sortantes.append({
          "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
          "Element_de_carriere": carriere.CRR_desc,
          "Référence_carriere": reference.REF_desc,
          "Type_carriere_groupe":f"{type_relation.TYP_groupes} e{type_relation.TYP_sous_groupes}",
          "Type_carriere_libelle":type_relation.TYP_lib,    
          "Date_debut": carriere.CRR_dat_deb,
          "Date_fin": carriere.CRR_dat_fin,
          "Description": carriere.CRR_lib
        })
      else:
        # Gérer le cas où la référence est manquante
        carrieres_sortantes.append({
          "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
          "Date_debut": carriere.CRR_dat_deb,
          "Date_fin": carriere.CRR_dat_fin,
          "Element_de_carriere": carriere.CRR_desc,
          "Référence_carriere": "Référence manquante",
          "Type_carriere_groupe":f"{type_relation.TYP_groupes} {type_relation.TYP_sous_groupes}",
          "Type_carriere_libelle":type_relation.TYP_lib,    
          "Description": carriere.CRR_lib
        })
    carrieres_sortantes_triees = sorted(carrieres_sortantes, key=lambda x: x['Date_debut'])
    return render_template("pages/un_individu.html",donnee=individu_1,carrieres=carrieres_sortantes_triees,sous_titre=id_individu)
  else:
    return render_template("pages/un_individu.html",donnee=individu_1,sous_titre=id_individu)



@app.route("/all_carrieres")
def all_carrieres():
  results = CrrCarriere.query.all()

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
        "Date_debut": carriere.CRR_dat_deb,
        "Date_fin": carriere.CRR_dat_fin,
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
        "Date_debut": carriere.CRR_dat_deb,
        "Date_fin": carriere.CRR_dat_fin,
        "Element_de_carriere": carriere.CRR_desc,
        "Référence_carriere": "Référence manquante",
        "Type_carriere_groupe":f"{type_relation.TYP_groupes} {type_relation.TYP_sous_groupes}",
        "Type_carriere_libelle":type_relation.TYP_lib
      }) 
  donnees_triees = sorted(donnees, key=lambda x: x['Type_carriere_libelle'])

  return render_template("pages/toutes_carrieres.html", donnees=donnees_triees, sous_titre="Toutes les carrieres")

@app.route("/recherche", methods=['GET', 'POST'])
def recherche():
  form = Recherche() 

    # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
  nom_individu =  (request.form.get("nom_individu", None))
  nom_bapteme =   (request.form.get("nom_bapteme", None))
      
    # initialisation des données de retour dans le cas où il n'y ait pas de requête
  donnees = []
  try:
    if form.validate_on_submit():
          nom_individu = form.nom_individu.data
          nom_bapteme = form.nom_bapteme.data
          
          # Si l'un des champs de recherche a une valeur, alors cela veut dire que le formulaire a été rempli et qu'il faut lancer une recherche 
          # dans les données
          
          if nom_individu or nom_bapteme:
              # Initialisation de la recherche
              query_results = IndIndividus.query

              # Application des filtres en fonction des champs remplis
              if nom_individu:
                  query_results = query_results.filter(IndIndividus.IND_lignage.ilike(f"%{nom_individu.lower()}%"))
              if nom_bapteme:
                  query_results = query_results.filter(IndIndividus.IND_prenom.ilike(f"%{nom_bapteme.lower()}%"))
              
              donnees = query_results.order_by(IndIndividus.IND_lignage).all()
              print(f"Résultats de la recherche : {donnees}")  # Pour le débogage

              # Renvoi des filtres de recherche pour préremplissage du formulaire
              form.nom_individu.data = nom_individu
              form.nom_bapteme.data = nom_bapteme
              
              flash("La recherche a été effectuée avec succès", "info")
              return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", donnees=donnees, form=form)
          
          else:
              flash("Veuillez remplir au moins un champ de recherche", "warning")

    # Si le formulaire n'a pas été soumis ou n'est pas valide, on affiche simplement le formulaire
    return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", form=form)

  except Exception as e:
    print(f"Erreur détaillée : {str(e)}")  # Pour le débogage
    flash(f"La recherche a rencontré une erreur : {str(e)}", "error")
  return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", form=form)
