# Author: Ali Uneri
# Date: 2013-11-24

set(EP_OPTION_NAME "USE_${EP_NAME}")
set(EP_REQUIRED_PROJECTS DCMTK Git ITK Python Qt Subversion VTK zlib OpenIGTLink)
set(EP_URL "git://github.com/Slicer/Slicer.git")
set(EP_PATCH "${CMAKE_CURRENT_LIST_DIR}/${EP_NAME}.patch")
set(EP_OPTION_DESCRIPTION "3D Slicer")

cma_envvar(@LIBRARYPATH@ PREPEND
  "@BINARY_DIR@/${EP_NAME}-build/bin/@INTDIR@"
  "@BINARY_DIR@/${EP_NAME}-build/lib/Slicer-${${PROJECT_NAME}_Slicer_VERSION}/cli-modules/@INTDIR@"
  "@BINARY_DIR@/${EP_NAME}-build/lib/Slicer-${${PROJECT_NAME}_Slicer_VERSION}/qt-loadable-modules/@INTDIR@"
  "@BINARY_DIR@/CTK-build/CTK-build/bin/@INTDIR@"
  "@BINARY_DIR@/CTK-build/PythonQt-build/@INTDIR@"
  "@BINARY_DIR@/CTK-build/QtTesting-build/@INTDIR@"
  "@BINARY_DIR@/LibArchive-install/@LIBDIR@"
  "@BINARY_DIR@/OpenIGTLink-build/bin/@INTDIR@"
  "@BINARY_DIR@/SlicerExecutionModel-build/ModuleDescriptionParser/bin/@INTDIR@"
  "@BINARY_DIR@/teem-build/bin/@INTDIR@")
cma_envvar(PYTHONPATH PREPEND
  "@BINARY_DIR@/${EP_NAME}-build/bin/@INTDIR@"
  "@BINARY_DIR@/${EP_NAME}-build/bin/Python"
  "@BINARY_DIR@/${EP_NAME}-build/lib/Slicer-${${PROJECT_NAME}_Slicer_VERSION}/qt-loadable-modules/@INTDIR@"
  "@BINARY_DIR@/${EP_NAME}-build/bin/lib/Slicer-${${PROJECT_NAME}_Slicer_VERSION}/qt-loadable-modules/Python")
cma_envvar(QT_PLUGIN_PATH APPEND
  "@BINARY_DIR@/${EP_NAME}-build/bin"
  "@BINARY_DIR@/CTK-build/CTK-build/bin")

if(WIN32)
  cma_envvar(SLICER_EXECUTABLE "@BINARY_DIR@/${EP_NAME}-build/bin/@INTDIR@/SlicerApp-real.exe")
elseif(APPLE)
  cma_envvar(SLICER_EXECUTABLE "@BINARY_DIR@/${EP_NAME}-build/bin/Slicer.app/Contents/MacOS/Slicer")
elseif(UNIX)
  cma_envvar(SLICER_EXECUTABLE "@BINARY_DIR@/${EP_NAME}-build/bin/SlicerApp-real")
else()
  message(FATAL_ERROR "Platform is not supported.")
endif()

cma_end_definition()
# -----------------------------------------------------------------------------

if(WIN32)
  string(LENGTH "${PROJECT_BINARY_DIR}/${EP_NAME}-build" LENGTH)
  if(LENGTH GREATER 36)
    message(FATAL_ERROR "Shorter path for ${PROJECT_NAME} build directory is required, since Slicer path is ${LENGTH} > 36 characters")
  endif()
endif()

cmake_dependent_option(${EP_OPTION_NAME}_CLI_MODULES "Build Slicer's CLI Modules" OFF ${EP_OPTION_NAME} OFF)

