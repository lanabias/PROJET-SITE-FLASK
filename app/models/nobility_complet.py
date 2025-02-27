from ..app import app, db

Crr_carriere= db.Table(
    "crr_carriere",
    db.Column('ind.IND_id_1', db.Integer, db.ForeignKey('ind.IND_id_1'),primary_key=True),
    db.Column('target', db.Integer, db.ForeignKey('ind.IND_id_2'),primary_key=True),
    db.Column('TYP_type_6',db.Integer,db.ForeignKey('TYP_type_6'),primary_key=True),
    db.Column('REF_id',db.Integer,db.ForeignKey('REF_id'),primary_key=True),
    db.Column('CRR_dat_deb',db.Text),
    db.Column('CRR_dat_fin',db.Text),
    db.Column('CRR_lib',db.Text),
    db.Column('CRR_desc',db.Text),
    db.Column('CRR_comment',db.Text),
    db.Column('CRR_fiab',db.Integer)
)

Rli_relations_individus=db.Table(
    "rli_relations_individus",
    db.Column('ind.IND_id_1', db.Integer, db.ForeignKey('ind.IND_id_1'),primary_key=True),
    db.Column('ind.IND_id_2', db.Integer, db.ForeignKey('ind.IND_id_2'),primary_key=True),
    db.Column('TYP_type_0',db.Integer,db.ForeignKey('TYP_type_0'),primary_key=True),
    db.Column('REF_id',db.Integer,db.ForeignKey('REF_id'),primary_key=True),
    db.Column('RLI_dat_deb',db.Text),
    db.Column('RLI_dat_fin',db.Text),
    db.Column('RLI_lib',db.Text),
    db.Column('RLI_desc',db.Text),
    db.Column('RLI_comment',db.Text),
    db.Column('RLI_fiab',db.Integer)
)

class Typ_type_0(db. Model):
    __tablename__="typ_type_0"
    TYP_type_0=db.Column(db.String(10), primary_key=True),
    TYP_groupe=db.Column(db.Text),
    TYP_sous_groupe=db.Column(db.Text),
    TYP_lib=db.Column(db.Text),
    TYP_fiab=db.COlumn(db.Integer)


class Typ_type_6(db.Model):
    __tablename__="typ_type_6"
    TYP_type_6=db.Column(db.String(10), primary_key=True),
    TYP_groupe=db.Column(db.Text),
    TYP_sous_groupe=db.Column(db.Text),
    TYP_lib=db.Column(db.Text),
    TYP_fiab=db.COlumn(db.Integer)


class Ref(db.Model):
    __tablename__="ref"
    REF_id=db.Column(db.String(10), primary_key=True),
    REF_code=db.Column(db.Text),
    REF_fond=db.Column(db.Text),
    REF_classification=db.Column(db.Text),
    REF_desc=db.Column(db.Text),
    REF_comm=db.Column(db.Text),
    REF_transc=db.Column(db.Text),
    REF_trad=db.Column(db.Text),
    REF_date=db.Column(db.Text),
    REF_fiab=db.Column(db.INteger)


class Ind(db.Model):
    __tablename__="ind"
    IND_id=db.Column(db.String(10), primary_key=True),
    IND_sexe=db.Column(db.Text),
    IND_prenom=db.Column(db.Text),
    IND_lignage=db.Column(db.Text),
    NUM_lignage=db.Column(db.Text),
    IND_surnom=db.Column(db.Text),
    IND_dat_naissance=db.Column(db.Text),
    IND_dat_naiss_approx_1=db.Column(db.Text),
    IND_dat_naiss_approx_2=db.Column(db.Text),
    IND_dat_deces=db.Column(db.Text),
    IND_dat_deces_approx_1=db.Column(db.Text),
    IND_dat_deces_approx_2=db.Column(db.Text),
    IND_dat_decs_desc=db.Column(db.Text),
    IND_dat_deb_apparition=db.Column(db.Text),
    IND_dat_fin_apparition=db.Column(db.Text),
    IND_inhumation=db.Column(db.Text), 
    IND_naiss_lieu=db.Column(db.Text), 
    IND_deces=db.Column(db.Text), 
    IND_origine_geo=db.Column(db.Text), 
    IND_mariage=db.Column(db.Text), 
    IND_documentation=db.Column(db.Text), 
    IND_comm=db.Column(db.Text), 
    IND_inhumation=db.Column(db.Integer)

#Relations avec d'autres individus (les patrons des institutions où se déroule la carrière) via la table carriere
    relation_carriere=db.relationship( 
        'Ind',
        secondary=Crr_carriere,
        primaryjoin=id==Crr_carriere.c.ind.IND_id_1,
        secondaryjoin=id==Crr_carriere.c.ind.IND_id_2,
        backref='related to'
    )

#Relations avec d'autres individus (de type parenté, féodalité, économique,juridique) via la table RLI_relations_individus
    relation_individus=db.relationship( 
        'Ind',
        secondary=Rli_relations_individus,
        primaryjoin=id==Rli_relations_individus.c.ind.IND_id_1,
        secondaryjoin=id==Rli_relations_individus.c.ind.IND_id_2,
        backref='related to'
    )

#Problème : comment décrire les relations qui lient la table des références aux tables carrières et relation qui y sont citées ?
