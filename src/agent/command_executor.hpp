#include <windows.h>
#include <string>
#include <sstream>
#include "types.hpp"

class CommandExecutor {
private:
    SECURITY_ATTRIBUTES securityAttributes;
    
public:
    CommandExecutor() {
        securityAttributes.nLength = sizeof(SECURITY_ATTRIBUTES);
        securityAttributes.bInheritHandle = TRUE;
        securityAttributes.lpSecurityDescriptor = NULL;
    }

    CommandResult execute(const Command& cmd) {
        HANDLE hPipeRead, hPipeWrite;
        CreatePipe(&hPipeRead, &hPipeWrite, &securityAttributes, 0);
        
        STARTUPINFOA si = {0};
        PROCESS_INFORMATION pi = {0};
        si.cb = sizeof(STARTUPINFOA);
        si.hStdError = hPipeWrite;
        si.hStdOutput = hPipeWrite;
        si.dwFlags |= STARTF_USESTDHANDLES;
        
        std::string cmdLine = buildSecureCommandLine(cmd);
        
        CreateProcessA(
            NULL,
            (LPSTR)cmdLine.c_str(),
            NULL,
            NULL,
            TRUE,
            CREATE_NO_WINDOW,
            NULL,
            NULL,
            &si,
            &pi
        );

        CloseHandle(hPipeWrite);
        
        CommandResult result;
        char buffer[4096];
        DWORD bytesRead;
        std::stringstream output;
        
        while (ReadFile(hPipeRead, buffer, sizeof(buffer), &bytesRead, NULL) && bytesRead > 0) {
            output.write(buffer, bytesRead);
        }
        
        DWORD exitCode;
        GetExitCodeProcess(pi.hProcess, &exitCode);
        
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        CloseHandle(hPipeRead);
        
        result.output = output.str();
        result.exitCode = exitCode;
        return result;
    }
    
private:
    std::string buildSecureCommandLine(const Command& cmd) {
        // Basic command sanitization - remove dangerous characters
        auto sanitize = [](const std::string& input) {
            std::string safe;
            for (char c : input) {
                if (isalnum(c) || c == ' ' || c == '-' || c == '/' || c == '.' || c == ':') {
                    safe += c;
                }
            }
            return safe;
        };
        
        return sanitize(cmd.baseCommand + " " + cmd.arguments);
    }
}; 