import math

import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingFreeType
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkMath,
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    rMin = 0.5
    rMax = 1.0
    dims = [13, 11, 11]

    sgrid = vtkStructuredGrid()
    sgrid.SetDimensions(dims)

    vectors = vtkDoubleArray()
    vectors.SetNumberOfComponents(3)
    vectors.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
    points = vtkPoints()
    points.Allocate(dims[0] * dims[1] * dims[2])

    deltaZ = 2.0 / (dims[2] - 1)
    deltaRad = (rMax - rMin) / (dims[1] - 1)
    x = [0.0] * 3
    v = [0.0] * 3
    for k in range(0, dims[2]):
        x[2] = -1.0 + k * deltaZ
        kOffset = k * dims[0] * dims[1]
        for j in range(0, dims[1]):
            radius = rMin + j * deltaRad
            jOffset = j * dims[0]
            for i in range(0, dims[0]):
                theta = i * vtkMath.RadiansFromDegrees(15.0)
                x[0] = radius * math.cos(theta)
                x[1] = radius * math.sin(theta)
                v[0] = -x[1]
                v[1] = x[0]
                offset = i + jOffset + kOffset
                points.InsertPoint(offset, x)
                vectors.InsertTuple(offset, v)
    sgrid.SetPoints(points)
    sgrid.GetPointData().SetVectors(vectors)

    hedgehog = vtkHedgeHog()
    hedgehog.SetInputData(sgrid)
    hedgehog.SetScaleFactor(0.1)

    sgridMapper = vtkPolyDataMapper()
    sgridMapper.SetInputConnection(hedgehog.GetOutputPort())
    sgridActor = vtkActor()
    sgridActor.SetMapper(sgridMapper)
    sgridActor.GetProperty().SetColor(colors.GetColor3d('Gold'))

    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetWindowName('SGrid')

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renderer.AddActor(sgridActor)
    renderer.SetBackground(colors.GetColor3d('MidnightBlue'))
    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(60.0)
    renderer.GetActiveCamera().Azimuth(30.0)
    renderer.GetActiveCamera().Dolly(1.0)
    renWin.SetSize(640, 480)
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()
