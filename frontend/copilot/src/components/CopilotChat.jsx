import React, { useState } from 'react';
import { askCopilot } from '../services/api';
import { Bot, Send, FileText, Loader2 } from 'lucide-react';

export default function CopilotChat() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');

  const handleAsk = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const data = await askCopilot(question);
      setResponse(data);
    } catch {
      setError('Could not connect to the AI Copilot.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-card border border-line bg-white p-6 shadow-card">
      <h3 className="text-lg font-bold text-primary mb-4 flex items-center gap-2">
        <Bot className="h-5 w-5 text-accent" />
        Ask Manufacturing Copilot
      </h3>
      
      <div className="flex gap-4 mb-6">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about the decision... (e.g., Why was Supplier B rejected?)"
          className="flex-1 rounded-lg border border-line bg-fog px-4 py-3 text-sm text-ink focus:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-accent px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-accent/90 disabled:opacity-50"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

      {error && <p className="text-sm font-medium text-danger">{error}</p>}

      {response && (
        <div className="space-y-6">
          {/* Facts & Recommendation */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="bg-fog rounded-lg p-4">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-2">Verified Facts</h4>
              <ul className="space-y-2 text-sm text-ink list-disc pl-4">
                {response.answer.facts?.map((fact, i) => <li key={i}>{fact}</li>)}
              </ul>
            </div>
            
            <div className="bg-fog rounded-lg p-4">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-2">Recommendation</h4>
              <p className="text-sm font-medium text-primary">{response.answer.recommendation}</p>
              
              {response.answer.assumptions?.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-warning mb-2">Assumptions</h4>
                  <ul className="space-y-1 text-xs text-muted list-disc pl-4">
                    {response.answer.assumptions.map((a, i) => <li key={i}>{a}</li>)}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Citations */}
          <div className="border-t border-line pt-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-3">Evidence Citations</h4>
            <div className="flex flex-wrap gap-3">
              {response.answer.citations?.map((cite, i) => (
                <div key={i} className="flex items-center gap-2 rounded-md border border-line bg-mist px-3 py-2 text-xs font-medium text-ink">
                  <FileText className="h-4 w-4 text-muted" />
                  <span>{cite.source}</span>
                  {cite.page && <span className="text-muted">— Page {cite.page}</span>}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}