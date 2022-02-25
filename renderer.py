import math, time, pygame, threading, psutil
from flib import *

'''
This is my 3D Renderer.

'''
## (Mostly) Constant Definitions
pygame.font.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOV = 75 
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
physicsClock = pygame.time.Clock()
physicsSpeed = 50  #default:50
FPS = 90  # Frames per second.
surface = pygame.Surface((WIDTH, HEIGHT))
ASPECT_RATIO = WIDTH/HEIGHT
NEAR_PLANE = 0.1
FAR_PLANE = 1000

class WorldObject():
    """Base WorldObject class. Grabs a mesh of points in a world position."""
    objects = [] #collects objects to make rendering easier

    def __init__(self, initialPosition):#
        self.vertices = []
        self.projectedCoordinates = None
        self.transformBuffer = []
        self.initX, self.initY, self.initZ = initialPosition
        self.scale = 1/15 * self.initZ
        self.objects.append(self)
        self.centreX, self.centreY, self.centreZ = self.initX, self.initY, self.initZ
        self.render = True

    def definePoints(self, *points) -> None:
        self.vertexMatrix =  Matrix([self.initX+int(points[0][0])], [self.initY+int(points[0][1])], [self.initZ+int(points[0][2])],[1])
        for i in range(len(points)):
            if i == 0:
                pass
            x, y, z = points[i]
            self.vertices.append(Matrix(self.initX+x, self.initY+y, self.initZ+z,1))
            self.vertexMatrix = concantenate(self.vertexMatrix, self.vertices[i])
        self.recalculateCentre()

    def getPoints(self) -> list:
        return self.vertexMatrix

    def applyTransformation(self, matrix) -> None: #when applying multiple transformations, pass the product of the matrices
        self.transformBuffer.append(matrix)

    def getProjectedCoordinates(self, theta, f, n) -> Matrix:
        projectedCoordinates = []
        projectionMatrix = Matrix([1/(math.tan((theta/2)*(math.pi/180))),0,0,0] , [0,1/(math.tan((theta/2)*(math.pi/180))),0,0] , [0,0,f+n/(f-n),-1] , [0,0,-(f*n)/(f-n),0])
        #projectionMatrix = Matrix([1/(math.tan((theta/2))),0,0,0] , [0,1/(math.tan((theta/2)*(math.pi/180))),0,0] , [0,0,f/(f-n),1] , [0,0,-(f*n)/(f-n),0])
        projectedCoordinates = vSplit(roundMatrix(mMult(projectionMatrix,self.vertexMatrix)))
        return projectedCoordinates

    
    def recalculateCentre(self):
        self.centreX = sum(self.vertexMatrix[0])/len(self.vertexMatrix[0])
        self.centreY = sum(self.vertexMatrix[1])/len(self.vertexMatrix[1])
        self.centreZ = sum(self.vertexMatrix[2])/len(self.vertexMatrix[2])
    @staticmethod
    def physicsUpdate():
        for object in range(len(__class__.objects)): #loops through all the objects
            transformation = TRANSLATE(-__class__.objects[object].centreX, -__class__.objects[object].centreY, -__class__.objects[object].centreZ) #moves the shape to the origin
            __class__.objects[object].vertexMatrix = mMult(transformation, __class__.objects[object].vertexMatrix)
            
            if len(__class__.objects[object].transformBuffer) != 0:
                for j in range(len(__class__.objects[object].transformBuffer)):
                    __class__.objects[object].vertexMatrix = mMult(__class__.objects[object].transformBuffer[j], __class__.objects[object].vertexMatrix)
            
            transformation = TRANSLATE(__class__.objects[object].centreX, __class__.objects[object].centreY, __class__.objects[object].centreZ) #moves the shape back to its original position
            __class__.objects[object].vertexMatrix = mMult(transformation, __class__.objects[object].vertexMatrix)
            __class__.objects[object].vertices = vSplit(__class__.objects[object].vertexMatrix)
            __class__.objects[object].transformBuffer = []
            __class__.objects[object].recalculateCentre()


    @staticmethod
    def render(surface):
        for object in range(len(__class__.objects)):
            __class__.objects[object].scale = 1/15 * __class__.objects[object].centreZ
            __class__.objects[object].projectedCoordinates = __class__.objects[object].getProjectedCoordinates(FOV, FAR_PLANE, NEAR_PLANE)
            for j in range(len(__class__.objects[object].projectedCoordinates)):
                for i in range(len(__class__.objects[object].projectedCoordinates)): # modify this to support a matrix of vertices
                    if (__class__.objects[object].vertexMatrix[2][j] < NEAR_PLANE or __class__.objects[object].vertexMatrix[2][i] > FAR_PLANE):
                        pass
                    else:
                        try:
                            pygame.draw.line(surface, WHITE, (int(__class__.objects[object].projectedCoordinates[j][0]), int(__class__.objects[object].projectedCoordinates[j][1])), (int(__class__.objects[object].projectedCoordinates[i][0]), int(__class__.objects[object].projectedCoordinates[i][1])))
                        except:
                            pass

#testAxis = WorldObject((150, 150, 1))
#testAxis.definePoints((-1000, 150, 1), (1000, 150, 1))
testCube = WorldObject((100,100,100))
testCube.definePoints((100,100,0),(100,0,100),(100,0,0),(0,100,100),(0,100,0),(0,0,100),(0,0,0))

def drawAxisGuides(surface):
    pygame.draw.line(surface, (0, 255, 0), (10, 110), (110, 110)) #x
    pygame.draw.line(surface, (255, 0, 0), (10, 110), (10, 10)) #y

myfont = pygame.font.SysFont("Comic Sans MS", 20)
timevals = []
running = True
rendering = True

def physicsClockThread():
    while running:
        ### Physics Updates Go Below Here
        translationz = TRANSLATE(1, 0, 0)
        rotation_matrix_y = ROTATIONY(4.5)
        testCube.applyTransformation(translationz)
        testCube.applyTransformation(rotation_matrix_y)
        ###


        WorldObject.physicsUpdate()
        physicsClock.tick(physicsSpeed)

coordinate = pygame.font.Font("freesansbold.ttf", 24)

physicsThread = threading.Thread(target=physicsClockThread)
print("Starting Physics Thread...")
physicsThread.start()
cpu_usage = []
while running:
    cpu_usage= psutil.cpu_percent()
    start_ns = time.time_ns()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print(f'The average frame render time was {round((sum(timevals)/len(timevals))/ 1000000000, 5)} seconds')
            running = False
            print("Stopping Physics Thread...")
            physicsThread.join()
            print("Stopped.")
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rendering = not rendering
                print(f"Rendering: {rendering}\n The centre at this value was {testCube.centreY}")

    coordinateImage = coordinate.render(f"CPU:{cpu_usage}%; FPS{FPS}", True, WHITE)
    other = coordinate.render(f'({testCube.centreX},{testCube.centreY},{testCube.centreZ})', True, WHITE)

    if rendering:
        screen.fill(BLACK)
        drawAxisGuides(screen)
        WorldObject.render(screen)        
        screen.blit(coordinateImage, (1000,10))
        pygame.draw.circle(screen, (125, 0,0), (testCube.centreX, testCube.centreY), 5)
        screen.blit(other, (10, 670))
        pygame.display.update()
        timevals.append(time.time_ns() - start_ns)
    clock.tick(FPS)
physicsThread.join()



