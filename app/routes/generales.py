import requests
from ..app import app, db
from flask import render_template,request,flash,redirect, url_for
from sqlalchemy import text,or_,and_
from ..models.nobility import CrrCarriere,IndIndividus,TypType6,RefDocuments
from ..models.formulaire import Recherche

@app.route("/")
def accueil():
    return redirect(url_for("all_individus"))
"""
    Redirige l'url du serveur vers la page all_individus qui liste les individus de la base de données et constitue la page d'accueil.
    
    Args:
        racine du site.
      
    
    Returns:
        l'url appelée par la root définie par la fonction all_individus.
  """

@app.route("/all_individus")
@app.route("/all_individus/")
def all_individus():
    
    """
    définit la fonction qui généère ensuite le contenu de la rout affichant la liste de tous les individus de la base de données.
    
    Args:
        aucun

    Fonction : 
       - construit le dictionnaire des données pour chaque individu trouvé dans la table des individus IndIndividus : identifia,t; nom, numéro de lignage, dates de début et de fin d'apparition dans les textes
       - met en place une pagination des résultats trouvés avec 15 résultats par page
    
    Returns:
        l'url pages/individus.html appelée par la root définie par la fonction all_individus, avec transfert des données du dictionnaire construitp our chaque individu et le paramétrage de la pagination
    """

    page = request.args.get('page',1, type=int)
    pagination = IndIndividus.query.order_by(IndIndividus.IND_lignage).paginate(page=page,per_page=app.config["PER_PAGE"],error_out=False)
        
    donnees = []
    for item in pagination.items:
        donnees.append({
            "identifindividu": item.IND_id,
            "nomindividu": f"{item.IND_prenom} {item.IND_lignage}" if item else "Inconnu",
            "numindividu": item.NUM_lignage,
            "debappindividu": item.IND_dat_deb_apparition,
            "finappindividu":item.IND_dat_fin_apparition
        })
    return render_template("pages/individus.html", donnees=donnees, pagination=pagination, sous_titre="Tous les individus")

def search_wikidata(term, language="fr"):
  """
    Recherche un terme sur Wikidata et retourne le QID et l'URL du premier résultat.
    
    Args:
        term (str): Terme à rechercher.
        language (str): Langue de recherche (par défaut "fr").
    
    Returns:
        dict: Dictionnaire contenant le QID et l'URL, ou None si aucun résultat.
  """
  try:
      base_url = "https://www.wikidata.org/w/api.php"
      params = {
          "action": "wbsearchentities",
          "format": "json",
          "search": term,
          "language": language,
          "limit": 1  # Limite à un seul résultat
      }
      
      response = requests.get(base_url,params=params)
      response.raise_for_status()  # Vérifie si la requête a réussi
      data = response.json()
      print(data)
      # Récupérer le QID de la première réponse
      if 'search' in data and len(data['search']) > 0:
        first_result = data['search'][0]
        qid = first_result['id']
        url = f"https://www.wikidata.org/wiki/{qid}"
        return {"qid": qid, "url": url}
      else:
        return None  # Aucun résultat trouvé
  except requests.exceptions.RequestException as e:
      print(f"Erreur lors de la requête : {e}")
      return None


@app.route("/individus/<int:id_individu>")
def un_individu(id_individu):
  """
    définit la fonction qui affiche le contenu de la page pour un in individu particulier. Les éléments suivants sont fournis :
    - l'état civil de l'individu (numéro dans la base, naissance, mariage, décès, avec les estimations associées)
    - la documentation établie avec un lien de complément vers la page correspondante Wikidata quand elle existe
    - la liste des éléments de carrière de l'individu
    
    
    Args:
        id_individu : le numéro de l'individu dans la base de données, défini comme entier.

    Fonction : 
       - Recherche les informations de l'individu sur wikipedia et fournit l'url pour y parvenir
       - Recherche les éléments "relations_carrieres_sortantes" de la carrière de l'individu quand ils existent : le dictionnaire de données "carrieres_sortantes" est mis à jour pour chaque élément trouvé.
            Pour chaque élément de carrière trouvé sont stockés dans le dictionnaire :
            * le patron pour lequel l'individu travaille (Individu_2)
            * la description proprement dite de l'élément de carrière
            * la référence documentaire dans laquelle la relation est identifiée. Attention, la base de données est en migration, il est possible que tous les éléments de la table de référence ne soient pas remplis.
              (d'où la précaution : "if reference is not None:")
            * La catégorie et le type de relation de carrière
            * les dates de début et de fin de carrière
            L'affichage est réalisé dans l'ordre chronologique (tri par l"Date_debut"). Il n'y a pas de pagination pour cette page.

    
    Returns:
        l'url pages/un_individu.html est appelée par la route définie par la fonction un_individu, avec transfert des données du dictionnaire des informations sur létat civil, la documentation et la carrières quand cette dernière est connue
    """

  #Récupération de l'enregistrement des données sur l'identité de l'individu identifié par son identité
  individu_1 = IndIndividus.query.get(id_individu)
  
  # Rechercher un lien Wikipédia
  nom_complet=f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu"


  # Recherche sur Wikidata
  wikidata_result = search_wikidata(nom_complet)
  print(wikidata_result)
  if not wikidata_result:
    wikidata_search_url = f"https://www.wikidata.org/w/index.php?search={nom_complet.replace(' ', '+')}"
    wikidata_result = {'url': wikidata_search_url}
  
  carrieres_sortantes=[]
  
  relations_carrieres_sortantes=individu_1.relation_carriere_sortante.all()

  if relations_carrieres_sortantes:
    for carriere in relations_carrieres_sortantes:
      
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
    return render_template("pages/un_individu.html",donnee=individu_1,carrieres=carrieres_sortantes_triees,wikidata_result=wikidata_result,sous_titre=id_individu)
  else:
    return render_template("pages/un_individu.html",donnee=individu_1,sous_titre=id_individu)



