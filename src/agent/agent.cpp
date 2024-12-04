#include <memory>
#include <unordered_set>
#include <string>
#include <iostream>
#include <thread>
#include <chrono>
#include "types.hpp"
#include "data_collector.hpp"
#include "network_manager.hpp"
#include "encryption_service.hpp"
#include "command_executor.hpp"
#include "ids/ids_engine.hpp"
#include "xdr/correlation_engine.hpp"
#include "threat_intel/threat_intelligence.hpp"

class SecurityAgent {
private:
    std::unique_ptr<DataCollector> collector;
    std::unique_ptr<NetworkManager> network;
    std::unique_ptr<EncryptionService> encryption;
    std::unique_ptr<CommandExecutor> cmdExecutor;
    std::unique_ptr<IDSEngine> ids;
    std::unique_ptr<CorrelationEngine> xdr;
    std::unique_ptr<ThreatIntelligence> threatIntel;
    
    // Command whitelist for security
    const std::unordered_set<std::string> ALLOWED_COMMANDS = {
        "netstat", "tasklist", "systeminfo", "ipconfig",
        "dir", "ping", "tracert", "route", "arp"
    };

public:
    void initialize() {
        // Initialize all components
        collector = std::make_unique<DataCollector>();
        network = std::make_unique<NetworkManager>();
        encryption = std::make_unique<EncryptionService>();
        cmdExecutor = std::make_unique<CommandExecutor>();
        ids = std::make_unique<IDSEngine>();
        xdr = std::make_unique<CorrelationEngine>();
        threatIntel = std::make_unique<ThreatIntelligence>();

        // Start monitoring
        startMonitoring();
    }

private:
    void startMonitoring() {
        // Start IDS monitoring
        ids->startMonitoring();
        
        // Start XDR correlation
        xdr->startCorrelation();
        
        // Start threat intel updates
        threatIntel->startUpdates();
        
        // Start command listener
        startCommandListener();
    }
    
    void startCommandListener() {
        network->onCommandReceived([this](const Command& cmd) {
            if (validateCommand(cmd)) {
                auto result = executeCommand(cmd);
                sendCommandResponse(result);
            }
        });
    }

private:
    bool validateCommand(const Command& cmd) {
        return ALLOWED_COMMANDS.find(cmd.baseCommand) != ALLOWED_COMMANDS.end() && 
               validateSignature(cmd.signature);
    }
    
    CommandResult executeCommand(const Command& cmd) {
        return cmdExecutor->execute(cmd);
    }
    
    void sendCommandResponse(const CommandResult& result) {
        auto encrypted = encryption->encryptData(result);
        network->sendToServer(encrypted);
    }
    
    bool validateSignature(const std::string& signature) {
        return encryption->validateSignature(signature);
    }
};

int main() {
    try {
        std::cout << "Starting Security Agent..." << std::endl;
        
        SecurityAgent agent;
        std::cout << "Initializing components..." << std::endl;
        agent.initialize();
        
        std::cout << "Agent running. Press Ctrl+C to exit." << std::endl;
        
        // Keep the program running
        using namespace std::chrono_literals;
        while (true) {
            std::this_thread::sleep_for(1s);
        }
        
        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
} 