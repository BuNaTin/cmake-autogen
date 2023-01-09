import os

source_types = ["exe","lib"]
INDEX_EXE = 0
INDEX_LIB = 1

def gen(folder: str, type: str, find_deps: list, force: bool = False) -> bool:
    if not type in source_types:
        print("Wrong type")
        return False

    name = folder[folder.rfind('/') + 1:]
    

    if type == source_types[INDEX_EXE]:
        print("Gen executable cmake")
        genExe()

    if type == source_types[INDEX_LIB]:
        print("Gen library cmake")
        genLib(folder, name, find_deps)

    return True

def genExe():
    return

def genLib(folder: str, name: str, find_deps: list):
    head = f"""
cmake_minimum_required(VERSION 3.16)
project({name})
set(Project {name})

set(CMAKE_C_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS "-Wall")

add_library(${{Project}} STATIC)

set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
set(CMAKE_MODULE_PATH ${{CMAKE_MODULE_PATH}} "${{CMAKE_SOURCE_DIR}}/cmake/") 

"""
    sources = f"""
target_include_directories({name} PUBLIC
    ${{CMAKE_CURRENT_SOURCE_DIR}}/include
)

set(SRC_DIR ${{CMAKE_CURRENT_SOURCE_DIR}}/src)

target_include_directories({name} PRIVATE
    ${{CMAKE_CURRENT_SOURCE_DIR}}/src
)

target_sources({name} PRIVATE
"""
    all_libs = "set(ALL_LIBS\n"

    tail = f"""
target_link_libraries(${{Project}} PUBLIC
    ${{ALL_LIBS}}
)

target_compile_definitions(${{Project}} PUBLIC

)

install(TARGETS ${{Project}} LIBRARY DESTINATION bin)
"""

    for dep in find_deps:
        dep = dep.capitalize()
        head += f"find_package({dep})\n"
        dep = dep.upper()
        all_libs += f"    ${{{dep}_LIBRARIES}}\n"
    all_libs += ')\n'

    for source in getSources(folder, "*.c") + getSources(folder, "*.cpp"):
        sources += "    ${SRC_DIR}" + source[4:]
    sources += ')\n'

    with open(f"{folder}/CMakeLists.txt", "w") as f:
        f.write(head)
        f.write(sources)
        f.write(all_libs)
        f.write(tail)

def getSources(folder: str, pattern: str = "*.c")-> list:
    name = folder[folder.rfind('/') + 1:]
    stream = os.popen(f'find {folder} -type f -name "{pattern}" | grep -v "test" | grep -v "/build"')
    lines = stream.readlines()
    lines = [line[line.index(name) + len(name):] for line in lines]
    return lines