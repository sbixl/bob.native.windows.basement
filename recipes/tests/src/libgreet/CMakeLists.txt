cmake_minimum_required(VERSION 3.15)
project(LibGreet LANGUAGES C)

include(GNUInstallDirs)
include(GenerateExportHeader)

option(LIBGREET_INSTALL_HEADERS "Install public headers" OFF)

# Find dependency if target does not exist yet in build tree
if (NOT TARGET LibHoller::LibHoller)
  find_package(LibHoller CONFIG REQUIRED)
endif()

# Add library
add_library(LibGreet greet.c greet.h)
add_library(LibGreet::LibGreet ALIAS LibGreet)
target_include_directories(LibGreet
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>)
target_link_libraries(LibGreet PUBLIC LibHoller::LibHoller)

# Generate header for export/import definitions
#generate_export_header(LibGreet)
if(LIBGREET_INSTALL_HEADERS)
  target_include_directories(LibGreet PUBLIC
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )
  install(FILES
    greet.h
    "${CMAKE_CURRENT_BINARY_DIR}/libgreet_export.h"
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  )
endif()

install(TARGETS LibGreet EXPORT LibGreetTargets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# package stuff
export(TARGETS LibGreet
  FILE "${CMAKE_CURRENT_BINARY_DIR}/LibGreetTargets.cmake"
  NAMESPACE LibGreet::
)
configure_file(LibGreetConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/LibGreetConfig.cmake"
  @ONLY
)

set(ConfigPackageLocation ${CMAKE_INSTALL_LIBDIR}/cmake/LibGreet)
install(EXPORT LibGreetTargets
  FILE LibGreetTargets.cmake
  NAMESPACE LibGreet::
  DESTINATION ${ConfigPackageLocation}
)
install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/LibGreetConfig.cmake"
  DESTINATION ${ConfigPackageLocation}
)

