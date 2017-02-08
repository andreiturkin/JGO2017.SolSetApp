import abc
from math import sqrt
from ete3 import Tree
#Plotting
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#Images
from PIL import Image
# Date and Time
import datetime

class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.right = left + width
        self.top = top
        self.bottom = top + height
        self.width = width
        self.height = height
        self.centerx = left + width/2
        self.centery = top + height/2
        self.center = (left + width/2, top + height/2)
        self.diam = sqrt(self.width**2.0 + self.height**2.0)

    def getD(self, iRect):
        return self.diam

    def __str__(self):
        return '<Rect: {}, {}, {}, {}>'.format(self.left, self.top, self.width, self.height)

class CoveringTree:
############################################################################################
# Constructor
############################################################################################
    __metaclass__ = abc.ABCMeta
    def __init__(self, iRect, idelta=0, ieps=0):
        #Initialize initial Space where the workspace lie
        self.__Xspace = iRect
        #Initialize the minimal size of the rectangle
        self.__delta = idelta
        # Initialize the epsilon value
        self.__eps = ieps

    @abc.abstractmethod
    def getMaxVal(self, xbounds, ybounds, diam):
        raise NotImplementedError
    @abc.abstractmethod
    def getMinVal(self, xbounds, ybounds, diam):
        raise NotImplementedError
    @abc.abstractmethod
    def drawRings(self, ax):
        raise NotImplementedError
############################################################################################
# Private Members
############################################################################################
    def __vSplitter(self, iRect):
        newleft1 = iRect.left
        newtop1 = iRect.top
        newwidth1 = iRect.width/2.0
        newheight1 = iRect.height
        Rleft = Rect(newleft1, newtop1, newwidth1, newheight1)

        newleft2 = iRect.left + iRect.width/2.0
        newtop2 = iRect.top
        newwidth2 = iRect.width/2.0
        newheight2 = iRect.height
        Rright = Rect(newleft2, newtop2, newwidth2, newheight2)
        return Rleft, Rright

    def __hSplitter(self, iRect):
        newleft1 = iRect.left
        newtop1 = iRect.top
        newwidth1 = iRect.width
        newheight1 = iRect.height/2.0
        Rleft = Rect(newleft1, newtop1, newwidth1, newheight1)

        newleft2 = iRect.left
        newtop2 = iRect.top + iRect.height/2.0
        newwidth2 = iRect.width
        newheight2 = iRect.height/2.0
        Rright = Rect(newleft2, newtop2, newwidth2, newheight2)
        return Rleft, Rright

    def __analyseRect(self, iRect):

        xmin = iRect.left
        xmax = iRect.left + iRect.width
        ymin = iRect.top
        ymax = iRect.top + iRect.height

        inrange = False
        cont = True

        # Call an abstract method
        maxval = self.getMaxVal((xmin, xmax), (ymin, ymax), iRect.diam)
        #The whole rectangle is a part of the solution -> save it
        if maxval < -self.__eps:
            #mark it as in range
            inrange = True
            cont = False
            return cont, inrange

        # Call an abstract method
        minval = self.getMinVal((xmin, xmax), (ymin, ymax), iRect.diam)
        #There is no solution for the rectangle -> get rid of it
        if minval > self.__eps:
            #mark it as out of range
            inrange = False
            cont = False
            return cont, inrange

        #The rectangle should be processed further
        return cont, inrange

    def __addToTree(self, motherNode, iRect1, iRect2, childNodeLevel):
        # and add the nodes as children.
        oNode2 = motherNode.add_child(name='{}'.format(childNodeLevel))
        oNode1 = motherNode.add_child(name='{}'.format(childNodeLevel))
        #add features
        oNode2.add_feature('Rect', iRect2)
        oNode1.add_feature('Rect', iRect1)

    def __getNewRect(self, iRect, level):
        (oRleft, oRright) = self.__vSplitter(iRect) if (level%2 == 0) else self.__hSplitter(iRect)
        return (oRleft, oRright)

    def __initTree(self, Xspace):
        self.__sTree = Tree('0;') #name here is the level of the tree
        motherNode = self.__sTree.search_nodes(name='0')[0]
        motherNode.add_feature('Rect',Xspace)

    ########################################################################################
    # Plotting
    ########################################################################################
    def __drawRect(self, iRect, fillIt, inQI=False, inQE=True):
        #Internal
        if inQI and (not inQE):
            edgeColor = 'black'
            LineStyle='solid'
            LineWidth = 1
            Alpha=0.3
        #External
        if inQE and (not inQI):
            edgeColor = 'red'
            LineStyle='solid'
            LineWidth = 1
            Alpha=0.3
        #Out of range
        if (not inQE) and (not inQI):
            edgeColor = 'green'
            LineStyle='solid'
            LineWidth = 1
            Alpha=None
        self.__ax.add_patch(
                      patches.Rectangle(
                                        (iRect.left, iRect.top),   # (x,y)
                                        iRect.width,          # width
                                        iRect.height,         # height
                                        fill = inQI,
                                        alpha = Alpha,
                                        linestyle = LineStyle,
                                        edgecolor = edgeColor,
                                        lw = LineWidth)
                      )
