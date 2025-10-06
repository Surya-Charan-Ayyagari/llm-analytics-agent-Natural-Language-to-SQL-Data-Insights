import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import re
load_dotenv()


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL is not set.")
        _engine = create_engine(url)
    return _engine


FORBID = ("UPDATE","DELETE","INSERT","ALTER","DROP","TRUNCATE","MERGE","GRANT","REVOKE")


def validate_select(sql: str) -> str:
    clean_sql = re.sub(r'--.*$', '', sql.lower(),flags=re.MULTILINE).removeprefix("```sql").removesuffix("```")
    if "select" not in clean_sql:
        raise ValueError("Query must be a SELECT.")
    for kw in FORBID:
        if kw.lower() in clean_sql:
            raise ValueError(f"Forbidden keyword detected: {kw}")
    return clean_sql



def run_sql(sql: str) -> pd.DataFrame:
    sql = validate_select(sql)
    print('sql:',sql)
    eng = get_engine()
    with eng.connect() as c:
        return pd.read_sql(text(sql), c)



def fetch_schema_catalog() -> dict:
    eng = get_engine()
    with eng.connect() as c:
        tables = c.exec_driver_sql("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public' AND table_type='BASE TABLE'
            ORDER BY table_name
        """).fetchall()
        catalog = {}
        for (tname,) in tables:
            cols = c.exec_driver_sql(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema='public' AND table_name=%s
                ORDER BY ordinal_position
                """, (tname,)
            ).fetchall()
            catalog[tname] = {"columns": [{"name":n, "type":dt} for n,dt in cols]}
        return catalog