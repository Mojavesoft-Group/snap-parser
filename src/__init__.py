"""Snap! project parsing module."""
from xmltodict import parse
class Project:
    """A Snap! project."""
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data["project"]["@name"]
        self.app = self.data["project"]["@app"]
        self.version = self.data["project"]["@version"]
        self.notes = self.data["project"]["notes"]
        self.thumbnail = self.data["project"]["thumbnail"]

        scenes = self.data["project"]["scenes"]["scene"]
        if isinstance(scenes, list):
            self.scenes = [Scene(i) for i in scenes]
        else:
            self.scenes = [Scene(scenes)]
    
    def __repr__(self) -> str:
        return str({"name": self.name, "notes": self.notes, "data": self.data})

class Scene:
    """A Snap! scene."""
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data["@name"]
        self.custom_blocks = []
        self.stage = Stage(self.data["stage"])

        if self.data["blocks"]:
            for i in self.data["blocks"]["block-definition"]:
                self.custom_blocks.append(CustomBlock(i))

class CustomBlock:
    """A Snap! custom block definition."""
    def __init__(self, data: dict):
        self.data = data
        self.spec = self.data["@s"]
        self.type = self.data["@type"]
        self.category = self.data["@category"]
    
    def __repr__(self) -> str:
        return self.spec

class Stage:
    """A Snap! stage."""
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data["@name"]
        self.width = self.data["@width"]
        self.height = self.data["@height"]
        self.costume = self.data["@costume"]
        self.color = tuple(self.data["@color"].split(","))
        self.tempo = self.data["@tempo"]
        self.threadsafe = self.data["@threadsafe"]
        self.penlog = self.data["@penlog"]
        self.volume = self.data["@volume"]
        self.pan = self.data["@pan"]
        self.lines = self.data["@lines"]
        self.ternary = self.data["@ternary"]
        self.hyperops = self.data["@hyperops"]
        self.codify = self.data["@codify"]
        self.inheritance = self.data["@inheritance"]
        self.sublist_ids = self.data["@sublistIDs"]
        self.id = self.data["@id"]
        self.pentrails = self.data["pentrails"]
        self.sprites = [Sprite(i) for i in self.data["sprites"]["sprite"]]
        self.costumes = [Costume(i) for i in self.data["costumes"]["list"].get("item", [])]

class Sprite:
    """A Snap! sprite."""
    def __init__(self, data: dict):
        self.data = data
        self.name = self.data["@name"]
        self.idx = self.data["@idx"]
        self.x = self.data["@x"]
        self.y = self.data["@y"]
        self.heading = self.data["@heading"]
        self.scale = self.data["@scale"]
        self.volume = self.data["@volume"]
        self.pan = self.data["@pan"]
        self.rotation = self.data["@rotation"]
        self.instrument = self.data.get("@instrument")
        if self.data["@draggable"] == "true":
            self.draggable = True
        else:
            self.draggable = False
        self.hidden = self.data.get("@hidden")
        self.costume = self.data["@costume"]
        self.color = tuple(self.data["@color"].split(","))
        self.pen = self.data["@pen"]
        self.id = self.data["@id"]

class Costume:
    """A Snap! costume."""
    def __init__(self, data):
        self.data = data
        print(data)
        self.name = self.data["costume"]["@name"]
        self.center_x = self.data["costume"]["@center-x"]
        self.center_y = self.data["costume"]["@center-y"]
        self.image = self.data["costume"]["@image"]
        self.id = self.data["costume"]["@id"]

def project_from_xml(xml: str) -> Project:
    """Obtain a Project object from an XML string."""
    return Project(parse(xml, force_list=("sprite", "scene", "item")))

def project_from_path(path: str) -> Project:
    """Obtain a Project object from an XML file, given its path."""
    f = open(path)
    project = project_from_xml(f.read())
    f.close()
    return project
