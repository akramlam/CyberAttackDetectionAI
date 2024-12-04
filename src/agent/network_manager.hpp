#pragma once
#include <functional>
#include <iostream>
#include <memory>
#include "types.hpp"

class NetworkManager {
private:
    std::function<void(const Command&)> commandCallback;
    std::unique_ptr<IDSEngine> idsEngine;
    std::unique_ptr<ThreatIntelligence> threatIntel;
    std::unique_ptr<NetworkMonitor> networkMonitor;

public:
    NetworkManager();
    
    // EDR capabilities
    void onCommandReceived(std::function<void(const Command&)> callback);
    void sendToServer(const std::string& data);
    
    // XDR capabilities
    void correlateEvents(const SecurityEvent& event);
    void integrateWithSIEM(const std::string& siemEndpoint);
    
    // IDS capabilities
    void startNetworkMonitoring();
    void handleIntrusionAlert(const IntrusionAlert& alert);
}; 