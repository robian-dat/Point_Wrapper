import numpy as np

testPoints = [[60, 5],[50,5],[45,10],[40,15],[35,20],[30,25],[25, 30],[20,35],[15,40]]
gridSize = [100, 100]

# find and return the point closest to the bottom edge. If there are more than one, return # all of them. Add these to the list of perimeter points.
# set the extreme left point found as the origin

# iteratively, find the vector formed by successive points up the left side, starting with
# the point on the left side at the same elevation as the origin
# for each iteration, check whether the vector drawn to each given point matches the angle
# of the vector in the previous step. If there is a match, add it to a list.
# take the newly formed list and return the point that forms the least angle.
# add this point to the list of perimeter points.
# set this point as the origin and repeat.

# Functions:
# linearScan: scans from a given side and returns a list of the first points encountered
# radialScan: takes a scan origin point, a side, and a list of testPoints
# returns the first point encountered by the scan
# make sure to check if we are already on the grid boundary
# accumulate: need a function that constructs a list by calling a function with a
# starting value, adding the result to the list, then calling the same function with the
# updated value

def linearScan(side, points):
  edgePoints = []
  if side == 'bottom':
    for j in range(gridSize[1]):
      for point in points:
        if point[1] == j:
          edgePoints.append(point)
      if edgePoints: 
        break
  return edgePoints

def wrapScan(scan_origin, side, points):
  # wrapper for radialScan and accumulate
  def radialScan(scan_origin, side, points):
    # compare the rise/run of vectors formed by series of points
    # only compare points that are in the same quadrant as a reference vector
    # return the points that form vectors with the smallest rise/run
    # in a dict with the vector magnitudes as keys
    exclPoints = points.copy()
    exclPoints.pop(exclPoints.index(scan_origin))
    candPoints = {}
    if side == 'left':
      if scan_origin[0] == 0:
        return None
      refPoint = [0, gridSize[1] - scan_origin[1]]
      for point in exclPoints:
        if np.sign(point[1] - scan_origin[1]) == np.sign(refPoint[1] - scan_origin[1]) and\
        np.sign(point[0] - scan_origin[0]) == np.sign(refPoint[0] - scan_origin[0]):
          slope = (point[1] - scan_origin[1])/(point[0] - scan_origin[0])
          magnitude = np.sqrt((point[1] - scan_origin[1])**2 + (point[0] - scan_origin[0])**2)
          if slope not in candPoints:
            candPoints[slope] = []
            candPoints[slope].append([point, magnitude])
          else:
            candPoints[slope].append([point, magnitude])
  
      if candPoints:
        byMag = {}
        for point_mag in candPoints[min(candPoints.keys())]:
          byMag[point_mag[1]] = point_mag[0]
        print(byMag)
        return byMag
      else:
        return None

  def accumulate():
    # call radialScan iteratively and accumulate each result
    # radialScan can return a dict with more than one item;
    # each iteration call radialScan with the key with the greatest numerical value
    outerPoints = []
    basePoint = scan_origin
    while radialScan(basePoint, side, points):
      nextPoints = radialScan(basePoint, side, points)
      for point in nextPoints.values():
        print(point)
        outerPoints.append(point)
      basePoint = nextPoints[max(nextPoints.keys())]
    return outerPoints

  return accumulate()

print('linearScan:', linearScan('bottom',testPoints))
print('wrapScan:', wrapScan([50, 5], 'left', testPoints))