from ..app import app, db

class IndIndividus(db.Model):
    __tablename__="IndIndividus"
    IND_id=db.Column(db.Integer,primary_key=True)
    IND_sexe=db.Column(db.Text)
    IND_prenom=db.Column(db.Text)
    IND_lignage=db.Column(db.Text)
    NUM_lignage=db.Column(db.Text)
    IND_surnom=db.Column(db.Text)
    IND_dat_naissance=db.Column(db.Text)
    IND_dat_naiss_approx_1=db.Column(db.Text)
    IND_dat_naiss_approx_2=db.Column(db.Text)
    IND_dat_deces=db.Column(db.Text)
    IND_dat_deces_approx_1=db.Column(db.Text)
    IND_dat_deces_approx_2=db.Column(db.Text)
    IND_dat_decs_desc=db.Column(db.Text)
    IND_dat_deb_apparition=db.Column(db.Text)
    IND_dat_fin_apparition=db.Column(db.Text)
    IND_inhumation=db.Column(db.Text)
    IND_naiss_lieu=db.Column(db.Text)
    IND_deces=db.Column(db.Text)
    IND_origine_geo=db.Column(db.Text)
    IND_mariage=db.Column(db.Text)
    IND_documentation=db.Column(db.Text)
    IND_comm=db.Column(db.Text)

class CrrCarriere(db.Model):
    __tablename__="crrcarriere"
    CRR_id=db.Column(db.Integer,primary_key=True)
    IND_id_1=db.Column(db.Integer, db.ForeignKey('IndIndividus.IND_id'), primary_key=True)
    IND_id_2=db.Column(db.Integer, db.ForeignKey('IndIndividus.IND_id'), primary_key=True)
    TYP_type_6=db.Column(db.Integer,db.ForeignKey('typtype6.TYP_id_6'), primary_key=True)
    REF_id=db.Column(db.Integer,db.ForeignKey('refdocuments.REF_id'), primary_key=True)
    CRR_dat_deb=db.Column(db.Text)
    CRR_dat_fin=db.Column(db.Text)
    CRR_lib=db.Column(db.Text)
    CRR_desc=db.Column(db.Text)
    CRR_comment=db.Column(db.Text)
    CRR_fiab=db.Column(db.Integer)


#Relations avec d'autres individus (les patrons des institutions où se déroule la carrière) via la table carriere
relation_carriere_sortante = db.relationship(
    "CrrCarriere",
    foreign_keys=[CrrCarriere.IND_id_1],
    primaryjoin="IndIndividus.IND_id == CrrCarriere.IND_id_1",
    backref="ind_individus_sortante",
    lazy="dynamic"
    )

relation_carriere_entrante = db.relationship(
    "CrrCarriere",
    foreign_keys=[CrrCarriere.IND_id_2],
    primaryjoin="IndIndividus.IND_id == CrrCarriere.IND_id_2",
    backref="ind_individus_entrante",
    lazy="dynamic"
    )
#relations entre les champs  
references = db.relationship(
        'refdocuments', 
        backref='references',
        lazy='dynamic'
        )

class TypType6(db.Model):
    __tablename__="typtype6"
    TYP_id_6=db.Column(db.Integer, primary_key=True)
    TYP_groupe=db.Column(db.Text)
    TYP_sous_groupe=db.Column(db.Text)
    TYP_lib=db.Column(db.Text)
    TYP_fiab=db.Column(db.Integer)

#relations entre les champs
type_relation = db.relationship(
        'TypType6',
        foreign_keys=[TypType6.TYP_id_6],
        backref='TypType6',
        lazy='dynamic'
        )
    
carrieres_nommages=db.relationship(
        'CrrCarriere',
        backref='carrieres_nommages',
        lazy='dynamic'
        )



class RefDocuments(db.Model):
    __tablename__="refdocuments"
    REF_id=db.Column(db.Integer, primary_key=True)
    REF_code=db.Column(db.Text)
    REF_fond=db.Column(db.Text)
    REF_classification=db.Column(db.Text)
    REF_desc=db.Column(db.Text)
    REF_comm=db.Column(db.Text)
    REF_transc=db.Column(db.Text)
    REF_trad=db.Column(db.Text)
    REF_date=db.Column(db.Text)
    REF_fiab=db.Column(db.Integer)

    #relations entre les champs
    relations= db.relationship(
        'CrrCarriere', 
        backref='relations',
        lazy='dynamic'
        )
