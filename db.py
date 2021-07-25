from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()
engine = create_engine("sqlite:///:memory:", echo=True)


class VisitVisiter(Base):
    __tablename__ = "vist_visiter"
    visit_id = Column(Integer, ForeignKey("visit.visit_id"), primary_key=True)
    visiter_id = Column(Integer, ForeignKey("visiter.visiter_id"), primary_key=True)
    paid = Column(Boolean)
    visiter = relationship("Visiter")
    visit = relationship("Visit")


class Visiter(Base):
    __tablename__ = "visiter"
    visiter_id = Column(Integer, primary_key=True)
    name = Column(String)
    tg_id = Column(Integer)


class Visit(Base):
    __tablename__ = "visit"
    visit_id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)
    total_payment = Column(Float)
