import json
from scipy.spatial.transform import Rotation
import open3d as o3d

class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "]"


class Dimensions:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
    def __str__(self):
        return "[" + str(self.length) + "," + str(self.width) + "," + str(self.height) + "]"

class BoxObject:
    name = None
    centroid = None
    dimensions = None
    rotations = None
    
    def __init__(self, name = None, centroid = None, dimensions = None, rotations = None):
        self.name = name
        self.centroid = centroid
        self.dimensions = dimensions
        self.rotations = rotations

    def from_open3d_bb(self, bb: o3d.geometry.OrientedBoundingBox):
        self.centroid = Coordinates(bb.center[0], bb.center[1], bb.center[2])
        self.dimensions = Dimensions(bb.extent[0], bb.extent[1], bb.extent[2])
        rot = Rotation.from_matrix(bb.R).as_euler("xyz", degrees = True)
        self.rotations = Coordinates(rot[0], rot[1], rot[2])

        return self

    def __str__(self):
        return "Bounding Box with: \ncenter: " + str(self.centroid) + "\ndimensions: " + str(self.dimensions) + "\nrotations: " + str(self.rotations)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class SaveData:
    folder = None
    filename = None
    path = None
    objects = None

    def __init__(self, folder = None, filename = None, path = None, objects = None):
       self.folder = folder
       self.filename = filename
       self.path = path
       self.objects = objects

    def from_bounding_boxes(self, bbs):
        self.objects = []
        for i in range(len(bbs)):
            newBox = BoxObject().from_open3d_bb(bbs[i])
            newBox.name = i
            self.objects.append(newBox)
        return self

    def __str__(self):
        return "SaveData with: \nfolder: " + str(self.folder) + "\nfilename: " + str(self.filename) + "\npath: " + str(self.path) + "\nobjects: " + str(self.objects)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)