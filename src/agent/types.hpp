#pragma once

#include <string>
#include <vector>
#include <chrono>

// Basic command types
struct Command {
    std::string baseCommand;
    std::string arguments;
    std::string signature;
};

struct CommandResult {
    std::string output;
    int exitCode;
    std::string error;
};

// Network monitoring types
struct NetworkPacket {
    std::vector<uint8_t> data;
    std::string sourceIP;
    std::string destIP;
    uint16_t sourcePort;
    uint16_t destPort;
    std::string protocol;
};

// Logging types
struct LogEntry {
    std::string timestamp;
    std::string source;
    std::string message;
    int severity;
};

// Security event types
struct SecurityEvent {
    std::string id;
    std::string type;
    std::string description;
    int severity;
    std::chrono::system_clock::time_point timestamp;
    
    bool operator<(const SecurityEvent& other) const {
        return timestamp < other.timestamp;
    }
};

struct IntrusionAlert {
    std::string id;
    std::string description;
    int severity;
    std::string source;
};

struct Indicator {
    std::string type;
    std::string value;
    std::string source;
};

struct Threat {
    std::string id;
    std::string name;
    int severity;
    std::vector<SecurityEvent> relatedEvents;
}; 