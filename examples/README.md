Launched as follows:
```bash
sql2statsd \
    --db-servers examples/db-servers.yaml \
    --statsd-servers examples/statsd-servers.yaml \
    examples/count-active-users.yaml
```

Or if you set env vars:
```bash
export SQL2STATSD_DB_SERVERS=examples/db-servers.yaml
export SQL2STATSD_STATSD_SERVERS=examples/statsd-servers.yaml
sql2statsd examples/count-active-users.yaml
```
