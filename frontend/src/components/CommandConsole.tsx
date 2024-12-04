export const CommandConsole: React.FC = () => {
    const [command, setCommand] = useState('');
    const [output, setOutput] = useState<CommandOutput[]>([]);
    const [loading, setLoading] = useState(false);
    
    const executeCommand = async () => {
        try {
            setLoading(true);
            const response = await commandService.executeCommand({
                command,
                agentId: selectedAgent,
                timestamp: new Date().toISOString()
            });
            
            setOutput(prev => [...prev, {
                command,
                output: response.output,
                timestamp: new Date().toISOString(),
                status: response.status
            }]);
            
        } catch (error) {
            console.error('Command execution failed:', error);
            notificationService.error('Failed to execute command');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card>
            <CardHeader title="Command Console" />
            <CardContent>
                <TextField
                    fullWidth
                    value={command}
                    onChange={(e) => setCommand(e.target.value)}
                    placeholder="Enter command..."
                    InputProps={{
                        endAdornment: (
                            <IconButton 
                                onClick={executeCommand}
                                disabled={loading}
                            >
                                <SendIcon />
                            </IconButton>
                        )
                    }}
                />
                <CommandOutput output={output} />
            </CardContent>
        </Card>
    );
}; 