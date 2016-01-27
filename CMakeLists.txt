cmake_minimum_required(VERSION 2.8.7)

set(PROJECT_NAME "SuperBuild" CACHE STRING "")
project(${PROJECT_NAME})


# CMakeAll
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake")
find_package(CMakeAll REQUIRED)


# options
option(SuperBuild_BUILD_DOCUMENTATION "Support for Doxygen documentation" OFF)
option(SuperBuild_BUILD_TESTING "Support for CTest testing" ON)
option(SuperBuild_BUILD_PACKAGING "Support for CPack packaging" ON)

#Externals
set(USE_External_Slicer_DIR "" CACHE PATH "Slicer Build directory")
#set(SuperBuild_VTK_DIR ${SuperBuild_Slicer_DIR} CACHE PATH "Slicer Build directory" FORCE)
set(USE_External_BOOST_ROOT "" CACHE PATH "Boost Root directory")
set(USE_External_PointSetProcessing_BIN_DIR "" CACHE PATH "PointSetProcessing Build directory")
set(USE_External_PointSetProcessing_SRC_DIR "" CACHE PATH "PointSetProcessing Source directory")
set(USE_External_PoissonReconstruction_BIN_DIR "" CACHE PATH "Boost PoissonReconstruction Build directory")
set(USE_External_PoissonReconstruction_SRC_DIR "" CACHE PATH "Boost PoissonReconstruction Source directory")

# version
set(SuperBuild_VERSION_MAJOR 1)
set(SuperBuild_VERSION_MINOR 2)
cma_git_revision(${PROJECT_SOURCE_DIR} SuperBuild_VERSION_PATCH)
set(SuperBuild_VERSION "${SuperBuild_VERSION_MAJOR}.${SuperBuild_VERSION_MINOR}.${SuperBuild_VERSION_PATCH}")


# configure projects
file(GLOB SuperBuild_PROJECTS "${PROJECT_SOURCE_DIR}/Projects/*.cmake")
cma_add_projects(${SuperBuild_PROJECTS})

if(EXISTS "${USE_External_Slicer_DIR}" AND IS_DIRECTORY "${USE_External_Slicer_DIR}")
  message( STATUS "Using external Slicer")
else()
  message(STATUS "Building Slicer and all the dependencies")
  file(GLOB SuperBuild_PROJECTS "${PROJECT_SOURCE_DIR}/Projects/ExtraProjects/*.cmake")
  cma_add_projects(${SuperBuild_PROJECTS})
endif()


cma_print_projects()
message(STATUS "${PROJECT_NAME} ${SuperBuild_VERSION}")

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC" AND USE_Slicer)
  set(CMAKE_CONFIGURATION_TYPES "Release;RelWithDebInfo;Debug" CACHE STRING "" FORCE)
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang" AND APPLE)
  set(CMAKE_CXX_FLAGS "-stdlib=libstdc++ ${CMAKE_CXX_FLAGS}")
endif()

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  set(CMAKE_CXX_WARNING_LEVEL_DEBUG 1  CACHE STRING "" FORCE)
  # Use the highest lower level for visual studio for debug compiling configuration
  #https://msdn.microsoft.com/en-us/library/ksk5k0ta%28VS.80%29.aspx?f=255&MSPPError=-2147217396

  # Save previous value for CMAke Variables
  set(OLD_CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
  set(OLD_CMAKE_C_FLAGS ${CMAKE_C_FLAGS})
  set(OLD_CMAKE_CXX_FLAGS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG})
  set(OLD_CMAKE_C_FLAGS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG})

  if(OLD_CMAKE_CXX_FLAGS_DEBUG MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W1" OLD_CMAKE_CXX_FLAGS_DEBUG "${OLD_CMAKE_CXX_FLAGS_DEBUG}")
  else()
    set(OLD_CMAKE_CXX_FLAGS_DEBUG "${OLD_CMAKE_CXX_FLAGS_DEBUG} /W1"  CACHE STRING "" FORCE)
  endif()
  set(CMAKE_CXX_FLAGS_DEBUG ${OLD_CMAKE_CXX_FLAGS_DEBUG} CACHE STRING "" FORCE)

  if(OLD_CMAKE_C_FLAGS_DEBUG MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W1" OLD_CMAKE_C_FLAGS_DEBUG "${OLD_CMAKE_C_FLAGS_DEBUG}")
  else()
    set(OLD_CMAKE_C_FLAGS_DEBUG "${OLD_CMAKE_C_FLAGS_DEBUG} /W1"  CACHE STRING "" FORCE)
  endif()
  set(CMAKE_C_FLAGS_DEBUG ${OLD_CMAKE_C_FLAGS_DEBUG} CACHE STRING "" FORCE)

  if(OLD_CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W1" OLD_CMAKE_CXX_FLAGS "${OLD_CMAKE_CXX_FLAGS}")
  else()
    set(OLD_CMAKE_CXX_FLAGS "${OLD_CMAKE_CXX_FLAGS} /W1"  CACHE STRING "" FORCE)
  endif()
  set(CMAKE_CXX_FLAGS ${OLD_CMAKE_CXX_FLAGS} CACHE STRING "" FORCE)

  if(OLD_CMAKE_C_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W1" OLD_CMAKE_C_FLAGS "${OLD_CMAKE_C_FLAGS}")
  else()
    set(OLD_CMAKE_C_FLAGS "${OLD_CMAKE_C_FLAGS} /W1"  CACHE STRING "" FORCE)
  endif()
  set(CMAKE_C_FLAGS ${OLD_CMAKE_C_FLAGS} CACHE STRING "" FORCE)

endif()

if(SuperBuild_BUILD_DOCUMENTATION AND NOT USE_Doxygen)
  message("SuperBuild_BUILD_DOCUMENTATION is enabling Doxygen")
  set(USE_Doxygen ON CACHE BOOL "" FORCE)
endif()

cma_configure_projects()

if(SuperBuild_BUILD_DOCUMENTATION)
  add_subdirectory(Documentation)
endif()

if(SuperBuild_BUILD_TESTING)
  #cma_test_projects(CudaTools ItkTools MatlabTools PythonTools)
endif()

# configure files
file(WRITE ${PROJECT_BINARY_DIR}/CMake.h "#ifndef __CMake_h\n#define __CMake_h\n\n")
file(WRITE ${PROJECT_BINARY_DIR}/CMake.py "")
file(WRITE ${PROJECT_BINARY_DIR}/CMake.m "")
get_cmake_property(VARIABLES VARIABLES)
foreach (KEY ${VARIABLES})
  if(KEY MATCHES "^SuperBuild_")
    file(TO_NATIVE_PATH "${${KEY}}" VALUE)
    if(WIN32)
      string(REPLACE "\\" "\\\\" VALUE "${VALUE}")
    endif()
    file(APPEND ${PROJECT_BINARY_DIR}/CMake.h "#define ${KEY} \"${VALUE}\"\n")
    file(APPEND ${PROJECT_BINARY_DIR}/CMake.py "${KEY} = '${VALUE}'\n")
    file(APPEND ${PROJECT_BINARY_DIR}/CMake.m "${KEY} = '${VALUE}';\n")
  endif()
endforeach()
file(APPEND ${PROJECT_BINARY_DIR}/CMake.h "\n#endif  // __CMake_h\n")


# configure launcher
cma_configure_launcher("${PROJECT_SOURCE_DIR}/CMake/Launcher.cmake")

cma_launcher_target(Terminal
  NAME run_Terminal)
cma_launcher_shortcut(Terminal
  NAME Terminal)

if(USE_Qt)
  cma_launcher_target(designer
    NAME run_QtDesigner)
endif()
