from math import sqrt
import numpy as np

#Plotting
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from JGO2017CoveringTree import CoveringTree
from JGO2017CoveringTree import Rect

class Example2GlobOpt(CoveringTree):

    def __init__(self, l0, l1_bounds, l2_bounds, idelta=0):
        # Initialize Base
        self.__l0 = l0
        # Initialize the Bounds
        self.__l1_bounds = l1_bounds
        self.__l2_bounds = l2_bounds
        # Define the Initial Rectangle P
        left = -self.__l1_bounds[1]-idelta
        top = 0-idelta
        width = self.__l1_bounds[1]+self.__l0+self.__l2_bounds[1]+2*idelta
        height = min(self.__l1_bounds[1], self.__l2_bounds[1])+2*idelta

        # Initialize algorithm parameters
        self.delta = idelta
        self.eps = self.getCurrentHalfL(Rect(left, top, width, height))*idelta
        # The CoveringTree class constructor
        CoveringTree.__init__(self, Rect(left, top, width, height), self.delta, self.eps)

    def drawRings(self, ax):
        #Example 2:
        #Initialize Base
        l0 = 6
        #Initialize the Bounds
        l1_bounds = [2, 12]
        l2_bounds = [6, 12]
        self.__ax.add_patch(patches.Circle((0, 0), l1_bounds[0], fill=False, lw=1, ls='dashed', color='black'))
        self.__ax.add_patch(patches.Circle((0, 0), l1_bounds[1], fill=False, lw=1, ls='dashed', color='black'))
        self.__ax.add_patch(patches.Circle((l0, 0), l2_bounds[0], fill=False, lw=1, ls='dashed', color='black'))
        self.__ax.add_patch(patches.Circle((l0, 0), l2_bounds[1], fill=False, lw=1, ls='dashed', color='black'))
        plt.draw()

    def g1(self, x):
        return x[0]**2.0 + x[1]**2.0 - (self.__l1_bounds[1]**2.0)

    def g2(self, x):
        return self.__l1_bounds[0]**2.0 - (x[0]**2.0) - (x[1]**2.0)

    def g3(self, x):
        return ((x[0] - self.__l0)**2.0) + (x[1]**2.0) - (self.__l2_bounds[1]**2.0)

    def g4(self, x):
        return self.__l2_bounds[0]**2.0 - ((x[0] - self.__l0)**2.0) - (x[1]**2.0)

    def g3m(self, x):
        return np.array([(x[0]**2.0) + (x[1]**2.0) - (self.__l2_bounds[1]**2.0)])

    def g4m(self, x):
        return np.array([self.__l2_bounds[0]**2.0 - (x[0]**2.0) - (x[1]**2.0)])

    def phi(self, x):
        return max(self.g1(x), self.g2(x), self.g3(x), self.g4(x))

    def objfunc(self, x):
        f = max(self.g1(x), self.g2(x), self.g3(x), self.g4(x))
        g = []

        fail = 0
        return f, g, fail

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
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2))-self.getCurrentHalfL(iBox)*iBox.diam

    def getCurrentHalfL(self, iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        #L = sup_{x in P}(||grad(phi(x))||)=sup_{x in P}(||grad(gi(x))||)
        return max(sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2),\
                   sqrt(max(abs(xmin-self.__l0), abs(xmax-self.__l0))**2 + max(abs(ymin), abs(ymax))**2))

    def getCurrentEps(self, iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        #L = sup_{x in P}(||grad(phi(x))||)=sup_{x in P}(||grad(gi(x))||)
        half_L = max(sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2),\
                     sqrt(max(abs(xmin-self.__l0), abs(xmax-self.__l0))**2 + max(abs(ymin), abs(ymax))**2))
        return half_L*iBox.diam

    def getCurrentCntrVal(self, iBox):
        xmin = iBox.left
        xmax = iBox.left + iBox.width
        ymin = iBox.top
        ymax = iBox.top + iBox.height

        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2))

    ############################################################################################
    # Global Optimization
    # with Predefined Accuracy (eps)
    ############################################################################################
    def getMinVal(self, xbounds, ybounds, diam):

        iBox = Rect(xbounds[0], ybounds[0], xbounds[1] - xbounds[0], ybounds[1] - ybounds[0])
        curBoxes = [iBox]
        lCntrs = [self.getCurrentCntrVal(iBox)]
        tempBoxes = []
        eps = self.getCurrentHalfL(iBox)*self.delta

        while curBoxes:
            for box in curBoxes:
                minorant = self.getCurrentMinVal(box)
                if minorant >= min(lCntrs) - eps:
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
        #g3(x1,x2)
        g3a1max = max(abs(xmin-self.__l0), abs(xmax-self.__l0))
        g3a2max = max(abs(ymin), abs(ymax))
        #g4(x1,x2)
        g4a1max = min(abs(xmin-self.__l0), abs(xmax-self.__l0))
        g4a2max = min(abs(ymin), abs(ymax))

        #MAXPHI(x) = MAXMAX(g1(x),g2(x),g3(x),g4(x)
        return max(self.g1((g1a1max, g1a2max)), self.g2((g2a1max, g2a2max)),\
                   self.g3m((g3a1max, g3a2max)), self.g4m((g4a1max, g4a2max)))

