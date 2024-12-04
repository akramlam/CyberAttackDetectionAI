cmake_minimum_required(VERSION 3.10)
project(SecurityAgent)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
set(SOURCES
    agent.cpp
    network_manager.cpp
    encryption_service.cpp
    ids/ids_engine.cpp
    xdr/correlation_engine.cpp
    threat_intel/threat_intelligence.cpp
)

# Add header files
set(HEADERS
    types.hpp
    data_collector.hpp
    network_manager.hpp
    encryption_service.hpp
    command_executor.hpp
    ids/ids_engine.hpp
    xdr/correlation_engine.hpp
    threat_intel/threat_intelligence.hpp
    network/network_monitor.hpp
    log/log_analyzer.hpp
    threat_intel/ioc_database.hpp
    threat_intel/mitre_mapper.hpp
)

# Create executable
add_executable(SecurityAgent ${SOURCES} ${HEADERS})

# Add Windows libraries
if(WIN32)
    target_link_libraries(SecurityAgent wsock32 ws2_32)
endif()

# Include directories
target_include_directories(SecurityAgent PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}) 