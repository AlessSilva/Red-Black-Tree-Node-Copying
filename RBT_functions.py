import myglobal
from persistence_functions import *
from Node import *

def Rotate(u, side):
  if u == None:
    return None
  v = Child(u, side)
  beta = Child(v, not side)
  Modify(v, not side, None)
  Modify(u, side, beta)
  u = Active(u)
  if u.parent != None:
    Modify(u.parent, Child(u.parent,1) == u, v)
  else:
    myglobal.root[myglobal.current] = Active(v)
  Modify(v, not side, u)

def Insert( value ):

  myglobal.current = myglobal.current+1
  myglobal.root[myglobal.current] = myglobal.root[myglobal.current-1]
  x = Node(value)
  x.T = myglobal.current
  if myglobal.root[myglobal.current] == None:
    myglobal.root[myglobal.current] = x
    
  else:
    u = myglobal.root[myglobal.current]
    while u != None:
      
      v = u
      u = Child(u, value > u.value)
    
    Modify(v, value>v.value, x)
  if x.parent != None:
    while (x.red) & (x.parent != None) & (x.parent.red):
      y = x.parent
      z = y.parent
      sideX = (Child(y,1) == x)
      sideY = (Child(z,1) == y)
      w = Child(z, not sideY)
      if (w != None):
        if (w.red):
          z.red = True
          y.red = False
          w.red = False
          x = z
      else:
        if sideX != sideY:
          Rotate(y, sideX)
          x,y = y,x
        Rotate(z,sideX)
        Active(z).red = True
        Active(y).red = False
        break
      if x.parent == None:
        break
  myglobal.root[myglobal.current].red = False

def AddBlack(y, side):

  y = Active(y)
  while y != None:
    z = Child(y, not side)
    if z.red:
      aux = y.red
      y.red = z.red
      z.red = aux
      Rotate(y, not side)
      y = Active(y)
      z = Child(y, not side)
    zx = Child(z, side)
    zz = Child(z, not side)
    i1 = False
    i2 = False
    if zx == None:
      i1 = True
    elif not zx.red:
      i1 = True
    if zz == None:
      i2 = True
    elif not zz.red:
      i2 = True

    if (i2) & ( i2 ):
        z.red = True
        if (y == myglobal.root[myglobal.current]) | (y.red):
           y.red = False
           break
        else:
          side = ( Child(y.parent, 1) == y )
          y = y.parent
    else:
        if (zx!= None):
         if (zx.red):
            aux = z.red
            z.red = zx.red
            zx.red = aux
            Rotate(z, side)
            y = Active(y)
            z = Child(y, not side)
            zz = Child(z, not side)
        aux = y.red
        y.red = z.red
        z.red = aux
        zz.red = False
        Rotate(y, not side)
        break

def MinElement(u, version = None):
  while Child(u,0,version) != None:
    u = Child(u,0,version)
  return u

def Transplant(u,x):

  x = Active(x)
  if (x!=None):
    if (x.parent!=None):
      Modify(x.parent, Child(x.parent,1)==x, None)
  u = Active(u)
  if u == None: v = None
  else: v = u.parent
  if v != None:
    Modify(v, Child(v,1) == u,x)
  else:
    myglobal.root[myglobal.current] = x
  if x != None:
    x.red = u.red

def Remove( value ):
  
  myglobal.current = myglobal.current + 1
  myglobal.root[myglobal.current] = myglobal.root[myglobal.current-1]
  u = Find(value, myglobal.current)
  v = u.parent
  if Child(u, 1) == None:
    needFix = (v != None) & (not u.red) & (Child(u,0) == None)
    Transplant(u, Child(u,0))
    if needFix:
      AddBlack(v, Child(v,1) == None)
  else:
    x = MinElement(Child(u,1))
    if x == Child(u,1):
      y = x
    else:
      y = x.parent
    needFix = (not x.red) & (Child(x,1) == None)
    Transplant(x, Child(x,1))
    Transplant(u,x)
    for side in [0,1]:
      child = Child(u, side)
      Modify(u, side, None)
      Modify(x, side, child)
    if needFix:
      AddBlack(y, Child(y,1) == None)

def Successor( value, version ):

  def em_ordem( node , version ):
    if node != None:
      return em_ordem( Child( node, 0, version ), version) + [node.value] + em_ordem( Child( node, 1, version), version)
    return []

  u = myglobal.root[version]
  suc = None

  mylist = em_ordem( u, version)
  suc = mylist.index(value)

  if suc == (len(mylist)-1):
    return None 
  return mylist[suc+1]

def PrintTree( version ):

  def em_ordem( node , version, depth ):
    if node != None:
      return f'{em_ordem( Child( node, 0, version ), version, depth+1)} {node.value},{depth},{node.red and "R" or "N"} {em_ordem( Child( node, 1, version), version, depth+1 )}'
    return ""
  u = myglobal.root[version]

  return em_ordem( u, version, 0 )

def DisplayTree( version ):
        
        lines, *_ = _display_aux(myglobal.root[version], version)
        return lines

def _display_aux(node, version):
        
        left = Child(node,0, version)
        right = Child(node,1, version)
        
        if (node == None): return

        if (not right) & (not left) :
            if node.red:
              line = '%s R' % node.value
            else:
              line = '%s N' % node.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if not right:
            lines, n, p, x = _display_aux(left, version)
            if node.red:
              s = '%s R' % node.value
            else:
              s = '%s N' % node.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if not left:
            lines, n, p, x = _display_aux(right,version)
            if node.red:
              s = '%s R' % node.value
            else:
              s = '%s N' % node.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left_d, n, p, x = _display_aux(left,version)
        right_d, m, q, y = _display_aux(right,version)
        if node.red:
          s = '%s R' % node.value
        else:
          s = '%s N' % node.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left_d += [n * ' '] * (q - p)
        elif q < p:
            right_d += [m * ' '] * (p - q)
        zipped_lines = zip(left_d, right_d)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2