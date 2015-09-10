# SlicerSurfaceFromUnorganizedPoints
![Alt text](https://github.com/brudfors/SlicerPointSetProcessing/blob/master/PointSetProcessingScreenShot.PNG?raw=true "SlicerPointSetProcessing")

SlicerSurfaceFromUnorganizedPoints is a module for 3D Slicer which reconstructs a surface from a set of unorganized points. The first step of the reconstruction is to approximate the normals of the point set and their orientaion [1]. Next, the surface reconstruction is performed, which can be either a Possion surface reconstruction [2, 3] or a Delaunay triangulation [4].

1. Hoppe, Hugues, et al. Surface reconstruction from unorganized points. Vol. 26. No. 2. ACM, 1992.
2. Kazhdan, Michael, Matthew Bolitho, and Hugues Hoppe. "Poisson surface reconstruction." Proceedings of the fourth Eurographics symposium on Geometry processing. Vol. 7. 2006.
3. Doria D., Gelas A. Poisson Surface Reconstruction for VTK. 2010 Mar (with minor changes/improvements by me)
4. http://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html 

## Parameters
Below are descriptions off each of the module parameters.

### Compute Normals
* **Mode**:
* **Fixed Neighbors**:
* **Radius**:
* **K-Nearest Neighbors**:
* **Graph Type**:

### Compute Surface
* **Depth**: This integer controls the reconstruction depth; the maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a voxel grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound.
* **Scale**: This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube.
* **Solver Divide**: Solver subdivision depth; This integer argument specifies the depth at which a block Gauss-Seidel solver is used to solve the Laplacian equation. Using this parameter helps reduce the memory overhead at the cost of a small increase in reconstruction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)
* **Iso Divide**: Iso-surface extraction subdivision depth; This integer argument specifies the depth at which a block isosurface extractor should be used to extract the iso-surface. Using this parameter helps reduce the memory overhead at the cost of a small increase in extraction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)
* **Samples Per Node**: Minimum number of samples; This floating point value specifies the minimum number of sample points that should fall within an octree node as the octree construction is adapted to sampling density. For noise-free samples, small values in the range [1.0 - 5.0] can be used. For more noisy samples, larger values in the range [15.0 - 20.0] may be needed to provide a smoother, noise-reduced, reconstruction.
* **Confidence**: Enabling tells the reconstructor to use the size of the normals as confidence information. When the flag is not enabled, all normals are normalized to have unit-length prior to reconstruction.
* **Verbose**: Enabling this flag provides a more verbose description of the running times and memory usages of individual components of the surface reconstructor.

## Build Instructions
1. **3D Slicer** - Follow the instructions found here: http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions
2. **vtkInfoVisBoost** - Download the latest version of Boost from here: http://www.boost.org/users/history/version_1_59_0.html, and extract to a folder of your choice (BOOST_ROOT). Open CMake and set the build directory to the VTK-build folder located in your 3D Slicer build. Add an entry called BOOST_ROOT, enable vtkInfoVisBoost and vtkInfoVisBoostGraphAlgorithms, then press Generate. Open the Slicer.sln located in the top directory of your Slicer build and build Slicer again.
4. **PoissonReconstruction** - Build the PoissonReconstruction library located here: https://github.com/daviddoria/PoissonReconstruction, and link it with the VTK-build located in your 3D Slicer build folder.
5. **PointSetProcessing** - Build the PointSetProcessing library located here: https://github.com/daviddoria/PointSetProcessing, and link it with the VTK-build located in your 3D Slicer build folder.
6. **SlicerSurfaceFromUnorganizedPoints** - Build the SlicerSurfaceFromUnorganizedPoints module after adding: the PoissonReconstruction library and includes; the PointSetProcessing library and includes; and the vtkInfovisBoostGraphAlgorithms library, in CMake.

## TODO
* Add params to readme and update screenshot
* Visualize normals: Size from UI, color
* Rename to SurfaceFromUnorganizedPoints
* Add ToolTips
* Add VTK filters for normals and surface
* If there is interest: Reset to default, save params in Slicer.ini, calculate in separate thread