# datadog-conntrack

Quick hack [DataDog](https://github.com/DataDog/) agent check for conntrack
metrics.

Place [conntrack.py](conntrack.py) in `/etc/dd-agent/checks.d/` and
[conntrack.yaml](conntrack.yaml) in `/etc/dd-agent/conf.d/` and
`service datadog-agent restart`.

The sampling keeps a copy of the current conntrack entries after an event happened. Useful to track down the culprits (who are using all your sockets). If you want to use the sampling, it requires some fixing first.

## Requirements

Snapshot method (which saves a tmp file with the conntrack entries) requires the `conntrack` command available in the path + the datadog agent needs to either run as root or get the `NET_CAP_ADMIN` capability.

The only way I've found so far is to do it on the binary itself, even though I've tried with `pam_cap.so` / `capability.conf`... let me know if you find out how to make it happen:

```
setcap cap_net_admin=ep /usr/sbin/conntrack
```

### Requirements (Fedora)

```
dnf install conntrack-tools
```

### Requirements (Ubuntu)

```
apt-get install conntrack-tools
```
