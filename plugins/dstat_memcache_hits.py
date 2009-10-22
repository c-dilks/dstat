### Dstat Display Memcache Hit Count plugin
### Displays the number of Memcache "get_hits" and "get_misses"
###
### Authority: dean.wilson@gmail.com

class dstat_memcache_hits(dstat):
    def __init__(self):
        self.name = 'Memcache Hits'
        self.type = 'd'
        self.width = 6
        self.scale = 50
        self.nick = ('Hit', 'Miss')
        self.vars = ('get_hits', 'get_misses')
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)

        self.init(self.vars, 1)

    def check(self):
        try:
            global memcache
            import memcache
        except:
            raise Exception, 'Plugin needs the memcache module.'
        return True

    def extract(self):
        stats = self.mc.get_stats()

        self.val['get_hits'] = int( stats[0][1]['get_hits'] )
        self.val['get_misses'] = int( stats[0][1]['get_misses'] )