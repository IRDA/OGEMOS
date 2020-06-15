from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Boolean

Base = declarative_base()


class FacteurClimatique(Base):
    __tablename__ = 'FacteurClimatique'
    region = Column(String, primary_key=True)
    utm = Column(String)
    facteur_temperature_sol = Column(Float)
    facteur_humidite_sol = Column(Float)


class FacteurSerieDeSol(Base):
    __tablename__ = 'FacteurSerieDeSol'
    serie_de_sol = Column(String, primary_key=True)
    coefficient_mineralisation_pool_jeune = Column(Float)
    coefficient_mineralisation_pool_vieux = Column(Float)


class CoefficientDesResidusDeCulture(Base):
    __tablename__ = 'CoefficientDesResidusDeCulture'
    culture_principale = Column(String, primary_key=True)
    ratio_partie_recolte = Column(Float)
    ratio_partie_tige_non_recolte = Column(Float)
    ratio_partie_racinaire = Column(Float)
    ratio_partie_extra_racinaire = Column(Float)
    taux_carbone_chaque_partie = Column(Float)
    coefficient_humidification_residus_culture = Column(Float)
    est_culture_fourragere = Column(Boolean)
    hproduit = Column(Float)
    htige = Column(Float)
    hracine = Column(Float)
    hextraracinaire = Column(Float)
    proportion_des_tiges_exportees = Column(Float)
    taux_matiere_seche = Column(Float)


class CoefficientDesAmendements(Base):
    __tablename__ = 'CoefficientAmendements'
    amendement = Column(String, primary_key=True)
    matiere_seche = Column(Float) #% sur base humide
    carbon_nitrogen = Column(Float)
    nitrogen_total = Column(Float)
    coefficient_humidification = Column(Float)


class FacteurTravailDuSol(Base):
    __tablename__ = 'FacteurTravailDuSol'
    travail_du_sol = Column(String, primary_key=True)
    facteur_travail_du_sol = Column(Float)


class CoefficientClasseDeDrainage(Base):
    __tablename__ = 'CoefficientClasseDeDrainage'
    classe_de_drainage = Column(String, primary_key=True)
