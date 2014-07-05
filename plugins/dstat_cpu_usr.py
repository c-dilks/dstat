class dstat_plugin(dstat):

    def __init__(self):
        import multiprocessing
        ncpu = multiprocessing.cpu_count()

        core_arr = []
        core_str = ''
        for i in range(ncpu):
            core_arr.append(str(i))
            core_str += ','+str(i)

        self.name = 'cpu'
        self.nick = tuple(core_arr)
        self.vars = core_arr
        self.type = 'p'
        self.width = 4
        self.scale = 34
        self.open('/proc/stat')
        self.cols = 1 
        self.cpulist = core_str.split(',')

    def discover(self, *objlist):
        ret = []
        for l in self.splitlines():
            if len(l) < 9 or l[0][0:3] != 'cpu': continue
            ret.append(l[0][3:])
        ret.sort()
        for item in objlist: ret.append(item)
        return ret


    def extract(self):
        for l in self.splitlines():
            if len(l) < 9: continue
            for name in self.vars:
                if l[0] == 'cpu' + name or ( l[0] == 'cpu' and name == 'total' ):
                    self.set2[name] = ( long(l[1]) + long(l[2]) + long(l[6]) + long(l[7]), long(l[3]), long(l[4]), long(l[5]), long(l[8]) )

        for name in self.vars:
            if sum(self.set2[name]) > sum(self.set1[name]):
                self.val[name] = 100.0 * (self.set2[name][0] - self.set1[name][0]) / (sum(self.set2[name]) - sum(self.set1[name]))
            else:
                self.val[name] = 0
#                    print >>sys.stderr, "Error: tick problem detected, this should never happen !"

        if step == op.delay:
            self.set1.update(self.set2)

