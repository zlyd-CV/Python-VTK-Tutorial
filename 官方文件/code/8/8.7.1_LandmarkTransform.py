from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData
)
from vtkmodules.vtkCommonTransforms import vtkLandmarkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter

sourcePoints = vtkPoints()
sourcePoint1 = [0.5, 0.0, 0.0]
sourcePoints.InsertNextPoint(sourcePoint1)
sourcePoint2 = [0.0, 0.5, 0.0]
sourcePoints.InsertNextPoint(sourcePoint2)
sourcePoint3 = [0.0, 0.0, 0.5]
sourcePoints.InsertNextPoint(sourcePoint3)

targetPoints = vtkPoints()
targetPoint1 = [0.0, 0.0, 0.5]
targetPoints.InsertNextPoint(targetPoint1)
targetPoint2 = [0.0, 0.5, 0.0]
targetPoints.InsertNextPoint(targetPoint2)
targetPoint3 = [-0.5, 0.0, 0.0]
targetPoints.InsertNextPoint(targetPoint3)

landmarkTransform = vtkLandmarkTransform()
landmarkTransform.SetSourceLandmarks(sourcePoints)
landmarkTransform.SetTargetLandmarks(targetPoints)
landmarkTransform.SetModeToRigidBody()
landmarkTransform.Update()

source = vtkPolyData()
source.SetPoints(sourcePoints)

target = vtkPolyData()
target.SetPoints(targetPoints)

landmarkTransformFilter = vtkTransformPolyDataFilter()
landmarkTransformFilter.SetInputData(source)
landmarkTransformFilter.SetTransform(landmarkTransform)
landmarkTransformFilter.Update()

transformedSource = landmarkTransformFilter.GetOutput()
# ============ display transformed points ==============
pointCount = 3
for index in range(pointCount):
    point = [0, 0, 0]
    transformedSource.GetPoint(index, point)
    print("transformed source point[%s]=%s" % (index, point))
