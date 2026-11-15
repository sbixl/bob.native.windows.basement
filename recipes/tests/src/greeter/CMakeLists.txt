cmake_minimum_required(VERSION 4.4)
project(Greeter LANGUAGES C)

include(GNUInstallDirs)

if(NOT TARGET LibGreet::LibGreet)
   find_package(LibGreet CONFIG REQUIRED)
endif()

add_executable(greeter greeter.c)
target_link_libraries(greeter PUBLIC LibGreet::LibGreet)
install(TARGETS greeter DESTINATION "${CMAKE_INSTALL_BINDIR}")
