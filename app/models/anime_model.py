from . import conn_cur, commit_and_close
from psycopg2 import sql, IntegrityError


class Anime():
    anime_keys = ['anime', 'released_date', 'seasons']

    def __init__(self, fields):
        if type(fields) is tuple:
            self.id, self.anime, self.released_date, self.seasons = fields

        elif type(fields) is dict:
            for key in fields.keys():
                if key in Anime.anime_keys:
                    self.anime = str(fields['anime']).title()
                    self.released_date = fields['released_date']
                    self.seasons = fields['seasons']
                else:
                    if KeyError():
                        raise KeyError({
                            'available_keys': [key for key in Anime.anime_keys],
                            'wrong_keys_sent': [key for key in fields.keys() if key not in Anime.anime_keys]
                        })
                    raise IntegrityError()
    

    def create(self):
        conn, cur = conn_cur()

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        query_values = list(self.__dict__.values())

        cur.execute(query, query_values)

        anime_created = cur.fetchone()

        commit_and_close(conn, cur)

        return Anime(anime_created).__dict__


    @staticmethod
    def update_anime(anime_id, payload):
        if 'anime' in payload.keys():
            payload['anime'] = payload['anime'].title()

        conn, cur = conn_cur()

        cur.execute("""
                    SELECT * FROM animes WHERE id=(%s);
                """, (anime_id,))

        has_id = cur.fetchone()
        err_message = {}

        if has_id:
            err_message = {
                'available_keys': [key for key in Anime.anime_keys],
                'wrong_keys_sent': [key for key in payload.keys() if key not in Anime.anime_keys]
            }
        else:
            err_message = {'error': 'Not found'}
            raise KeyError(err_message)

        for key in payload.keys():
            if key in Anime.anime_keys:
                columns = [sql.Identifier(key) for key in payload.keys()]
                values = [sql.Literal(value) for value in payload.values()]
            raise KeyError(err_message)

        query = sql.SQL(
            """
                UPDATE 
                    animes
                SET 
                    ({columns}) = row({values}) 
                WHERE 
                    id={id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(anime_id), 
            columns=sql.SQL(",").join(columns), 
            values=sql.SQL(",").join(values),
        )

        cur.execute(query)

        updated_anime = cur.fetchone()

        commit_and_close(conn, cur)

        return Anime(updated_anime).__dict__


    @staticmethod
    def read_all():
        conn, cur = conn_cur()

        cur.execute("""
            SELECT * FROM animes;
        """)

        animes = cur.fetchall()

        commit_and_close(conn, cur)

        output = {'data': []}

        if animes:
            output['data'] = [Anime(anime).__dict__ for anime in animes]
        return output
    

    @staticmethod
    def read_by_id(anime_id):
        conn, cur = conn_cur()

        cur.execute("""
            SELECT * FROM animes WHERE id=(%s);
        """, (anime_id,))

        anime = cur.fetchone()

        commit_and_close(conn, cur)

        if anime:
            anime_found = {'data': [Anime(anime).__dict__]}
            return anime_found
        raise KeyError({'error': 'Not found'})
    

    @staticmethod
    def delete_anime(anime_id):
        conn, cur = conn_cur()

        query = """
            DELETE FROM
                animes
            WHERE
                id=(%s)
            RETURNING *
        """

        cur.execute(query, (anime_id,))

        deleted_anime = cur.fetchone()

        commit_and_close(conn, cur)

        if deleted_anime:
            return {}
        raise KeyError({'error': 'Not found'})