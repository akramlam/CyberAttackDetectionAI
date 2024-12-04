#pragma once
#include <memory>
#include <vector>
#include "types.hpp"

class IDSEngine {
private:
    struct Rule {
        std::string id;
        std::string description;
        int severity;
        std::string pattern;
    };

    std::vector<Rule> rules;
    std::unique_ptr<NetworkMonitor> networkMonitor;
    std::unique_ptr<LogAnalyzer> logAnalyzer;

public:
    IDSEngine();
    
    // Real-time network traffic analysis
    void analyzeTraffic(const NetworkPacket& packet);
    
    // Log analysis for intrusion detection
    void analyzeLogs(const LogEntry& log);
    
    // Rule management
    void loadRules(const std::string& rulePath);
    void addRule(const Rule& rule);
    
    void startMonitoring() {
        if (networkMonitor) {
            networkMonitor->startMonitoring();
        }
    }
}; 