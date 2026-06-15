// API Service for UniBot

const API = {
    // Base URL
    baseUrl: '',
    
    // Send message
    async sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Get history
    async getHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error loading history:', error);
            return [];
        }
    },
    
    // Clear history
    async clearHistory() {
        try {
            const response = await fetch('/api/clear', { method: 'POST' });
            return response.ok;
        } catch (error) {
            console.error('Error clearing history:', error);
            return false;
        }
    },
    
    // Get system status
    async getStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting status:', error);
            return null;
        }
    },
    
    // Health check
    async healthCheck() {
        try {
            const response = await fetch('/api/health');
            return response.ok;
        } catch (error) {
            return false;
        }
    }
};