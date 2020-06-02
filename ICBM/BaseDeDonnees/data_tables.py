from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String

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


class CoefficientDesAmendements(Base):
    __tablename__ = 'CoefficientAmendements'
    amendement = Column(String, primary_key=True)
    pourcentage_matiere_seche = Column(Float)
    coefficient_mineralisation_amendement = Column(Float)  # pourcentage %
