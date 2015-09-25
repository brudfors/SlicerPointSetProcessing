# Author: Ali Uneri
# Date: 2012-10-28

set(EP_OPTION_NAME "USE_${EP_NAME}")
set(EP_REQUIRED_PROJECTS Git)
set(EP_OPTION_DESCRIPTION "Visualization Toolkit")

cma_list(APPEND EP_REQUIRED_PROJECTS Python IF USE_Python)
cma_list(APPEND EP_REQUIRED_PROJECTS Qt IF USE_Qt)
cma_list(APPEND EP_REQUIRED_PROJECTS zlib IF USE_zlib)

if(USE_Slicer)
  set(EP_URL "git://github.com/Slicer/VTK.git")
  set(EP_VERSION "b55dad7dbdf8bdbe25d814b411aa5f211b68c09f")
else()
  set(EP_URL "git://vtk.org/VTK.git")
  set(EP_VERSION "v6.1.0")
endif()

if(USE_PointSetProcessing)
  list(APPEND EP_REQUIRED_PROJECTS Boost)
endif()

cma_envvar(@LIBRARYPATH@ PREPEND "@BINARY_DIR@/@LIBDIR@/@INTDIR@")
cma_envvar(PYTHONPATH PREPEND
  "@BINARY_DIR@/@LIBDIR@/@INTDIR@"
  "@BINARY_DIR@/Wrapping/Python")

cma_end_definition()
# -----------------------------------------------------------------------------

cmake_dependent_option(${EP_OPTION_NAME}_DEBUG_LEAKS "Build leak checking support into VTK" OFF ${EP_OPTION_NAME} OFF)
cmake_dependent_option(${EP_OPTION_NAME}_TDx "Support for 3DConnexion devices" OFF ${EP_OPTION_NAME} OFF)

set(EP_CMAKE_ARGS
  -DBUILD_EXAMPLES:BOOL=OFF
  -DBUILD_TESTING:BOOL=OFF
  -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
  -DCMAKE_C_FLAGS:STRING=${CMAKE_C_FLAGS}
  -DCMAKE_CXX_FLAGS:STRING=${CMAKE_CXX_FLAGS}
  -DModule_vtkTestingRendering:BOOL=ON
  -DVTK_DEBUG_LEAKS:BOOL=${${EP_OPTION_NAME}_DEBUG_LEAKS}
  -DVTK_USE_DISPLAY:BOOL=OFF
  -DVTK_USE_GUISUPPORT:BOOL=${USE_Qt}
  -DVTK_USE_PARALLEL:BOOL=ON
  -DVTK_Group_Qt:BOOL=${USE_Qt}
  -DVTK_USE_QT:BOOL=${USE_Qt}
  -DVTK_USE_QVTK_QTOPENGL:BOOL=${USE_Qt}
  -DVTK_USE_SYSTEM_ZLIB:BOOL=${USE_zlib}
  -DVTK_USE_TDX:BOOL=${${EP_OPTION_NAME}_TDx}
  -DVTK_USE_TK:BOOL=OFF
  -DVTK_WRAP_PYTHON:BOOL=${USE_Python})

if(APPLE)
  list(APPEND EP_CMAKE_ARGS
    -DVTK_REQUIRED_OBJCXX_FLAGS:STRING=
    -DVTK_USE_CARBON:BOOL=OFF
    -DVTK_USE_COCOA:BOOL=ON
    -DVTK_USE_X:BOOL=OFF)
elseif(UNIX)
  list(APPEND EP_CMAKE_ARGS
    -DModule_vtkRenderingFreeTypeFontConfig:BOOL=ON
    -DVTK_USE_X:BOOL=ON)
endif()

if(USE_Python OR USE_Slicer)
  list(APPEND EP_CMAKE_ARGS -DBUILD_SHARED_LIBS:BOOL=ON)
else()
  list(APPEND EP_CMAKE_ARGS -DBUILD_SHARED_LIBS:BOOL=OFF)
endif()
if(USE_PLUS)
  list(APPEND EP_CMAKE_ARGS -DVTK_LEGACY_REMOVE:BOOL=OFF)
else()
  list(APPEND EP_CMAKE_ARGS -DVTK_LEGACY_REMOVE:BOOL=ON)
endif()
if(USE_Python)
  list(APPEND EP_CMAKE_ARGS
    -DPYTHON_EXECUTABLE:PATH=${${PROJECT_NAME}_PYTHON_EXECUTABLE}
    -DPYTHON_INCLUDE_DIR:PATH=${${PROJECT_NAME}_PYTHON_INCLUDE_DIR}
    -DPYTHON_LIBRARY:FILEPATH=${${PROJECT_NAME}_PYTHON_LIBRARY})
endif()
if(USE_Qt)
  list(APPEND EP_CMAKE_ARGS -DQT_QMAKE_EXECUTABLE:FILEPATH=${${PROJECT_NAME}_QT_QMAKE_EXECUTABLE})
endif()
if(USE_zlib)
  list(APPEND EP_CMAKE_ARGS
    -DZLIB_ROOT:PATH=${${PROJECT_NAME}_ZLIB_ROOT}
    -DZLIB_INCLUDE_DIR:PATH=${${PROJECT_NAME}_ZLIB_INCLUDE_DIR}
    -DZLIB_LIBRARY:FILEPATH=${${PROJECT_NAME}_ZLIB_LIBRARY})
endif()

if(USE_PointSetProcessing)
  list(APPEND EP_CMAKE_ARGS
    -DBOOST_ROOT:PATH=${${PROJECT_NAME}_BOOST_ROOT}
    -DBOOST_INCLUDE_DIR:PATH=${${PROJECT_NAME}_BOOST_INCLUDE_DIR}
    -DModule_vtkInfovisBoost:BOOL=ON
    -DModule_vtkInfovisBoostGraphAlgorithms:BOOL=ON
    )
endif()

ExternalProject_Add(${EP_NAME}
  DEPENDS ${EP_REQUIRED_PROJECTS}
  # download
  GIT_REPOSITORY ${EP_URL}
  GIT_TAG ${EP_VERSION}
  # patch
  # update
  UPDATE_COMMAND ""
  # configure
  SOURCE_DIR ${PROJECT_BINARY_DIR}/${EP_NAME}
  CMAKE_ARGS ${EP_CMAKE_ARGS}
  # build
  BINARY_DIR ${PROJECT_BINARY_DIR}/${EP_NAME}-build
  # install
  INSTALL_COMMAND ""
  # test
  )

set(${PROJECT_NAME}_${EP_NAME}_DIR "${PROJECT_BINARY_DIR}/${EP_NAME}-build" CACHE INTERNAL "")
