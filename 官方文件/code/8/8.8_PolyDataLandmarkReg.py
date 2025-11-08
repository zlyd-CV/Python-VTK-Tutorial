import vtk


def main():

    sourcePoints =vtk.vtkPoints()
    sourcePoint1 = [0.5, 0.0, 0.0]
    sourcePoints.InsertNextPoint(sourcePoint1)
    sourcePoint2=[0.0, 0.5, 0.0]
    sourcePoints.InsertNextPoint(sourcePoint2)
    sourcePoint3=[30.0, 0.0, 0.5]
    sourcePoints.InsertNextPoint(sourcePoint3)

    targetPoints =vtk.vtkPoints()

    targetPoint1=[0.0, 0.0, 0.55]
    targetPoints.InsertNextPoint(targetPoint1)
    targetPoint2=[0.0, 0.55, 0.0]
    targetPoints.InsertNextPoint(targetPoint2)
    targetPoint3=[-0.55, 0.0, 0.0]
    targetPoints.InsertNextPoint(targetPoint3)

    landmarkTransform =vtk.vtkLandmarkTransform()
    landmarkTransform.SetSourceLandmarks(sourcePoints)
    landmarkTransform.SetTargetLandmarks(targetPoints)
    landmarkTransform.SetModeToRigidBody()
    landmarkTransform.Update()

    source = vtk.vtkPolyData()
    source.SetPoints(sourcePoints)

    target =vtk.vtkPolyData()
    target.SetPoints(targetPoints)

    sourceGlyphFilter =vtk.vtkVertexGlyphFilter()
    sourceGlyphFilter.SetInputData(source)
    sourceGlyphFilter.Update()

    targetGlyphFilter =vtk.vtkVertexGlyphFilter()
    targetGlyphFilter.SetInputData(target)
    targetGlyphFilter.Update()

    transformFilter =vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(sourceGlyphFilter.GetOutput())
    transformFilter.SetTransform(landmarkTransform)
    transformFilter.Update()

    sourceMapper =vtk.vtkPolyDataMapper()
    sourceMapper.SetInputConnection(sourceGlyphFilter.GetOutputPort())

    sourceActor =vtk.vtkActor()
    sourceActor.SetMapper(sourceMapper)
    sourceActor.GetProperty().SetColor(1,1,0)
    sourceActor.GetProperty().SetPointSize(5)

    targetMapper =vtk.vtkPolyDataMapper()
    targetMapper.SetInputConnection(targetGlyphFilter.GetOutputPort())

    targetActor =vtk.vtkActor()
    targetActor.SetMapper(targetMapper)
    targetActor.GetProperty().SetColor(1,0,0)
    targetActor.GetProperty().SetPointSize(5)

    solutionMapper =vtk.vtkPolyDataMapper()
    solutionMapper.SetInputConnection(transformFilter.GetOutputPort())

    solutionActor =vtk.vtkActor()
    solutionActor.SetMapper(solutionMapper)
    solutionActor.GetProperty().SetColor(0,0,1)
    solutionActor.GetProperty().SetPointSize(5)

    renderer =vtk.vtkRenderer()

    renderWindow =vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderer.AddActor(sourceActor)
    renderer.AddActor(targetActor)
    renderer.AddActor(solutionActor)

    axes =vtk.vtkAxesActor()
    axes.SetScale(30)

    renderer.AddActor(axes)
    renderer.SetBackground(.3, .6, .3)

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("PolyDataLandmarkReg")
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()