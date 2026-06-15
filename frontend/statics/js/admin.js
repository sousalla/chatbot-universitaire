// Admin dashboard functionality

document.addEventListener('DOMContentLoaded', async () => {
    await loadSystemStatus();
    
    // Refresh every 30 seconds
    setInterval(loadSystemStatus, 30000);
});

async function loadSystemStatus() {
    try {
        const status = await API.getStatus();
        
        if (status) {
            // LLM Status
            const llmStatus = document.getElementById('llmStatus');
            if (status.llm_loaded) {
                llmStatus.innerHTML = '<span class="text-success">✅ Actif</span>';
                document.getElementById('llmName').innerHTML = status.llm_info?.name || 'Gemma 2B';
                document.getElementById('deviceStatus').innerHTML = status.llm_info?.device || 'CPU';
            } else {
                llmStatus.innerHTML = '<span class="text-danger">❌ Inactif</span>';
            }
            
            // Vector Store
            const vectorStatus = document.getElementById('vectorStatus');
            if (status.vector_store_ready) {
                vectorStatus.innerHTML = '<span class="text-success">✅ Prêt</span>';
                document.getElementById('docCount').innerHTML = `${status.documents_count || 0} documents`;
            } else {
                vectorStatus.innerHTML = '<span class="text-warning">⚠️ Non initialisé</span>';
            }
        }
        
        // Conversations count
        const history = await API.getHistory();
        document.getElementById('convCount').innerHTML = history.length || 0;
        
    } catch (error) {
        console.error('Error loading status:', error);
    }
}