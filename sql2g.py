import json
import click
import psycopg2
from statsd import StatsClient


def get_config(path):
    with open(path) as f:
        return json.load(f)


class DataBase(object):

    def __init__(self, host, port, username, password, database):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database
        )

    def __del__(self):
        self.conn.close()

    def aggregate(self, query):
        with self.conn as conn, conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchmany()
            if len(rows) == 1:
                cols = rows[0]
                if len(cols) == 1:
                    return cols[0]
                else:
                    raise ValueError("Query must return exactly one column.")
            else:
                raise ValueError("Query must return exactly one row.")


@click.command()
@click.option(
    "-d", "--db-config-path",
    type=click.Path(),
    required=True
)
@click.option(
    "-s", "--stats-config-path",
    type=click.Path()
)
@click.option(
    "-q", "--query",
    type=click.File(),
    required=True
)
@click.option(
    "-n", "--metric-name",
    required=True
)
def main(db_config_path, stats_config_path, query, metric_name):
    """
    Foo? Bar.
    """
    db_config = get_config(db_config_path)
    stats_config = get_config(stats_config_path)

    db = DataBase(
        host=db_config["HOST"],
        port=db_config["PORT"],
        username=db_config["USERNAME"],
        password=db_config["PASSWORD"],
        database=db_config["DATABASE"]
    )
    stats = StatsClient(
        host=stats_config["HOST"],
        port=stats_config["PORT"],
        prefix=stats_config.get("PREFIX")
    )

    rv = db.aggregate(query.read())
    stats.gauge(metric_name, rv)


if __name__ == "__main__":
    main()
