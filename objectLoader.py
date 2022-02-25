import flib as fb

class FileFormatter():
    def __init__(self, filename):
        self.filename = filename
        self.vertexList = []
        self.vertexIndex = []
        self.faceLib = []
        self.openfile()

    def decode(self, content):
        if content[0] == "v":
            """Vertex"""
            self.vertexList.append(fb.StrToInt(content[1:-1]))
            self.vertexIndex.append(int(content[-1]))
        elif content[0] == "f":
            self.faceLib.append(content[1:])


    def openfile(self):
        f = open(self.filename, "r")
        for content in f.readlines():
            content = content.split(" ")
            content[-1] = content[-1][:-1]
            
            self.decode(content)
    
    def getData(self):
        return f"There are {len(self.faceLib)} faces and The vertices are \n{self.vertexList}, {self.vertexIndex}"

filename = "3D Engine\WorldObjects\cube.FUCKOFF"

x = FileFormatter(filename)
print(x.getData())