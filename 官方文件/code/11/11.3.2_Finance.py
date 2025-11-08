import vtk

def main():
    colors = vtk.vtkNamedColors()
    colors.SetColor("PopColor", [230, 230, 230, 255])

    keys = ['NUMBER_POINTS', 'MONTHLY_PAYMENT', 'INTEREST_RATE', 'LOAN_AMOUNT', 'TIME_LATE']
    dataSet = make_dataset("../data/financial.txt", keys)
    popSplatter = vtk.vtkGaussianSplatter()
    popSplatter.SetInputData(dataSet)
    popSplatter.SetSampleDimensions(100, 100, 100)
    popSplatter.SetRadius(0.05)
    popSplatter.ScalarWarpingOff()

    popSurface = vtk.vtkContourFilter()
    popSurface.SetInputConnection(popSplatter.GetOutputPort())
    popSurface.SetValue(0, 0.01)

    popMapper = vtk.vtkPolyDataMapper()
    popMapper.SetInputConnection(popSurface.GetOutputPort())
    popMapper.ScalarVisibilityOff()

    popActor = vtk.vtkActor()
    popActor.SetMapper(popMapper)
    popActor.GetProperty().SetOpacity(0.3)
    popActor.GetProperty().SetColor(colors.GetColor3d("PopColor"))

    lateSplatter = vtk.vtkGaussianSplatter()
    lateSplatter.SetInputData(dataSet)
    lateSplatter.SetSampleDimensions(50, 50, 50)
    lateSplatter.SetRadius(0.05)
    lateSplatter.SetScaleFactor(0.005)

    lateSurface = vtk.vtkContourFilter()
    lateSurface.SetInputConnection(lateSplatter.GetOutputPort())
    lateSurface.SetValue(0, 0.01)

    lateMapper = vtk.vtkPolyDataMapper()
    lateMapper.SetInputConnection(lateSurface.GetOutputPort())
    lateMapper.ScalarVisibilityOff()

    lateActor = vtk.vtkActor()
    lateActor.SetMapper(lateMapper)
    lateActor.GetProperty().SetColor(colors.GetColor3d("Red"))

    popSplatter.Update()
    bounds = popSplatter.GetOutput().GetBounds()

    axes = vtk.vtkAxes()
    axes.SetOrigin(bounds[0], bounds[2], bounds[4])
    axes.SetScaleFactor(popSplatter.GetOutput().GetLength() / 5)

    axesTubes = vtk.vtkTubeFilter()
    axesTubes.SetInputConnection(axes.GetOutputPort())
    axesTubes.SetRadius(axes.GetScaleFactor() / 25.0)
    axesTubes.SetNumberOfSides(6)

    axesMapper = vtk.vtkPolyDataMapper()
    axesMapper.SetInputConnection(axesTubes.GetOutputPort())

    axesActor = vtk.vtkActor()
    axesActor.SetMapper(axesMapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(lateActor)
    ren.AddActor(axesActor)
    ren.AddActor(popActor)
    ren.SetBackground(colors.GetColor3d("Wheat"))
    ren.ResetCamera()
    ren.GetActiveCamera().Dolly(1.3)
    ren.ResetCameraClippingRange()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("Financial Data")
    renWin.SetSize(640, 480)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Start()

def normalise(maximum, minimum, x):
    return minimum + x / (maximum - minimum)

def read_file(filename):
    res = dict()
    with open(filename) as ifn:
        k = ''
        v = list()
        for line in ifn:
            cl = ' '.join(line.split()).split()  # Clean the line.
            if cl:
                if len(cl) == 2 and cl[0] == 'NUMBER_POINTS':
                    k = cl[0]
                    v = [int(cl[1])]
                    has_key = True
                    continue
                if len(cl) == 1 and not has_key:
                    has_key = True
                    k = cl[0]
                    v = list()
                else:
                    v += map(float, cl)
            else:
                if has_key:
                    # Normalise the data.
                    minimum = min(v)
                    maximum = max(v)
                    # Emulate the bug in the C++ code.
                    for i in v:
                        if i > minimum:
                            maximum = i
                    if maximum != minimum:
                        res[k] = list(map(lambda x: minimum + x / (maximum - minimum), v))
                    else:
                        res[k] = v
                    has_key = False
    return res

def make_dataset(filename, keys):
    res = read_file(filename)
    if res:
        newPts = vtk.vtkPoints()
        newScalars = vtk.vtkFloatArray()
        xyz = list(zip(res[keys[1]], res[keys[2]], res[keys[3]]))
        for i in range(0, res[keys[0]][0]):
            # print(xyz[i])
            newPts.InsertPoint(i, xyz[i])
            newScalars.InsertValue(i, res[keys[4]][i])

        dataset = vtk.vtkUnstructuredGrid()
        dataset.SetPoints(newPts)
        dataset.GetPointData().SetScalars(newScalars)
        return dataset

if __name__ == '__main__':
    main()