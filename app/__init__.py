from flask import Flask
from app import routes
from app.models import conn_cur, commit_and_close


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    routes.init_app(app)
    return app


#Criando tabela animes
conn, cur = conn_cur()
cur.execute("""
    CREATE TABLE IF NOT EXISTS animes (
        id              BIGSERIAL PRIMARY KEY,
        anime           VARCHAR(100) NOT NULL UNIQUE,
        released_date   DATE NOT NULL,
        seasons         INTEGER NOT NULL 
    );
""")
commit_and_close(conn, cur)