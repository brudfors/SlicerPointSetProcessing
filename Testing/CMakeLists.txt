cmake_minimum_required (VERSION 2.8.11)
project (PoissonSurfaceRecontruction)

find_package (VTK REQUIRED)
if (VTK_FOUND)
  include (${VTK_USE_FILE})
endif (VTK_FOUND)

add_subdirectory (PoissonSurfaceRecontruction)
add_subdirectory (Data)