import materials


# 垂径定理, 要求有直径和垂直
# 逻辑:
#     1. 判断perpendicular中含有直径边,
#     2. 判断perpendicular另一个边是弦
#     3. 返回相等, 弧相等
def vdt(diameter, perpendicular):
    result = list()
    this_edge = diameter.edge
    this_circle = diameter.circle
    if this_edge in perpendicular.partners:
        other_edge = 1 - perpendicular.partners.index(this_edge)
        if perpendicular.partners[other_edge] in this_circle.strings:
            p1 = materials.Edge(other_edge.points[0], perpendicular.foot)
            p2 = materials.Edge(perpendicular.foot, other_edge.points[1])
            result.append(materials.Equal(p1, p2))
            # TODO: return 弧相等
    return result

drugs_backet = [
    {"id": "cjdl", "name": "垂径定理", "desc": "垂直于弦的直径平分弦，并且平分弦所对的两条弧", "function": vdt}
]


