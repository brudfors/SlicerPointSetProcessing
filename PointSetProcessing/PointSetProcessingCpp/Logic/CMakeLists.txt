project(vtkSlicer${MODULE_NAME}ModuleLogic)

set(KIT ${PROJECT_NAME})

set(${KIT}_EXPORT_DIRECTIVE "VTK_SLICER_${MODULE_NAME_UPPER}_MODULE_LOGIC_EXPORT")

# Future super-build here
# Fork and build from my GitHub

# PointSetProcessing
find_library(POINTSETPROCESSING_LIBRARY PointSetProcessing
          PATHS "H:/bin/PointSetProcessing/R/Release"
          DOC "Path to the PointSetProcessing library." )  
find_path(POINTSETPROCESSING_INCLUDE_DIR vtkPointSetNormalEstimation.h
          PATHS "H:/src/PointSetProcessing"
          DOC "Path to PointSetProcessing include directory." )                        
          
if (NOT POINTSETPROCESSING_LIBRARY)
  message( FATAL_ERROR "PointSetProcessing library not found." )
elseif (NOT POINTSETPROCESSING_INCLUDE_DIR)
  message( FATAL_ERROR "PointSetProcessing include directory not found." )
endif()

# PoissonReconstruction
find_path(POISSONRECONSTRUCTION_BINARY_DIR vtkPoissonReconstructionConfigure.h
          PATHS "H:/bin/PoissonReconstruction/R"
          DOC "Path to PoissonReconstruction binary directory." )
find_path(POISSONRECONSTRUCTION_INCLUDE_DIR vtkPoissonReconstruction.h
          PATHS "H:/src/PoissonReconstruction/source"
          DOC "Path to PoissonReconstruction include directory." )
find_library(POISSONRECONSTRUCTION_LIBRARY vtkPoissonReconstruction
          PATHS "H:/bin/PoissonReconstruction/R/lib/Release"
          DOC "Path to the PoissonReconstruction library." )
          
if (NOT POISSONRECONSTRUCTION_LIBRARY)
  message( FATAL_ERROR "PoissonReconstruction library not found." )
elseif (NOT POISSONRECONSTRUCTION_BINARY_DIR)
  message( FATAL_ERROR "PoissonReconstruction binary directory not found." )
elseif (NOT POISSONRECONSTRUCTION_INCLUDE_DIR)
  message( FATAL_ERROR "PoissonReconstruction include directory not found." )
endif()

set(${KIT}_INCLUDE_DIRECTORIES
  "${POINTSETPROCESSING_INCLUDE_DIR}"
  "${POISSONRECONSTRUCTION_INCLUDE_DIR}"
  "${POISSONRECONSTRUCTION_BINARY_DIR}"
  )

set(${KIT}_SRCS
  vtkSlicer${MODULE_NAME}Logic.cxx
  vtkSlicer${MODULE_NAME}Logic.h
  )

set(${KIT}_TARGET_LIBRARIES
  "${POINTSETPROCESSING_LIBRARY}"
  "${POISSONRECONSTRUCTION_LIBRARY}"
  )

#-----------------------------------------------------------------------------
SlicerMacroBuildModuleLogic(
  NAME ${KIT}
  EXPORT_DIRECTIVE ${${KIT}_EXPORT_DIRECTIVE}
  INCLUDE_DIRECTORIES ${${KIT}_INCLUDE_DIRECTORIES}
  SRCS ${${KIT}_SRCS}
  TARGET_LIBRARIES ${${KIT}_TARGET_LIBRARIES}
  )
