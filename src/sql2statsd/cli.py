__title__ = "sql2statsd"
__version__ = "1.2.2"


import os
import click
import psycopg2
from statsd import StatsClient
from sql2statsd.utils import YamlFile, log


APP_DIR = click.get_app_dir(__title__)


def ensure_app_dir():
    try:
        log("Creating app dir...")
        os.makedirs(APP_DIR)
    except OSError as e:
        if e.errno == os.errno.EEXIST:
            log("{} already exists.", APP_DIR)
        else:
            raise


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
    ensure_app_dir()

    log("Started job execution.")
    log("Job: {}", job)

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

    log("Querying...")
    with conn, conn.cursor() as cur:
        cur.execute(job["query"])
        assert cur.rowcount == 1, "Query must return exactly one row."
        row = cur.fetchone()
        assert len(row) == 1, "Query must return exactly one column."
    log("Got result {}.", row[0])

    log("Sending stats...")
    statsd.gauge(job["stat"], row[0])

    log("Closing db connection...")
    conn.close()

    log("Finished job execution.")
