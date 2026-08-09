import React from 'react';

export default function SafetyPanel({ data }) {
  if (!data) return null;

  const issues = data.issues || [];
  const missing = data.missing_information || [];
  const confidence = data.recommendation?.confidence || 'LOW';
  const requiresReview = data.review_required;

  const unverified = issues.filter(i => i.type === 'UNVERIFIED_EXTRACTION');
  const otherIssues = issues.filter(i => i.type !== 'UNVERIFIED_EXTRACTION');

  const getConfidenceColor = (conf) => {
    if (conf === 'HIGH') return 'text-success';
    if (conf === 'MEDIUM') return 'text-warning';
    return 'text-danger';
  };

  return (
    <section className="rounded-card border border-line bg-white p-6 shadow-card">
      <h3 className="text-lg font-bold text-primary mb-4">Safety & Review Status</h3>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-fog rounded-lg p-4 text-center">
          <div className="text-xs font-bold uppercase text-muted mb-1">Evidence Coverage</div>
          <div className="text-xl font-bold text-primary">{data.evidence?.length || 0} Docs</div>
        </div>
        <div className="bg-fog rounded-lg p-4 text-center">
          <div className="text-xs font-bold uppercase text-muted mb-1">Overall Confidence</div>
          <div className={`text-xl font-bold ${getConfidenceColor(confidence)}`}>{confidence}</div>
        </div>
      </div>

      <div className="space-y-2 text-sm mb-4">
        <div className="flex justify-between items-center">
          <span className="text-muted">Unresolved Conflicts:</span>
          <span className="font-bold text-danger">{issues.length}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-muted">Missing Requirements:</span>
          <span className="font-bold text-warning">{missing.length}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-muted">Unverified Extractions:</span>
          <span className="font-bold text-danger">{unverified.length}</span>
        </div>
      </div>

      {unverified.length > 0 && (
        <div className="mb-4">
          <h4 className="font-bold text-danger flex items-center gap-2 mb-2">
            ⚠ Unverified Extractions
          </h4>
          <p className="text-xs text-muted mb-2">
            The AI extracted these values but they could not be confirmed in the source
            document. They are flagged separately from verified facts and missing data.
          </p>
          {unverified.map((item, i) => (
            <div key={i} className="border-l-4 border-danger bg-danger/5 p-3 mb-2 rounded-r-md">
              <p className="text-sm text-ink">{item.message}</p>
            </div>
          ))}
        </div>
      )}

      {otherIssues.length > 0 && (
        <div className="mb-4">
          <h4 className="font-bold text-warning flex items-center gap-2 mb-2">Other Issues</h4>
          {otherIssues.map((item, i) => (
            <div key={i} className="border-l-4 border-warning bg-warning/5 p-3 mb-2 rounded-r-md">
              <p className="text-sm text-ink">{item.message}</p>
            </div>
          ))}
        </div>
      )}

      {requiresReview && (
        <div className="border-l-4 border-warning bg-warning/5 p-4 rounded-r-md">
          <h4 className="font-bold text-warning flex items-center gap-2">
            ⚠ Human Review Required
          </h4>
          <p className="text-sm text-ink mt-1">
            The system requires human verification before proceeding with this recommendation.
          </p>
          <div className="mt-4 flex gap-2">
            <button className="px-4 py-2 bg-success text-white text-xs font-bold rounded-md hover:bg-success/90">
              Approve Recommendation
            </button>
            <button className="px-4 py-2 bg-danger text-white text-xs font-bold rounded-md hover:bg-danger/90">
              Reject Recommendation
            </button>
          </div>
        </div>
      )}
    </section>
  );
}