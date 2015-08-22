# PointSetProcessing
find_path(PointSetProcessing_INCLUDE_DIR vtkPointSetNormalEstimation.h
          PATHS "H:/src/PointSetProcessing"
          DOC "Path to PointSetProcessing include directory." )
find_library(PointSetProcessing_LIBRARY PointSetProcessing
          PATHS "H:/bin/PointSetProcessing/R/Release"
          DOC "Path to the PointSetProcessing library." )                          
          
if (NOT PointSetProcessing_LIBRARY)
  message( FATAL_ERROR "PointSetProcessing library not found." )
elseif (NOT PointSetProcessing_INCLUDE_DIR)
  message( FATAL_ERROR "PointSetProcessing include directory not found." )
endif()

# PoissonReconstruction
find_path(PoissonReconstruction_BINARY_DIR vtkPoissonReconstructionConfigure.h
          PATHS "H:/bin/PoissonReconstruction/R"
          DOC "Path to PoissonReconstruction binary directory." )
find_path(PoissonReconstruction_INCLUDE_DIR vtkPoissonReconstruction.h
          PATHS "H:/src/PoissonReconstruction/source"
          DOC "Path to PoissonReconstruction include directory." )
find_library(PoissonReconstruction_LIBRARY vtkPoissonReconstruction
          PATHS "H:/bin/PoissonReconstruction/R/lib/Release"
          DOC "Path to the PoissonReconstruction library." )
          
if (NOT PoissonReconstruction_LIBRARY)
  message( FATAL_ERROR "PoissonReconstruction library not found." )
elseif (NOT PoissonReconstruction_BINARY_DIR)
  message( FATAL_ERROR "PoissonReconstruction binary directory not found." )
elseif (NOT PoissonReconstruction_INCLUDE_DIR)
  message( FATAL_ERROR "PoissonReconstruction include directory not found." )
endif()

add_executable(PoissonSurfaceRecontruction main.cxx )

target_include_directories(PoissonSurfaceRecontruction PUBLIC
  "${PointSetProcessing_INCLUDE_DIR}"
  "${PoissonReconstruction_INCLUDE_DIR}"
  "${PoissonReconstruction_BINARY_DIR}"
)

target_link_libraries(PoissonSurfaceRecontruction 
  "${VTK_LIBRARIES}"
  "${PointSetProcessing_LIBRARY}"
  "${PoissonReconstruction_LIBRARY}"
)