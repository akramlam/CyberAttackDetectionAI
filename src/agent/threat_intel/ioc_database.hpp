#pragma once
#include "types.hpp"

class IOCDatabase {
public:
    IOCDatabase() = default;
    virtual ~IOCDatabase() = default;
    
    virtual void addIndicator(const Indicator& ioc) = 0;
    virtual bool checkIndicator(const std::string& value) = 0;
}; 