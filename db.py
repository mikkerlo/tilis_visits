from sqlalchemy import Column, Integer, String, DateTime, Float, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()
engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)

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

    def __repr__(self) -> str:
        return f"Visiter(visiter_id={self.visiter_id}, name={self.name}, tg_id={self.tg_id}, donate_sum={self.donate_sum})"


class Visit(Base):
    __tablename__ = "visit"
    visit_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    total_payment = Column(Float, default=0)
    visiters = relationship("Visiter", secondary=visit_visiter)
    tg_message_id = Column(Integer)

    def __repr__(self) -> str:
        return f"Visit(visit_id={self.visit_id}, date={self.date}, total_payment={self.total_payment}, tg_message_id={self.tg_message_id})"

Base.metadata.create_all(engine)
