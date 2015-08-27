# SlicerPointSetProcessing

A module performing point-set processing tasks in 3D Slicer. Currently implemented tasks are:
* Poisson Surface Reconstruction (based on http://research.microsoft.com/en-us/um/people/hoppe/recon.pdf)

## Build Instructions
1. Follow the instructions found here: http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions, in order to build **3D Slicer**.  
2. Download the latest version of **Boost** from here: http://www.boost.org/users/history/version_1_59_0.html, and extract to a folder of your choice (BOOST_ROOT).
3. Open CMake and set the build directory to the VTK-build folder located in your 3D Slicer build. Add an entry called BOOST_ROOT (point it to the corresponding foder from step 2), enable **vtkInfoVisBoost** and **vtkInfoVisBoostGraphAlgorithms**, then press Generate. Open the Slicer.sln located in the top directory of your Slicer build and build Slicer again.
4. Build the **PoissonReconstruction** library located here: https://github.com/daviddoria/PoissonReconstruction, and link it with the VTK-build located in your 3D Slicer build folder.
5. Build the **PointSetProcessing** library located here: https://github.com/daviddoria/PointSetProcessing, and link it with the VTK-build located in your 3D Slicer build folder.
6. Build the **SlicerPointSetProcessing** module after adding: the PoissonReconstruction library and includes; the PointSetProcessing library and includes; and the vtkInfovisBoostGraphAlgorithms library, in CMake.

![Alt text](https://github.com/brudfors/SlicerPointSetProcessing/blob/master/PointSetProcessingScreenShot.PNG?raw=true "SlicerPointSetProcessing")


