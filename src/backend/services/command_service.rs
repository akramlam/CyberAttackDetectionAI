pub struct CommandService {
    agent_manager: Arc<AgentManager>,
    audit_logger: Arc<AuditLogger>,
}

impl CommandService {
    pub async fn execute_command(&self, request: CommandRequest) -> Result<CommandResponse> {
        // Validate user permissions
        self.validate_user_permissions(&request.user_id, &request.command)?;
        
        // Create signed command
        let signed_command = self.create_signed_command(&request.command);
        
        // Send to specific agent
        let response = self.agent_manager
            .send_command(request.agent_id, signed_command)
            .await?;
            
        // Log command execution
        self.audit_logger.log_command_execution(&request, &response);
        
        Ok(response)
    }
    
    fn validate_user_permissions(&self, user_id: &UserId, command: &str) -> Result<()> {
        // Check user permissions against command type
        if !self.permission_manager.can_execute_command(user_id, command) {
            return Err(Error::PermissionDenied);
        }
        Ok(())
    }
} 