"""
使用VTK创建一个带有光源的圆锥体渲染场景,最后得到一个只能看到面朝红色光照射下的圆锥体效果
出现此现象的原因是vtk默认不指定光源时启用头顶光照明,始终跟随着程序视线（相机）
在指定了光源后,头顶光照明被禁用,只能看到面朝光源的部分被照亮,背光部分则变暗
"""
import vtk


def main():
    # 创建圆锥体数据源
    cone = vtk.vtkConeSource()
    cone.SetHeight(2.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)

    # 创建映射器
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    # 创建演员
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    # 设置灯光属性
    light = vtk.vtkLight()  # 创建一个光源对象
    light.SetColor(1, 0, 0)  # 红色光
    light.SetPosition(0, 0, 10)  # 光源位置

    # 创建渲染器
    ren = vtk.vtkRenderer()
    ren.SetBackground(0, 0, 0)  # 设置背景为黑色,更容易看出光照效果
    ren.AddActor(coneActor)
    light.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())  # 设置光源的焦点为摄像机的焦点位置
    ren.AddLight(light)  # 将光源添加到渲染器中

    # 创建渲染窗口
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(500, 500)
    renWin.Render()
    renWin.SetWindowName('ConeRenderLight')

    # 创建交互器
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)  # 将渲染窗口(renWin)与交互器(iren)关联起来
    style = vtk.vtkInteractorStyleTrackballActor()  # 创建一个交互样式对象，这里使用的是“轨迹球演员”样式
    iren.SetInteractorStyle(style)  # 将这个交互样式设置给交互器(如果不设置,默认使用vtkInteractorStyleTrackballCamera)

    # 场景设置和渲染
    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)
    iren.Start()


if __name__ == '__main__':
    main()
"""
学习收获:
1.再次复习了VTK的可视化管线结构和各个组件的作用。
2.通过添加光源，我们可以控制场景中的光照效果，从而影响物体的外观。
3.由此可见,演员＋灯光都可被视为渲染对象,它们共同决定了最终的渲染效果。

尝试改进:
①试着将如下代码加入main()函数中,观察渲染效果的变化:
light_green = vtk.vtkLight() # 创建另一个光源对象
light_green.SetColor(0, 1, 0) # 绿色光
light_green.SetPosition(0, 0, -10) # 光源位置
ren.AddLight(light_green) # 将另一个光源添加到渲染器中

②试着删掉如下代码,比较两种交互器下鼠标按住左键逐渐偏离窗口时的的渲染变化(删除代码后交互器与第二章中的例子一致):
iren.SetInteractorStyle(style) # 将这个交互样式设置给交互器

③尝试把交互器换成下面格式,比较这两种交互器的不同效果:
style = vtk.vtkInteractorStyleJoystickCamera()  # 创建一个交互样式对象，这里使用的是“轨迹球相机”样式
vtkInteractorStyleTrackballCamera (轨迹球相机):当您拖动鼠标时，您移动的是相机（您的视点）,即没有光照的区域永远是黑暗的
vtkInteractorStyleJoystickActor (操纵杆演员):当您拖动鼠标时，您移动的是演员（场景中的物体）,当不同区域面向光源时,这些区域会被照亮
在这两种交互器中,光源位置是不变的,但由于交互器控制的对象不同,导致渲染效果也不同
"""
