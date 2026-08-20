from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_URI = "sqlite:///nutrition.sqlite"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_URI, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Food(Base):
    __tablename__ = "foods"

    fdc_id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    calories = Column(Float, nullable=True)
    protein_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)

    def to_dict(self):
        return {
            "fdc_id": self.fdc_id,
            "description": self.description,
            "calories": self.calories,
            "protein_g": self.protein_g,
            "fat_g": self.fat_g,
            "carbs_g": self.carbs_g,
            "fiber_g": self.fiber_g,
        }

    def __repr__(self):
        return f"<Food id={self.fdc_id} name='{self.description}' cal={self.calories}>"


def init_db():
    Base.metadata.create_all(bind=engine)
