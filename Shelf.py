#Author-Tyzhkiy Grigoriy
#Description-Create simple shelf

import adsk.core, adsk.fusion, adsk.cam, traceback

defaultNumberOfHorizontalSections = 4
defaultNumberOfVerticalSections = 3
defaultSectionSize = 335
defaultInnerWalls = 15
defaultOuterWalls = 37
defaultDepth = 390

shelfHorizontalSize = defaultOuterWalls * 2 + defaultNumberOfHorizontalSections * defaultSectionSize + defaultInnerWalls * (defaultNumberOfHorizontalSections - 1)
shelfVerticalSize = defaultOuterWalls * 2 + defaultNumberOfVerticalSections * defaultSectionSize + defaultInnerWalls * (defaultNumberOfVerticalSections - 1)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        #Create shelf sketch
        sketches = rootComp.sketches
        yzPlane = rootComp.yZConstructionPlane
        sketch = sketches.add(yzPlane)
        lines1 = sketch.sketchCurves.sketchLines
        shelfForm = lines1.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-shelfVerticalSize/10, shelfHorizontalSize/10, 0))

        #Create shelf body
        prof = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByString(str(defaultDepth)+"mm")
        extrudes = rootComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeInput.setDistanceExtent(False, distance)
        extrude1 = extrudes.add(extrudeInput)

        #Create section sketch
        sketch2 = sketches.add(yzPlane)
        lines2 = sketch2.sketchCurves.sketchLines
        section = lines2.addTwoPointRectangle(adsk.core.Point3D.create(-defaultOuterWalls/10, defaultOuterWalls/10, 0), adsk.core.Point3D.create(-(defaultOuterWalls + defaultSectionSize)/10, (defaultOuterWalls + defaultSectionSize)/10, 0))

        #Cut section from shelf
        prof = sketch2.profiles.item(0)
        distance = adsk.core.ValueInput.createByString(str(defaultDepth)+"mm")
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setDistanceExtent(False, distance)
        extrude2 = extrudes.add(extrudeInput)

        #---Use rectangular pattern for sections---

        # Get the body created by extrusion
        # Create input entities for rectangular pattern
        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(extrude2)

        # Get x and y axes for rectangular pattern
        yAxis = rootComp.yConstructionAxis
        zAxis = rootComp.zConstructionAxis

        # Quantity and distance
        quantityOne = adsk.core.ValueInput.createByString(str(defaultNumberOfHorizontalSections))
        distanceOne = adsk.core.ValueInput.createByString(str(defaultInnerWalls + defaultSectionSize))
        quantityTwo = adsk.core.ValueInput.createByString(str(defaultNumberOfVerticalSections))
        distanceTwo = adsk.core.ValueInput.createByString(str(defaultInnerWalls + defaultSectionSize))

        # Create the input for rectangular pattern
        rectangularPatterns = rootComp.features.rectangularPatternFeatures
        rectangularPatternInput = rectangularPatterns.createInput(inputEntites, yAxis, quantityOne, distanceOne, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)

        # Set the data for second direction
        rectangularPatternInput.setDirectionTwo(zAxis, quantityTwo, distanceTwo)

        # Create the rectangular pattern
        rectangularFeature = rectangularPatterns.add(rectangularPatternInput)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
