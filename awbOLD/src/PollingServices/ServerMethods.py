import random as r

class ServerMethods:
    def initServerMethods(self, map):
            self.agentMap = map
            r.seed(a=None)
            self.randomized = True
            return True
    def getDataFromURL(ServerAdr,PagePath):
            http = httplib.HTTP(ServerAdr)
            http.putrequest('GET', PagePath)
            http.putheader('Accept', 'text/html')
            http.putheader('Accept', 'text/plain')
            http.endheaders()
            httpcode, httpmsg, headers = http.getreply()
            if httpcode != 200:
              raise "Could not get document: Check URL and Path."
            doc = http.getfile()
            data = doc.read()  # read file
            doc.close()
            return data
    def getGeneratedData(self, agent):
        i = r.randint(0,200)
        self.agentMap[agent] += i
        return self.agentMap[agent]

    def ReceiveData(self, data):
            print 'ReceiveData :', data
            return data
