# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sk/workspas/demo_ur/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sk/workspas/demo_ur/build

# Utility rule file for TT_autogen.

# Include the progress variables for this target.
include demo_cv/CMakeFiles/TT_autogen.dir/progress.make

demo_cv/CMakeFiles/TT_autogen:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/sk/workspas/demo_ur/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC for target TT"
	cd /home/sk/workspas/demo_ur/build/demo_cv && /usr/bin/cmake -E cmake_autogen /home/sk/workspas/demo_ur/build/demo_cv/CMakeFiles/TT_autogen.dir ""

TT_autogen: demo_cv/CMakeFiles/TT_autogen
TT_autogen: demo_cv/CMakeFiles/TT_autogen.dir/build.make

.PHONY : TT_autogen

# Rule to build all files generated by this target.
demo_cv/CMakeFiles/TT_autogen.dir/build: TT_autogen

.PHONY : demo_cv/CMakeFiles/TT_autogen.dir/build

demo_cv/CMakeFiles/TT_autogen.dir/clean:
	cd /home/sk/workspas/demo_ur/build/demo_cv && $(CMAKE_COMMAND) -P CMakeFiles/TT_autogen.dir/cmake_clean.cmake
.PHONY : demo_cv/CMakeFiles/TT_autogen.dir/clean

demo_cv/CMakeFiles/TT_autogen.dir/depend:
	cd /home/sk/workspas/demo_ur/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sk/workspas/demo_ur/src /home/sk/workspas/demo_ur/src/demo_cv /home/sk/workspas/demo_ur/build /home/sk/workspas/demo_ur/build/demo_cv /home/sk/workspas/demo_ur/build/demo_cv/CMakeFiles/TT_autogen.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : demo_cv/CMakeFiles/TT_autogen.dir/depend

