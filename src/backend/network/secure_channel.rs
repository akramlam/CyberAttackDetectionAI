pub struct SecureChannel {
    pub fn establish_connection(&self) -> Result<Channel> {
        // Setup TLS 1.3 with mutual authentication
        let config = ServerConfig::builder()
            .with_safe_defaults()
            .with_client_cert_verifier(self.cert_verifier.clone())
            .with_single_cert(self.certificates.clone(), self.private_key.clone())?;
            
        Ok(Channel::new(config))
    }
} 