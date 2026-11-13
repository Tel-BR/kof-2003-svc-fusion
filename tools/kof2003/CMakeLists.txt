cmake_minimum_required(VERSION 3.21)
project(kof2003_local LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(KOF2003_SOURCE "" CACHE PATH "Public KOF 2003 port source")
set(NEOGEORECOMP_SOURCE "" CACHE PATH "Adapted neogeorecomp toolkit source")
set(KOF2003_ROMS "" CACHE PATH "Prepared KOF 2003 and Europe MVS v2 ROMs")
set(KOF2003_ENTRIES "${CMAKE_BINARY_DIR}/entries.txt" CACHE FILEPATH "Extra entry points from profiling")

if(NOT EXISTS "${KOF2003_SOURCE}/src/recomp_main.c")
    message(FATAL_ERROR "Set KOF2003_SOURCE to the KOF 2003 port checkout.")
endif()
if(NOT EXISTS "${NEOGEORECOMP_SOURCE}/CMakeLists.txt")
    message(FATAL_ERROR "Set NEOGEORECOMP_SOURCE to the adapted neogeorecomp toolkit.")
endif()

set(program "${KOF2003_ROMS}/271-pd.bin")
set(bios "${KOF2003_ROMS}/sp-s2.sp1")
if(NOT EXISTS "${program}" OR NOT EXISTS "${bios}")
    message(FATAL_ERROR "Set KOF2003_ROMS to the prepared ROM directory with the Europe MVS v2 BIOS.")
endif()

add_subdirectory("${NEOGEORECOMP_SOURCE}" toolkit)
if(NOT TARGET SDL2::SDL2)
    message(FATAL_ERROR "Set SDL2_DIR to the Windows x64 SDL2 development package's CMake directory.")
endif()

set(cartridge "${KOF2003_SOURCE}/src/game.c")
add_executable(kof2003_generator "${KOF2003_SOURCE}/src/recomp_main.c" "${cartridge}")
target_link_libraries(kof2003_generator PRIVATE m68krecomp_core)

set(generated "${CMAKE_BINARY_DIR}/generated")
file(MAKE_DIRECTORY "${generated}")
if(NOT EXISTS "${KOF2003_ENTRIES}")
    file(TOUCH "${KOF2003_ENTRIES}")
endif()

set(native_sources "${generated}/recomp_table.c")
set(part_count 24)
math(EXPR last_part "${part_count} - 1")
foreach(part RANGE ${last_part})
    set(suffix "${part}")
    if(part LESS 10)
        set(suffix "0${part}")
    endif()
    list(APPEND native_sources "${generated}/recomp_${suffix}.c")
endforeach()

add_custom_command(
    OUTPUT ${native_sources} "${generated}/recomp_common.h"
    COMMAND kof2003_generator --rom-path "${KOF2003_ROMS}" --bios sp-s2.sp1
            --out "${generated}" --files ${part_count} --entries "${KOF2003_ENTRIES}"
    DEPENDS kof2003_generator "${program}" "${bios}" "${KOF2003_ENTRIES}"
    VERBATIM
)
add_custom_target(kof2003_generate DEPENDS ${native_sources} "${generated}/recomp_common.h")

add_executable(kof2003_player "${KOF2003_SOURCE}/src/main.c" "${cartridge}" ${native_sources})
add_dependencies(kof2003_player kof2003_generate)
set_target_properties(kof2003_player PROPERTIES OUTPUT_NAME "KOF 2003")
target_compile_definitions(kof2003_player PRIVATE KOF2003_HAVE_RECOMP)
target_link_libraries(kof2003_player PRIVATE neogeorecomp)
if(WIN32)
    target_link_libraries(kof2003_player PRIVATE dbghelp)
    add_custom_command(TARGET kof2003_player POST_BUILD
        COMMAND "${CMAKE_COMMAND}" -E copy_if_different
                "$<TARGET_FILE:SDL2::SDL2>" "$<TARGET_FILE_DIR:kof2003_player>"
        VERBATIM
    )
endif()
if(MSVC)
    set_source_files_properties(${native_sources} PROPERTIES COMPILE_OPTIONS "/bigobj;/O1")
else()
    set_source_files_properties(${native_sources} PROPERTIES COMPILE_OPTIONS "-O1")
endif()
if(WIN32 AND CMAKE_C_COMPILER_ID STREQUAL "Clang" AND NOT MSVC)
    # The MinGW SDL2 package links with -mwindows. Keep the CLI synchronous
    # in PowerShell and link the Clang runtime so the player runs outside PATH.
    target_link_libraries(kof2003_player PRIVATE "-Wl,--subsystem,console")
    target_link_options(kof2003_player PRIVATE -static-libstdc++ -static-libgcc)
    # This part contains a large dispatch function that takes minutes to optimize.
    set_source_files_properties("${generated}/recomp_06.c" PROPERTIES COMPILE_OPTIONS "-O0")
endif()
