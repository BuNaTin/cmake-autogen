import re
import os
import shutil

cmake_folder = "/cmake"

def init(folder: str, forse: bool = False) -> bool:
    try:
        os.mkdir(folder + cmake_folder)
    except OSError as _:
        print("Cmake find files exists")
        if not forse:
          return False
        # something like exit
        shutil.rmtree(folder + cmake_folder)
        os.mkdir(folder + cmake_folder)

    return True

def get_all(folder: str) -> list:
    with open(folder + "/debian/control", "r") as f:
        lines = f.readlines()
        matches = [re.search(r'lib\w+-dev', line) for line in lines if "Package:" not in line]
        return [m.group(0)[3:-4] for m in matches if m is not None]

def create(folder: str, name: str):
    lib_upper = name.upper()
    lib_lower = name.lower()
    lib_capit = name.capitalize()
    with open(folder + "/cmake/Find" + lib_capit + ".cmake", "w") as f:
        f.write(f"""
if ({lib_upper}_LIBRARIES AND {lib_upper}_INCLUDE_DIRS)                                                                                                                                                                  
# in cache already                                                                                                                                                                                         
set({lib_upper}_FOUND TRUE)                                                                                                                                                                                       
else ({lib_upper}_LIBRARIES AND {lib_upper}_INCLUDE_DIRS)                                                                                                                                                                
find_path({lib_upper}_INCLUDE_DIR
  NAMES
    {lib_lower}.h
  PATHS
    /usr/include
    /usr/local/include
    /opt/local/include
    /sw/include
)

find_library({lib_upper}_LIBRARY
  NAMES
    lib{lib_lower}
  PATHS
    /usr/lib
    /usr/local/lib
)

if ({lib_upper}_LIBRARY)
  set({lib_upper}_FOUND TRUE)
endif ({lib_upper}_LIBRARY)

set({lib_upper}_INCLUDE_DIRS
  ${{INIPARSER_INCLUDE_DIR}}
)

if ({lib_upper}_FOUND)
  set({lib_upper}_LIBRARIES
    ${{{lib_upper}_LIBRARIES}}
    ${{{lib_upper}_LIBRARY}}
  )
endif ({lib_upper}_FOUND)

if ({lib_upper}_INCLUDE_DIRS AND {lib_upper}_LIBRARIES)
   set({lib_upper}_FOUND TRUE)
endif ({lib_upper}_INCLUDE_DIRS AND {lib_upper}_LIBRARIES)

if ({lib_upper}_FOUND)
  if (NOT {lib_capit}_FIND_QUIETLY)
    message(STATUS "Found {lib_capit}: ${{{lib_upper}_LIBRARIES}}")
  endif (NOT {lib_capit}_FIND_QUIETLY)
else ({lib_upper}_FOUND)
  if ({lib_capit}_FIND_REQUIRED)
    message(FATAL_ERROR "Could not find {lib_capit}")
  endif ({lib_capit}_FIND_REQUIRED)
endif ({lib_upper}_FOUND)

# show the INIPARSER_INCLUDE_DIRS and INIPARSER_LIBRARIES variables only in the advanced view
mark_as_advanced({lib_upper}_INCLUDE_DIRS {lib_upper}_LIBRARIES) 

endif ({lib_upper}_LIBRARIES AND {lib_upper}_INCLUDE_DIRS)
        """)
    return
