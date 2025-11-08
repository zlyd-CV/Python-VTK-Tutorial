import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import (
    vtkColorSeries,
    vtkNamedColors
)
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    aPlane = vtkPlaneSource()
    aPlane.SetXResolution(3)
    aPlane.SetYResolution(3)
    aPlane.Update()

    # Create cell data.
    cellData = vtkFloatArray()
    for i in range(10):
        cellData.InsertNextValue(i)
    aPlane.Update()  # Force an update so we can set cell data.
    aPlane.GetOutput().GetCellData().SetScalars(cellData)

    # Get the lookup table.
    m_mask_opacity = 1
    lut = vtkLookupTable()
    lut.SetNumberOfTableValues(10)
    lut.SetTableRange(0, 9)
    lut.SetTableValue(0, 1, 1, 1, m_mask_opacity)  # White
    lut.SetTableValue(1, 1, 0, 0, m_mask_opacity)  # RED
    lut.SetTableValue(2, 0, 1, 0, m_mask_opacity)  # GREEN
    lut.SetTableValue(3, 1, 1, 0, m_mask_opacity)  # YELLOW
    lut.SetTableValue(4, 0, 0, 1, m_mask_opacity)  # BLUE
    lut.SetTableValue(5, 1, 0, 1, m_mask_opacity)  # MAGENTA
    lut.SetTableValue(6, 0, 1, 1, m_mask_opacity)  # CYAN
    lut.SetTableValue(7, 1, 0.5, 0.5, m_mask_opacity)  # RED_2
    lut.SetTableValue(8, 0.5, 1, 0.5, m_mask_opacity)  # GREEN_2
    lut.SetTableValue(9, 0.5, 0.5, 1, m_mask_opacity)  # BLUE_2
    lut.Build()

    # Set up the actor and mapper.
    mapper = vtkPolyDataMapper()
    mapper.SetLookupTable(lut)
    mapper.SetInputConnection(aPlane.GetOutputPort())
    mapper.SetScalarModeToUseCellData()
    mapper.SetScalarRange(0, 9)

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()

    # Setup render window, renderer, and interactor.
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName('CreateColorSeriesDemo')

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('SlateGray'))
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
