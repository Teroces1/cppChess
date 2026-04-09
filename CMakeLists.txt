cmake_minimum_required(VERSION 3.28)
project(SalonChess CXX)

# Force modern C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find all standard .cpp files (like main.cpp)
file(GLOB SOURCES "src/*.cpp")

# Create the executable
add_executable(engine ${SOURCES})

# MAGIC FOR MODULES: Find all .cppm files and compile them as modules
file(GLOB MODULES "src/*.cppm")
target_sources(engine PUBLIC FILE_SET CXX_MODULES FILES ${MODULES})

# Maximum speed optimizations for Chess Engines
target_compile_options(engine PRIVATE -O3 -march=native -flto -Wall -Wextra)
target_link_options(engine PRIVATE -flto)