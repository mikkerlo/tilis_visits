from sqlalchemy import Column, Integer, String, DateTime, Float, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

visit_visiter = Table(
    "visit_visiter",
    Base.metadata,
    Column("visit_id", ForeignKey("visit.visit_id")),
    Column("visiter_id", ForeignKey("visiter.visiter_id")),
)


class Visiter(Base):
    __tablename__ = "visiter"
    visiter_id = Column(Integer, primary_key=True)
    name = Column(String)
    tg_id = Column(Integer)
    visits = relationship("Visit", secondary=visit_visiter)
    donate_sum = Column(Integer)


class Visit(Base):
    __tablename__ = "visit"
    visit_id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)
    total_payment = Column(Float)
    visiters = relationship("Visit", secondary=visit_visiter)
