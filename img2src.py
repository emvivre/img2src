#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

"""
  ===========================================================================

  Copyright (C) 2014 Emvivre

  This file is part of IMG2SRC.

  IMG2SRC is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  IMG2SRC is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with IMG2SRC.  If not, see <http://www.gnu.org/licenses/>.

  ===========================================================================
*/
"""

import os
import sys
from PIL import Image

if len(sys.argv) < 4:
    print 'Usage: %s <INPUT_IMAGE> <OUTPUT_SOURCE> <OUTPUT_HEADER>' % sys.argv[0]
    quit(1)

(input_img, output_source, output_header) = sys.argv[1:]
img = Image.open(input_img).convert('RGBA')
(w,h) = img.size
pix = img.load()

output_header_basename = os.path.basename(output_header)
variable_name = output_header_basename.split('.')[0]
o_fd = open(output_source, 'w+')
o_fd.write(
'''#include "%s"

const unsigned char %s[] = {
''' % (output_header_basename, variable_name))
o_fd.write('    ')
l = 0
f = open(input_img)
for y in range(h):
    for x in range(w):
        p = pix[x,y]
        o_fd.write('0x%02x, 0x%02x, 0x%02x, 0x%02x, ' % (p[0], p[1], p[2], p[3]))
        l += 1
        if l == 16:
            o_fd.write('\n    ')
            l = 0
o_fd.write(
'''
};

const unsigned int %s_width = %s;
const unsigned int %s_height = %s;
''' % (variable_name, w, variable_name, h))

o_fd = open(output_header, 'w+')
define_name = os.path.basename(output_header).replace('.', '_').upper()
o_fd.write(
'''#ifndef _%s_
#define _%s_

extern const unsigned char %s[];
extern const unsigned int %s_width;
extern const unsigned int %s_height;

#endif
''' % (define_name, define_name, variable_name, variable_name, variable_name))
