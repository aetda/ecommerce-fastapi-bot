from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100, collation="utf8mb4_unicode_ci"))
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(255, collation="utf8mb4_unicode_ci"))
    category: Mapped[str] = mapped_column(String(50, collation="utf8mb4_unicode_ci"))

