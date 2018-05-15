import yaml
import click
from datetime import datetime


LOG_FMT = "%Y-%m-%d %H:%M:%S,%f"


class YamlFile(click.File):

    name = "yaml-file"

    def convert(self, value, param, ctx):
        f = super(YamlFile, self).convert(value, param, ctx)
        try:
            return yaml.load(f)
        except Exception as e:
            self.fail(e)


def log(msg, *args, **kwargs):
    if args or kwargs:
        msg = msg.format(*args, **kwargs)
    timestamp = datetime.utcnow().strftime(LOG_FMT)
    msg = "{} - {}".format(timestamp, msg)
    click.echo(msg, err=True)
