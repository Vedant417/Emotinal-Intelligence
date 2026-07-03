import React, { useState, useEffect } from 'react';
import './index.css';
import MovieForm from './components/MovieForm';
import Dashboard from './components/Dashboard';

const LOADING_STEPS = [
  "Initializing CinemAI Predictor Engine...",
  "Running token scanners and semantic filters...",
  "Evaluating emotional resonance curves...",
  "Cross-referencing budget against theatrical ROI...",
  "Executing Monte Carlo success simulations..."
];

export default function App() {
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Animate loading steps sequentially
  useEffect(() => {
    let interval;
    if (loading) {
      setActiveStep(0);
      interval = setInterval(() => {
        setActiveStep(prev => {
          if (prev < LOADING_STEPS.length - 1) {
            return prev + 1;
          }
          return prev;
        });
      }, 700); // advance step every 700ms
    } else {
      setActiveStep(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleAnalyze = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `HTTP ${response.status} Error`);
      }

      const data = await response.json();
      
      // Delay setting result slightly if loading goes too fast, 
      // ensuring the user sees the cool step-by-step loading analysis animations
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      // Merge original synopsis into result so sandbox can reference it
      setResult({
        ...data,
        synopsis: formData.synopsis,
        budget: formData.budget,
        cast_star_power: formData.cast_star_power,
        genres: formData.genres,
        target_emotions: formData.target_emotions
      });
      
    } catch (err) {
      setError(err.message || "Could not connect to the analysis agent server. Please make sure the backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleReAnalyze = async (updatedData) => {
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: updatedData.title,
          synopsis: updatedData.synopsis,
          genres: updatedData.genres,
          budget: updatedData.budget,
          cast_star_power: updatedData.cast_star_power,
          target_emotions: updatedData.target_emotions
        })
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `HTTP ${response.status} Error`);
      }

      const data = await response.json();
      setResult({
        ...data,
        synopsis: updatedData.synopsis,
        budget: updatedData.budget,
        cast_star_power: updatedData.cast_star_power,
        genres: updatedData.genres,
        target_emotions: updatedData.target_emotions
      });
    } catch (err) {
      setError(err.message || "Failed to update analysis.");
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="container">
      {/* CinemAI Header */}
      <header>
        <div className="logo">
          <div className="logo-icon">🎬</div>
          <div className="logo-title">
            <h1>CinemAI</h1>
            <p>Emotion Arc & ROI Predictor</p>
          </div>
        </div>
        <div className="agent-badge">
          <span className="badge-dot"></span>
          Predictor Agent Online
        </div>
      </header>

      {/* Error Card */}
      {error && (
        <div className="glass-card mb-4" style={{ borderColor: 'var(--danger)', background: 'rgba(239, 68, 68, 0.05)', display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <span style={{ color: 'var(--danger)', fontSize: '1.25rem' }}>⚠️</span>
          <span style={{ fontSize: '0.88rem', color: 'var(--danger)' }}>{error}</span>
        </div>
      )}

      {/* Main Flow Rendering */}
      {!loading && !result && (
        <div className="studio-layout">
          <div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: '0.75rem', background: 'linear-gradient(90deg, #fff 0%, var(--accent-secondary) 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Analyze Movie Commercial Viability
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: '1.5rem' }}>
              Welcome to the CinemAI Studio. Write your film concept, define genres, configure production variables, and run our Agentic AI model to forecast screenplay emotional dynamics, audience appeal, and box office success.
            </p>
            <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '3px solid var(--accent)' }}>
              <h3 style={{ fontSize: '0.9rem', color: 'var(--accent-secondary)', marginBottom: '0.4rem' }}>Predictive Metrics</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                The agent combines semantic text analyzers with budget-revenue historical statistics to simulate critical and audience reception scores, generating clear script fixes to maximize theatrical performance.
              </p>
            </div>
          </div>
          <MovieForm onSubmit={handleAnalyze} isLoading={loading} />
        </div>
      )}

      {/* Cinematic Loading Screen */}
      {loading && (
        <div className="glass-card loading-panel">
          <div className="loading-scanner"></div>
          <h2 className="loading-title">Agent Simulating Screenplay Success</h2>
          <p className="loading-subtitle">Computing neural text weights and commercial indexes...</p>
          
          <ul className="loading-steps-list">
            {LOADING_STEPS.map((step, index) => {
              let statusClass = '';
              if (index < activeStep) statusClass = 'done';
              else if (index === activeStep) statusClass = 'active';
              
              return (
                <li key={index} className={`loading-step-item ${statusClass}`}>
                  <span className="step-indicator-dot"></span>
                  <span>{step}</span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {/* Dashboard Screen */}
      {result && !loading && (
        <Dashboard 
          data={result} 
          onReAnalyze={handleReAnalyze} 
          onReset={handleReset} 
        />
      )}

      {/* Page Footer */}
      <footer className="page-footer">
        <div className="footer-copy">
          &copy; {new Date().getFullYear()} CinemAI Agentic Studio. For development and predictive simulation purposes.
        </div>
        <div className="footer-links">
          <a href="#" className="footer-link" onClick={handleReset}>Home</a>
          <a href="https://github.com" target="_blank" rel="noreferrer" className="footer-link">Documentation</a>
        </div>
      </footer>
    </div>
  );
}
