#Copyright (c) 2009-10, Walter Bender (on behalf of Sugar Labs)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

# A naive approach to running myfunc in a jail
import logging
_logger = logging.getLogger('turtleart-activity')
import traceback
from time import *
from math import *


def myfunc(f, args):
    # check to make sure no import calls are made
    if len(args) == 1:
        myf = "def f(x): return " + f.replace("import","")
        userdefined = {}
        exec myf in globals(), userdefined
        return userdefined.values()[0](args[0])
    elif len(args) == 2:
        myf = "def f(x,y): return " + f.replace("import","")
        userdefined = {}
        exec myf in globals(), userdefined
        return userdefined.values()[0](args[0], args[1])
    elif len(args) == 3:
        myf = "def f(x,y,z): return " + f.replace("import","")
        userdefined = {}
        exec myf in globals(), userdefined
        return userdefined.values()[0](args[0], args[1], args[2])


def myfunc_import(lc, f, x):
    userdefined = {}
    try:
        exec f in globals(), userdefined
        return userdefined['myblock'](lc, x)
    except:
        traceback.print_exc()
        return None
