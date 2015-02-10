# datadog-conntrack

Quick hack [DataDog](https://github.com/DataDog/) agent check for conntrack
metrics.

Place [conntrack.py](conntrack.py) in `/etc/dd-agent/checks.d/` and
[conntrack.yaml](conntrack.yaml) in `/etc/dd-agent/conf.d/` and
`service datadog-agent restart`.

