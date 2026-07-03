import { useState } from 'react';

const QUICK_SYMPTOMS = [
  'Fever','Headache','Cough','Fatigue','Nausea','Vomiting',
  'Chest pain','Shortness of breath','Sore throat','Runny nose',
  'Body aches','Dizziness','Rash','Diarrhea','Joint pain',
  'Loss of appetite','Chills','Sweating','Insomnia','Blurred vision'
];

export default function SymptomForm({ onAnalyze }) {
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('');
  const [duration, setDuration] = useState('');
  const [notes, setNotes] = useState('');
  const [symptoms, setSymptoms] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleAddSymptom = (name) => {
    const clean = name.trim();
    if (!clean || symptoms.includes(clean)) return;
    setSymptoms([...symptoms, clean]);
  };

  const handleRemoveSymptom = (name) => {
    setSymptoms(symptoms.filter(s => s !== name));
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSymptom(inputValue);
      setInputValue('');
    }
  };

  const submitAnalysis = () => {
    if (symptoms.length === 0) {
      alert('Please add at least one symptom before analyzing.');
      return;
    }
    onAnalyze({ age, sex, duration, symptoms, notes });
  };

  return (
    <div id="form-section">
      <div className="main-grid">

        <div className="card">
          <div className="card-label">Patient Age</div>
          <input 
            type="number" 
            placeholder="e.g. 28" 
            min="1" max="120" 
            value={age}
            onChange={e => setAge(e.target.value)}
          />
        </div>

        <div className="card">
          <div className="card-label">Biological Sex</div>
          <select value={sex} onChange={e => setSex(e.target.value)}>
            <option value="">Select...</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other / Prefer not to say</option>
          </select>
        </div>

        <div className="card" style={{ gridColumn: '1/-1' }}>
          <div className="card-label">Duration of Symptoms</div>
          <select value={duration} onChange={e => setDuration(e.target.value)}>
            <option value="">Select duration...</option>
            <option>Less than 24 hours</option>
            <option>1–3 days</option>
            <option>4–7 days</option>
            <option>1–2 weeks</option>
            <option>More than 2 weeks</option>
            <option>Chronic / Ongoing</option>
          </select>
        </div>

        <div className="card" style={{ gridColumn: '1/-1' }}>
          <div className="card-label">Symptoms</div>
          <div className="tag-container">
            {symptoms.map(s => (
              <span key={s} className="tag">
                {s} 
                <button className="tag-remove" onClick={() => handleRemoveSymptom(s)}>×</button>
              </span>
            ))}
          </div>
          <div className="symptom-input-row">
            <input 
              type="text" 
              placeholder="Type a symptom and press Enter or +" 
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyDown={handleInputKeyDown}
            />
            <button className="add-btn" onClick={() => { handleAddSymptom(inputValue); setInputValue(''); }}>+</button>
          </div>
          <div className="quick-chips">
            {QUICK_SYMPTOMS.map(s => (
              <button key={s} className="chip" onClick={() => handleAddSymptom(s)}>{s}</button>
            ))}
          </div>
        </div>

        <div className="card" style={{ gridColumn: '1/-1' }}>
          <div className="card-label">Additional Notes</div>
          <textarea 
            placeholder="Any other relevant details: medical history, medications, allergies, recent travel, severity scale 1–10, etc."
            value={notes}
            onChange={e => setNotes(e.target.value)}
          ></textarea>
        </div>

      </div>

      <button className="analyze-btn" onClick={submitAnalysis}>
        <span className="btn-shimmer"></span>
        🔍 Analyze Symptoms with AI
      </button>
    </div>
  );
}