set(EP_CMAKE_ARGS
  -DADDITIONAL_C_FLAGS:STRING=${CMAKE_C_FLAGS}
  -DADDITIONAL_CXX_FLAGS:STRING=${CMAKE_CXX_FLAGS}
  -DBUILD_TESTING:BOOL=OFF
  -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
  -DDCMTK_DIR:PATH=${${PROJECT_NAME}_DCMTK_DIR}
  -DITK_DIR:PATH=${${PROJECT_NAME}_ITK_DIR}
  -DITK_SOURCE_DIR:PATH=${PROJECT_BINARY_DIR}/ITK
  -DPYTHON_EXECUTABLE:FILEPATH=${${PROJECT_NAME}_PYTHON_EXECUTABLE}
  -DPYTHON_INCLUDE_DIR:PATH=${${PROJECT_NAME}_PYTHON_INCLUDE_DIR}
  -DPYTHON_LIBRARY:FILEPATH=${${PROJECT_NAME}_PYTHON_LIBRARY}
  -DQT_QMAKE_EXECUTABLE:PATH=${${PROJECT_NAME}_QT_QMAKE_EXECUTABLE}
  -DSlicer_BUILD_BRAINSTOOLS:BOOL=OFF
  -DSlicer_BUILD_CLI:BOOL=${${EP_OPTION_NAME}_CLI_MODULES}
  -DSlicer_BUILD_DIFFUSION_SUPPORT:BOOL=OFF
  -DSlicer_BUILD_EMSegment:BOOL=OFF
  -DSlicer_BUILD_MULTIVOLUME_SUPPORT:BOOL=OFF
  -DSlicer_BUILD_MultiVolumeExplorer:BOOL=OFF
  -DSlicer_BUILD_MultiVolumeImporter:BOOL=OFF
  -DSlicer_BUILD_OpenIGTLinkIF:BOOL=ON
  -DSlicer_ITKV3_COMPATIBILITY:BOOL=OFF
  -DSlicer_USE_PYTHONQT_WITH_OPENSSL:BOOL=OFF
  -DSlicer_USE_PYTHONQT_WITH_TCL:BOOL=OFF
  -DSlicer_USE_SimpleITK:BOOL=OFF
  -DSlicer_USE_SYSTEM_DCMTK:BOOL=ON
  -DSlicer_USE_SYSTEM_ITKv4:BOOL=ON
  -DSlicer_USE_SYSTEM_python:BOOL=ON
  -DSlicer_USE_SYSTEM_VTK:BOOL=ON
  -DSlicer_USE_SYSTEM_OpenIGTLink:BOOL=ON
  -DOpenIGTLink_DIR:PATH=${${PROJECT_NAME}_OpenIGTLink_DIR}
  -DSlicer_USE_VTK_DEBUG_LEAKS:BOOL=${USE_VTK_DEBUG_LEAKS}
  -DVTK_DIR:PATH=${${PROJECT_NAME}_VTK_DIR}
  -DVTK_SOURCE_DIR:PATH=${PROJECT_BINARY_DIR}/VTK
  -DZLIB_ROOT:PATH=${${PROJECT_NAME}_ZLIB_ROOT}
  -DOpenIGTLink_DIR:PATH=${${PROJECT_NAME}_OpenIGTLink_DIR})

list(APPEND EP_CMAKE_ARGS
  -DGIT_EXECUTABLE:FILEPATH=${${PROJECT_NAME}_GIT_EXECUTABLE}
  -DBiiGTK_CMakeAll_DIR:PATH=${CMakeAll_DIR}
  -DBiiGTK_PATCH_CTK:FILEPATH=${PROJECT_SOURCE_DIR}/Projects/CTK.patch
  -DBiiGTK_PROJECT_HOME:STRING=Main
  -DBiiGTK_PROJECT_NAME:STRING=${PROJECT_NAME}
  -DBiiGTK_PROJECT_SPLASH:FILEPATH=${PROJECT_SOURCE_DIR}/Resources/biigtkLogoSplash.png
  -DBiiGTK_PROJECT_VERSION:STRING=${${PROJECT_NAME}_VERSION_MAJOR}.${${PROJECT_NAME}_VERSION_MINOR})

ExternalProject_Add(${EP_NAME}
  DEPENDS ${EP_REQUIRED_PROJECTS}
  # download
  GIT_REPOSITORY ${EP_URL}
  GIT_TAG 200c569a6c73798a19a6f9e365045e4ac7f31295
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

set(${PROJECT_NAME}_${EP_NAME}_VERSION 4.4 CACHE INTERNAL "")
set(${PROJECT_NAME}_${EP_NAME}_DIR "${PROJECT_BINARY_DIR}/${EP_NAME}-build/${EP_NAME}-build" CACHE INTERNAL "")
