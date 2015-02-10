"""
Linux conntrack metrics (AWS NAT Instance)
"""

import subprocess as sp
import re
from checks import AgentCheck


class Conntrack(AgentCheck):

    def check(self, instance):
        conntrack_info = self._get_sysctl_metrics()
        for metric, value in conntrack_info.iteritems():
            metric_key = "system.net.nf.%s" % (metric)
            self.gauge(metric_key, value)

    def _get_sysctl_metrics(self):
        sysctl = sp.Popen(['sysctl', 'net.netfilter.nf_conntrack_max',
                           'net.netfilter.nf_conntrack_count'],
                          stdout=sp.PIPE, close_fds=True).communicate()[0]
        #
        # net.netfilter.nf_conntrack_max = 1000000
        # net.netfilter.nf_conntrack_count = 56
        #
        lines = sysctl.split('\n')
        regexp = re.compile(r'^net\.netfilter\.nf_(\w+)\s+=\s+([0-9]+)')
        conntrack_info = {}
        for line in lines:
            try:
                match = re.search(regexp, line)
                if match is not None:
                    conntrack_info[match.group(1)] = match.group(2)
            except Exception:
                self.log.exception("Cannot parse %s" % (line,))

        return conntrack_info
