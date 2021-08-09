cmake_minimum_required(VERSION 3.8.2)

set(IMPLOT_SOVERSION 0)
mark_as_advanced(IMPLOT_SOVERSION)

set(IMPLOT_VERSION 0.11)
mark_as_advanced(IMPLOT_VERSION)

project(implot LANGUAGES CXX VERSION ${IMPLOT_VERSION})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(IMGUI CONFIG REQUIRED)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

option(IMPLOT_DEMO "Include the ImPlot demo window implementation in library" ON)

add_library(implot
   src/implot.cpp
   src/implot_items.cpp

   $<$<BOOL:IMPLOT_DEMO>:src/implot_demo.cpp>
)

target_link_libraries(implot PUBLIC imgui::imgui)

add_library(implot::implot ALIAS implot)

target_include_directories(implot
   PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>

   PUBLIC $<INSTALL_INTERFACE:include>
)

set_target_properties(implot PROPERTIES
   SOVERSION ${IMPLOT_SOVERSION}
   VERSION ${IMPLOT_VERSION}
)

if(NOT APPLE)
   set_target_properties(implot PROPERTIES INSTALL_RPATH $ORIGIN)
endif()


#
# Installation
#
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(IMPLOT_CONFIG_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")

set(IMPLOT_GENERATED_CMAKE_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated/cmake")
set(IMPLOT_VERSION_CONFIG "${IMPLOT_GENERATED_CMAKE_DIR}/ImPlotConfigVersion.cmake")
set(IMPLOT_PROJECT_CONFIG "${IMPLOT_GENERATED_CMAKE_DIR}/ImPlotConfig.cmake")

set(IMPLOT_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/ImPlot" CACHE STRING "Path to the ImPlot cmake files")

write_basic_package_version_file(${IMPLOT_VERSION_CONFIG} COMPATIBILITY SameMajorVersion)
configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/Config.cmake.in
   ${IMPLOT_PROJECT_CONFIG}
   INSTALL_DESTINATION ${IMPLOT_INSTALL_CMAKEDIR}
)

set(IMPLOT_BINARIES implot)

install(
   TARGETS
      ${IMPLOT_BINARIES}

   EXPORT IMPLOT_Targets

   BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT IMPLOT_Runtime
   RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT IMPLOT_Runtime
   LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT IMPLOT_Runtime NAMELINK_COMPONENT IMPLOT_Development
   ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT IMPLOT_Development
   INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
   FILES
      src/implot.h

   DESTINATION
      ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
   FILES
      ${IMPLOT_PROJECT_CONFIG}
      ${IMPLOT_VERSION_CONFIG}

   DESTINATION
      ${IMPLOT_INSTALL_CMAKEDIR}
)

install(EXPORT IMPLOT_Targets
   DESTINATION ${IMPLOT_INSTALL_CMAKEDIR}
   NAMESPACE implot::
   COMPONENT IMPLOT_Development
)
