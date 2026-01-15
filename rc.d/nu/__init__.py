import pandas as pd
import duckdb

class NuxDB:
    def __init__(self, con: duckdb.DuckDBPyConnection, relname: str):
        self.con = con
        self.relname = relname

    def __or__(self, f):
        if not callable(f):
            raise TypeError("Right-hand side of | must be callable")
        out = f(self)
        if not isinstance(out, NuxDB):
            raise TypeError("Pipe function must return NuxDB")
        return out

    def sql(self, query: str):
        # create a temp view for chaining
        name = f"v{abs(hash((self.relname, query)))%10**10}"
        self.con.execute(f'CREATE OR REPLACE TEMP VIEW "{name}" AS {query}')
        return NuxDB(self.con, name)

    def rel(self):
        return self.con.table(self.relname)

    def df(self):
        return self.rel().df()

    def __repr__(self):
        return repr(self.df())

def df_ls(path="."):
    from pathlib import Path
    import pwd, grp, stat

    rows = []
    for p in Path(path).iterdir():
        s = p.lstat()
        rows.append({
            "name": p.name,
            "type": "dir" if p.is_dir() else "file",
            "mode": stat.filemode(s.st_mode),
            "user": pwd.getpwuid(s.st_uid).pw_name,
            "group": grp.getgrgid(s.st_gid).gr_name,
            "size": s.st_size,
            "inode": s.st_ino,
            "path": str(p),
        })

    df = pd.DataFrame(rows)

    con = duckdb.connect(database=":memory:")
    con.register("ls", df)          # <-- no create/insert
    return NuxDB(con, "ls")

def select(*cols):
      cols_sql = ", ".join(f'"{c}"' for c in cols)
      return lambda db: db.sql(f'SELECT {cols_sql} FROM "{db.relname}"')

def where(expr: str):
    return lambda db: db.sql(f'SELECT * FROM "{db.relname}" WHERE {expr}')

def sort(col: str, desc=False):
    direction = "DESC" if desc else "ASC"
    return lambda db: db.sql(f'SELECT * FROM "{db.relname}" ORDER BY "{col}" {direction}')
