#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp

TDIR='xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'abc', """
uftrace file header: magic         = 4674726163652100
uftrace file header: version       = 4
uftrace file header: header size   = 40
uftrace file header: endian        = 1 (little)
uftrace file header: class         = 2 (64 bit)
uftrace file header: features      = 0x63
uftrace file header: info          = 0x3ff

reading 5231.dat
58348.873430946   5231: [entry] __monstartup(4004d0) depth: 0
58348.873433169   5231: [exit ] __monstartup(4004d0) depth: 0
58348.873439477   5231: [entry] __cxa_atexit(4004f0) depth: 0
58348.873440994   5231: [exit ] __cxa_atexit(4004f0) depth: 0
58348.873444506   5231: [entry] main(400512) depth: 0
58348.873444843   5231: [entry] a(4006b2) depth: 1
58348.873445107   5231: [entry] b(4006a0) depth: 2
58348.873445348   5231: [entry] c(400686) depth: 3
58348.873445830   5231: [entry] getpid(4004b0) depth: 4
58348.873447154   5231: [exit ] getpid(4004b0) depth: 4
58348.873448318   5231: [exit ] c(400686) depth: 3
58348.873448707   5231: [exit ] b(4006a0) depth: 2
58348.873448996   5231: [exit ] a(4006b2) depth: 1
58348.873449309   5231: [exit ] main(400512) depth: 0
""", sort='dump')

    def pre(self):
        record_cmd = '%s record -d %s %s' % (TestBase.ftrace, TDIR, 't-' + self.name)
        sp.call(record_cmd.split())
        return TestBase.TEST_SUCCESS

    def runcmd(self):
        return '%s dump -d %s' % (TestBase.ftrace, TDIR)

    def post(self, ret):
        sp.call(['rm', '-rf', TDIR])
        return ret

    def fixup(self, cflags, result):
        return result.replace("2 (64 bit)", "1 (32 bit)")
