# -*- coding: utf-8 -*-
#Copyright (c) 2010 Walter Bender

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

from taconstants import TURTLE_LAYER
from tasprite_factory import SVG, svg_str_to_pixbuf
from tacanvas import wrap100, color_table
from sprites import Sprite

import logging
_logger = logging.getLogger('turtleart-activity')


SHAPES = 36


def generate_turtle_pixbufs(colors):
    """ Generate pixbufs for generic turtles """
    shapes = []
    svg = SVG()
    svg.set_scale(1.0)
    for i in range(SHAPES):
        svg.set_orientation(i * 10)
        shapes.append(svg_str_to_pixbuf(svg.turtle(colors)))
    return shapes


class Turtles:

    def __init__(self, sprite_list):
        """ Class to hold turtles """
        self.dict = dict()
        self.sprite_list = sprite_list
        self.default_pixbufs = []

    def get_turtle(self, k, append=False, colors=None):
        """ Find a turtle """
        if k in self.dict:
            return self.dict[k]
        elif not append:
            return None
        else:
            if colors == None:
                Turtle(self, k)
            else:
                Turtle(self, k, colors.split(','))
            return self.dict[k]

    def get_turtle_key(self, turtle):
        """ Find a turtle's name """
        for k in iter(self.dict):
            if self.dict[k] == turtle:
                return k
        return None

    def turtle_count(self):
        """ How many turtles are there? """
        return(len(self.dict))

    def add_to_dict(self, k, turtle):
        """ Add a new turtle """
        self.dict[k] = turtle

    def remove_from_dict(self, k):
        """ Delete a turtle """
        if k in self.dict:
            del(self.dict[k])

    def show_all(self):
        """ Make all turtles visible """
        for k in iter(self.dict):
            self.dict[k].show()

    def spr_to_turtle(self, spr):
        """ Find the turtle that corresponds to sprite spr. """
        for k in iter(self.dict):
            if spr == self.dict[k].spr:
                return self.dict[k]
        return None

    def get_pixbufs(self):
        """ Get the pixbufs for the default turtle shapes. """
        if self.default_pixbufs == []:
            self.default_pixbufs = generate_turtle_pixbufs(
                ["#008000", "#00A000"])
        return(self.default_pixbufs)


class Turtle:

    def __init__(self, turtles, key, turtle_colors=None):
        """ The turtle is not a block, just a sprite with an orientation """
        self.x = 0
        self.y = 0
        self.hidden = False
        self.shapes = []
        self.custom_shapes = False
        self.type = 'turtle'
        self.heading = 0
        self.pen_shade = 50
        self.pen_color = 0
        self.pen_gray = 100
        self.pen_size = 5
        self.pen_state = True

        # If the turtle key is an int, we'll use a palette color as the
        # turtle color
        try:
            int_key = int(key)
            use_color_table = True
        except ValueError:
            use_color_table = False

        if turtle_colors is not None:
            self.colors = turtle_colors[:]
            self.shapes = generate_turtle_pixbufs(self.colors)
        elif use_color_table:
            fill = wrap100(int_key)
            stroke = wrap100(fill + 10)
            self.colors = ['#%06x' % (color_table[fill]),
                           '#%06x' % (color_table[stroke])]
            self.shapes = generate_turtle_pixbufs(self.colors)
        else:
            self.shapes = turtles.get_pixbufs()

        if turtles.sprite_list is not None:
            self.spr = Sprite(turtles.sprite_list, 0, 0, self.shapes[0])
        else:
            self.spr = None
        turtles.add_to_dict(key, self)

    def set_shapes(self, shapes):
        """ Reskin the turtle """
        n = len(shapes)
        if n == SHAPES:
            self.shapes = shapes[:]
        else:
            if n != 1:
                _logger.debug("%d images passed to set_shapes: ignoring" % (n))
            images = [shapes[0]]
            if self.heading == 0:
                for i in range(3):
                    images.append(images[i].rotate_simple(270))
                for i in range(SHAPES):
                    j = (i + 4) % SHAPES
                    self.shapes[j] = images[int(j / 9)]
            else:
                j = int(self.heading + 5) % 360 / (360 / SHAPES)
                self.shapes[j] = images[0]
        self.custom_shapes = True
        self.show()

    def reset_shapes(self):
        """ Reset the shapes to the standard turtle """
        if self.custom_shapes:
            self.shapes = generate_turtle_pixbufs(self.colors)
            self.custom_shapes = False

    def set_heading(self, heading):
        """ Set the turtle heading (one shape per 360/SHAPES degrees) """
        self.heading = heading
        i = (int(self.heading + 5) % 360) / (360 / SHAPES)
        if not self.hidden and self.spr is not None:
            try:
                self.spr.set_shape(self.shapes[i])
            except IndexError:
                self.spr.set_shape(self.shapes[0])

    def set_color(self, color):
        """ Set the pen color for this turtle. """
        self.pen_color = color

    def set_gray(self, gray):
        """ Set the pen gray level for this turtle. """
        self.pen_gray = gray

    def set_shade(self, shade):
        """ Set the pen shade for this turtle. """
        self.pen_shade = shade

    def set_pen_size(self, pen_size):
        """ Set the pen size for this turtle. """
        self.pen_size = pen_size

    def set_pen_state(self, pen_state):
        """ Set the pen state (down==True) for this turtle. """
        self.pen_state = pen_state

    def hide(self):
        """ Hide the turtle. """
        if self.spr is not None:
            self.spr.hide()
        self.hidden = True

    def show(self):
        """ Show the turtle. """
        if self.spr is not None:
            self.spr.set_layer(TURTLE_LAYER)
            self.hidden = False
        self.move((self.x, self.y))
        self.set_heading(self.heading)

    def move(self, pos):
        """ Move the turtle. """
        self.x, self.y = int(pos[0]), int(pos[1])
        if not self.hidden and self.spr is not None:
            self.spr.move(pos)
        return(self.x, self.y)

    def get_xy(self):
        """ Return the turtle's x, y coordinates. """
        return(self.x, self.y)

    def get_heading(self):
        """ Return the turtle's heading. """
        return(self.heading)

    def get_color(self):
        """ Return the turtle's color. """
        return(self.pen_color)

    def get_gray(self):
        """ Return the turtle's gray level. """
        return(self.pen_gray)

    def get_shade(self):
        """ Return the turtle's shade. """
        return(self.pen_shade)

    def get_pen_size(self):
        """ Return the turtle's pen size. """
        return(self.pen_size)

    def get_pen_state(self):
        """ Return the turtle's pen state. """
        return(self.pen_state)
