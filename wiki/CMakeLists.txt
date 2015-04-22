cmake_minimum_required(VERSION 2.8)

project(wiki)

FILE(GLOB SOURCE_FILES *.c)

add_executable(
    wiki
    ${SOURCE_FILES})

add_definitions(-std=c99 -O3)
