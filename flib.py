import math
import time


def Matrix(*args):
    """The args are the rows, and should be definded as n variables for n columns
    To create an empty array, pass in "size", the width of the matrix and the height of the matrix as three variables."""
    matrixConstructor = []
    if args[0] == "size":
        for i in range(args[2]):
                matrixConstructor.append([])
                for j in range(args[1]):
                    matrixConstructor[i].append(0)
    else:
        for i in range(len(args)):
            try:
                if len(args[i]) > 1:
                    matrixConstructor.append([])
                    for j in range(len(args[i])):
                        matrixConstructor[i].append(args[i][j])
                else:
                    matrixConstructor.append(args[i])
            except TypeError:
                matrixConstructor.append(args[i])
    return matrixConstructor

def mMult(matrix1, matrix2): #issue, wont multiply a 4x4 matrix with an 4xn matrix
    """Multiply a ixk matrix with a kxj matrix
    Returns a ixj matrix"""
    list(matrix1)
    list(matrix2)
    mat1xy = ( len(matrix1[0]),len(matrix1)) #column, row
    mat2xy = (len(matrix2[0]),len(matrix2))
    resMat = Matrix("size", mat2xy[0], mat1xy[1])
    #print(resMat)
    if mat1xy[0] != mat2xy[1]: 
        raise Exception("Matrix Multiplication Error: Epic FAIL!\n(the matrix sizes are not compatible for multiplication)")
    for i in range(mat1xy[1]): #row 1
        #print(f'i value: {i}')
        for j in range(mat2xy[0]): #column 2
            #print(f'j value: {j}')
            for k in range(mat2xy[1]): #row 2
                resMat[i][j] += matrix1[i][k] * matrix2[k][j]
    return resMat

def concantenate(matrix1, matrix2) -> Matrix:
    """Combines two matrices non mathematically"""

    for i in range(len(matrix1)): #goes
        try:
            for j in range(len(matrix2[i])):
                matrix1[i].append(matrix2[i][j]) #is it that easy?????????
        except TypeError:
            matrix1[i].append(matrix2[i])
    return matrix1

def vSplit(matrix):
    """Splits a matrix into 1xn columns"""
    matlist = []
    matlis = []
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            matlis.append(matrix[j][i])
        matlist.append(Matrix(matlis[0], matlis[1], matlis[2], matlis[3]))
        matlis = []
    return matlist

def roundMatrix(matrix):
    """Rounds all values in a matrix to whole numbers"""
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix[x][y] = round(matrix[x][y])
    return matrix

def ROTATIONZ(theta):
    theta /= 50
    return Matrix([math.cos(theta), -math.sin(theta), 0, 0],[math.sin(theta), math.cos(theta), 0, 0],[0, 0, 1, 0], [0,0,0,1]) #rotmat on the z axis

def ROTATIONY(theta):
    theta /= 50
    return Matrix([math.cos(theta), 0, math.sin(theta), 0], [0, 1, 0, 0], [-math.sin(theta), 0, math.cos(theta), 0],[0, 0, 0, 1])

def ROTATIONX(theta):
    theta /= 50
    return Matrix([1, 0, 0, 0],[0, math.cos(theta), -math.sin(theta), 0],[0, math.sin(theta), math.cos(theta), 0],[0,0,0,1])

def TRANSLATE(x,y,z):
    """Returns a 4x4 translation matrix"""
    #x /= 50
    #y /= 50
    #z /= 50
    return Matrix([1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1])

def SCALE(factor):
    """Returns a 4x4 scale matrix"""
    return Matrix([factor,0,0,0],[0,factor,0,0],[0,0,factor,0],[0,0,0,1])

def TEST(TARGET,REPEATS, *ARGS):
    """Tests the time difference between functions executions"""
    end = 0
    for i in range(REPEATS):
        start = time.time_ns()
        exec(f"{TARGET}({ARGS})")
        end += time.time_ns() - start
    return (end//REPEATS)/1000000

def StrToInt(array):
    """Converts an array of strings to an array of integers"""
    x = []
    for i in range(len(array)):
        try:
            x.append(int(array[i]))
        except TypeError:
            pass
    return x



if __name__ == "__main__":
    matrix1 = Matrix((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
    matrix2 = Matrix((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
    mat3 = mMult(matrix2, matrix1)
    print(mat3)
    #mat4 = concantenate(matrix1, mat3)
    #rint(mat4)
    #print(vSplit(mat4))
    MINE, THEIRS = 0,0
    for i in range(10):
        MINE += TEST('Matrix', 10000, (1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16)) 
        THEIRS += TEST('np.array', 10000, [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
    print(f"Mine was {MINE/10}ms and theirs was {THEIRS/10}ms on average. ")