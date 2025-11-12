#-----------Modelado con width, height, depth ----------------------------import pandas as pd
import pandas as pd


#---------------FUNCION GENERAR .CGA ---------------------------

class GenerarCGA():

    #Funcion para ingresar datos con csv y generar regla procedural - SIRVE PARA LA VISTA DE CSV
    
    def GenerarProceduralCsv(row):    
        
        reglaProcedural = ''
        
        TypeBuild = row['TipoEdificio']
        HeightValue = row['Altura']
        WidthValue = row['Ancho']
        DepthValue = row['Profundidad']
        windowsAmount = row['CantidadVentanas']
        FloorsValue = row['floors']
            
        
        
        if TypeBuild == "residencial":
            

            reglaProcedural += f"""version "2020.0"

#Measures Build
attr lotWidth = scope.sx        // Ancho total del lote
attr lotDepth = scope.sz        // Profundidad total del lote
attr uThickness = lotWidth * 0.25  // Grosor de los lados de la "U"
attr lotHeight = {HeightValue}

#BuildInf
attr floorsLevel = {FloorsValue}
attr floorMeasure = lotHeight/floorsLevel - 1
attr floorPerLevel = {windowsAmount}
attr floorQuantity = (lotDepth * 0.7) / floorPerLevel

#Textures
attr wall_texture = "assets/ladrillo.jpg"
attr roof_texture = "assets/wall3.jpeg"
attr window_texture = "assets/texture.jpg"
attr glass_texture = "assets/glass.jpg"
attr column_texture = "assets/blanco.jpg"
attr topDown_texture = "assets/greyPaint.jpg"
attr ground_texture = "assets/ground.jpg"

#OBJECTS
door_obj = "assets/Door.fbx"
attr window_obj = "assets/ventanaObj5.obj"

Lot --> 
split(x) {{ uThickness: LeftSide | lotWidth * 0.5: Center | uThickness: RightSide }}

LeftSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.6 : blockMiddle |lotDepth * 0.2 : blockBack }}

RightSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.6 : blockMiddle |lotDepth * 0.2 : blockBack }}
	
	
//SIDES
blockTop-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockTopFront
        | back: blockTopBack
        | left: blockTopLeft
        | right: blockTopRight
        | top: RoofTop}}

//Bloque esquina fachada frontal
blockTopBack-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
	 		 
groundCornerFront-->
	PaintColumns
	
topCornerFront-->
	PaintColumns

//DivisionHorizontal		
blockTopLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}       

blockTopRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}   
	 		 
groundCorner-->
	PaintColumns
topCorner-->
	PaintColumns

//Division vertical	 		 
floorCornerSide-->
	split(x){{ {{1: column |~(lotDepth * 0.2) / 2: floorsCorners}}*
	 		 |1 : lastColumn}}
	 		 
column-->
	PaintColumns
lastColumn-->
	PaintColumns	


floorsCorners-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeCenterCorner
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeCenterCorner-->
	split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeCenterWindow
	 		 |floorMeasure/3: facadeDown}}
	 		 
facadeCenterWindow-->
	Window
	
//Bloque fachada frontal parte de atras

blockBack-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackFront
        | back: blockBackBack
        | left: blockBackLeft
        | right: blockBackRight
        | top: RoofTop}}

blockBackFront-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
		
blockBackLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}

blockBackRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}
	 		 
	 		 
//Bloques de los lados central

blockMiddle-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockMiddleFront
        | back: blockMiddleBack
        | left: blockMiddleLeft
        | right: blockMiddleRight
        | top: RoofTop}}

//DivisionHorizontal
blockMiddleLeft-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}

blockMiddleRight-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 
//Division lateral
floorCornerFront-->
	split(x){{ {{1: column |~(lotDepth * 0.6) / floorPerLevel: floorsCornersCenter}}*
	 		 |1 : lastColumn}}
	 		 
floorsCornersCenter-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeMiddleCenter
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeMiddleCenter-->
		split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeMiddleCenterWindow
			 		 |floorMeasure/3: facadeDown}}

facadeLeft-->
	PaintWalls
facadeRight-->
	PaintWalls
facadeUp-->
	PaintWalls
facadeDown-->
	PaintWalls
	
facadeMiddleCenterWindow-->
	Window
//center	
Center-->
	split(z){{lotDepth * 0.2 : blockTopCenter |lotDepth * 0.6 : blockMiddleCenter |lotDepth * 0.2 : blockBackCenter }}
	
blockBackCenter-->
	split(x){{(lotWidth * 0.5)*0.3: towerLeft | (lotWidth * 0.5)*0.4: aisle |(lotWidth * 0.5)*0.3: towerRight }}
	
aisle-->
	Paintground	

blockMiddleCenter-->
	Paintground	
	
blockTopCenter-->
	split(x){{(lotWidth * 0.5)*0.3: towerLeft | (lotWidth * 0.5)*0.4: aisle |(lotWidth * 0.5)*0.3: towerRight }}
	
//TOWEr HALL
towerLeft-->
	extrude(lotHeight)
	comp(f) {{
        front: towerFrontTopFront
        | back: towerFrontTopBack
        | left: towerFrontTopLeft
        | right: towerFrontTopRight
        | top: RoofTop}}
        
towerFrontTopFront-->
	PaintColumns
towerFrontTopBack-->
	PaintColumns
towerFrontTopRight-->
	PaintColumns

towerRight-->
	extrude(lotHeight)
	comp(f) {{
        front: towerFrontBottomFront
        | back: towerFrontBottomBack
        | left: towerFrontBottomLeft
        | right: towerFrontBottomRight
        | top: RoofTop}}

towerFrontBottomFront-->
	PaintColumns
towerFrontBottomBack-->
	PaintColumns
towerFrontBottomRight-->
	PaintColumns
towerFrontBottomLeft-->
	PaintColumns
	
#DESARROLLO TECHO
RoofTop --> 
    comp(f) {{
        front: RoofFront
        | back: RoofBack
        | left: RoofLeft
        | right: RoofRight
        | top: RoofT
    }}
    
RoofFront-->
	split(x){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	split(y){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	
	
sideLeft-->
	extrude(2)
	PaintColumns
	
sideRight-->
	extrude(2)
	PaintColumns
	
#TEXTURAS Y OBJETOS	
PaintRoof-->
	setupProjection(0, scope.xy, 30 , 30)
	texture(roof_texture)
	projectUV(0)
	
PaintColumns-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(topDown_texture)
	projectUV(0) 
	
PaintWalls-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(column_texture)
	projectUV(0)
	
Paintground-->
	setupProjection(0, scope.xz, 10 , 10)
	texture(ground_texture)
	projectUV(0)	

PaintFacadeTopDown-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(wall_texture)
	projectUV(0)
	
Door -->
      i(door_obj)
      s(1  , floorMeasure, floorQuantity-10)  // Escala la ventana al tama o deseado
      t(0,-1,1)
      r(0,90,0)

Glass-->
	setupProjection(0, scope.xy, 6 , 6)
	texture(glass_texture)
	projectUV(0) 
	
Window-->
      i(window_obj)
      s(((lotDepth * 0.2) / 2)*0.44 , floorMeasure/3, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass

WindowCorner-->
      i(window_obj)
      s(floorMeasure-0.7 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass


      
WindowBackCenter-->
      i(window_obj)
      s(floorMeasure+3.8 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass	"""
            
            return reglaProcedural

        elif TypeBuild == "comercial":
            
            reglaProcedural += f"""version "2020.0"

#Measures Build
attr lotWidth = scope.sx        // Ancho total del lote
attr lotDepth = scope.sz        // Profundidad total del lote
attr uThickness = lotWidth * 0.25  // Grosor de los lados de la "U"
attr lotHeight = {HeightValue}

#BuildInf
attr floorsLevel = {FloorsValue}
attr floorMeasure = lotHeight/floorsLevel - 1
attr floorPerLevel = {windowsAmount}
attr floorQuantity = (lotDepth * 0.7) / floorPerLevel

#Textures
attr wall_texture = "assets/ladrillo.jpg"
attr roof_texture = "assets/wall3.jpeg"
attr window_texture = "assets/texture.jpg"
attr glass_texture = "assets/glass.jpg"
attr column_texture = "assets/blanco.jpg"
attr topDown_texture = "assets/greyPaint.jpg"
attr ground_texture = "assets/ground.jpg"
attr grass_texture = "assets/grass.jpg"

#OBJECTS
door_obj = "assets/Door.fbx"
attr window_obj = "assets/ventanaObj5.obj"

Lot --> 
    split(x) {{ uThickness: LeftSide | lotWidth * 0.5: Center | uThickness: RightSide }}   // Dividir el lote en 3 partes

LeftSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.7 : blockMiddle |lotDepth * 0.1 : blockBack }}

RightSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.7 : blockMiddle |lotDepth * 0.1 : blockBack }}
	
	
//SIDES
blockTop-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockTopFront
        | back: blockTopBack
        | left: blockTopLeft
        | right: blockTopRight
        | top: RoofTop}}

//Bloque esquina fachada frontal
blockTopBack-->
	PaintColumns
	 		 
groundCornerFront-->
	PaintColumns
	
topCornerFront-->
	PaintColumns

//DivisionHorizontal		
blockTopLeft-->
	PaintColumns      

blockTopRight-->
	PaintColumns   
	 		 
groundCorner-->
	PaintColumns
topCorner-->
	PaintColumns

//Division vertical	 		 
floorCornerSide-->
	split(x){{{{1: column |~(lotDepth * 0.2) / 2: floorsCorners}}*
	 		 |1 : lastColumn}}
	 		 
column-->
	PaintColumns
lastColumn-->
	PaintColumns	


floorsCorners-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeCenterCorner
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeCenterCorner-->
	split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeCenterWindow
	 		 |floorMeasure/3: facadeDown}}
	 		 
facadeCenterWindow-->
	Window
	
//Bloque fachada frontal parte de atras

blockBack-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackFront
        | back: blockBackBack
        | left: blockBackLeft
        | right: blockBackRight
        | top: RoofTop}}

blockBackFront-->
	split(y){{{{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
		
blockBackLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}        

blockBackRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}} 
	 		 
	 		 
//Bloques de los lados central

blockMiddle-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockMiddleFront
        | back: blockMiddleBack
        | left: blockMiddleLeft
        | right: blockMiddleRight
        | top: RoofTop}}

//DivisionHorizontal
blockMiddleLeft-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}

blockMiddleRight-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 
//Division lateral
floorCornerFront-->
	split(x){{ {{1: column |~(lotDepth * 0.6) / floorPerLevel: floorsCornersCenter}}*
	 		 |1 : lastColumn}}
	 		 
floorsCornersCenter-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeMiddleCenter
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeMiddleCenter-->
		split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeMiddleCenterWindow
			 		 |floorMeasure/3: facadeDown}}

facadeLeft-->
	PaintWalls
facadeRight-->
	PaintWalls
facadeUp-->
	PaintWalls
facadeDown-->
	PaintWalls
	
facadeMiddleCenterWindow-->
	Window
//center	
Center-->
	split(z){{lotDepth * 0.2 : blockTopCenter |lotDepth * 0.6 : blockMiddleCenter |lotDepth * 0.2 : blockBackCenter }}
	
blockMiddleCenter-->
	Paintground
blockTopCenter-->
	Paintground
	
blockBackCenter-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackCenterFront
        | back: blockBackCenterBack
        | left: blockBackCenterLeft
        | right: blockBackCenterRight
        | top: RoofTop}}
        


//DivisionHorizontal
blockBackCenterBack-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*

	 		 |1 : topCornerFront}}
blockBackCenterFront-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 

#DESARROLLO TECHO
RoofTop --> 
    comp(f) {{
        front: RoofFront
        | back: RoofBack
        | left: RoofLeft
        | right: RoofRight
        | top: RoofT
    }}
    
RoofFront-->
	split(x){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	split(y){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	
	
sideLeft-->
	extrude(2)
	PaintColumns
	
sideRight-->
	extrude(2)
	PaintColumns

	
	
#TEXTURAS Y OBJETOS	
PaintRoof-->
	setupProjection(0, scope.xy, 30 , 30)
	texture(roof_texture)
	projectUV(0)
	
PaintColumns-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(topDown_texture)
	projectUV(0) 
	
PaintWalls-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(column_texture)
	projectUV(0)
	
Paintground-->
	setupProjection(0, scope.xz, 20 , 20)
	texture(grass_texture)
	projectUV(0)	

PaintFacadeTopDown-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(wall_texture)
	projectUV(0)
	
Door -->
      i(door_obj)
      s(1  , floorMeasure, floorQuantity-10)  // Escala la ventana al tama o deseado
      t(0,-1,1)
      r(0,90,0)

Glass-->
	setupProjection(0, scope.xy, 6 , 6)
	texture(glass_texture)
	projectUV(0) 
	
Window-->
      i(window_obj)
      s(((lotDepth * 0.2) / 2)*0.44 , floorMeasure/3, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass

WindowCorner-->
      i(window_obj)
      s(floorMeasure-0.7 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass


      
WindowBackCenter-->
      i(window_obj)
      s(floorMeasure+3.8 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass	"""
        
            return reglaProcedural
        
            

        elif TypeBuild == "industrial":
            
            reglaProcedural += f"""version "2020.0"

attr wall_texture = "assets/textureChapGreca.jpg"
attr door_obj = "assets/industrialDoor.obj"

attr height = 30
attr width = scope.sx
attr depth = scope.sz
attr modulos = 6
attr frontModules = 5
attr sizeWind = depth/modulos - 1
attr sizeFrontModule = width/frontModules +1




Structure-->
	extrude(height)

	ShipBuilding
	
ShipBuilding-->
	comp(f){{ front: FrontFacade
			|left: LeftFacade
			|right: RightFacade
			|back: BackFacade
			|top: RoofShip}}
			

	
FrontFacade-->
	split(x){{ {{~1: beamsFrontFacade
			| sizeFrontModule : WallFrontFacade(split.index)}}*
			|~1:  LastBeam}}
			

	
RightFacade-->
	split(x){{ {{1: beamsRightFacade(split.index)
			 |sizeWind : WallRightFacade(split.index)}}*
			 | ~1: LastBeam}}
	

			 
LeftFacade-->	
	split(x){{ {{1: beamsLeftFacade(split.index)
			 |~sizeWind : WallLeftFacade(split.index)}}*
			 | 1: LastBeam}}
			 
BackFacade-->
	split(x){{ {{1: beamsFrontFacade
			| ~sizeFrontModule : WallBackFacade(split.index)}}*
			|1:  LastBeam}}
			


//ROOF RULES
RoofShip-->	
	roofGable(5)
	split(z){{ {{1: beamsRoof
			 |~14 : RoofTiles}}*
			 | 1: LastBeamRoof}}

RoofTiles-->
	RoofTexture
	
beamsRoof-->
	RoofTexture
	
LastBeamRoof-->
	RoofTexture	


WallBackFacade(backIndex)-->
	case backIndex == 0:
				WallTexture
		
		
	else :
		split(y){{0.5:FloorFrontFacade
				|height-2: WallFront(split.index)
				|1: WindowFront}}
			 
//FRONT RULES						 
WallFrontFacade(wallIndex)-->
	case wallIndex == 3:
			split(y){{height/2 +1: doorLevel
					|height/2 -1: restLevel}}
				
	case wallIndex == frontModules - 1:
				Door
		
	else :
		split(y){{0.5:FloorFrontFacade
				|height-2: WallFront(split.index)
				|1: WindowFront}}
				
doorLevel-->
	Door
	
restLevel-->
	WallTexture
				
WallFront(WallFrontIndex)-->
	case WallFrontIndex == 1:
		WallTexture
	
	else:
		WallTexture

FloorFrontFacade-->
	WallTexture
	
beamsFrontFacade-->
	WallTexture
			
//LEFT RULES
WallLeftFacade(wallLeftIndex)-->
	case wallLeftIndex == 0:
		split(y){{10:windowSides}}
		
	else :
		split(y){{0.5:FloorLeftFacade
				|height-2: WallLeft
				|1: WindowSidesLeft}}
				
WallLeft-->
	WallTexture	
	
FloorLeftFacade-->
	WallTexture

beamsLeftFacade(beamLeftIndex)-->
	case beamLeftIndex == 0 :
		WallTexture
	else:
		WallTexture
		
//RIGHT RULES					
WallRightFacade(wallRightIndex)-->
	case wallRightIndex == 0:
		split(y){{10:WindowSidesRight}}
		
	else :
		split(y){{0.5:FloorRightFacade
				|height-2: WallRight
				|1: WindowSidesRight}}

WallRight-->
	WallTexture	
	
FloorRightFacade-->
	WallTexture
		
beamsRightFacade(beamRightIndex)-->
	case beamRightIndex == 0 :
		WallTexture
	else:
		WallTexture

LastBeam-->
	WallTexture
		
//TEXTURE WALLS RULE		
WallTexture -->
	setupProjection(0, scope.xz, 5, 5)
  	texture(wall_texture)
  	projectUV(0)
  	
//TEXTURE ROOF RULE  	
 RoofTexture -->
	setupProjection(0, scope.zx, 20, 20)
  	texture(wall_texture)
  	projectUV(0)


 Door-->
    i(door_obj)
    s(sizeFrontModule , height/2+1, 0.5)  // Escala la ventana al tamaño deseado
    r(0, 0, 0)
    t(0, 0, -0.5)
    
Window -->
    i("window.obj")
    s(1, 1, sizeFrontModule )  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeFrontModule)
    
WindowFront -->
    i("window.obj")
    s(1, 1.5, sizeFrontModule)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeFrontModule)
    
 WindowSidesRight -->
    i("window.obj")
    s(1, 1.5, sizeWind+1)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeWind)       
    
WindowSidesLeft -->
    i("window.obj")
    s(1, 1.5, sizeWind)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeWind)"""

            
        return reglaProcedural
    
  
    
    def GenerarProceduralManual(typebuild, width, height, depth, ventanasPorPiso, floors):    

        TypeBuild = typebuild
        
        reglaProcedural =''
        WidthValue = width
        HeightValue = height
        DepthValue = depth
        windowsAmount = ventanasPorPiso
        FloorsValue = floors
        
        if TypeBuild == "residencial":
            

            reglaProcedural += f"""version "2020.0"

#Measures Build
attr lotWidth = scope.sx        // Ancho total del lote
attr lotDepth = scope.sz        // Profundidad total del lote
attr uThickness = lotWidth * 0.25  // Grosor de los lados de la "U"
attr lotHeight = {HeightValue}

#BuildInf
attr floorsLevel = {FloorsValue}
attr floorMeasure = lotHeight/floorsLevel - 1
attr floorPerLevel = {windowsAmount}
attr floorQuantity = (lotDepth * 0.7) / floorPerLevel

#Textures
attr wall_texture = "assets/ladrillo.jpg"
attr roof_texture = "assets/wall3.jpeg"
attr window_texture = "assets/texture.jpg"
attr glass_texture = "assets/glass.jpg"
attr column_texture = "assets/blanco.jpg"
attr topDown_texture = "assets/greyPaint.jpg"
attr ground_texture = "assets/ground.jpg"

#OBJECTS
door_obj = "assets/Door.fbx"
attr window_obj = "assets/ventanaObj5.obj"

Lot --> 
split(x) {{ uThickness: LeftSide | lotWidth * 0.5: Center | uThickness: RightSide }}

LeftSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.6 : blockMiddle |lotDepth * 0.2 : blockBack }}

RightSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.6 : blockMiddle |lotDepth * 0.2 : blockBack }}
	
	
//SIDES
blockTop-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockTopFront
        | back: blockTopBack
        | left: blockTopLeft
        | right: blockTopRight
        | top: RoofTop}}

//Bloque esquina fachada frontal
blockTopBack-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
	 		 
groundCornerFront-->
	PaintColumns
	
topCornerFront-->
	PaintColumns

//DivisionHorizontal		
blockTopLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}       

blockTopRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}   
	 		 
groundCorner-->
	PaintColumns
topCorner-->
	PaintColumns

//Division vertical	 		 
floorCornerSide-->
	split(x){{ {{1: column |~(lotDepth * 0.2) / 2: floorsCorners}}*
	 		 |1 : lastColumn}}
	 		 
column-->
	PaintColumns
lastColumn-->
	PaintColumns	


floorsCorners-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeCenterCorner
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeCenterCorner-->
	split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeCenterWindow
	 		 |floorMeasure/3: facadeDown}}
	 		 
facadeCenterWindow-->
	Window
	
//Bloque fachada frontal parte de atras

blockBack-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackFront
        | back: blockBackBack
        | left: blockBackLeft
        | right: blockBackRight
        | top: RoofTop}}

blockBackFront-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
		
blockBackLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}

blockBackRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}
	 		 
	 		 
//Bloques de los lados central

blockMiddle-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockMiddleFront
        | back: blockMiddleBack
        | left: blockMiddleLeft
        | right: blockMiddleRight
        | top: RoofTop}}

//DivisionHorizontal
blockMiddleLeft-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}

blockMiddleRight-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 
//Division lateral
floorCornerFront-->
	split(x){{ {{1: column |~(lotDepth * 0.6) / floorPerLevel: floorsCornersCenter}}*
	 		 |1 : lastColumn}}
	 		 
floorsCornersCenter-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeMiddleCenter
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeMiddleCenter-->
		split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeMiddleCenterWindow
			 		 |floorMeasure/3: facadeDown}}

facadeLeft-->
	PaintWalls
facadeRight-->
	PaintWalls
facadeUp-->
	PaintWalls
facadeDown-->
	PaintWalls
	
facadeMiddleCenterWindow-->
	Window
//center	
Center-->
	split(z){{lotDepth * 0.2 : blockTopCenter |lotDepth * 0.6 : blockMiddleCenter |lotDepth * 0.2 : blockBackCenter }}
	
blockBackCenter-->
	split(x){{(lotWidth * 0.5)*0.3: towerLeft | (lotWidth * 0.5)*0.4: aisle |(lotWidth * 0.5)*0.3: towerRight }}
	
aisle-->
	Paintground	

blockMiddleCenter-->
	Paintground	
	
blockTopCenter-->
	split(x){{(lotWidth * 0.5)*0.3: towerLeft | (lotWidth * 0.5)*0.4: aisle |(lotWidth * 0.5)*0.3: towerRight }}
	
//TOWEr HALL
towerLeft-->
	extrude(lotHeight)
	comp(f) {{
        front: towerFrontTopFront
        | back: towerFrontTopBack
        | left: towerFrontTopLeft
        | right: towerFrontTopRight
        | top: RoofTop}}
        
towerFrontTopFront-->
	PaintColumns
towerFrontTopBack-->
	PaintColumns
towerFrontTopRight-->
	PaintColumns

towerRight-->
	extrude(lotHeight)
	comp(f) {{
        front: towerFrontBottomFront
        | back: towerFrontBottomBack
        | left: towerFrontBottomLeft
        | right: towerFrontBottomRight
        | top: RoofTop}}

towerFrontBottomFront-->
	PaintColumns
towerFrontBottomBack-->
	PaintColumns
towerFrontBottomRight-->
	PaintColumns
towerFrontBottomLeft-->
	PaintColumns
	
#DESARROLLO TECHO
RoofTop --> 
    comp(f) {{
        front: RoofFront
        | back: RoofBack
        | left: RoofLeft
        | right: RoofRight
        | top: RoofT
    }}
    
RoofFront-->
	split(x){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	split(y){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	
	
sideLeft-->
	extrude(2)
	PaintColumns
	
sideRight-->
	extrude(2)
	PaintColumns
	
#TEXTURAS Y OBJETOS	
PaintRoof-->
	setupProjection(0, scope.xy, 30 , 30)
	texture(roof_texture)
	projectUV(0)
	
PaintColumns-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(topDown_texture)
	projectUV(0) 
	
PaintWalls-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(column_texture)
	projectUV(0)
	
Paintground-->
	setupProjection(0, scope.xz, 10 , 10)
	texture(ground_texture)
	projectUV(0)	

PaintFacadeTopDown-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(wall_texture)
	projectUV(0)
	
Door -->
      i(door_obj)
      s(1  , floorMeasure, floorQuantity-10)  // Escala la ventana al tama o deseado
      t(0,-1,1)
      r(0,90,0)

Glass-->
	setupProjection(0, scope.xy, 6 , 6)
	texture(glass_texture)
	projectUV(0) 
	
Window-->
      i(window_obj)
      s(((lotDepth * 0.2) / 2)*0.44 , floorMeasure/3, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass

WindowCorner-->
      i(window_obj)
      s(floorMeasure-0.7 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass


      
WindowBackCenter-->
      i(window_obj)
      s(floorMeasure+3.8 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass	"""
            
            return reglaProcedural

        elif TypeBuild == "comercial":
            reglaProcedural += f"""version "2020.0"

#Measures Build
attr lotWidth = scope.sx        // Ancho total del lote
attr lotDepth = scope.sz        // Profundidad total del lote
attr uThickness = lotWidth * 0.25  // Grosor de los lados de la "U"
attr lotHeight = {HeightValue}

#BuildInf
attr floorsLevel = {FloorsValue}
attr floorMeasure = lotHeight/floorsLevel - 1
attr floorPerLevel = {windowsAmount}
attr floorQuantity = (lotDepth * 0.7) / floorPerLevel

#Textures
attr wall_texture = "assets/ladrillo.jpg"
attr roof_texture = "assets/wall3.jpeg"
attr window_texture = "assets/texture.jpg"
attr glass_texture = "assets/glass.jpg"
attr column_texture = "assets/blanco.jpg"
attr topDown_texture = "assets/greyPaint.jpg"
attr ground_texture = "assets/ground.jpg"
attr grass_texture = "assets/grass.jpg"

#OBJECTS
door_obj = "assets/Door.fbx"
attr window_obj = "assets/ventanaObj5.obj"

Lot --> 
    split(x) {{ uThickness: LeftSide | lotWidth * 0.5: Center | uThickness: RightSide }}   // Dividir el lote en 3 partes

LeftSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.7 : blockMiddle |lotDepth * 0.1 : blockBack }}

RightSide-->
	split(z){{lotDepth * 0.2 : blockTop |lotDepth * 0.7 : blockMiddle |lotDepth * 0.1 : blockBack }}
	
	
//SIDES
blockTop-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockTopFront
        | back: blockTopBack
        | left: blockTopLeft
        | right: blockTopRight
        | top: RoofTop}}

//Bloque esquina fachada frontal
blockTopBack-->
	PaintColumns
	 		 
groundCornerFront-->
	PaintColumns
	
topCornerFront-->
	PaintColumns

//DivisionHorizontal		
blockTopLeft-->
	PaintColumns      

blockTopRight-->
	PaintColumns   
	 		 
groundCorner-->
	PaintColumns
topCorner-->
	PaintColumns

//Division vertical	 		 
floorCornerSide-->
	split(x){{{{1: column |~(lotDepth * 0.2) / 2: floorsCorners}}*
	 		 |1 : lastColumn}}
	 		 
column-->
	PaintColumns
lastColumn-->
	PaintColumns	


floorsCorners-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeCenterCorner
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeCenterCorner-->
	split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeCenterWindow
	 		 |floorMeasure/3: facadeDown}}
	 		 
facadeCenterWindow-->
	Window
	
//Bloque fachada frontal parte de atras

blockBack-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackFront
        | back: blockBackBack
        | left: blockBackLeft
        | right: blockBackRight
        | top: RoofTop}}

blockBackFront-->
	split(y){{{{1:groundCornerFront |floorMeasure: floorCornerSide}}*
	 		 |1 : topCornerFront}}
		
blockBackLeft-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}}        

blockBackRight-->
	split(y){{ {{1:groundCorner |floorMeasure: floorCornerSide}}*
	 		 |1 : topCorner}} 
	 		 
	 		 
//Bloques de los lados central

blockMiddle-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockMiddleFront
        | back: blockMiddleBack
        | left: blockMiddleLeft
        | right: blockMiddleRight
        | top: RoofTop}}

//DivisionHorizontal
blockMiddleLeft-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}

blockMiddleRight-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 
//Division lateral
floorCornerFront-->
	split(x){{ {{1: column |~(lotDepth * 0.6) / floorPerLevel: floorsCornersCenter}}*
	 		 |1 : lastColumn}}
	 		 
floorsCornersCenter-->
	split(x){{~((lotDepth * 0.2) / 2)*0.28: facadeLeft |((lotDepth * 0.2) / 2)*0.44: facadeMiddleCenter
	 		 |~((lotDepth * 0.2) / 2)*0.28 : facadeRight}}

facadeMiddleCenter-->
		split(y){{floorMeasure/3: facadeUp |floorMeasure/3: facadeMiddleCenterWindow
			 		 |floorMeasure/3: facadeDown}}

facadeLeft-->
	PaintWalls
facadeRight-->
	PaintWalls
facadeUp-->
	PaintWalls
facadeDown-->
	PaintWalls
	
facadeMiddleCenterWindow-->
	Window
//center	
Center-->
	split(z){{lotDepth * 0.2 : blockTopCenter |lotDepth * 0.6 : blockMiddleCenter |lotDepth * 0.2 : blockBackCenter }}
	
blockMiddleCenter-->
	Paintground
blockTopCenter-->
	Paintground
	
blockBackCenter-->
	extrude(lotHeight) 
	comp(f) {{
        front: blockBackCenterFront
        | back: blockBackCenterBack
        | left: blockBackCenterLeft
        | right: blockBackCenterRight
        | top: RoofTop}}
        


//DivisionHorizontal
blockBackCenterBack-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*

	 		 |1 : topCornerFront}}
blockBackCenterFront-->
	split(y){{ {{1:groundCornerFront |floorMeasure: floorCornerFront}}*
	 		 |1 : topCornerFront}}
	 		 

#DESARROLLO TECHO
RoofTop --> 
    comp(f) {{
        front: RoofFront
        | back: RoofBack
        | left: RoofLeft
        | right: RoofRight
        | top: RoofT
    }}
    
RoofFront-->
	split(x){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	split(y){{2: sideLeft | ~lotWidth/3 : sideMidle | 2: sideRight}}
	
	
sideLeft-->
	extrude(2)
	PaintColumns
	
sideRight-->
	extrude(2)
	PaintColumns

	
	
#TEXTURAS Y OBJETOS	
PaintRoof-->
	setupProjection(0, scope.xy, 30 , 30)
	texture(roof_texture)
	projectUV(0)
	
PaintColumns-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(topDown_texture)
	projectUV(0) 
	
PaintWalls-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(column_texture)
	projectUV(0)
	
Paintground-->
	setupProjection(0, scope.xz, 20 , 20)
	texture(grass_texture)
	projectUV(0)	

PaintFacadeTopDown-->
	setupProjection(0, scope.xy, 10 , 10)
	texture(wall_texture)
	projectUV(0)
	
Door -->
      i(door_obj)
      s(1  , floorMeasure, floorQuantity-10)  // Escala la ventana al tama o deseado
      t(0,-1,1)
      r(0,90,0)

Glass-->
	setupProjection(0, scope.xy, 6 , 6)
	texture(glass_texture)
	projectUV(0) 
	
Window-->
      i(window_obj)
      s(((lotDepth * 0.2) / 2)*0.44 , floorMeasure/3, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass

WindowCorner-->
      i(window_obj)
      s(floorMeasure-0.7 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass


      
WindowBackCenter-->
      i(window_obj)
      s(floorMeasure+3.8 , floorMeasure/2, 0.2)  // Escala la ventana al tama o deseado
      t(0,0, 0)
      Glass	"""
        
            return reglaProcedural

        elif TypeBuild == "industrial":
            
            reglaProcedural += f"""version "2020.0"

attr wall_texture = "assets/textureChapGreca.jpg"
attr door_obj = "assets/industrialDoor.obj"

attr height =  {HeightValue}
attr width = scope.sx
attr depth = scope.sz
attr modulos =  {FloorsValue}
attr frontModules = 5
attr sizeWind = depth/modulos - 1
attr sizeFrontModule = width/frontModules +1




Structure-->
	extrude(height)

	ShipBuilding
	
ShipBuilding-->
	comp(f){{ front: FrontFacade
			|left: LeftFacade
			|right: RightFacade
			|back: BackFacade
			|top: RoofShip}}
			

	
FrontFacade-->
	split(x){{ {{~1: beamsFrontFacade
			| sizeFrontModule : WallFrontFacade(split.index)}}*
			|~1:  LastBeam}}
			

	
RightFacade-->
	split(x){{ {{1: beamsRightFacade(split.index)
			 |sizeWind : WallRightFacade(split.index)}}*
			 | ~1: LastBeam}}
	

			 
LeftFacade-->	
	split(x){{ {{1: beamsLeftFacade(split.index)
			 |~sizeWind : WallLeftFacade(split.index)}}*
			 | 1: LastBeam}}
			 
BackFacade-->
	split(x){{ {{1: beamsFrontFacade
			| ~sizeFrontModule : WallBackFacade(split.index)}}*
			|1:  LastBeam}}
			


//ROOF RULES
RoofShip-->	
	roofGable(5)
	split(z){{ {{1: beamsRoof
			 |~14 : RoofTiles}}*
			 | 1: LastBeamRoof}}

RoofTiles-->
	RoofTexture
	
beamsRoof-->
	RoofTexture
	
LastBeamRoof-->
	RoofTexture	


WallBackFacade(backIndex)-->
	case backIndex == 0:
				WallTexture
		
		
	else :
		split(y){{0.5:FloorFrontFacade
				|height-2: WallFront(split.index)
				|1: WindowFront}}
			 
//FRONT RULES						 
WallFrontFacade(wallIndex)-->
	case wallIndex == 3:
			split(y){{height/2 +1: doorLevel
					|height/2 -1: restLevel}}
				
	case wallIndex == frontModules - 1:
				Door
		
	else :
		split(y){{0.5:FloorFrontFacade
				|height-2: WallFront(split.index)
				|1: WindowFront}}
				
doorLevel-->
	Door
	
restLevel-->
	WallTexture
				
WallFront(WallFrontIndex)-->
	case WallFrontIndex == 1:
		WallTexture
	
	else:
		WallTexture

FloorFrontFacade-->
	WallTexture
	
beamsFrontFacade-->
	WallTexture
			
//LEFT RULES
WallLeftFacade(wallLeftIndex)-->
	case wallLeftIndex == 0:
		split(y){{10:windowSides}}
		
	else :
		split(y){{0.5:FloorLeftFacade
				|height-2: WallLeft
				|1: WindowSidesLeft}}
				
WallLeft-->
	WallTexture	
	
FloorLeftFacade-->
	WallTexture

beamsLeftFacade(beamLeftIndex)-->
	case beamLeftIndex == 0 :
		WallTexture
	else:
		WallTexture
		
//RIGHT RULES					
WallRightFacade(wallRightIndex)-->
	case wallRightIndex == 0:
		split(y){{10:WindowSidesRight}}
		
	else :
		split(y){{0.5:FloorRightFacade
				|height-2: WallRight
				|1: WindowSidesRight}}

WallRight-->
	WallTexture	
	
FloorRightFacade-->
	WallTexture
		
beamsRightFacade(beamRightIndex)-->
	case beamRightIndex == 0 :
		WallTexture
	else:
		WallTexture

LastBeam-->
	WallTexture
		
//TEXTURE WALLS RULE		
WallTexture -->
	setupProjection(0, scope.xz, 5, 5)
  	texture(wall_texture)
  	projectUV(0)
  	
//TEXTURE ROOF RULE  	
 RoofTexture -->
	setupProjection(0, scope.zx, 20, 20)
  	texture(wall_texture)
  	projectUV(0)


 Door-->
    i(door_obj)
    s(sizeFrontModule , height/2+1, 0.5)  // Escala la ventana al tamaño deseado
    r(0, 0, 0)
    t(0, 0, -0.5)
    
Window -->
    i("window.obj")
    s(1, 1, sizeFrontModule )  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeFrontModule)
    
WindowFront -->
    i("window.obj")
    s(1, 1.5, sizeFrontModule)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeFrontModule)
    
 WindowSidesRight -->
    i("window.obj")
    s(1, 1.5, sizeWind+1)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeWind)       
    
WindowSidesLeft -->
    i("window.obj")
    s(1, 1.5, sizeWind)  // Escala la ventana al tamaño deseado
    r(0, -90, 0)
    t(-1, 0, -sizeWind)"""

            
        return reglaProcedural


    def GenerarProceduralDetect(typeObject, floors, floorlevels):
        
        reglaProcedural = ''
        
        floor  = typeObject
        floorLevels = floorlevels
        floorsBuild = floors
        
        if floor == "balcony":
             reglaProcedural += f"""version "2020.0"

attr wall_texture = "assets/texture2.jpg"
window_texture = "assets/windowWall.jpg"
balcony_texture = "assets/windowTwo.jpg"
attr window_obj = "assets/ventanaObj5.obj"
white_texture = "assets/whitetexture.jpg"
Roof_texture = "assets/tejas.jpg"
attr balcony_obj = "assets/BALCON.fb"
attr middle_texture = "assets/blanco.jpg"


    attr pisos = {floorLevels}
    attr height = 60
    attr width = scope.sx
    attr depth = scope.sz
    attr roof = "no"
    attr floor = 1
    attr topledge = 1
    attr floors = {floorsBuild}
    attr widthWall = (width/floors) 
    attr heightwall = (height/pisos) - 1



    Structure -->
        extrude(height)  
        building

    building-->
        comp(f){{ front: FrontFacade
                | left : LeftSide 
                | right: RigthSide
                | back: BackSide
                | top: Roof }}
        
LeftSide-->	
	PinturaParedes
	
RigthSide-->
	PinturaParedes
	
BackSide-->
	PinturaParedes

        
    FrontFacade-->
        split(y) {{ {{floor : Floor(split.index) 
                | ~heightwall : FloorWall(split.index)}}*
                | ~topledge: TopLedge(split.index)}}
        
    TopLedge(topindex) -->

        case topindex == 0:
            extrude(0)
        else:
            extrude(0)
        
        PinturaParedes
        
    Floor(floorindex)-->
        split(x){{ {{0.5: BottomColumn(split.index)
                |~widthWall -1: Balcony(split.index)}}*
                | 0.5 :final	}}

final -->
	PinturaParedes
				
	last-->
		extrude(0)
				
    BottomColumn(bottomcolumnindex)-->
        case bottomcolumnindex == 0:
            extrude(0)
        PinturaParedes
        case bottomcolumnindex == 2:
            extrude(0)
            MiddleBalcony
        case bottomcolumnindex == 3:
            extrude(0)
            
        else:
            MiddleBalcony
        
        PinturaParedes			
        
    Balcony(balconyindex)-->
        case balconyindex == 0:
            extrude(0)
            PinturaParedes
            
            
            
            
        else:
            MiddleBalcony
            balconyObj
        
        
    FloorWall(floorwallindex)-->
        split(x) {{ {{~0.5:sideColumn(split.index)
                |widthWall -1 :WallColumn(split.index) }}*
                |~0.5: final}}
                
                
 	sideColumn(columnIndex)-->
 		case columnIndex == 0:
 			extrude(0)
 			PinturaParedes
 		else:
 			extrude(0)
 			PinturaParedes
        
    WallColumn(wallcolumnindex)-->
        case wallcolumnindex == 0:
			extrude(0)

        else:
            extrude(1)
            WindowBalcony


    SideCenterFloor(sidecenter)-->
        extrude(0)
        PinturaParedes

    SideLeftFloor(sideleftfloor)-->

        split(y){{~1.5 : top(split.index)
                | 1.5 : middle(split.index)
                |~1.5 : bottom(split.index)}}
        PinturaParedes
        
    SideRightFloor(sideleftfloor)-->
        split(y){{~1.5 : top(split.index)
                | 1.5 : middle(split.index)
                |~1.5 : bottom(split.index)}}
		
    top(topside)-->
        extrude(0)
        PinturaParedes

    middle(middleside)-->
        Window
        
        
    bottom(topside)-->
        extrude(0)
        PinturaParedes
        

        
    PinturaParedes-->
        setupProjection(0, scope.xy, 6 , 6)
        texture(wall_texture)
        projectUV(0)
        
    
    WindowTexture-->
        setupProjection(0, scope.xz, 5, 5)
        texture(window_texture)
        projectUV(0)
        rotateUV(0, 180)
        
    TexturaBalcony-->
        setupProjection(0, scope.xz, 5, 5)
        texture(balcony_texture)
        projectUV(0)
        rotateUV(0, 180)	
    
    PinturaBlanca-->
        setupProjection(0, scope.xy, 5, 5)
        texture(white_texture)
        projectUV(0)
        rotateUV(0, 180)
        
	TextureRoof-->
		setupProjection(0, scope.xz, 10, 10)
        texture(Roof_texture)
        projectUV(0)
        rotateUV(0, 180)
    
    Window -->
        i(window_obj)
        s(widthWall/2 -1  , 1.5, 0.7)  // Escala la ventana al tama o deseado
        t(0,0,0)
        PinturaBlanca
        
    WindowBalcony -->
        i(window_obj)
        s('1, 'heightwall, 1)  // Escala la ventana al tama o deseado
        t(0,-1,heightwall)
        r(270, 0, 0)
        PinturaBlanca
        
    balconyObj -->
        i(balcony_obj)
        s('1, 3, '1)  // Escala la ventana al tama o deseado
        t(0 , 1,0)
        r(0, 0, 0)
        
    MiddleBalcony-->
        setupProjection(0, scope.xz, 5, 5)
        texture(middle_texture)
        projectUV(0)
        rotateUV(0, 180)"""
        
             return reglaProcedural
        
        elif floor == "window":
            reglaProcedural += f"""version "2020.0"

attr wall_texture = "assets/texture2.jpg"
wall_texture2 = "assets/texture2.jpg"
window_texture = "assets/windowWall.jpg"
balcony_texture = "assets/windowTwo.jpg"
attr window_obj = "assets/ventanaObj5.obj"
white_texture = "assets/whitetexture.jpg"
Roof_texture = "assets/tejas.jpg"
middle_texture = "assets/blanco.jpg"
door_obj = "assets/Door.fbx"


    attr pisos = {floorLevels}
    attr height = 60
    attr width = scope.sx
    attr depth = scope.sz
    attr roof = "no"
    attr floor = 1
    attr topledge = 1
    attr floors = {floorsBuild}
    attr widthWall = (width/floors) 
    attr widthWallFirstFloor = (width/4)
    attr heightwall = (height/pisos) - 1



    Structure -->
        extrude(height)  
        building

    building-->
        comp(f){{ front: FrontFacade
                | left : LeftSide 
                | right: RigthSide
                | back: BackSide
                | top: Roof }}
        
LeftSide-->	
	PinturaParedes
	
RigthSide-->
	PinturaParedes
	
BackSide-->
	PinturaParedes

        
    FrontFacade-->
        split(y) {{ {{floor : Floor(split.index) 
                | ~heightwall : FloorWall(split.index)}}*
                | ~topledge: TopLedge(split.index)}}
        
    TopLedge(topindex) -->

        case topindex == 0:
            extrude(0)
        else:
            extrude(0.2)
        
        PinturaParedesTop
        
    Floor(floorindex)-->
        split(x){{ {{0.5: BottomColumn(split.index)
                |~widthWall -1: Middle(split.index)}}*
				}}
		
		
	BottomColumn(ColInd)-->
		extrude(0.2)
		PinturaParedesTop
	
	Middle(middleInd)-->
		extrude(0.2)
		PinturaParedesTop
				
        
        
    FloorWall(floorwallindex)-->
    	case floorwallindex == 1:
    		split(x){{ {{1:sideColumn(split.index)
	                |~width/3  : firstFloor(split.index) }}*
	                |1: final}}
    		
    	else:
    	
	        split(x) {{ {{~0.5:sideColumn(split.index)
	                |widthWall -0.5 :WallColumn(split.index) }}*
	                |~0.5: final}}
	                
	final -->
		PinturaParedes
                
                
 	sideColumn(columnIndex)-->
 		case columnIndex == 0:
 			extrude(0)
 			PinturaParedes
 		else:
 			extrude(0)
 			PinturaParedes
        
    WallColumn(wallcolumnindex)-->
        case wallcolumnindex == 0:
            split(x){{~widthWall: SideLeftFloor(split.index)
                    |1: SidCenterFloor(split.index)
                    |~widthWall: SideRightFloor(split.index)}}
                    


        else:
            split(x){{~widthWall/2 - 2: SideLeftFloor(split.index)
                    |widthWall: SideCenterFloor(split.index)
                    |~widthWall/2 -2: SideRightFloor(split.index)}}

	firstFloor(firstIndx)-->
		case firstIndx == 3:
				split(x){{~3: SideLeftFloor(split.index)
                    |widthWallFirstFloor: SideCenterFirstFloor
                    |~3: SideRightFloor(split.index)}}
                
		else:
			split(x){{~widthWallFirstFloor/2 - 2: SideLeftFloor(split.index)
                    |4: SideCenterFloorF(split.index)
                    |~widthWallFirstFloor/2 -2: SideRightFloor(split.index)}}
                    
	SideCenterFirstFloor-->
		
		Door                
	
	
	
    SideCenterFloor(sidecenter)-->
  
        split(y){{~1.5 : top(split.index)
                | 1.5 : middle(split.index)
                |~1.5 : bottom(split.index)}}
                
    SideCenterFloorF(sidecenter)-->
  
        split(y){{~1.5 : top(split.index)
                | 1.5 : middleF(split.index)
                |~1.5 : bottom(split.index)}}
                

	middleF(midind)-->
		WindowFirstF

    SideLeftFloor(sideleftfloor)-->
        PinturaParedes
        
    SideRightFloor(sideleftfloor)-->
    	PinturaParedes
		
    top(topside)-->
        extrude(0)
        PinturaParedes

    middle(middleside)-->
        Window
        
        
    bottom(topside)-->
        extrude(0)
        PinturaParedes
        

        
    PinturaParedes-->
        setupProjection(0, scope.xy, 6 , 6)
        texture(wall_texture)
        projectUV(0)
        
	PinturaParedesTop-->
        setupProjection(0, scope.xz, 6 , 6)
        texture(wall_texture2)
        projectUV(0)
        
    
    WindowTexture-->
        setupProjection(0, scope.xz, 5, 5)
        texture(window_texture)
        projectUV(0)
        rotateUV(0, 180)
        
    TexturaBalcony-->
        setupProjection(0, scope.xz, 5, 5)
        texture(balcony_texture)
        projectUV(0)
        rotateUV(0, 180)	
    
        
	TextureRoof-->
		setupProjection(0, scope.xz, 10, 10)
        texture(Roof_texture)
        projectUV(0)
        rotateUV(0, 180)
    
    Window -->
        i(window_obj)
        s(widthWall-0.5 , 1.5, 0.7)  // Escala la ventana al tama o deseado
        t(0,0,0)
        PinturaBlanca
        
    WindowFirstF -->
        i(window_obj)
        s(4 , 1.5, 0.7)  // Escala la ventana al tama o deseado
        t(0,0,0)
        PinturaBlanca
    
    Door -->
        i(door_obj)
        s(1  , heightwall, widthWallFirstFloor)  // Escala la ventana al tama o deseado
        t(0,0,1)
        r(0,90,0)
        PinturaBlanca
        
    WindowBalcony -->
        i(window_obj)
        s('1, 'heightwall, 1)  // Escala la ventana al tama o deseado
        t(0,-1,heightwall)
        r(270, 0, 0)
        PinturaBlanca
        

        
    MiddleBalcony-->
        setupProjection(0, scope.xz, 5, 5)
        texture(middle_texture)
        projectUV(0)
        rotateUV(0, 180)"""
        
            return reglaProcedural
    
    
    
    


