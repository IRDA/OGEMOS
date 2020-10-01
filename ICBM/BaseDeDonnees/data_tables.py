from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Boolean, Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

Base = declarative_base()


class FacteurClimatique(Base):
    __tablename__ = 'FacteurClimatique'
    utm = Column(Integer, primary_key=True)
    facteur_temperature_sol = Column(Float)
    facteur_humidite_sol = Column(Float)


class FacteurGroupeTextural(Base):
    __tablename__ = 'FacteurGroupeTextural'
    groupe_textural = Column(String, primary_key=True)
    coefficient_mineralisation_pool_jeune = Column(Float)
    coefficient_mineralisation_pool_stable = Column(Float)


class CoefficientDesResidusDeCulture(Base):
    __tablename__ = 'CoefficientDesResidusDeCulture'
    culture_principale = Column(String, primary_key=True)
    ratio_partie_recolte = Column(Float)
    ratio_partie_tige_non_recolte = Column(Float)
    ratio_partie_racinaire = Column(Float)
    ratio_partie_extra_racinaire = Column(Float)
    taux_carbone_chaque_partie = Column(Float)
    est_culture_fourragere = Column(Boolean)
    proportion_des_tiges_exportees = Column(Float)
    taux_matiere_seche = Column(Float)
    biomasse_aerienne_sur_racinaire = Column(Float)


class CoefficientAmendements(Base):
    __tablename__ = 'CoefficientAmendements'
    amendement = Column(String, primary_key=True)
    matiere_seche = Column(Float)  # % sur base humide
    carbon_nitrogen = Column(Float)
    nitrogen_total = Column(Float)
    est_amendement_originel_ogemos = Column(Boolean)


class FacteurTravailDuSol(Base):
    __tablename__ = 'FacteurTravailDuSol'
    travail_du_sol = Column(String, primary_key=True)
    facteur_travail_du_sol = Column(Float)


class CoefficientClasseDeDrainage(Base):
    __tablename__ = 'CoefficientClasseDeDrainage'
    classe_de_drainage = Column(String, primary_key=True)


class CoefficientDesCulturesSecondaires(Base):
    __tablename__ = 'CoefficientDesCulturesSecondaires'
    culture_secondaire = Column(String, primary_key=True)
    ratio_partie_recolte = Column(Float)
    ratio_partie_tige_non_recolte = Column(Float)
    ratio_partie_racinaire = Column(Float)
    ratio_partie_extra_racinaire = Column(Float)
    taux_carbone_chaque_partie = Column(Float)
    proportion_des_tiges_exportees = Column(Float)
    taux_matiere_seche = Column(Float)
    biomasse_aerienne_sur_racinaire = Column(Float)


class TableDesMunicipalites(Base):
    __tablename__ = 'TableDesMunicipalites'
    code_geographique_municipalite = Column(String)
    nom_municipalite = Column(String, primary_key=True)
    rendement_avoine = Column(Float)
    rendement_ble = Column(Float)
    rendement_mais_fourrager = Column(Float)
    rendement_orge = Column(Float)
    rendement_mais_grain = Column(Float)
    rendement_soya = Column(Float)
    rendement_haricot = Column(Float)
    rendement_pomme_de_terre_de_semence = Column(Float)
    rendement_pomme_de_terre_de_table = Column(Float)
    rendement_pomme_de_terre_de_transformation = Column(Float)
    rendement_seigle = Column(Float)
    rendement_triticale = Column(Float)
    rendement_foin = Column(Float)
    rendement_canola = Column(Float)
    utm_principal = Column(Integer, ForeignKey('FacteurClimatique.utm'))
    utm = relationship("FacteurClimatique")


class TablePercentile(Base):
    __tablename__ = 'TablePercentile'
    id = Column(Integer, Sequence('percentile_seq'), primary_key=True)
    utm = Column(Integer)
    groupe_textural = Column(String)
    percentile50 = Column(Float)
    percentile90 = Column(Float)
