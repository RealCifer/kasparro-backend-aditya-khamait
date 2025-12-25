from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from core.db import Base

Base = declarative_base()

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    price = Column(Float)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    source = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

class RawCoinGecko(Base):
    __tablename__ = "raw_coingecko"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    price = Column(Float)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class CSVAsset(Base):
    __tablename__ = "csv_assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    source = Column(String, default="csv")
    updated_at = Column(DateTime, default=datetime.utcnow)
