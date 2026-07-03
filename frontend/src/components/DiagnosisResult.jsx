export default function DiagnosisResult({ resultText, symptoms, onReset }) {
  // Extract severity
  const severityMatch = resultText.match(/SEVERITY:\s*(LOW|MEDIUM|HIGH)/i);
  const severity = severityMatch ? severityMatch[1].toUpperCase() : 'MEDIUM';
  const cleanText = resultText.replace(/SEVERITY:\s*(LOW|MEDIUM|HIGH)\n?/i, '').trim();

  const badgeClass = { LOW: 'sev-low', MEDIUM: 'sev-medium', HIGH: 'sev-high' }[severity] || 'sev-medium';
  const badgeIcon = { LOW: '●', MEDIUM: '◆', HIGH: '▲' }[severity] || '◆';

  const renderMarkdown = (text) => {
    return text
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/##\s+(.+)/g, '<h2>$1</h2>')
      .replace(/###\s+(.+)/g, '<h3>$1</h3>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/^[-•]\s+(.+)$/gm, '<li>$1</li>')
      .replace(/(<li>[\s\S]*?<\/li>)(?!\s*<li>)/g, '<ul>$1</ul>')
      .replace(/\n{2,}/g, '</p><p>')
      .replace(/\n/g, '<br>');
  };

  const htmlContent = renderMarkdown(cleanText);
  const now = new Date();
  const timeStr = now.toLocaleTimeString();

  return (
    <div className="result-card" style={{ display: 'block' }}>
      <div className="result-header">
        <div>
          <div className="result-title">AI Diagnostic Report</div>
          <div className="result-meta">
            Generated {timeStr} · {symptoms.length} symptom{symptoms.length !== 1 ? 's' : ''} analyzed
          </div>
        </div>
        <div>
          <span className={`severity-badge ${badgeClass}`}>
            {badgeIcon} {severity} urgency
          </span>
        </div>
      </div>
      <div className="result-body">
        <div className="ai-content" dangerouslySetInnerHTML={{ __html: htmlContent }}></div>
      </div>
      <div className="result-footer">
        <div className="footer-disclaimer">
          ⚕ This analysis is AI-generated for educational purposes only — not a substitute for professional medical advice.
        </div>
        <button className="new-btn" onClick={onReset}>+ New Assessment</button>
      </div>
    </div>
  );
}
