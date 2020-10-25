from threading import Thread
import EnterInSystem
from raitRemont import rate_room
from multiprocessing.dummy import Pool as ThreadPool

class ren_tread (Thread):
    def __init__(self, db, apId, photos):
        Thread.__init__(self)
        self.db = db
        self.Ap = apId
        self.photos = photos

    def run(self):
        print("try: " + str(self.Ap))
        try:
            ren = rate_room(self.photos)
            self.db.push_ren(self.Ap, ren)
            print("done: " + str(self.Ap))
        except:
            print("fail: " + str(self.Ap))
        # ren = rate_room(self.photos)
        # self.db.push_ren(self.Ap, ren)


db = EnterInSystem.createBd()
aps = db.pull_ap_ren()


# pool = ThreadPool(20)
# pool.map(ren_tread, db, aps[][0], aps[1])

n = 20
treds = []
for ap in aps:
    if len(treds) < n:
        tread = ren_tread(db, ap[0], ap[1].split())
        tread.start()
        treds.append(tread)
    else:
        for t in treds:
            t.join()
        treds = []

print("done")
