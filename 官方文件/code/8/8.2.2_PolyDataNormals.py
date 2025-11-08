import vtk

reader=vtk.vtkPolyDataReader()
reader.SetFileName("../data/fran_cut.vtk")
reader.Update()

normFilter =  vtk.vtkPolyDataNormals()
normFilter.SetInputData(reader.GetOutput())
normFilter.SetComputePointNormals(1)
normFilter.SetComputeCellNormals(0)
normFilter.SetAutoOrientNormals(1)
normFilter.SetSplitting(0)
normFilter.Update()

mask=vtk.vtkMaskPoints()
mask.SetInputData(normFilter.GetOutput());
mask.SetMaximumNumberOfPoints(300);
mask.RandomModeOn();
mask.Update();

arrow=vtk.vtkArrowSource()
arrow.Update()

glyph=vtk.vtkGlyph3D()
glyph.SetInputData(mask.GetOutput());
glyph.SetSourceData(arrow.GetOutput());
glyph.SetVectorModeToUseNormal();
glyph.SetScaleFactor(0.01);
glyph.Update()

originmapper=vtk.vtkPolyDataMapper()
originmapper.SetInputData(reader.GetOutput());

originactor=vtk.vtkActor()
originactor.SetMapper(originmapper)

normedmapper=vtk.vtkPolyDataMapper()
normedmapper.SetInputData(normFilter.GetOutput());

normedactor=vtk.vtkActor()
normedactor.SetMapper(normedmapper)

glyphmapper =vtk.vtkPolyDataMapper()
glyphmapper.SetInputData(glyph.GetOutput());

glyphactor=vtk.vtkActor()
glyphactor.SetMapper(glyphmapper)
glyphactor.GetProperty().SetColor(1., 0.,0.)

originalviewport = [0.0, 0.0, 0.33, 1.0]
normviewport = [0.33, 0.0, 0.66, 1.0]
glphviewport= [0.66, 0.0, 1.0, 1.0]

originalrenderer=vtk.vtkRenderer()
originalrenderer.SetViewport(originalviewport);
originalrenderer.AddActor(originactor);
originalrenderer.ResetCamera();
originalrenderer.SetBackground(1.0, 1.0, 1.0);

normedrenderer=vtk.vtkRenderer()
normedrenderer.SetViewport(normviewport);
normedrenderer.AddActor(normedactor);
normedrenderer.ResetCamera();
normedrenderer.SetBackground(1.0, 1.0, 1.0);

glyphRenderer=vtk.vtkRenderer()
glyphRenderer.SetViewport(glphviewport);
glyphRenderer.AddActor(glyphactor);
glyphRenderer.AddActor(normedactor);
glyphRenderer.ResetCamera();
glyphRenderer.SetBackground(1.0, 1.0, 1.0);

renwin=vtk.vtkRenderWindow()
renwin.AddRenderer(originalrenderer)
renwin.AddRenderer(normedrenderer);
renwin.AddRenderer(glyphRenderer)
renwin.SetSize(640,480)
renwin.Render()
renwin.SetWindowName("PolyDataNormals")


iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)
iren.Initialize()
iren.Start()
























































