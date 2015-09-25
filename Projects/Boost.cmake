# Author: Eugenio Marinetto
# Date: 2015-09-22

  set(EP_OPTION_NAME "USE_${EP_NAME}")
  set(EP_URL "http://sourceforge.net/projects/boost/files/boost/1.59.0/boost_1_59_0.zip")
  set( EP_CONFIGURE_COMMAND )
  if( UNIX )
    set( EP_CONFIGURE_COMMAND ./bootstrap.sh )
    set( EP_BUILD_COMMAND ./b2 )
  else()
    if( WIN32 )
      set( EP_CONFIGURE_COMMAND bootstrap.bat )
      set( EP_BUILD_COMMAND b2.exe )
    endif()
  endif()

  cma_end_definition()
  # -----------------------------------------------------------------------------


if(EXISTS "${USE_External_BOOST_ROOT}" AND IS_DIRECTORY "${USE_External_BOOST_ROOT}")

    message(STATUS "Using Boost from ${USE_External_BOOST_ROOT}")

    set(${PROJECT_NAME}_BOOST_ROOT "${USE_External_BOOST_ROOT}" CACHE INTERNAL "")
    #set(${PROJECT_NAME}_BOOST_INCLUDE_DIR "${USE_External_BOOST_ROOT}" CACHE INTERNAL "")

    ExternalProject_Add(${EP_NAME}
      DOWNLOAD_COMMAND ""
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      INSTALL_COMMAND "")

else()

  ExternalProject_Add(${EP_NAME}
    URL ${EP_URL}
    BUILD_IN_SOURCE 1
    UPDATE_COMMAND ""
    # configure
    SOURCE_DIR ${PROJECT_BINARY_DIR}/${EP_NAME}
    CONFIGURE_COMMAND ${EP_CONFIGURE_COMMAND}
    BUILD_COMMAND  ${EP_BUILD_COMMAND} install
      --without-python
      --without-mpi
      --disable-icu
      --prefix=${PROJECT_BINARY_DIR}/${EP_NAME}-build/
      --threading=single,multi
      --link=shared
      --variant=release
      -j8
    INSTALL_COMMAND ""
  )

  if( NOT WIN32 )
    set(${PROJECT_NAME}_BOOST_ROOT "${PROJECT_BINARY_DIR}/${EP_NAME}" CACHE INTERNAL "")
    set(${PROJECT_NAME}_BOOST_INCLUDE_DIR "${PROJECT_BINARY_DIR}/${EP_NAME}-build/include/" CACHE INTERNAL "")
  else()
    set(${PROJECT_NAME}_BOOST_ROOT "${PROJECT_BINARY_DIR}/${EP_NAME}" CACHE INTERNAL "")
    set(${PROJECT_NAME}_BOOST_INCLUDE_DIR "${PROJECT_BINARY_DIR}/${EP_NAME}-build/include/boost-1_49/" CACHE INTERNAL "")
  endif()

endif()











