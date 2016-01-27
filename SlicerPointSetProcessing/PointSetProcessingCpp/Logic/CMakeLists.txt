project(vtkSlicer${MODULE_NAME}ModuleLogic)

set(KIT ${PROJECT_NAME})

set(${KIT}_EXPORT_DIRECTIVE "VTK_SLICER_${MODULE_NAME_UPPER}_MODULE_LOGIC_EXPORT")

# Future super-build here
# Fork and build from my GitHub

# PointSetProcessing

find_library( PointSetProcessing_LIB PointSetProcessing REQUIRED
              PATHS
              "${PointSetProcessing_DIR}"
              "${PointSetProcessing_DIR}/Release"
              "${PointSetProcessing_DIR}/Debug"
              NO_CMAKE_PATH)
message(STATUS "PointSetProcessing found at ${PointSetProcessing_LIB}")


# PoissonReconstruction
find_library( PoissonReconstruction_LIB vtkPoissonReconstruction REQUIRED
              PATHS
              "${PoissonReconstruction_DIR}/lib"
              "${PoissonReconstruction_DIR}/lib/Release"
              "${PoissonReconstruction_DIR}/lib/Debug"
              NO_CMAKE_PATH)

message(STATUS "PoissonReconstruction found at ${PoissonReconstruction_LIB}")


# vtkInfovisBoostGraphAlgorithms
find_package(VTK REQUIRED
             PATHS
             ${VTK_DIR}
             NO_CMAKE_PATH)

find_library(vtkInfovisBoostGraphAlgorithms_LIB "vtkInfovisBoostGraphAlgorithms-${VTK_MAJOR_VERSION}.${VTK_MINOR_VERSION}" REQUIRED
              PATHS
              "${VTK_DIR}/lib"
              "${VTK_DIR}/lib/Release"
              "${VTK_DIR}/lib/Debug")

message(STATUS "vtkInfovisBoostGraphAlgorithms_LIB: ${vtkInfovisBoostGraphAlgorithms_LIB}")



set(${KIT}_INCLUDE_DIRECTORIES
  "${PointSetProcessing_INCLUDE_DIR}"
  "${PoissonReconstruction_INCLUDE_DIR}"
  "${PoissonReconstruction_DIR}"
  )

set(${KIT}_SRCS
  vtkSlicer${MODULE_NAME}Logic.cxx
  vtkSlicer${MODULE_NAME}Logic.h
  )

set(${KIT}_TARGET_LIBRARIES
  "${PointSetProcessing_LIB}"
  "${PoissonReconstruction_LIB}"
  "${vtkInfovisBoostGraphAlgorithms_LIB}"
  "${VTK_LIBRARIES}"
  )

#-----------------------------------------------------------------------------
SlicerMacroBuildModuleLogic(
  NAME ${KIT}
  EXPORT_DIRECTIVE ${${KIT}_EXPORT_DIRECTIVE}
  INCLUDE_DIRECTORIES ${${KIT}_INCLUDE_DIRECTORIES}
  SRCS ${${KIT}_SRCS}
  TARGET_LIBRARIES ${${KIT}_TARGET_LIBRARIES}
  )
