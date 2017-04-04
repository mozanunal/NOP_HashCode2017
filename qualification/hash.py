
class scoring:
    def __init__(self,video,score):
       self.video= video
       self.score = score
    def __lt__(self, other):
         return self.score > other.score + 5 
         
class connection:
    def __init__(self,ep,cacheNum,latency):
        self.ep = ep
        self.cacheNum = cacheNum
        self.latency = latency

class video:
    def __init__(self, id , size):
        self.id = id
        self.size = size

class cache:
    def __init__(self, id , capacity):
        self.id = id
        self.capacity = capacity
        self.videos = []
        self.endpoints = []

    def addVideo(self,video):
        if self.capacity >= video.size: 
            self.videos.append(video)
            self.capacity = self.capacity - video.size
            return True
        else:
            return False
        

class endpoint:
    def __init__(self,id,latencyDataC,connectionNumber):
        self.id = id 
        self.latencyDataC= latencyDataC
        self.connections = []
        self.requests = [] 

class request:
    def __init__(self,reqNumber, videoID, endpointID,count):
        self.reqNumber = reqNumber
        self.videoID = videoID
        self.endpointID = endpointID
        self.count = count


class solver:
    def __init__(self, file):
        self.videos = []
        self.eps = []
        self.requests = []
        self.caches= []
        f = open(file, 'r')
        fline = f.readline()
        [V, E, R, C, X] = fline.split(' ')
        self.videoCount = int(V)
        for indexC in range(0,int(C)):
            c = cache(indexC, int(X))
            self.caches.append(c)
        fline = f.readline()
        for index, size in enumerate(fline.split(' ')):
            v = video(index,int(size))
            self.videos.append(v)
        for currentEpID in range(0,int(E)):
            fline = f.readline()
            [latencyDataC, connectionNumber] = fline.split(' ')
            ep = endpoint(currentEpID,int(latencyDataC),int(connectionNumber))
            self.eps.append(ep)
            for i in range(0,int(connectionNumber)):
                [cNUm,latency] = f.readline().split(' ')
                c = connection(ep,int(cNUm),int(latency))
                ep.connections.append(c)
                self.caches[int(cNUm)].endpoints.append(self.eps[currentEpID])
        for curReqId in range(0,int(R)):
            [reqVideoID,reqEpID,reqCount] = f.readline().split(' ')
            r = request(curReqId,int(reqVideoID),int(reqEpID),int(reqCount))
            self.requests.append(r)
            self.eps[int(reqEpID)].requests.append(r)


    def getvideosofcache(self,cache):
        #print "cache id:", cache,
        scoreList = []
        for i in self.videos:
            s = scoring(i,0)
            scoreList.append(s)
        for ep in cache.endpoints:
            for req in ep.requests:
                curLat = self.getlatency(cache,ep)
                score = (req.count*(ep.latencyDataC-curLat))
                #print "videoid : ", req.videoID, "ep: ", ep.id, "req count", req.count, "dc latiency: ", ep.latencyDataC, "connect latency",curLat, "puan", score)
                scoreList[req.videoID].score += score
                #print "videoid : ", req.videoID, scoreList[req.videoID].score
        scoreList.sort()
        #for a in scoreList:
            #print a.video.id, a.score, a.video.size
        return scoreList

    def getlatency(self,cache,endpoint):
        ali = 0
        for i in endpoint.connections:
            if i.cacheNum == cache.id:
                ali = i.latency
                break
        return ali

    def solve(self):
        for curCache in self.caches:
            print curCache.id
            scoreList = mysolver.getvideosofcache(curCache)
            for curVideo in scoreList:
                if curVideo.score == 0:
                    break
                curCache.addVideo(curVideo.video)
    
    def result(self):
        result = str(len(self.caches))
        for curCache in self.caches:
            result += "\n"+str(curCache.id)  
            for curVideo in curCache.videos:
                result += " "+str(curVideo.id)
        #print result 
        file = open("videos_worth_spreading.txt","w")
        file.write(result)
        file.close()  



mysolver = solver('videos_worth_spreading.in')
mysolver.solve()
mysolver.result()
