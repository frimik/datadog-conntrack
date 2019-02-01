"""
Linux conntrack metrics (AWS NAT Instance)
"""

import subprocess as sp
import re
from checks import AgentCheck


class Conntrack(AgentCheck):

    def check(self, instance):
        snapshot_limit = self.init_config.get('snapshot_limit', None)
        conntrack_info = self._get_sysctl_metrics()
        for metric, value in conntrack_info.iteritems():
            metric_key = "system.net.nf.%s" % (metric)
            self.gauge(metric_key, value)
            if (
                snapshot_limit and metric == 'conntrack_count' and
                int(value) > int(snapshot_limit)
            ):
                self._save_conntrack(value=int(value),
                                     limit=int(snapshot_limit))

    def _get_sysctl_metrics(self):
        max = sp.Popen(['cat', '/proc/sys/net/netfilter/nf_conntrack_max'],
                       stdout=sp.PIPE, close_fds=True).communicate()[0]

        count = sp.Popen(['cat', '/proc/sys/net/netfilter/nf_conntrack_count'],
                         stdout=sp.PIPE, close_fds=True).communicate()[0]
        conntrack_info = {
            "conntrack_max": max,
            "conntrack_count": count
        }
        return conntrack_info

    def _save_conntrack(self, value, limit):
        import time
        import commands
        from tempfile import mkstemp
        timestr = time.strftime("%Y%m%d-%H%M%S")
        _prefix = 'conntrack-%s-' % timestr
        tmpfile = mkstemp(suffix='.txt', prefix=_prefix)[1]

        conntrack = commands.getstatusoutput('sudo conntrack -L')
        with open(tmpfile, "w") as tempfile:
            tempfile.write(conntrack[1])
        _message_title = (
            "NAT: Conntrack entries (%d) exceeded limit (%d)"
            " - sample saved to '%s'."
        ) % (value, limit, tmpfile)
        self.event({
            'timestamp': int(time.time()),
            'msg_title': _message_title,
            'event_type': 'nat_conntrack_entries',
        })
        self.log.info(_message_title)
