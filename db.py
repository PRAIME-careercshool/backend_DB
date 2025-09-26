import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)  # 경로 명시

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")

    print("[env check]",
          
          
          f"HOST={DB_HOST}, PORT={DB_PORT}, USER={DB_USER}, "
          f"PASS={'***' if DB_PASS else None}, DB={DB_NAME}, env_path={ENV_PATH}")

    missing = [k for k,v in {
        "DB_HOST": DB_HOST, "DB_PORT": DB_PORT, "DB_USER": DB_USER,
        "DB_PASS": DB_PASS, "DB_NAME": DB_NAME
    }.items() if not v]
    if missing:
        raise RuntimeError(f".env 로드 실패 또는 값 누락: {missing} (경로: {ENV_PATH})")

    DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

print("[DB_URL]", DB_URL.replace(os.getenv("DB_PASS") or "", "***"))

engine = create_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
