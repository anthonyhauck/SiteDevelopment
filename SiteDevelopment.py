from random import randint, uniform
import traceback

from hypar import glTF

from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup

model = glTF()
colorAqua = model.add_material(0.0, 0.631, 0.945, 0.9, 0.8, "Aqua")
colorBlue = model.add_material(0.0, 0.631, 0.945, 0.9, 0.8, "Blue")
colorGranite = model.add_material(0.25, 0.25, 0.25, 0.9, 0.8, "Granite")
colorGray = model.add_material(0.5, 0.5, 0.5, 0.9, 0.8, "Gray")
colorGreen = model.add_material(0.486, 0.733, 0.0, 0.9, 0.8, "Green")
colorOrange = model.add_material(0.964, 0.325, 0.078, 0.9, 0.8, "Orange")
colorPurple = model.add_material(0.75, 0.07, 1.0, 0.9, 0.8, "Purple")
colorSand = model.add_material(1.0, 0.843, 0.376, 1.0, 0.8, "Sand") 
colorWhite = model.add_material(1.0, 1.0, 1.0, 0.5, 0.8, "White")    
colorYellow = model.add_material(1.0, 0.733, 0.0, 0.9, 0.8, "Yellow")    


siteWest = \
[
    aecPoint(1335.5515, 2415.9574),
    aecPoint(1263.2383, 2389.3717),
    aecPoint(1398.0416, 2022.7068),
    aecPoint(1551.4579, 1522.2420),
    aecPoint(1696.0947, 1356.2240),
    aecPoint(1900.4278, 2314.2330),
    aecPoint(1900.2106, 2351.8979),
]

siteEast = \
[
    aecPoint(2000.1994, 2289.2733),
    aecPoint(2700.4829, 2289.2733),
    aecPoint(2700.4829, 1737.8546),
    aecPoint(2108.5229, 1263.0727),
    aecPoint(1792.2478, 1263.0727),
    aecPoint(1771.8803, 1282.6400)
]

buildings = \
[
    {
        'color' : colorAqua,
        'name' : 'venue',
        'plan' : (1, 9)
    },
    
    {
        'color' : colorYellow,
        'name' : 'conference',
        'plan' : (1, 13)
    },
    
    {
        'color' : colorOrange,
        'name' : 'event',
        'plan' : (1, 13)        
    },   
    
    {
        'color' : colorPurple,
        'name' : 'hotelluxury',
        'plan' : (1, 13)
    },
    
    {
        'color' : colorBlue,
        'name' : 'office',
        'plan' : (1, 13)
    },
    
    {
        'color' : colorGranite,
        'name' : 'parking',
        'plan' : (2, 8)
    },
    
    {
        'color' : colorGreen,
        'name' : 'retail',
        'plan' : (1, 13)        
    },
    
    {
        'color' : colorWhite,
        'name' : 'administration',
        'plan' : (1, 9)   
    }
]

def makeSpace(building, point, xSize, ySize):
    try:
        spcType = randint(building['plan'][0], building['plan'][1])
        space = aecSpace()
        shaper = aecShaper()
        if spcType == 1:
            space.boundary = shaper.makeBox(point, xSize, ySize)
            space.rotate(uniform(0, 360))
            x = 0
            boundaries = randint(1, 5)
            tempFloor = aecSpace()
            while x < boundaries:
                if xSize <= ySize:
                    tempFloor.boundary = \
                    shaper.makeBox(point, uniform(xSize, ySize), uniform(xSize, ySize))
                else:
                    tempFloor.boundary = \
                    shaper.makeBox(point, uniform(ySize, xSize), uniform(ySize, xSize))                   
                tempFloor.rotate(uniform(0, 360))
                space.add(tempFloor.points_floor)
                x += 1  
        if spcType == 2:  space.boundary = shaper.makeCylinder(point, (xSize * 0.5))
        if spcType > 2 and spcType < 9: 
                          space.boundary = shaper.makePolygon(point, (xSize * 0.5), spcType) 
        if spcType == 9:  space.boundary = shaper.makeCross(point, xSize, ySize)     
        if spcType == 10: space.boundary = shaper.makeH(point, xSize, ySize) 
        if spcType == 11: space.boundary = shaper.makeL(point, xSize, ySize) 
        if spcType == 12: space.boundary = shaper.makeT(point, xSize, ySize) 
        if spcType == 13: space.boundary = shaper.makeU(point, xSize, ySize)
        return space
    except Exception:
        traceback.print_exc()
        return None

def siteDevelopment(diameter: float = 100, targetArea: float = 100000):
    spacer = aecSpacer()        
    sitWest = aecSpace()
    sitEast = aecSpace()
    sitWest.boundary = siteWest
    sitEast.boundary = siteEast
    sitWest.height = 20    
    sitWest.level = -20
    sitEast.height = 20   
    sitEast.level = -20
    mesh = sitWest.mesh_graphic
    model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, colorSand)  
    mesh = sitEast.mesh_graphic
    model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, colorSand)      
    spcGroup = aecSpaceGroup()
    allLevels = 0
    area = 0
    for building in buildings:
        if randint(0, 1) == 0 : site = sitWest
        else: site = sitEast
        boundary = site.points_floor
        point = site.point_ceiling
        xSize = diameter * uniform(1, 3)
        ySize = diameter * uniform(1, 3)
        targetArea = uniform((targetArea - 20000), (targetArea + 20000))        
        space = None
        while not space:
            space = makeSpace(building, point, xSize, ySize)
            if not space.fitWithin(boundary): 
                point = site.point_ceiling
                space = None
        space.height = 15
        build = [space] + spacer.stackToArea(space, targetArea)
        spcGroup.clear()
        spcGroup.add(build)
        levels = spcGroup.count
        allLevels += levels
        area += spcGroup.area
        if building['name'] != 'parking':
            if levels >= 10:
                index = 10
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1
            if levels >= 20:
                index = 20
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1                   
            if levels >= 30:
                index = 30
                while index < levels:
                    spcGroup.scale(0.8, 0.8, 1, index = index)
                    index += 1      
        build = spcGroup.spaces
        color = building['color']
        for space in build:
            mesh = space.mesh_graphic
            model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, color)                  
    return {"model": model.save_base64(), 'computed':{'floors':allLevels, 'area':area}}   
#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\siteDevelopment\\model.glb')
#
#siteDevelopment(diameter = uniform(50, 200), targetArea = uniform(100000, 250000))




