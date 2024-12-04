#pragma once
#include <memory>
#include <queue>
#include "types.hpp"

class CorrelationEngine {
private:
    std::unique_ptr<EventProcessor> eventProcessor;
    std::unique_ptr<RuleEngine> ruleEngine;
    std::priority_queue<SecurityEvent> eventQueue;

public:
    // Event correlation
    void correlateEvents(const SecurityEvent& event);
    
    // Threat detection
    void detectThreats();
    
    // Response automation
    void automateResponse(const Threat& threat);
    
    // Integration with other security tools
    void integrateWithSIEM(const std::string& siemEndpoint);
    void integrateWithSOAR(const std::string& soarEndpoint);
    
    // Add to public section:
    void startCorrelation() {
        // Initialize event processing
        if (eventProcessor) {
            eventProcessor->start();
        }
    }
}; 