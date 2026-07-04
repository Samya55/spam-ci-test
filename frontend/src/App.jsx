import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/history`);
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to fetch history', error);
    }
  };

  const handlePredict = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, { text });
      setResult(response.data);
      // Prepend to history for immediate feedback
      setHistory([response.data, ...history]);
    } catch (error) {
      console.error('Prediction failed', error);
      alert('Failed to get prediction from server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', width: '100%' }}>
      <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
          Spam Detection AI
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Powered by Scikit-learn and FastAPI
        </p>
      </header>

      <main className="glass-panel" style={{ marginBottom: '2rem' }}>
        <textarea
          className="input-area"
          placeholder="Paste an SMS or email message here to analyze..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button 
          className={`btn-primary ${loading ? 'loading' : ''}`}
          onClick={handlePredict}
          disabled={loading || !text.trim()}
        >
          {loading ? 'Analyzing...' : 'Predict'}
        </button>

        {result && (
          <div style={{
            marginTop: '2rem',
            padding: '1.5rem',
            borderRadius: '12px',
            background: result.prediction === 'Spam' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
            border: `1px solid ${result.prediction === 'Spam' ? 'var(--danger)' : 'var(--success)'}`,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <h2 style={{ fontSize: '1.5rem', marginBottom: '0.25rem', color: result.prediction === 'Spam' ? 'var(--danger)' : 'var(--success)' }}>
                {result.prediction.toUpperCase()}
              </h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                Confidence Score: {(result.confidence * 100).toFixed(2)}%
              </p>
            </div>
            <div style={{ fontSize: '2.5rem' }}>
              {result.prediction === 'Spam' ? '🚨' : '✅'}
            </div>
          </div>
        )}
      </main>

      <section className="glass-panel">
        <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Prediction History</h3>
        {history.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No recent predictions.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {history.map((item) => (
              <div key={item.id} style={{
                background: 'rgba(0,0,0,0.2)',
                padding: '1rem',
                borderRadius: '8px',
                borderLeft: `4px solid ${item.prediction === 'Spam' ? 'var(--danger)' : 'var(--success)'}`
              }}>
                <p style={{ marginBottom: '0.5rem', fontSize: '0.95rem' }}>"{item.text}"</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <span>{item.prediction} ({(item.confidence * 100).toFixed(1)}%)</span>
                  <span>{new Date(item.timestamp).toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
