#include "ids_engine.hpp"

IDSEngine::IDSEngine() {
    networkMonitor = std::make_unique<NetworkMonitor>();
    logAnalyzer = std::make_unique<LogAnalyzer>();
}

void IDSEngine::analyzeTraffic(const NetworkPacket& packet) {
    // Implement traffic analysis
}

void IDSEngine::analyzeLogs(const LogEntry& log) {
    // Implement log analysis
} 