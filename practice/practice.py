

class pizza:

    def __init__(self, file):
        f = open(file, 'r')
        fline = f.readline()
        [R, C, L, H] = fline.split(' ')
        self.L = int(L)
        self.H = int(H)
        self.R = int(R)
        self.C = int(C)
        self.Matrix = []
        self.Matrix2 = []
        self.result = []
        self.resultS = []
        for index, line in enumerate(f):
            self.Matrix.append([])
            self.Matrix2.append([])
            for i in range(0, self.C):
                self.Matrix[index].append(line[i])
                self.Matrix2[index].append(False)

    def calculate(self):
        # print('Calculating')
        for i in range(0, self.R):
            for j in range(0, self.C):
                if self.Matrix2[i][j] is False:
                    self.trycreateSlice(i, j)
        
        for index,curSlice in enumerate(self.result):
            self.decommitResult(curSlice)
            for i in [3,2,1,0]:
                for j in [3,2,1,0]:
                    trySlice = slice(curSlice.r1, curSlice.c1, curSlice.r2 + i, curSlice.c2 + j)
                    if self.testSlice(trySlice) is True:
                        #print 'updated'
                        self.result[index].r1 = trySlice.r1
                        self.result[index].c1 = trySlice.c1
                        self.result[index].r2 = trySlice.r2
                        self.result[index].c2 = trySlice.c2
                        for i in range(trySlice.r1, trySlice.r2 + 1):
                            for j in range(trySlice.c1, trySlice.c2 + 1):
                                self.Matrix2[i][j] = True
                        break
        

    def trycreateSlice(self, r, c):
        # print(r,c),'start'
        for i in range(0, 15):
            for j in range(0, 15):
                trySlice = slice(r, c, r + i, c + j)
                if self.testSlice(trySlice) is True:
                    # print 'finded'
                    self.commitResult(trySlice)
                    break
        return (r, c)

    def testSlice(self, slice):
        test = False
        if (((slice.r2 - slice.r1 + 1) * (slice.c2 - slice.c1 + 1)) > self.H) | ((slice.r2 + 1) > self.R) | ((slice.c2 + 1) > self.C):
            # print '>boundries'
            a = 5
        else:
            tNum, mNum = self.getNumbers(slice)
            avaible = self.getAvaible(slice)
            if avaible is True:
                if(mNum >= self.L) & (tNum >= self.L):
                    test = True
            else:
                # print 'not Avaible'
                a = 5
        return test

    def getAvaible(self, slice):
        avaible = True
        for i in range(slice.r1, slice.r2 + 1):
            for j in range(slice.c1, slice.c2 + 1):
                if self.Matrix2[i][j] == True:
                    avaible = False
        return avaible

    def getNumbers(self, slice):
        tNum = 0
        mNum = 0
        for i in range(slice.r1, slice.r2 + 1):
            for j in range(slice.c1, slice.c2 + 1):
                if self.Matrix[i][j] == 'T':
                    tNum += 1
                elif self.Matrix[i][j] == 'M':
                    mNum += 1
        return tNum, mNum

    def commitResult(self, slice):
        self.result.append(slice)
        # print 'done',str(r1)+" "+str(c1)+" "+str(r2)+" "+str(c2)
        for i in range(slice.r1, slice.r2 + 1):
            for j in range(slice.c1, slice.c2 + 1):
                self.Matrix2[i][j] = True

    def decommitResult(self, slice):
        # print 'done',str(r1)+" "+str(c1)+" "+str(r2)+" "+str(c2)
        for i in range(slice.r1, slice.r2 + 1):
            for j in range(slice.c1, slice.c2 + 1):
                self.Matrix2[i][j] = False

    def convertRestultString(self):
        for slice in self.result:
            self.resultS.append(str(slice.r1) + " " + str(slice.c1) +
                           " " + str(slice.r2) + " " + str(slice.c2))    

    def printSucces(self):  
        trueC = 0
        falseC = 0
        for i in range(0, self.R):
            for j in range(0, self.C):
                if self.Matrix2[i][j] == True:
                    trueC += 1
                else:
                    falseC += 1
        print "Score: ", trueC, " / ", trueC+falseC

class slice:
    def __init__(self,r1,c1,r2,c2):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2


mypizza = pizza('medium.in')
# print mypizza.Matrix
# print mypizza.Matrix2
mypizza.calculate()
mypizza.convertRestultString()
s = str(len(mypizza.resultS))+"\n"
for res in mypizza.resultS:
    s += res + "\n"
file = open("medium.txt","w")
file.write(s)
file.close()


mypizza.printSucces()
