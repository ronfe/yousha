from bson.objectid import ObjectId


class Point():

    def __init__(self, name):
        self.id = str(ObjectId())
        self.notation = name
        self.name = "点" + self.notation


class Circle():

    def __init__(self, point):
        self.id = str(ObjectId())
        self.center = point
        self.notation = point.notation
        self.name = "圆" + self.notation
        self.strings = []

    def add_string(self, string):
        self.strings.append(string)


class Edge():

    def __init__(self, point_A, point_B):
        self.id = str(ObjectId())
        self.points = [point_A, point_B]
        self.notation = point_A.notation + point_B.notation
        self.name = "线段" + self.notation
        self.related_attr = dict()


class Perpendicular():

    def __init__(self, edge_a, edge_b, point_c):
        self.id = str(ObjectId())
        self.partners = [edge_a, edge_b]
        self.foot = point_c
        self.notation = edge_a.notation + "⊥" + edge_b.notation
        self.name = self.notation


class Diameter():

    def __init__(self, edge, circle):
        self.id = str(ObjectId())
        self.edge = edge
        self.circle = circle
        self.name = edge.name + "是" + circle.name + "的直径"


class Cutting():

    def __init__(self, edge, circle, point):
        self.id = str(ObjectId())
        self.edge = edge
        self.circle = circle
        self.cutting_point = point
        self.name = edge.name + "是" + circle.name + "的切线,切点是" + point.notation



class Equal():

    def __init__(self, part_a, part_b):
        self.id = str(ObjectId())
        self.partners = [part_a, part_b]
        self.name = part_a.name + "=" + part_b.name
