#pragma once
#include "types.hpp"

class MITREMapper {
public:
    MITREMapper() = default;
    virtual ~MITREMapper() = default;
    
    virtual void mapTechnique(const SecurityEvent& event) = 0;
}; 