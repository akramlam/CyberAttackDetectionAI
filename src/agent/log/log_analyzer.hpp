#pragma once
#include "types.hpp"

class LogAnalyzer {
public:
    LogAnalyzer() = default;
    virtual ~LogAnalyzer() = default;
    
    virtual void analyze(const LogEntry& log) = 0;
}; 