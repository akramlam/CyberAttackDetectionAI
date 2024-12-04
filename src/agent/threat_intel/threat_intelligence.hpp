#pragma once
#include <string>
#include <vector>
#include <memory>

class ThreatIntelligence {
private:
    std::unique_ptr<IOCDatabase> iocDb;
    std::unique_ptr<MITREMapper> mitreMapper;

public:
    // MITRE ATT&CK Framework integration
    void mapToMITRE(const SecurityEvent& event);
    
    // Threat feeds integration
    void updateThreatFeeds();
    
    // IOC management
    void addIOC(const Indicator& ioc);
    bool checkIOC(const std::string& value);
    
    // Add to public section:
    void startUpdates() {
        // Start periodic updates of threat feeds
        updateThreatFeeds();
    }
}; 