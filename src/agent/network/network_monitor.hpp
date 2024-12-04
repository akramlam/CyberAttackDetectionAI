#pragma once
#include <memory>
#include "types.hpp"

class NetworkMonitor {
public:
    NetworkMonitor() = default;
    virtual ~NetworkMonitor() = default;
    
    virtual void startMonitoring() = 0;
    virtual void stopMonitoring() = 0;
}; 