# SlicerSurfaceFromUnorganizedPoints
![Alt text](https://github.com/brudfors/SlicerPointSetProcessing/blob/master/PointSetProcessingScreenShot.PNG?raw=true "SlicerPointSetProcessing")

SlicerSurfaceFromUnorganizedPoints is a module for 3D Slicer which can compute normals and reconstruct surfaces from sets of unorganized points. 

### M1
The first step of the reconstruction is to approximate the normals of the point set and their orientaion [1]. Next, the surface reconstruction is performed, which can be either a Possion surface reconstruction [2, 3] or a Delaunay triangulation [4].

### M2
blabla

### M3
blabla

1. http://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html
2. http://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html
3. Hoppe, Hugues, et al. Surface reconstruction from unorganized points. Vol. 26. No. 2. ACM, 1992.
4. Kazhdan, Michael, Matthew Bolitho, and Hugues Hoppe. "Poisson surface reconstruction." Proceedings of the fourth Eurographics symposium on Geometry processing. Vol. 7. 2006.
5. Doria D., Gelas A. Poisson Surface Reconstruction for VTK. 2010 Mar (with minor changes/improvements by me)
6. http://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html 

## Build Instructions
1. **3D Slicer** - Follow the instructions found here: http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions
2. **vtkInfoVisBoost** - Download the latest version of Boost from here: http://www.boost.org/users/history/version_1_59_0.html, and extract to a folder of your choice (BOOST_ROOT). Open CMake and set the build directory to the VTK-build folder located in your 3D Slicer build. Add an entry called BOOST_ROOT, enable vtkInfoVisBoost and vtkInfoVisBoostGraphAlgorithms, then press Generate. Open the Slicer.sln located in the top directory of your Slicer build and build Slicer again.
4. **PoissonReconstruction** - Build the PoissonReconstruction library located here: https://github.com/daviddoria/PoissonReconstruction, and link it with the VTK-build located in your 3D Slicer build folder.
5. **PointSetProcessing** - Build the PointSetProcessing library located here: https://github.com/daviddoria/PointSetProcessing, and link it with the VTK-build located in your 3D Slicer build folder.
6. **SlicerSurfaceFromUnorganizedPoints** - Build the SlicerSurfaceFromUnorganizedPoints module after adding: the PoissonReconstruction library and includes; the PointSetProcessing library and includes; and the vtkInfovisBoostGraphAlgorithms library, in CMake.

## TODO
* Rename to SurfaceFromUnorganizedPoints
* If there is interest: Reset to default, save params in Slicer.ini, calculate in separate thread