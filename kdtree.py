"""k-d tree"""

class node: pass

class kdtree:

  def __init__(self, coor_list, depth = 0):
    self.root = self.construct(coor_list, depth)

  def construct(self, coor_list, depth = 0):

    if not coor_list:
      return None

    k = len(coor_list[0])
    axis = depth % k

    coor_list.sort(key=lambda coor: coor[axis])
    median = len(coor_list) // 2

    n = node()
    n.location = coor_list[median]
    n.lc = kdtree(coor_list[:median], depth+1)
    n.rc = kdtree(coor_list[median+1:], depth+1)
    return n

  def nnSearch(self, point, maxDist, depth = 0):
    kd = self.root

    if kd is None:
      return (None, float("inf"))

    k = len(kd.location)
    axis = depth % k

    # Set the current node to be the nearest
    nearest = kd.location
    dist = abs(point - nearest)
    maxDist = dist

    # Checking whether the point is in left or right hplane
    pivot = kd.location[axis]
    target = point[axis]

    # If point in left
    if pivot > target:
      nearerKd = kd.lc
      furtherKd = kd.rc
    # point in right
    else:
      nearerKd = kd.rc
      furtherKd = kd.lc

    (tmpNearest, tmpDist) = nearerKd.nnSearch(point, maxDist, depth + 1)
    if tmpDist < dist:
      nearest = tmpNearest
      dist = tmpDist
      maxDist = tmpDist

    # Check if the hplane intersects with hsphere
    # If intersect, check
    if abs(pivot - target) < maxDist:
      (tmpNearest, tmpDist) = furtherKd.nnSearch(point, maxDist, depth + 1)
      if tmpDist < dist:
        nearest = tmpNearest
        dist = tmpDist
        maxDist = tmpDist

    return (nearest, dist)

  def rangeSearch(self, point, maxDist, depth = 0):
    kd = self.root

    if kd is None:
      return ([], [])

    near = []; dists = []

    k = len(kd.location)
    axis = depth % k

    # Append the current node to near
    if abs(kd.location - point) < maxDist:
      near.append(kd.location)
      dists.append(abs(kd.location - point))

    # Check whether the point is in left hplane or right
    pivot = kd.location[axis]
    target = point[axis]

    # If point in left
    if pivot > target:
      nearerKd = kd.lc
      furtherKd = kd.rc
    # If point in right
    else:
      nearerKd = kd.rc
      furtherKd = kd.lc

    (tmpNear, tmpDists) = nearerKd.rangeSearch(point, maxDist, depth + 1)
    near = near + tmpNear
    dists = dists + tmpDists

    # Check if hplane intersect with hsphere
    # If intersect check:
    if abs(pivot - target) < maxDist:
      (tmpNear, tmpDists) = furtherKd.rangeSearch(point, maxDist, depth + 1)
      near = near + tmpNear
      dists = dists + tmpDists

    return (near, dists)