#         plt.draw()

############################################################################################
# Public Members
############################################################################################
    def getSolution(self, maxLevels, saveasmovie=True):

        # Initialize the Root of the Tree and additional variables
        self.__initTree(self.__Xspace)
        cdRect = self.__Xspace.diam
        print 'The diameter of the initial box is {}'.format(cdRect)
        bExit = False
        nIter = 0

        for curLevel in range(0, maxLevels):
            #Get all the rectangles that are on some level of the tree
            curLevelNodes = self.__sTree.get_leaves_by_name(name='{}'.format(curLevel))
            #Loop over the rectangles
            for curLevelNode in curLevelNodes:
                nIter = nIter + 1
                #Get a rectangle from the tree level
                oRect = curLevelNode.Rect
                #Save current rectangle diameter
                if oRect.diam < cdRect:
                    cdRect = oRect.diam
                inQE = False
                inQI = False
                #The diameter of the rectangle is less than or equal to the predefined delta value
                if oRect.diam <= self.__delta:
                    #It is too small but we have to analyze it
                    cont = False
                    ocont, inrange = self.__analyseRect(oRect)
                    if (ocont==True):
                        inQI = False
                        inQE = True
                    else:
                        if(inrange == True):
                            inQI = True
                            inQE = False
                        #else: defaults
                    #Return the result on the next iteration
                    bExit = True
                #Otherwise
                else:
                    #Analyze it
                    (cont, inrange) = self.__analyseRect(oRect)
                    if inrange:
                        inQI = True
                        inQE = False
                    #else: defaults
                #Save the obtained results
                if cont and (curLevel < maxLevels-1):
                    (oRleft,oRright) = self.__getNewRect(oRect,curLevel)
                    self.__addToTree(curLevelNode, oRleft, oRright, curLevel + 1)
                else:
                    #save results to the analyzed node
                    curLevelNode.add_feature('Inrange',inrange)
                    curLevelNode.add_feature('inQI',inQI)
                    curLevelNode.add_feature('inQE',inQE)

            #All of the rectangles could be obtained on the next iterations are too small
            #so break it
            if bExit:
                print 'Number of levels were processed: {}'.format(curLevel)
                print 'Number of iterations: {}'.format(nIter)
                break

    def saveResultAsImage(self, fileName='./Images/{0}__{1:02d}_{2:02d}_{3:02d}_covering.eps'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second),\
                                                           AddRings=False, Zoomed=False):
        #Initialize plotting facilities
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111)
        self.__ax.axis('scaled')
        self.__ax.axis([self.__Xspace.left, self.__Xspace.right, self.__Xspace.top, self.__Xspace.bottom ])

        if(Zoomed):
            dif = 0.002
            zoomxmin = 1 - dif
            zoomxmax = 1 + dif
            zoomymin = -dif
            zoomymax = dif

            self.__ax.axis([zoomxmin-dif/4.0, zoomxmax-dif/4.0, zoomymin, zoomymax])

            print 'Drawing rectangles...'
            for leaf in self.__sTree.iter_leaves():
                xmin = leaf.Rect.left
                xmax = leaf.Rect.left + leaf.Rect.width
                ymin = leaf.Rect.top
                ymax = leaf.Rect.top + leaf.Rect.height

                if((zoomxmin-2*dif <= xmin) and (zoomxmax+2*dif  >= xmax) and (zoomymin-2*dif <= ymin) and (zoomymax+2*dif >= ymax)):
                    #Draw the rectangle with edges
                    self.__drawRect(leaf.Rect, leaf.Inrange, leaf.inQI, leaf.inQE)
        else:
            print 'Drawing rectangles...'
            for leaf in self.__sTree.iter_leaves():
                #Draw the rectangle with edges
                self.__drawRect(leaf.Rect, leaf.Inrange, leaf.inQI, leaf.inQE)

        if(AddRings):
            print 'Adding rings...'
            # Call an abstract method
            self.drawRings(self.__ax)

        plt.draw()
        plt.pause(1)
        #Save the result
        print 'Saving an image...'
        self.__fig.savefig(fileName, dpi = 600)
        print 'The image has been saved correctly'
