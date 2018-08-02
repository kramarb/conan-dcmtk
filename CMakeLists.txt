project(conan-dcmtk)
cmake_minimum_required(VERSION 3.2)

include(ucm.cmake)
if(MSVC)
	if(BUILD_STATIC_RUNTIME)
		ucm_set_runtime(STATIC)
	endif()
endif()


add_subdirectory(src)
