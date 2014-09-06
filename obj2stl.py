#!/usr/bin/env python
import sys

def usage():
  print "usage:"
  print "  python [--binary] %s < myfile.obj > myfile.stl" % sys.argv[0]
  print
  print "Convert a Wavefront .obj file into a ASCII or binary .stl file."


def write_face(fout, p1, p2, p3, binary=False):
  x1,y1,z1 = p1
  x2,y2,z2 = p2
  x3,y3,z3 = p3
  if binary:
    fout.write(pack('<12f2x',0,0,0,x1,y1,z1,x2,y2,z2,x3,y3,z3))
  else:
    fout.write("\tfacet normal {0:e} {1:e} {2:e}\n".format(0, 0, 0))
    fout.write("\t\tfouter loop\n")
    fout.write("\t\t\tvertex {0:e} {1:e} {2:e}\n".format(x1, y1, z1))
    fout.write("\t\t\tvertex {0:e} {1:e} {2:e}\n".format(x2, y2, z2))
    fout.write("\t\t\tvertex {0:e} {1:e} {2:e}\n".format(x3, y3, z3))
    fout.write("\t\tendloop\n")
    fout.write("\tendfacet\n")

def write_stl(fout, triangles, binary=False):
  if binary:
    fout.write(pack('<80xI',nt))
  else:
    fout.write("solid surface\n")
  
  for v1,v2,v3 in triangles:
    write_face(fout, v1,v2,v3, binary)
  
  if not binary:
    fout.write("endsolid surface\n")


def convert(fin, fout, binary=False):
  name = "surface"
  vertices = []
  faces = []
  for line in fin.readlines():
    # todo: strip comments
    
    values = line.split()
    linetype, values = values[0], values[1:]
    if linetype == 'o':
      # object name
      if len(values) > 0:
        name = values[0]
      pass
    elif linetype == 'g':
      # group name
      if len(values) > 0:
        name = values[0]
      pass
    elif linetype == 'v':
      # vertex position
      vertices.append(map(float, values))
      pass
    elif linetype == 'vt':
      # texture coordinate
      pass
    elif linetype == 'vn':
      # vertex normal
      pass
    elif linetype == 'vp':
      # parameter-space vertex (on a NURBS or something)
      pass
    elif linetype == 'f':
      # face
      # todo: support v/vt/vn instead of just v
      
      vs = map(lambda s: vertices[int(s)-1], values)
      for i in range(1,len(vs)-1):
        v1,v2,v3 = vs[0], vs[i], vs[i+1]
        faces.append((v1,v2,v3))
    else:
      print "Unknown linetype %s" % linetype
      sys.exit(1)
  write_stl(fout, faces, binary)


binary = False
for arg in sys.argv[1:]:
  if arg == '-h' or arg == '--help':
    usage()
    sys.exit(0)
  elif arg == '-b' or arg == '--binary':
    binary = True
  else:
    print "Unknown option %s" % arg
    sys.exit(1)

convert(sys.stdin, sys.stdout, binary)
