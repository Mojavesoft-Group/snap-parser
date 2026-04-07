"""Snap! project parsing module."""
from xmltodict import parse
class Project:
    """A Snap! project."""
    def __init__(self, data: dict):
        self._data = data
        self.name = self._data["project"]["@name"]
        self.app = self._data["project"]["@app"]
        self.version = self._data["project"]["@version"]
        self.notes = self._data["project"]["notes"]
        self.thumbnail = self._data["project"]["thumbnail"]

        scenes = self._data["project"]["scenes"]["scene"]
        if isinstance(scenes, list):
            self.scenes = [Scene(i) for i in scenes]
        else:
            self.scenes = [Scene(scenes)]
    
    def __repr__(self) -> str:
        return str({"name": self.name, "notes": self.notes, "data": self._data})

class Scene:
    """A Snap! scene."""
    def __init__(self, data: dict):
        self._data = data
        self.name = self._data["@name"]
        self.custom_blocks = []
        self.stage = Stage(self._data["stage"])
        self.variables = _variables_from_data(data)
        if self._data["blocks"]:
            for i in self._data["blocks"]["block-definition"]:
                self.custom_blocks.append(CustomBlock(i))

class CustomBlock:
    """A Snap! custom block definition."""
    def __init__(self, data: dict):
        self._data = data
        self.spec = self._data["@s"]
        self.type = self._data["@type"]
        self.category = self._data["@category"]
    
    def __repr__(self) -> str:
        return self.spec

class Stage:
    """A Snap! stage."""
    def __init__(self, data: dict):
        self._data = data
        self.name = self._data["@name"]
        self.width = self._data["@width"]
        self.height = self._data["@height"]
        self.costume = self._data["@costume"]
        self.color = tuple(self._data["@color"].split(","))
        self.tempo = self._data["@tempo"]
        self.threadsafe = self._data["@threadsafe"]
        self.penlog = self._data["@penlog"]
        self.volume = self._data["@volume"]
        self.pan = self._data["@pan"]
        self.lines = self._data["@lines"]
        self.ternary = self._data["@ternary"]
        self.hyperops = self._data["@hyperops"]
        self.codify = self._data["@codify"]
        self.inheritance = self._data["@inheritance"]
        self.sublist_ids = self._data["@sublistIDs"]
        self.id = self._data["@id"]
        self.pentrails = self._data["pentrails"]
        self.sprites = [Sprite(i) for i in self._data["sprites"]["sprite"]]
        self.costumes = [Costume(i) for i in self._data["costumes"]["list"].get("item", [])]
        self.sounds = [Sound(i) for i in self._data["sounds"]["list"].get("item", [])]
        self.watchers = [Watcher(i) for i in self._data["sprites"].get("watcher", [])]

class Sprite:
    """A Snap! sprite."""
    def __init__(self, data: dict):
        self._data = data
        self.name = self._data["@name"]
        self.idx = self._data["@idx"]
        self.x = self._data["@x"]
        self.y = self._data["@y"]
        self.heading = self._data["@heading"]
        self.scale = self._data["@scale"]
        self.volume = self._data["@volume"]
        self.pan = self._data["@pan"]
        self.rotation = self._data["@rotation"]
        self.instrument = self._data.get("@instrument")
        if self._data["@draggable"] == "true":
            self.draggable = True
        else:
            self.draggable = False
        self.hidden = self._data.get("@hidden")
        self.costume = self._data["@costume"]
        self.color = tuple(self._data["@color"].split(","))
        self.pen = self._data["@pen"]
        self.id = self._data["@id"]
        self.sounds = [Sound(i) for i in self._data["sounds"]["list"].get("item", [])]
        self.variables = _variables_from_data(data)
        
class Costume:
    """A Snap! costume."""
    def __init__(self, data):
        self._data = data
        self.name = self._data["costume"]["@name"]
        self.center_x = self._data["costume"]["@center-x"]
        self.center_y = self._data["costume"]["@center-y"]
        self.image = self._data["costume"]["@image"]
        self.id = self._data["costume"]["@id"]

class Sound:
    """A Snap! sound."""
    def __init__(self, data):
        self._data = data
        self.name = self._data["sound"]["@name"]
        self.sound = self._data["sound"]["@sound"]

class Variable:
    """A Snap! variable."""
    def __init__(self, data):
        self._data = data
        self.name = self._data["@name"]
        self.value = self._data["l"]

class Watcher:
    """A Snap! variable watcher."""
    def __init__(self, data):
        self._data = data
        self.var = self._data["@var"]
        self.style = self._data["@style"]
        self.x = self._data["@x"]
        self.y = self._data["@y"]
        self.color = tuple(self._data["@color"].split(","))
        self.scope = self._data.get("@scope")

def project_from_xml(xml: str) -> Project:
    """Obtain a Project object from an XML string."""
    return Project(parse(xml, force_list=("sprite", "scene", "item", "variable")))

def project_from_path(path: str) -> Project:
    """Obtain a Project object from an XML file, given its path."""
    f = open(path)
    project = project_from_xml(f.read())
    f.close()
    return project

def _variables_from_data(data: dict):
    if data.get("variables"):
        variables = [Variable(i) for i in data["variables"].get("variable", [])]
    else:
        variables = []
    return variables
