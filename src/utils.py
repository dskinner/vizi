#-----------------------------------------------------------------------------
#
#    Copyright (C) 2009  Daniel Skinner
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------

'''
Created on May 15, 2009

@author: daniel
@todo:  * constrained value is broken, only works with min always 0
'''
from math import atan, atan2, cos, degrees, pi, sin

def create_circle_vertices(segments, radius):
    result = []
    for i in range(segments):
        result.append(cos(i*2*pi/segments)*radius)
        result.append(sin(i*2*pi/segments)*radius)
    return result

def determine_constrained_value(min, max, val):
    if val > max:
        if int(val/max)%2: # decrement from max
            return max - (val % max)
        else: # increment from min
            return min + (val % max)
    else:
        return val


'''
def determine_constrained_value(min, max, val):
    if val > max:
        if int(val/max)%2: # decrement from max
            print 'first', val, max - (val % max)
            return determine_constrained_value(min, max, max - (val % max))
        else: # increment from min
            print 'second', val, min + (val % max)
            return determine_constrained_value(min, max, min + (val % max))
    elif val < min:
        if min <= min+min-val <= max:
            return min-val
        else:
            return max-abs(min-val)
    else:
        print 'returning: ', val
        return val
'''