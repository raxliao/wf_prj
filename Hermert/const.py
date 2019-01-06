import numpy as np
class const(object):

     def __init__(self):
         self.pi = 3.1415926535897932
         self.a = 6378137.0
         self.f = 1/298.257222101
         self.e = np.sqrt(2*self.f-self.f*self.f)
