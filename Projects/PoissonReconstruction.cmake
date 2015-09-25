# Author: Eugenio Marinetto
# Date: 2015-09-22

set(EP_OPTION_NAME "USE_${EP_NAME}")
set(EP_REQUIRED_PROJECTS Git)

if(EXISTS "${USE_External_Slicer_DIR}" AND IS_DIRECTORY "${USE_External_Slicer_DIR}")
else()
  list(APPEND EP_REQUIRED_PROJECTS
       VTK)
endif()

set(EP_URL "https://github.com/daviddoria/PoissonReconstruction.git")
set(EP_GIT_TAG "master")
set(EP_OPTION_DESCRIPTION "${EP_NAME} Project")
set(EP_OPTION_DEFAULT ON)

cma_list(APPEND EP_REQUIRED_PROJECTS Doxygen IF ${PROJECT_NAME}_BUILD_DOCUMENTATION)

cma_end_definition()
# -----------------------------------------------------------------------------

if((EXISTS "${USE_External_PoissonReconstruction_BIN_DIR}" AND IS_DIRECTORY "${USE_External_PoissonReconstruction_BIN_DIR}")
          AND (EXISTS "${USE_External_PoissonReconstruction_SRC_DIR}" AND IS_DIRECTORY "${USE_External_PoissonReconstruction_SRC_DIR}"))
  ExternalProject_Add(${EP_NAME}
        DOWNLOAD_COMMAND ""
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND "")

  set(${PROJECT_NAME}_${EP_NAME}_DIR "${USE_External_PoissonReconstruction_BIN_DIR}" CACHE INTERNAL "")
  set(${PROJECT_NAME}_${EP_NAME}_INCLUDE_DIR "${USE_External_PoissonReconstruction_SRC_DIR}/source" CACHE INTERNAL "")

else()

  set(EP_CMAKE_ARGS
    -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
    -DCMAKE_C_FLAGS:STRING=${CMAKE_C_FLAGS}
    -DCMAKE_CXX_FLAGS:STRING=${CMAKE_CXX_FLAGS}
    -DCMAKE_INSTALL_PREFIX:PATH=${${PROJECT_NAME}_INSTALL_DIR}
    -D${EP_NAME}_INSTALL_DIR:BOOL=${${PROJECT_NAME}_INSTALL_DIR}
    -D${EP_NAME}_BUILD_DOCUMENTATION:BOOL=${${PROJECT_NAME}_BUILD_DOCUMENTATION}
    -D${EP_NAME}_CMAKE_DEBUG_FLAG:BOOL=${${PROJECT_NAME}_CMAKE_DEBUG_FLAG}
    -DVTK_DIR:PATH=${${PROJECT_NAME}_VTK_DIR}
    )

  if(${${PROJECT_NAME}_BUILD_DOCUMENTATION})
    list(APPEND EP_CMAKE_ARGS
      -DDOXYGEN_EXECUTABLE:PATH=${${PROJECT_NAME}_DOXYGEN_EXECUTABLE}
      )
  endif()

  ExternalProject_Add(${EP_NAME}
    DEPENDS ${EP_REQUIRED_PROJECTS}
    # download
    GIT_REPOSITORY ${EP_URL}
    GIT_TAG ${EP_GIT_TAG}
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
  set(${PROJECT_NAME}_${EP_NAME}_INCLUDE_DIR "${PROJECT_BINARY_DIR}/${EP_NAME}/source" CACHE INTERNAL "")

endif()