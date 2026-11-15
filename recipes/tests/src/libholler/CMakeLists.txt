cmake_minimum_required(VERSION 4.4)
project(LibHoller LANGUAGES C)

include(GNUInstallDirs)

option(LIBHOLLER_INSTALL_HEADERS "Install public headers" OFF)

# Add library
add_library(libHoller holler.c holler.h)
add_library(LibHoller::LibHoller ALIAS libHoller)

target_include_directories(libHoller
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)

set_target_properties(libHoller PROPERTIES EXPORT_NAME LibHoller)

if(LIBHOLLER_INSTALL_HEADERS)
  target_include_directories(libHoller PUBLIC
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )
endif()

install(TARGETS libHoller EXPORT LibHollerTargets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# package stuff
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
  DESTINATION ${ConfigPackageLocation}
)

