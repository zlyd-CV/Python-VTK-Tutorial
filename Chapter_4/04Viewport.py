import vtk


def main():
    # 创建四个几何体数据源,分别是锥体、立方体、圆柱体和轮廓线
    cone = vtk.vtkConeSource()
    cube = vtk.vtkCubeSource()
    cylinder = vtk.vtkCylinderSource()
    outline = vtk.vtkOutlineSource()

    # 创建四个映射器，分别将几何体数据源连接到映射器
    conemapper = vtk.vtkPolyDataMapper()
    conemapper.SetInputConnection(cone.GetOutputPort())

    cubemapper = vtk.vtkPolyDataMapper()
    cubemapper.SetInputConnection(cube.GetOutputPort())

    cylindermapper = vtk.vtkPolyDataMapper()
    cylindermapper.SetInputConnection(cylinder.GetOutputPort())

    outlinemapper = vtk.vtkPolyDataMapper()
    outlinemapper.SetInputConnection(outline.GetOutputPort())

    # 创建四个演员，分别将映射器连接到演员
    coneactor = vtk.vtkActor()
    coneactor.SetMapper(conemapper)

    cubeactor = vtk.vtkActor()
    cubeactor.SetMapper(cubemapper)

    cylinderactor = vtk.vtkActor()
    cylinderactor.SetMapper(cylindermapper)

    outlineactor = vtk.vtkActor()
    outlineactor.SetMapper(outlinemapper)

    # 创建四个渲染器，分别设置演员、背景颜色和视口
    ren1 = vtk.vtkRenderer()
    ren1.AddActor(coneactor)
    ren1.SetBackground(0.5, 0, 0) # 红色背景
    # vtk默认采用左下角为坐标原点，设置视口范围为(xmin, ymin, xmax, ymax),取值范围均为0到1(规范化设备显示坐标系?)
    ren1.SetViewport(0.0, 0.0, 0.5, 0.5)  # 左下角视口(注意是先列出xy的最小值，再列出最大值)

    ren2 = vtk.vtkRenderer()
    ren2.AddActor(cubeactor)
    ren2.SetBackground(0, 1, 0) # 绿色背景
    ren2.SetViewport(0.5, 0.0, 1.0, 0.5) # 右下角视口

    ren3 = vtk.vtkRenderer()
    ren3.AddActor(cylinderactor)
    ren3.SetBackground(0, 0, 1) # 蓝色背景
    ren3.SetViewport(0.0, 0.5, 0.5, 1.0) # 左上角视口

    ren4 = vtk.vtkRenderer()
    ren4.AddActor(outlineactor)
    ren4.SetBackground(0.5, 0, 0) # 红色背景
    ren4.SetViewport(0.5, 0.5, 1.0, 1.0) # 右上角视口

    # 其余流程与之前所学类似
    renWin = vtk.vtkRenderWindow() # 创建渲染窗口
    renWin.AddRenderer(ren1)
    renWin.AddRenderer(ren2)
    renWin.AddRenderer(ren3)
    renWin.AddRenderer(ren4)
    renWin.SetSize(640, 480)
    renWin.Render()
    renWin.SetWindowName("Viewport")

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


if __name__ == "__main__":
    main()
"""
本代码演示了如何在一个渲染窗口中使用多个视口（Viewport）来显示不同的几何体。
代码创建了四个几何体数据源：锥体、立方体、圆柱体和轮廓线，并为每个几何体创建了对应的映射器和演员。
然后，代码创建了四个渲染器，每个渲染器负责渲染一个几何体，并设置了不同的背景颜色和视口位置。
最后，所有渲染器被添加到同一个渲染窗口中，从而实现了在同一窗口中显示多个视口的效果。
综上,我们可以知道一个渲染窗口可以包含多个渲染器,每个渲染器可以设置不同的视口范围,从而在同一窗口中显示多个不同的场景。
"""