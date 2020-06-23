#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TCP/IP Bindings Tester
Copyright (C) 2020 Matthias bolte <matthias@tinkerforge.com>

test_tcpip_bindings.py: Tests the TCP/IP bindings

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os

def run(root_dir):
    print('### no tests available')
    return True

if __name__ == '__main__':
    run(os.getcwd())
