from math import sqrt

from JGO2017CoveringTree import CoveringTree
from JGO2017CoveringTree import Rect

#Plotting
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Example1GlobOpt(CoveringTree):

    def __init__(self, idelta=0):
        # The Initial Rectangle P definition
        left = -1.5
        top = -1.5
        width = 3.0
        height = 3.0

        # The algorithm parameters initialization
        self.delta = idelta
        self.eps = self.getCurrentHalfL(Rect(left, top, width, height))*idelta
        self.halfL = self.getCurrentHalfL(Rect(left, top, width, height))

        # The CoveringTree class constructor
        CoveringTree.__init__(self, Rect(left, top, width, height), self.delta, self.eps)

    def drawRings(self, ax):
        #Example 1:
        ax.add_patch(patches.Circle((0, 0), 1, fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((0, 0), 0.999, fill=False, lw=1, ls='dashed', color='black'))
        plt.draw()
    @staticmethod
    def g2(x):
        return x[0]**2.0 + x[1]**2.0 - 1
    @staticmethod
    def g1(x):
        return 0.999**2 - x[0]**2.0 - x[1]**2.0

    def phi(self, x):
        return max(self.g1(x), self.g2(x))

    ############################################################################################
    # Global Optimization
    #
    ############################################################################################
    @staticmethod
    def splitCurrentBox(iBox):
        def vSplitter(iBox):
            newleft1 = iBox.left
            newtop1 = iBox.top
            newwidth1 = iBox.width/2.0
            newheight1 = iBox.height
            Rleft = Rect(newleft1, newtop1, newwidth1, newheight1)

            newleft2 = iBox.left + iBox.width/2.0
            newtop2 = iBox.top
            newwidth2 = iBox.width/2.0
            newheight2 = iBox.height
            Rright = Rect(newleft2, newtop2, newwidth2, newheight2)
            return Rleft, Rright

        def hSplitter(iBox):
            newleft1 = iBox.left
            newtop1 = iBox.top
            newwidth1 = iBox.width
            newheight1 = iBox.height/2.0
            Rleft = Rect(newleft1, newtop1, newwidth1, newheight1)

            newleft2 = iBox.left
            newtop2 = iBox.top + iBox.height/2.0
            newwidth2 = iBox.width
            newheight2 = iBox.height/2.0
            Rright = Rect(newleft2, newtop2, newwidth2, newheight2)
            return Rleft, Rright

        if iBox.height > iBox.width:
            return hSplitter(iBox)
        else:
            return vSplitter(iBox)

    def getCurrentMinVal(self, iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        #MINPHI(x) = MINMAX(g1(x),g2(x),g3(x),g4(x)
        return self.phi(((xmin+xmax)/2.0, (ymin+ymax)/2.0))-self.halfL*iBox.diam
    @staticmethod
    def getCurrentHalfL(iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        #L = sup_{x in P}(||grad(phi(x))||)=sup_{x in P}(||grad(gi(x))||)
        return sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2)

    def getCurrentCntrVal(self, iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        return self.phi(((xmin+xmax)/2.0, (ymin+ymax)/2.0))

    ############################################################################################
    # Global Optimization
    # with Predefined Accuracy (eps)
    ############################################################################################
    def getMinVal(self, xbounds, ybounds, diam):

        iBox = Rect(xbounds[0], ybounds[0], xbounds[1] - xbounds[0], ybounds[1] - ybounds[0])
        curBoxes = [iBox]
        lCntrs = [self.getCurrentCntrVal(iBox)]
        tempBoxes = []
        while curBoxes:
            for box in curBoxes:
                minorant = self.getCurrentMinVal(box)
                if minorant >= min(lCntrs) - self.eps:
                    continue

                lCntrs.append(self.getCurrentCntrVal(box))

                box1, box2 = self.splitCurrentBox(box)
                tempBoxes.append(box1)
                tempBoxes.append(box2)

            curBoxes = tempBoxes
            tempBoxes = []

        minVal = min(lCntrs)
        lCntrs = []

        return minVal

    def getMaxVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #MAX
        #g1(x1,x2)
        g1a1max = max(abs(xmin), abs(xmax))
        g1a2max = max(abs(ymin), abs(ymax))
        #g2(x1,x2)
        g2a1max = min(abs(xmin), abs(xmax))
        g2a2max = min(abs(ymin), abs(ymax))

        #MAXPHI(x) = MAXMAX(g1(x),g2(x)
        return max(self.g2((g1a1max, g1a2max)), self.g1((g2a1max, g2a2max)))

class Example1AppxGlobL(CoveringTree):

    def __init__(self, idelta=0):
        #Define the Initial Rectangle P
        left = -1.5
        top = -1.5
        width = 3.0
        height = 3.0
        #L = sup_{x in P}(||grad(phi(x))||)
        self.halfL = self.getCurrentHalfL(Rect(left, top, width, height))

        CoveringTree.__init__(self, Rect(left, top, width, height), idelta)

    def drawRings(self, ax):
            #Example 1:
        ax.add_patch(patches.Circle((0, 0), 1, fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((0, 0), 0.999, fill=False, lw=1, ls='dashed', color='black'))
        plt.draw()
    @staticmethod
    def phi(x):
        def g1(x):
            return x[0]**2.0 + x[1]**2.0 - 1

        def g2(x):
            return 0.999**2.0 - x[0]**2.0 - x[1]**2.0

        return max(g1(x), g2(x))
    @staticmethod
    def getCurrentHalfL(iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        return sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2)

    def getMinVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #MINPHI(x) = MINMAX(g1(x),g2(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2))-self.halfL*diam

    def getMaxVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #MINPHI(x) = MINMAX(g1(x),g2(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2)) + self.halfL*diam

class Example1AppxLocL(CoveringTree):

    def __init__(self, idelta=0):
        #Define the Initial Rectangle P
        left = -1.5
        top = -1.5
        width = 3.0
        height = 3.0

        CoveringTree.__init__(self, Rect(left, top, width, height), idelta)

    def drawRings(self, ax):
            #Example 1:
        ax.add_patch(patches.Circle((0, 0), 1, fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((0, 0), 0.999, fill=False, lw=1, ls='dashed', color='black'))
    @staticmethod
    def phi(x):
        def g1(x):
            return x[0]**2.0 + x[1]**2.0 - 1

        def g2(x):
            return 0.999**2.0 - x[0]**2.0 - x[1]**2.0

        return max(g1(x), g2(x))

    def getMinVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #L = sup_{x in P}(||grad(phi(x))||)
        half_L = sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2)
        #MINPHI(x) = MINMAX(g1(x),g2(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2))-half_L*diam

    def getMaxVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #L = sup_{x in P}(||grad(phi(x))||)
        half_L = sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2)
        #MINPHI(x) = MINMAX(g1(x),g2(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2)) + half_L*diam
