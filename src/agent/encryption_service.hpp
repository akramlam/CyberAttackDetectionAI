#pragma once
#include <string>
#include "types.hpp"

class EncryptionService {
public:
    EncryptionService() = default;
    std::string encryptData(const CommandResult& result);
    bool validateSignature(const std::string& signature);
}; 