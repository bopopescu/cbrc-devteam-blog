# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""Utilities
"""

__MYSQL_DEBUG__ = False

import struct

def intread(buf):
    """Unpacks the given buffer to an integer"""
    try:
        if isinstance(buf,int):
            return buf
        l = len(buf)
        if l == 1:
            return buf[0]
        elif l <= 4:
            tmp = buf + b'\x00'*(4-l)
            return struct.unpack('<I', tmp)[0]
        else:
            tmp = buf + b'\x00'*(8-l)
            return struct.unpack('<Q', tmp)[0]
    except:
        raise

def int1store(i):
    """
    Takes an unsigned byte (1 byte) and packs it as a bytes-object.
    
    Returns string.
    """
    if i < 0 or i > 255:
        raise ValueError('int1store requires 0 <= i <= 255')
    else:
        return struct.pack('<B',i)

def int2store(i):
    """
    Takes an unsigned short (2 bytes) and packs it as a bytes-object.
    
    Returns string.
    """
    if i < 0 or i > 65535:
        raise ValueError('int2store requires 0 <= i <= 65535')
    else:
        return struct.pack('<H',i)

def int3store(i):
    """
    Takes an unsigned integer (3 bytes) and packs it as a bytes-object.
    
    Returns string.
    """
    if i < 0 or i > 16777215:
        raise ValueError('int3store requires 0 <= i <= 16777215')
    else:
        return struct.pack('<I',i)[0:3]

def int4store(i):
    """
    Takes an unsigned integer (4 bytes) and packs it as a bytes-object.
    
    Returns string.
    """
    if i < 0 or i > 4294967295:
        raise ValueError('int4store requires 0 <= i <= 4294967295')
    else:
        return struct.pack('<I',i)

def int8store(i):
    """
    Takes an unsigned integer (4 bytes) and packs it as string.

    Returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError('int4store requires 0 <= i <= 2^64')
    else:
        return struct.pack('<Q',i)

def intstore(i):
    """
    Takes an unsigned integers and packs it as a bytes-object.
    
    This function uses int1store, int2store, int3store,
    int4store or int8store depending on the integer value.
    
    returns string.
    """
    if i < 0 or i > 18446744073709551616:
        raise ValueError('intstore requires 0 <= i <=  2^64')
        
    if i <= 255:
        fs = int1store
    elif i <= 65535:
        fs = int2store
    elif i <= 16777215:
        fs = int3store
    elif i <= 4294967295:
        fs = int4store
    else:
        fs = int8store
        
    return fs(i)

def read_bytes(buf, size):
    """
    Reads bytes from a buffer.
    
    Returns a tuple with buffer less the read bytes, and the bytes.
    """
    b = buf[0:size]
    return (buf[size:], b)

def read_lc_string(buf):
    """
    Takes a buffer and reads a length coded string from the start.
    
    This is how Length coded strings work
    
    If the string is 250 bytes long or smaller, then it looks like this:

      <-- 1b  -->
      +----------+-------------------------
      |  length  | a string goes here
      +----------+-------------------------
  
    If the string is bigger than 250, then it looks like this:
    
      <- 1b -><- 2/3/8 ->
      +------+-----------+-------------------------
      | type |  length   | a string goes here
      +------+-----------+-------------------------
      
      if type == \xfc:
          length is code in next 2 bytes
      elif type == \xfd:
          length is code in next 3 bytes
      elif type == \xfe:
          length is code in next 8 bytes
     
    NULL has a special value. If the buffer starts with \xfb then
    it's a NULL and we return None as value.
    
    Returns a tuple (trucated buffer, bytes).
    """    
    if buf[0] == 251: # \xfb
        # NULL value
        return (buf[1:], None)
        
    l = lsize = 0
    fst = buf[0]
    
    if fst <= 250: # \xFA
        l = fst
        return (buf[1+l:], buf[1:l+1])
    elif fst == 252:
        lsize = 2
    elif fst == 253:
        lsize = 3
    if fst == 254:
        lsize = 8
        
    l = intread(buf[1:lsize+1])
    return (buf[lsize+l+1:], buf[lsize+1:l+lsize+1])

def read_lc_string_list(buf):
    """Reads all length encoded strings from the given buffer
    
    Returns a list of bytes
    """
    byteslst = []
    v = memoryview(buf)
    sizes = {
        b'\xfc': 2,
        b'\xfd': 3,
        b'\xfe': 8
        }
    
    while v:
        first = bytes(v[0:1])
        if first == b'\xff':
            # Special case when MySQL error 1317 is returned by MySQL.
            # We simply return None.
            return None
        if first == b'\xfb':
            # NULL value
            byteslst.append(None)
            v = v[1:]
        else:
            if first <= b'\xfa':
                l = first[0]
                byteslst.append(bytes(v[1:l+1]))
                v = v[1+l:]
            else:
                lsize = 0
                try:
                    lsize = sizes[first]
                except KeyError:
                    print(buf)
                    print(_digest_buffer(buf))
                    return None
                l = intread(bytes(v[1:lsize+1]))
                byteslst.append(bytes(v[lsize+1:l+lsize+1]))
                v = v[lsize+l+1:]

    return tuple(byteslst)

def read_string(buf, end=None, size=None):
    """
    Reads a string up until a character or for a given size.
    
    Returns a tuple (trucated buffer, string).
    """
    if end is None and size is None:
        raise ValueError('read_string() needs either end or size')
    
    if end is not None:
        try:
            idx = buf.index(end)
        except (ValueError) as e:
            raise ValueError("end byte not precent in buffer")
        return (buf[idx+1:], buf[0:idx])
    elif size is not None:
        return read_bytes(buf,size)
    
    raise ValueError('read_string() needs either end or size (weird)')
    
def read_int(buf, size):
    """Read an integer from buffer
    
    Returns a tuple (truncated buffer, int)
    """
    
    try:
        res = intread(buf[0:size])
    except:
        raise
    
    return (buf[size:], res)

def read_lc_int(buf):
    """
    Takes a buffer and reads an length code string from the start.
    
    Returns a tuple with buffer less the integer and the integer read.
    """
    if len(buf) == 0:
        raise ValueError("Empty buffer.")
    
    sizes = {252:2, 253:3, 254:8}
    fst = int(buf[0])
    
    if fst == 251:
        return (buf[1:], None)
    
    if fst < 251:
        return (buf[1:], fst)
    else:
        lsize = sizes[fst]
        return (buf[lsize+1:], intread(buf[1:lsize+1]))


#
# For debugging
#
def _digest_buffer(buf):
    return ''.join([ "\\x%02x" % c for c in buf ])

