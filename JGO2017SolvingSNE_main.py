import timeit
import datetime

# Example 1
from JGO2017Example1 import Example1GlobOpt
from JGO2017Example1 import Example1AppxGlobL
from JGO2017Example1 import Example1AppxLocL
# Example 2
from JGO2017Example2 import Example2AppxLocL

def Example1():
    print'#############################################################################'
    print'                            Example 1                                        '
    print'#############################################################################\n'

    #Figure 2
    print 'Delta = {}\n'.format(0.06)
    Example1Figure2Table1(0.06, True)

    #Figure 3
    # Uncomment if you would like to replicate the result from Figure 3
    # Note that it will take a while
    #Example1Figure3(ShowRes=False)

    #Table 1
    deltas = [0.5, 0.3, 0.25, 0.15, 0.13, 0.08, 0.06, 0.035, 0.03, 0.018, 0.015, 0.01, 0.0001]
    # Kite like workspace
    for iDelta in deltas:
        print '\nDelta = {}\n'.format(iDelta)
        Example1Figure2Table1(iDelta, False)

def Example1Figure2Table1(iDelta, ShowRes=False):

    maxLevels = 64

    # Example 1: Solving systems of nonlinear inequalities by using
    # a global optimization technique

    System1 = Example1GlobOpt(iDelta)
    print 'The results obtained by using global optimization:'
    t = timeit.Timer(lambda: System1.getSolution(maxLevels, False))
    exectime = t.timeit(number=3)
    print 'Execution time: {}\n'.format(exectime)
    if ShowRes:
        System1.saveResultAsImage('./Images/Example1/Example1_GlobOpt_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True)

    # Example 1: Solving systems of nonlinear inequalities by using
    # approximation of extrema with a global L value
    System1 = Example1AppxGlobL(iDelta)
    print 'The results obtained by using Lipschits minorants and majorants and global L:'
    t = timeit.Timer(lambda: System1.getSolution(maxLevels, False))
    exectime = t.timeit(number=3)
    print 'Execution time: {}\n'.format(exectime)
    if ShowRes:
        System1.saveResultAsImage('./Images/Example1/Example1_Appx_GlobL_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True)

    # Example 1: Solving systems of nonlinear inequalities by using
    # approximation of extrema with a local L value
    System1 = Example1AppxLocL(iDelta)
    print 'The results obtained by using Lipschits minorants and majorants and local L:'
    t = timeit.Timer(lambda: System1.getSolution(maxLevels, False))
    exectime = t.timeit(number=3)
    print 'Execution time: {}'.format(exectime)
    if ShowRes:
        System1.saveResultAsImage('./Images/Example1/Example1_Appx_LocL_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True)

def Example1Figure3(ShowRes=False, iDelta=0.0001, maxLevels=64):
    print 'Delta = {}\n'.format(iDelta)

    # Example 1: Solving systems of nonlinear inequalities by using
    # approximation of extrema with a local L value
    System1 = Example1AppxLocL(iDelta)
    print 'The results obtained by using Lipschits minorants and majorants and local L:'
    t = timeit.Timer(lambda: System1.getSolution(maxLevels, False))
    exectime = t.timeit(number=3)
    print 'Execution time: {}'.format(exectime)
    if ShowRes:
        System1.saveResultAsImage('./Images/Example1/Example1_Appx_LocL_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True, Zoomed=False)
        System1.saveResultAsImage('./Images/Example1/Example1_Appx_LocL_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}_Zoomed.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True, Zoomed=True)

def Example2():
    print'\n#############################################################################'
    print'                            Example 2                                        '
    print'#############################################################################\n'
    #Table 2 and Figure 4
    deltas = [0.5, 0.3, 0.2, 0.15, 0.1, 0.07, 0.06, 0.035, 0.03, 0.018, 0.01, 0.009]

    # Kite like workspace
    for iDelta in deltas:
        print 'Delta = {}'.format(iDelta)
        Example2Figure5Table2(iDelta, False)

def Example2Figure5Table2(iDelta, ShowResOnly=False):

    # Example 2: Solving systems of nonlinear inequalities by using
    # approximation of extrema
    System2 = Example2AppxLocL(6, [2, 12], [6, 12], iDelta)
    print 'The results obtained by using Lipschits minorants and majorants and local L:'
    maxLevels = 64
    t = timeit.Timer(lambda: System2.getSolution(maxLevels, False))
    exectime = t.timeit(number=3)
    print 'Execution time: {}\n'.format(exectime)
    if ShowResOnly:
        System2.saveResultAsImage('./Images/Example2/Example2_Appx_LocL_{0}__{1:02d}_{2:02d}_{3:02d}_covering_{4}.jpeg'.format(datetime.date.today(), \
                                                           datetime.datetime.now().hour,\
                                                           datetime.datetime.now().minute,\
                                                           datetime.datetime.now().second,\
                                                           iDelta), AddRings=True)

if __name__ == '__main__':
    Example1()
    Example2()
