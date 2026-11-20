cmake_minimum_required(VERSION 3.21)
project(kof2003_local LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(KOF2003_SOURCE "" CACHE PATH "Public KOF 2003 port source")
set(NEOGEORECOMP_SOURCE "" CACHE PATH "Adapted neogeorecomp toolkit source")
set(KOF2003_ROMS "" CACHE PATH "Prepared KOF 2003 and Europe MVS v2 ROMs")
set(KOF2003_ENTRIES "${CMAKE_BINARY_DIR}/entries.txt" CACHE FILEPATH "Extra entry points from profiling")
# Build C of the graphics-set growth (docs/specs/graphics-set-growth/, ticket 04): the
# player plants one sprite pointing at the first tile of the Added Space. Off by
# default, so builds A and B carry neither the file nor the macro.
option(KOF2003_ADDED_SPACE_PROOF "Plant one sprite from the Added Space (graphics-set growth, ticket 04)" OFF)
option(KOF2003_REHEARSAL_MONITOR "Enable the optional private rehearsal event log" OFF)
# Per-frame memory probe (docs/specs/first-svc-character-import, ticket 08). Needs the
# hook from match/probe_hook.py in the private runtime copy; logs only when
# KOF_NATIVE_PROBE is set at run time.
option(KOF2003_NATIVE_PROBE "Compile the optional per-frame memory probe" OFF)

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
if(KOF2003_REHEARSAL_MONITOR)
    target_sources(neogeorecomp PRIVATE "${CMAKE_CURRENT_LIST_DIR}/import_slot/rehearsal_monitor.c")
    target_compile_definitions(neogeorecomp PRIVATE KOF2003_REHEARSAL_MONITOR)
endif()
if(KOF2003_NATIVE_PROBE)
    target_sources(neogeorecomp PRIVATE "${CMAKE_CURRENT_LIST_DIR}/match/native_probe.c")
    target_compile_definitions(neogeorecomp PRIVATE KOF2003_NATIVE_PROBE)
endif()
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
if(KOF2003_ADDED_SPACE_PROOF)
    # The renderer's call to the planter is compiled only under this macro, so the
    # toolkit needs it too; growth/added_space_patch.py inserts that call.
    target_sources(kof2003_player PRIVATE "${CMAKE_CURRENT_LIST_DIR}/growth/added_space_proof.c")
    target_compile_definitions(kof2003_player PRIVATE KOF2003_ADDED_SPACE_PROOF)
    target_compile_definitions(neogeorecomp PRIVATE KOF2003_ADDED_SPACE_PROOF)
endif()
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
