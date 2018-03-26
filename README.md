# `sql2g`

`sql2g` is a CLI utility that queries SQL database and posts results to
Graphite via StatsD based on a provided YAML config file and a job name.


## Usage:
`sql2g` is intended to be run as a scheduled task (e.g. a `cron` job).

1. Create a YAML config file based on a config schema provided below.
2. Run `sql2g --config-file <CONFIG_FILE> <JOB_NAME>` where:
    - `<CONFIG_FILE>` is a path to your config.
    - `<JOB_NAME>` is a key in a `config["jobs"]` section.

_Hint:_
Passing config file path as a parameter each time is tedious, so you may want
to specify `SQL2G_CONFIG_FILE` env var instead.


## Config schema:

```yaml
db_servers:
    <str>:  # Database server name
        host: <str>
        port: <int>
        user: <str>
        password: <str>

stats_servers:
    <str>:  # Stats server name
        host: <str>
        port: <int>

jobs:
    <str>:  # Job name
        db_server: <str>  # Database server name
        db_name: <str>
        stats_server: <str>  # Stats server name
        stat: <str>
        query: <str>
```
