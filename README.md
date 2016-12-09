# datadog-conntrack

Quick hack [DataDog](https://github.com/DataDog/) agent check for conntrack
metrics.

Place [conntrack.py](conntrack.py) in `/etc/dd-agent/checks.d/` and
[conntrack.yaml](conntrack.yaml) in `/etc/dd-agent/conf.d/` and
`service datadog-agent restart`.

The sampling keeps a copy of the current conntrack entries after an event happened. Useful to track down the culprits (who are using all your sockets). If you want to use the sampling, it requires some fixing first.

## Requirements

Snapshot method (which saves a tmp file with the conntrack entries) requires the `conntrack` command available in the path + the datadog agent needs to have sudoers rights to do access conntrack (because command require CAP_NET_ADMIN capabilities).

The simplest way to allow dd-agent to be able to open conntrack is to add dd-agent group in sudoers
like bellow :

```
echo "%dd-agent ALL=(root)NOPASSWD: /usr/sbin/conntrack -L" >> /etc/sudoers
```

### Requirements (Fedora)

```
dnf install conntrack-tools
```

### Requirements (Ubuntu)

```
apt-get install conntrack-tools
```
