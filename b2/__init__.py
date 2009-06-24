from Box2D import *

class BodyDef(object):
    def __call__(self):
        return self._d
    
    def __init__(self, position=(0, 0)):
        self._d = b2BodyDef()
        self._d.position = position


class CircleDef(object):
    def __get__(self, obj, type=None):
        return self._d

    def __init__(self, density=0, radius=0, friction=0, restitution=0):
        self._d = b2CircleDef()
        self._d.density = density
        self._d.radius = radius
        self._d.friction = friction
        self._d.restitution = restitution
    
    def __call__(self):
        return self._d


class DistanceJointDef(object):
    def __call__(self):
        return self._d
    
    def __init__(self, body1, body2, anchor1=None, anchor2=None):
        if anchor1 is None:
            anchor1 = body1.position
        if anchor2 is None:
            anchor2 = body2.position
        
        self._d = b2DistanceJointDef()
        self._d.Initialize(body1, body2, anchor1, anchor2)
        self._d.collideConnected = True

