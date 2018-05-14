__title__ = "sql2statsd"
__version__ = "1.1.1"


import os
import yaml
import click
import psycopg2
from statsd import StatsClient


APP_DIR = click.get_app_dir(__title__)

try:
    os.makedirs(APP_DIR)
except OSError as e:
    if e.errno != os.errno.EEXIST:
        raise


class YamlFile(click.File):

    name = "yaml-file"

    def convert(self, value, param, ctx):
        f = super(YamlFile, self).convert(value, param, ctx)
        try:
            return yaml.load(f)
        except Exception as e:
            self.fail(e)


@click.command(context_settings={
    "auto_envvar_prefix": "SQL2STATSD",
    "help_option_names": ["-h", "--help"]
})
@click.option(
    "--db-servers",
    type=YamlFile(),
    default=os.path.join(APP_DIR, "db-servers.yaml"),
    show_default=True
)
@click.option(
    "--statsd-servers",
    type=YamlFile(),
    default=os.path.join(APP_DIR, "statsd-servers.yaml"),
    show_default=True
)
@click.argument(
    "job",
    type=YamlFile()
)
def main(db_servers, statsd_servers, job):
    """
    `sql2statsd` is a CLI utility that queries SQL database and posts results
    to StatsD based on provided YAML config files.
    """
    db_server = db_servers[job["db_server"]]
    conn = psycopg2.connect(
        host=db_server["host"],
        port=db_server["port"],
        user=db_server["user"],
        password=db_server["password"],
        dbname=job["db_name"]
    )

    statsd_server = statsd_servers[job["statsd_server"]]
    statsd = StatsClient(
        host=statsd_server["host"],
        port=statsd_server["port"]
    )

    with conn, conn.cursor() as cur:
        cur.execute(job["query"])
        assert cur.rowcount == 1, "Query must return exactly one row."

        row = cur.fetchone()
        assert len(row) == 1, "Query must return exactly one column."

    statsd.gauge(job["stat"], row[0])

    conn.close()