@app.route("/all_carrieres")
@app.route("/all_carrieres/")
def all_carrieres():
  """
    définit la fonction qui génère ensuite le contenu de la route affichant la liste de tous les éléments de carrière contenus dans la base de données.
    
    Args:
        aucun

    Fonction : 
       - met en place une pagination des résultats trouvés avec 15 résultats par page
       - construit le dictionnaire des données pour chaque élément de carrière trouvé dans la table Crr_carriere impliquant :
          *deux individus individu1 et individu2 identifiés dans la table IndIndividus qui est en relation de type 1 vers n avec CrrCarriere. 
          *les dates de début et de fin de l'élément de carrière
          * la référence documentaire quand cette dernière existe
          * la catégorie et lelibellé du type d'élément de carrière.
        Les enregistremetns de la liste sont regroupés par type d'élément de carrière.
       
    
    Returns:
        l'url pages/toutes_carrieres.html appelée par la root définie par la fonction all_carrieres, avec transfert des données du dictionnaire des éléments de carrière et le paramétrage de la pagination
    """
  page = request.args.get('page',1, type=int)
  pagination = CrrCarriere.query.paginate(page=page,per_page=app.config["PER_PAGE"],error_out=False)
  
  donnees = []  
  for item in pagination.items:
    #Récupération des individus associés dans une relation de carrière
    individu_1 = IndIndividus.query.get(item.IND_id_1)
    individu_2 = IndIndividus.query.get(item.IND_id_2)

    #Récupération de la référence de la relation
    reference=RefDocuments.query.get(item.REF_id)

    #Récupération du type de relation
    type_relation=TypType6.query.get(item.TYP_type_6)

    # Construction des données
    if reference is not None:
      donnees.append({
        "idIndividu":individu_1.IND_id,
        "nomIndividu_1": f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu",
        "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
        "Date_debut": item.CRR_dat_deb,
        "Date_fin": item.CRR_dat_fin,
        "Element_de_carriere": item.CRR_desc,
        "Référence_carriere": reference.REF_desc,
        "Type_carriere_groupe":f"{type_relation.TYP_groupes} {type_relation.TYP_sous_groupes}",
        "Type_carriere_libelle":type_relation.TYP_lib
      })
    else:
      # Gérer le cas où la référence est manquante
      donnees.append({
        "idIndividu":individu_1.IND_id,
        "nomIndividu_1": f"{individu_1.IND_prenom} {individu_1.IND_lignage}" if individu_1 else "Inconnu",
        "nomIndividu_2": f"{individu_2.IND_prenom} {individu_2.IND_lignage}" if individu_2 else "Inconnu",
        "Date_debut": item.CRR_dat_deb,
        "Date_fin": item.CRR_dat_fin,
        "Element_de_carriere": item.CRR_desc,
        "Référence_carriere": "Référence manquante",
        "Type_carriere_groupe":f"{type_relation.TYP_groupes} {type_relation.TYP_sous_groupes}",
        "Type_carriere_libelle":type_relation.TYP_lib
      }) 
  donnees_triees = sorted(donnees, key=lambda x: x['Type_carriere_libelle'])
  return render_template("pages/toutes_carrieres.html", donnees=donnees_triees, pagination=pagination, sous_titre="Toutes les carrieres")

@app.route("/recherche", methods=['GET', 'POST'])
def recherche():
  """
    COnstruit un formulaire de recherche pour rechercher un individu par son nom de lignage et son nom de baptême.
    
    Args:
        aucun
    
    FOnction :
     - Récupère les informations de nom de lignage et de nom de baptême du formulaire rempli par l'utilisateur
     - Définit la requête dans la base de données en fonction de ces entrées
     - Remplit l'ensemble des objets IndIndividus qui constituent les enregistrements de la table INdINdividus qui correpsondent aux résultats associés à cette requête  
     - Remplit les inputs du formulaire des textes entrées par l'utilisateur    Returns:

    Returns   
      renvoie à l'url pages/resultats_recherche_individu.html la liste "données" des enregistrements trouvés et les mots-clés du formulaire remplis par l'utilisateur
      la procédure renvoie aussi l'absence d'information si rien n'est rempli dans le formulaire.
  """
  form = Recherche() 

    # initialisation des données de retour dans le cas où il n'y ait pas de requête
  donnees = []
  try:
    if form.validate_on_submit():
      # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
      nom_individu = request.form.get("nom_individu", None)
      nom_bapteme = request.form.get("nom_bapteme", None)
      
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
              
              donnees = query_results.order_by(IndIndividus.IND_dat_deb_apparition).all()

              # Renvoi des filtres de recherche pour préremplissage du formulaire
              form.nom_individu.data = nom_individu
              form.nom_bapteme.data = nom_bapteme
              
              flash("La recherche a été effectuée avec succès", "info")
              return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", donnees=donnees, form=form)
          
    else:
      flash("Veuillez remplir au moins un champ de recherche", "warning")

    # Si le formulaire n'a pas été soumis ou n'est pas valide, on affiche simplement le formulaire
    #return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", form=form)

  except Exception as e:
    print(f"Erreur détaillée : {str(e)}")  # Pour le débogage
    flash(f"La recherche a rencontré une erreur : {str(e)}", "error")
  return render_template("pages/resultats_recherche_individu.html", sous_titre="Recherche", form=form)



