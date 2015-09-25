# Author: Ali Uneri
# Date: 2013-05-02

set(EP_OPTION_NAME "USE_${EP_NAME}")

cma_end_definition()
# -----------------------------------------------------------------------------

find_package(Qt4 4.8 REQUIRED)

ExternalProject_Add(${EP_NAME}
  DOWNLOAD_COMMAND ""
  CONFIGURE_COMMAND ""
  BUILD_COMMAND ""
  INSTALL_COMMAND "")

set(${PROJECT_NAME}_QT_QMAKE_EXECUTABLE "${QT_QMAKE_EXECUTABLE}" CACHE INTERNAL "")
set(${PROJECT_NAME}_QT_VERSION "${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}.${QT_VERSION_PATCH}" CACHE INTERNAL "")
