from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_hunter_table = Table(
    "favorite_hunter_table",
    db.Model.metadata,
    Column("hunter_id", ForeignKey("hunter.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)

favorite_demon_table = Table(
    "favorite_demon_table",
    db.Model.metadata,
    Column("demon_id", ForeignKey("demon.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)

favorite_combatStyle_table = Table(
    "favorite_combatStyle_table",
    db.Model.metadata,
    Column("combat_style_id", ForeignKey("combat_style.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorite_hunter: Mapped[List["Hunter"]] = relationship(
        secondary=favorite_hunter_table, back_populates="favorited_by"
    )
    favorite_demon: Mapped[List["Demon"]] = relationship(
        secondary=favorite_demon_table, back_populates="favorited_by"
    )
    favorite_combatStyle: Mapped[List["CombatStyle"]] = relationship(
        secondary=favorite_combatStyle_table, back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password
        }

class Hunter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    favorited_by: Mapped[List["User"]] = relationship(
        secondary=favorite_hunter_table, back_populates="favorite_hunter"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

class Demon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    favorited_by: Mapped[List["User"]] = relationship(
        secondary=favorite_demon_table, back_populates="favorite_demon"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

class CombatStyle(db.Model):
    __tablename__ = "combat_style" 
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    favorited_by: Mapped[List["User"]] = relationship(
        secondary=favorite_combatStyle_table, back_populates="favorite_combatStyle"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }