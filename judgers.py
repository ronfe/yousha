from itertools import combinations

a = {
    "materials": [
        {
            "type": "material",
            "relation": "",
            "parts": ["平行四边形,ABCD"],
            "title": "四边形ABCD是平行四边形",
            "forge": [],
            "shape": "平行四边形"
        },
        {
            "type": "material",
            "ralation": "",
            "parts": ["角平分线,AE,BAD"],
            "title": "AE是∠BAD的角平分线",
            "forge": [
                {
                    "type": "material",
                    "relation": "equal",
                    "parts": ["角,BAE", "角,DAE"],
                    "title": "∠BAE=∠EAD",
                    "forge": [],
                    "shape": "角"
                },
                {
                    "type": "material",
                    "relation": "equal",
                    "parts": ["角,BAE", "角,BAD"],
                    "title": "∠BAE=1/2∠BAD",
                    "forge": [],
                    "shape": "角"
                },
                {
                    "type": "material",
                    "relation": "equal",
                    "parts": ["角,DAE", "角,BAD"],
                    "title": "∠DAE=1/2∠BAD",
                    "forge": [],
                    "shape": "角"
                },
            ],
            "shape": "角"
        }
    ],
    "notes": [
        {
            "type": "note",
            "relation": "colline",
            "parts": ["线段,CD", "线段,CE", "线段,DE"],
            "title": "CDE共线",
            "shape": "线"
        }
    ],
    "goals": [
        {
            "type": "material",
            "relation": "equal",
            "parts": ["线段,AD", "线段,DE"],
            "title": "AD=DE",
            "shape": "线"
        }
    ]
}

drugs = [
    {
        "title": "平行四边形的性质",
        "needParts": "平行四边形",
        "func":
    }
]

class Envir():

    def output_materials(self):
        x = [t["title"] for t in self.materials]
        return x

    def output_goals(self):
        x = [t["title"] for t in self.goals]
        return x

    def __init__(self, config):
        self.materials = config["materials"]
        self.notes = config["notes"]
        self.goals = config["goals"]
