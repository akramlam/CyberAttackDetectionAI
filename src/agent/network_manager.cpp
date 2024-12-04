#include "network_manager.hpp"
#include <iostream>
#include <thread>

void NetworkManager::onCommandReceived(std::function<void(const Command&)> callback) {
    this->commandCallback = callback;
    
    // Start a thread to simulate receiving commands
    std::thread([this]() {
        std::cout << "Network Manager started. Listening for commands..." << std::endl;
        
        // Simulate receiving a command every 5 seconds
        while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(5));
            
            Command testCmd;
            testCmd.baseCommand = "systeminfo";
            testCmd.arguments = "";
            testCmd.signature = "test";
            
            if (this->commandCallback) {
                std::cout << "Received command: " << testCmd.baseCommand << std::endl;
                this->commandCallback(testCmd);
            }
        }
    }).detach();
}

void NetworkManager::sendToServer(const std::string& data) {
    std::cout << "\nCommand output:\n" << data << std::endl;
} 