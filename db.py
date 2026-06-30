from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# TiDB Cloud / MySQL Database URL
DATABASE_URL = "mysql+pymysql://3Mh7tvHQy1t2ykB.root:HhGft7bS4aZRx8QR@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()