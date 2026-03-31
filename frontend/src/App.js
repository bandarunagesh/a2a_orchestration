import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('');
  const [agents, setAgents] = useState([
    { name: 'Startup', status: 'idle' },
    { name: 'Conduct', status: 'idle' },
    { name: 'Closeout', status: 'idle' },
    { name: 'Regulatory', status: 'idle' },
    { name: 'Analyst', status: 'idle' },
    { name: 'Insights', status: 'idle' },
    { name: 'Forecasting', status: 'idle' },
    { name: 'Report Builder', status: 'idle' },
    { name: 'Dashboard Creator', status: 'idle' },
    { name: 'ETL Orchestrator', status: 'idle' },
    { name: 'Data Profiler', status: 'idle' },
    { name: 'Notifications', status: 'idle' },
  ]);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8001/query', { query });
      setStatus(response.data.status);
      // Simulate updating agent statuses
      setAgents(agents.map(agent => ({ ...agent, status: 'processing' })));
    } catch (error) {
      setStatus('Error: ' + error.message);
    }
  };

  useEffect(() => {
    // Polling for agent statuses (simplified)
    const interval = setInterval(() => {
      // In real app, fetch from orchestrator or agents
      setAgents(prev => prev.map(agent => ({ ...agent, status: Math.random() > 0.5 ? 'completed' : 'processing' })));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Ecosystem Dashboard</h1>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter query"
        style={{ width: '300px', padding: '10px', marginRight: '10px' }}
      />
      <button onClick={handleSubmit} style={{ padding: '10px' }}>Submit</button>
      <p>Status: {status}</p>
      
      <h2>Agent Status</h2>
      <ul>
        {agents.map((agent, index) => (
          <li key={index}>{agent.name}: {agent.status}</li>
        ))}
      </ul>
      
      <h2>Message Bus Transitions</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '200px', overflowY: 'scroll' }}>
        {/* Placeholder for transitions log */}
        <p>Transitions will be logged here...</p>
      </div>
    </div>
  );
}

export default App;