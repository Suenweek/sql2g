import yaml
import click


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
    click.echo(msg, err=True)
