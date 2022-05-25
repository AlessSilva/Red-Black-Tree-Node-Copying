import myglobal

def Active( u ):
  if u == None:
    return u
  elif (u.copy_ == None):
    return u
  return u.copy_

def Child( u, side, version=None ):

  if u == None:
    return None

  if (version != None):

    if ( u.change["T"] != -1 ) & ( u.change["field"] == side ) & ( version >= u.change["T"] ):
      return u.change["value"]

    if side == 0: return u.child0
    else: return u.child1
    
  else:

    return Child( Active( u ), side, myglobal.current )

def Find( x, version ):

  u = myglobal.root[version]
  while( u != None ) & (x != u.value):
    u = Child(u, x>u.value,version)
  return u


from copy import copy

def MakeCopy(u):


  u_ = copy(u)

  u_.T = myglobal.current

  if u.change["T"] != -1:
    
    if u.change["field"] == 0:
      u_.child0 = u.change["value"]
    elif u.change["field"] == 1:
      u_.child1 = u.change["value"]
    u_.change["T"] = -1
    
  
  if myglobal.root[myglobal.current] == u:
    myglobal.root[myglobal.current] = u_

  if u_.child0 != None:
    u_.child0.parent = u_
  if u_.child1 != None:
    u_.child1.parent = u_
  
  u.parent = None
  if u_.parent != None:
    v = u_.parent
    side = (Child(v,1) == u)
    if v.T == myglobal.current:
      if side == 0:
        v.child0 = u_
      elif side ==1:
        v.child1 = u_
      elif v.change["T"] == (-1):
        v.change["T"] = myglobal.current
        v.change["value"] = u_
        v.change["field"] = side
    
    else:
      v.copy_ = MakeCopy(v)
      if side == 0: v.copy_.child0 = u_
      else: v.copy_.child1 = u_
      u_.parent = v.copy_
  
  return u_

def Modify(u, side, v):

  if u == None:
    return u

  u = Active(u)
  if u.T < myglobal.current:
    u.copy_ = MakeCopy(u)
    u = u.copy_
  if (side == 0) & (u.child0 != None):
    u.child0.parent = None
  if (side == 1) & (u.child1 != None):
    u.child1.parent = None
  if side == 0:
    u.child0 = Active(v)
  else:
    u.child1 = Active(v)
  if (side == 0) & (u.child0 != None):
    u.child0.parent = u
  if (side == 1) & (u.child1 != None):
    u.child1.parent = u