class Example2AppxLocL(CoveringTree):
    def __init__(self, l0, l1_bounds, l2_bounds, idelta=0):
        #Initialize Base
        self.__l0 = l0
        #Initialize the Bounds
        self.__l1_bounds = l1_bounds
        self.__l2_bounds = l2_bounds
        #Define the Initial Rectangle P
        left = -self.__l1_bounds[1]
        top = 0
        width = self.__l1_bounds[1]+self.__l0+self.__l2_bounds[1]
        height = min(self.__l1_bounds[1], self.__l2_bounds[1])

        CoveringTree.__init__(self, Rect(left, top, width, height), idelta)

    def drawRings(self, ax):
        #Example 2:
        #Initialize Base
        l0 = 6
        #Initialize the Bounds
        l1_bounds = [2, 12]
        l2_bounds = [6, 12]
        ax.add_patch(patches.Circle((0, 0), l1_bounds[0], fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((0, 0), l1_bounds[1], fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((l0, 0), l2_bounds[0], fill=False, lw=1, ls='dashed', color='black'))
        ax.add_patch(patches.Circle((l0, 0), l2_bounds[1], fill=False, lw=1, ls='dashed', color='black'))
        plt.draw()

    def g1(self, x):
        return x[0]**2.0 + x[1]**2.0 - (self.__l1_bounds[1]**2.0)

    def g2(self, x):
        return self.__l1_bounds[0]**2.0 - (x[0]**2.0) - (x[1]**2.0)

    def g3(self, x):
        return ((x[0] - self.__l0)**2.0) + (x[1]**2.0) - (self.__l2_bounds[1]**2.0)

    def g4(self, x):
        return self.__l2_bounds[0]**2.0 - ((x[0] - self.__l0)**2.0) - (x[1]**2.0)

    def phi(self, x):
        return max(self.g1(x), self.g2(x), self.g3(x), self.g4(x))

    def getMinVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #L = sup_{x in P}(||grad(phi(x))||)=sup_{x in P}(||grad(gi(x))||)
        half_L = max(sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2),\
                     sqrt(max(abs(xmin-self.__l0), abs(xmax-self.__l0))**2 + max(abs(ymin), abs(ymax))**2))

        #MINPHI(x) = MINMAX(g1(x),g2(x),g3(x),g4(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2))-half_L*diam

    def getMaxVal(self, xbounds, ybounds, diam):
        xmin = xbounds[0]
        xmax = xbounds[1]
        ymin = ybounds[0]
        ymax = ybounds[1]

        #L = sup_{x in P}(||grad(phi(x))||)=sup_{x in P}(||grad(gi(x))||)
        half_L = max(sqrt(max(abs(xmin), abs(xmax))**2 + max(abs(ymin), abs(ymax))**2),\
                     sqrt(max(abs(xmin-self.__l0), abs(xmax-self.__l0))**2 + max(abs(ymin), abs(ymax))**2))

        #MINPHI(x) = MINMAX(g1(x),g2(x),g3(x),g4(x)
        return self.phi(((xmin+xmax)/2, (ymin+ymax)/2)) + half_L*diam
