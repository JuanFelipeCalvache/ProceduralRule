from AppCityEngine.Component import cga_templates

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
            return cga_templates.get_residencial_cga(HeightValue, FloorsValue, windowsAmount)

        elif TypeBuild == "comercial":
            return cga_templates.get_comercial_cga(HeightValue, FloorsValue, windowsAmount)
        
            

        elif TypeBuild == "industrial":
            return cga_templates.get_industrial_cga(HeightValue, FloorsValue)

            
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
            return cga_templates.get_residencial_cga(HeightValue, FloorsValue, windowsAmount)

        elif TypeBuild == "comercial":
            return cga_templates.get_comercial_cga(HeightValue, FloorsValue, windowsAmount)

        elif TypeBuild == "industrial":
            return cga_templates.get_industrial_cga(HeightValue, FloorsValue)

            
        return reglaProcedural


    def GenerarProceduralDetect(typeObject, floors, floorlevels):
        
        reglaProcedural = ''
        
        floor  = typeObject
        floorLevels = floorlevels
        floorsBuild = floors
        
        if floor == "balcony":
             return cga_templates.get_balcony_cga(floorLevels, floorsBuild)
        
        elif floor == "window":
             return cga_templates.get_window_cga(floorLevels, floorsBuild)
             
        return reglaProcedural
    
    
    
    


