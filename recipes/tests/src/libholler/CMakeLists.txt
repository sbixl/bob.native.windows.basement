cmake_minimum_required(VERSION 3.15)
project(LibHoller
   VERSION 1.0.0
   LANGUAGES C)

include(GNUInstallDirs)
include(GenerateExportHeader)

# do not export any symbols by default
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)

# Add library
add_library(libHoller holler.c holler.h)
add_library(LibHoller::LibHoller ALIAS libHoller)
target_include_directories(libHoller
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>)
set_target_properties(libHoller PROPERTIES EXPORT_NAME LibHoller)

# Generate header for export/import definitions
generate_export_header(libHoller)
install(TARGETS libHoller EXPORT LibHollerTargets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# package stuff
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/LibHollerConfigVersion.cmake"
  VERSION ${LibHoller_VERSION}
  COMPATIBILITY SameMajorVersion
)

export(TARGETS libHoller
  FILE "${CMAKE_CURRENT_BINARY_DIR}/LibHollerTargets.cmake"
  NAMESPACE LibHoller::
)
configure_file(LibHollerConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/LibHollerConfig.cmake"
  @ONLY
)

set(ConfigPackageLocation ${CMAKE_INSTALL_LIBDIR}/cmake/LibHoller)
install(EXPORT LibHollerTargets
  FILE LibHollerTargets.cmake
  NAMESPACE LibHoller::
  DESTINATION ${ConfigPackageLocation}
)
install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/LibHollerConfig.cmake"
  "${CMAKE_CURRENT_BINARY_DIR}/LibHollerConfigVersion.cmake"
  DESTINATION ${ConfigPackageLocation}
)

