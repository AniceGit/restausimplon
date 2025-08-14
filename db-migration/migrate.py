from sqlalchemy import create_engine, MetaData, Table
import pandas as pd

# Connexion SQLite (fichier local)
sqlite_engine = create_engine("sqlite:///./restausimplon.db")

# Connexion PostgreSQL (via Docker exposé en local)
postgres_engine = create_engine("postgresql://myuser:mypassword@localhost:5432/mydatabase")

# Lire toutes les tables SQLite
metadata = MetaData()
metadata.reflect(bind=sqlite_engine)

for table_name in metadata.tables:
    print(f"Migration de la table : {table_name}")
    df = pd.read_sql_table(table_name, sqlite_engine)
    df.to_sql(table_name, postgres_engine, if_exists="replace", index=False)

print("Migration terminée.")
