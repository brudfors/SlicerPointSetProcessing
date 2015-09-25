cmake_minimum_required(VERSION 2.8.9)

project(SlicerPointSetProcessing)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.example.com/Slicer/Extensions/SlicerPointSetProcessing")
set(EXTENSION_CATEGORY "Filtering")
set(EXTENSION_CONTRIBUTORS "Mikael Brudfors (brudfors@gmail.com)")
set(EXTENSION_DESCRIPTION "Performs point set processing in Slicer.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/SlicerPointSetProcessing.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/SlicerPointSetProcessing/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED
             PATHS
             ${SlicerPointSetProcessing_Slicer_DIR}
             NO_DEFAULT_PATH)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(PointSetProcessingPy)
add_subdirectory(PointSetProcessingCpp)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
