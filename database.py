from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:TU_PASSWORD@db.xxx.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)