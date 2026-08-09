import React, { useState } from 'react';
import CopilotChat from './CopilotChat';
import { submitHumanReview } from '../services/api';
import { RotateCcw, Trophy, Check, X, AlertTriangle, AlertCircle } from 'lucide-react';

export default function ResultsDashboard({ data, onReset }) {
  const [reviewStatus, setReviewStatus] = useState(null);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectReason, setRejectReason] = useState("");

  if (!data) return null;

  const getEligibilityBadge = (status) => {
    if (status === 'ELIGIBLE') return 'bg-success/10 text-success ring-success/15';
    if (status === 'INELIGIBLE') return 'bg-danger/10 text-danger ring-danger/15';
    if (status === 'REQUIRES_REVIEW') return 'bg-warning/10 text-warning ring-warning/15';
    return 'bg-mist text-muted ring-waiting/15';
  };

  const getRiskBadge = (risk) => {
    if (risk === 'LOW') return 'bg-success/10 text-success';
    if (risk === 'MEDIUM') return 'bg-warning/10 text-warning';
    return 'bg-danger/10 text-danger';
  };

  const recommendation = data.recommendation;
  const topEval = data.evaluations?.find(e => e.supplier === recommendation?.supplier);

  const handleReview = async (status) => {
    try {
      await submitHumanReview(data.case_id, status);
      setReviewStatus(status);
    } catch (err) {
      console.error("Review failed", err);
    }
  };

  const handleRejectSubmit = async () => {
    try {
      await submitHumanReview(data.case_id, "REJECTED", rejectReason);
      setReviewStatus("REJECTED");
      setShowRejectModal(false);
    } catch (err) {
      console.error("Reject failed", err);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      
      {/* Header & Reset */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-extrabold text-primary">Supplier Shortlist Analysis</h2>
        <button 
          onClick={onReset}
          className="inline-flex items-center gap-2 rounded-lg border border-line bg-white px-4 py-2 text-sm font-semibold text-secondary transition-colors hover:bg-mist"
        >
          <RotateCcw className="h-4 w-4" /> Analyze New Pack
        </button>
      </div>

      {/* Executive Result Card */}
      <section className="rounded-card border border-line bg-white p-8 shadow-card">
        <div className="text-xs font-bold uppercase tracking-[0.08em] text-secondary mb-2">
          Executive Recommendation
        </div>
        {recommendation ? (
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h3 className="text-3xl font-extrabold text-primary flex items-center gap-3">
                <Trophy className="h-8 w-8 text-warning" />
                {recommendation.supplier}
              </h3>
              <div className="mt-3 flex flex-wrap gap-4 text-sm font-medium">
                <span className="inline-block rounded-md px-2 py-1 text-xs font-bold ring-2 ring-inset bg-success/10 text-success ring-success/15">
                  ELIGIBLE
                </span>
                <span className="flex items-center gap-1 text-muted">Confidence: <span className="text-accent font-bold">{recommendation.confidence}</span></span>
                <span className="flex items-center gap-1 text-muted">Requirements Met: <span className="text-ink font-bold">{topEval?.requirements_met || 'N/A'}</span></span>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <h3 className="text-xl font-bold text-danger">No Eligible Suppliers Found</h3>
            <p className="text-sm text-muted mt-1">All suppliers failed mandatory constraints or require human review.</p>
          </div>
        )}
      </section>

      {/* Supplier Comparison Table */}
      <section className="rounded-card border border-line bg-white p-6 shadow-card">
        <h3 className="text-lg font-bold text-primary mb-4">Supplier Comparison</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-line text-left text-muted">
                <th className="pb-3 font-semibold">Supplier</th>
                <th className="pb-3 font-semibold">Eligibility</th>
                <th className="pb-3 font-semibold">Requirements</th>
                <th className="pb-3 font-semibold">Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {data.evaluations?.map((sup, i) => (
                <tr key={i} className="border-b border-line/50 last:border-0">
                  <td className="py-3 font-medium text-ink">{sup.supplier}</td>
                  <td className="py-3">
                    <span className={`inline-block rounded-md px-2 py-1 text-xs font-bold ring-2 ring-inset ${getEligibilityBadge(sup.eligibility)}`}>
                      {sup.eligibility?.replace('_', ' ') || 'UNKNOWN'}
                    </span>
                  </td>
                  <td className="py-3 text-muted">{sup.requirements_met || 'N/A'}</td>
                  <td className="py-3">
                    <span className={`inline-block rounded-md px-2 py-1 text-xs font-bold ${getRiskBadge(sup.risk_level)}`}>
                      {sup.risk_level || 'HIGH'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Mandatory Constraint Details (For Top Supplier) */}
      {topEval && (
        <section className="rounded-card border border-line bg-white p-6 shadow-card">
          <h3 className="text-lg font-bold text-primary mb-1">Mandatory Constraint Analysis</h3>
          <p className="text-sm text-muted mb-4">Detailed breakdown for <span className="font-semibold text-ink">{topEval.supplier}</span></p>
          
          <div className="space-y-3">
            {topEval.constraints?.map((con, i) => (
              <div key={i} className="flex items-center justify-between border-b border-line/50 pb-2 last:border-0">
                <div className="flex items-center gap-3">
                  <span className={`h-2 w-2 rounded-full ${con.status === 'PASS' ? 'bg-success' : con.status === 'FAIL' ? 'bg-danger' : 'bg-warning'}`}></span>
                  <span className="text-sm font-medium text-ink">{con.requirement_name}</span>
                </div>
                <div className="flex items-center gap-6 text-xs text-muted">
                  <span className="font-bold text-ink">{con.status}</span>
                  <span className="w-20 text-right">Page {con.location?.replace('Page ', '') || '?'}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Sensitivity Analysis */}
      {Object.keys(data.sensitivity_analysis || {}).length > 0 && (
        <section className="rounded-card border border-line bg-white p-6 shadow-card">
          <h3 className="text-lg font-bold text-primary mb-1">Sensitivity Analysis</h3>
          <p className="text-sm text-muted mb-4">How ranking changes when business priorities shift.</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {Object.entries(data.sensitivity_analysis).map(([scenario, suppliers]) => (
              <div key={scenario} className="bg-fog rounded-lg p-4 border border-line/50">
                <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-3 capitalize">
                  {scenario.replace('_', ' ')}
                </h4>
                <ol className="space-y-2">
                  {suppliers.map((sup, i) => (
                    <li key={i} className="flex justify-between items-center text-sm">
                      <span className="font-medium text-ink">
                        {i + 1}. {sup.supplier}
                      </span>
                      <span className="text-xs text-muted font-mono">{sup.score}</span>
                    </li>
                  ))}
                </ol>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Safety & Conflict Panels */}
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
        <section className="rounded-card border border-line bg-white p-6 shadow-card">
          <h3 className="text-lg font-bold text-danger mb-4 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" /> Evidence Conflicts
          </h3>
          {data.conflicts?.length > 0 ? (
            data.conflicts.map((conf, i) => (
              <div key={i} className="border-l-4 border-danger bg-danger/5 p-4 mb-3">
                <h4 className="font-bold text-ink text-sm">{conf.type?.replace('_', ' ')}</h4>
                <p className="text-sm text-muted mt-1">{conf.message}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted">No conflicts detected.</p>
          )}
        </section>

        <section className="rounded-card border border-line bg-white p-6 shadow-card">
          <h3 className="text-lg font-bold text-warning mb-4 flex items-center gap-2">
            <AlertCircle className="h-5 w-5" /> Missing Information
          </h3>
          {data.missing_information?.length > 0 ? (
            data.missing_information.map((item, i) => (
              <div key={i} className="border-l-4 border-warning bg-warning/5 p-4 mb-3">
                <h4 className="font-bold text-ink text-sm">{item.requirement}</h4>
                <p className="text-sm text-muted mt-1">{item.message}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted">No missing information.</p>
          )}
        </section>
      </div>

      {/* AI Copilot (Facts / Assumptions / Recommendation) */}
      <CopilotChat />

      {/* Human Review Boundary */}
      <section className="rounded-card border-2 border-warning bg-warning/5 p-6 text-center">
        <h3 className="text-lg font-bold text-warning mb-2 flex items-center justify-center gap-2">
          <AlertTriangle className="h-5 w-5" /> Human Review Required
        </h3>
        <p className="text-sm text-ink mb-4 max-w-xl mx-auto">
          This AI recommendation is decision support only. It does not approve suppliers or place orders. 
          Final sourcing decisions must be verified by a human procurement professional.
        </p>
        
        {reviewStatus === null ? (
          <div className="flex justify-center gap-3">
            <button 
              onClick={() => handleReview("REVIEWED")}
              className="inline-flex items-center gap-2 px-6 py-2 bg-success text-white text-sm font-bold rounded-lg hover:bg-success/90 transition-colors"
            >
              <Check className="h-4 w-4" /> Mark Reviewed
            </button>
            <button 
              onClick={() => setShowRejectModal(true)}
              className="inline-flex items-center gap-2 px-6 py-2 bg-danger text-white text-sm font-bold rounded-lg hover:bg-danger/90 transition-colors"
            >
              <X className="h-4 w-4" /> Reject Recommendation
            </button>
          </div>
        ) : reviewStatus === "REVIEWED" ? (
          <div className="text-success font-bold text-sm flex items-center justify-center gap-2">
            <Check className="h-4 w-4" /> Recommendation Reviewed by Human
          </div>
        ) : (
          <div className="text-danger font-bold text-sm flex items-center justify-center gap-2">
            <X className="h-4 w-4" /> Recommendation Rejected by Human
          </div>
        )}
      </section>

      {/* Rejection Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-card p-6 shadow-card max-w-md w-full mx-4">
            <h3 className="text-lg font-bold text-primary mb-4">Reject Recommendation</h3>
            <p className="text-sm text-muted mb-4">Please select a reason for rejection:</p>
            <select 
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              className="w-full border border-line bg-fog rounded-lg px-4 py-2 text-sm mb-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-accent/40"
            >
              <option value="">Select a reason...</option>
              <option value="Supplier information is incorrect">Supplier information is incorrect</option>
              <option value="Evidence is insufficient">Evidence is insufficient</option>
              <option value="Requirement is incorrect">Requirement is incorrect</option>
              <option value="Prefer another supplier">Prefer another supplier</option>
              <option value="Other">Other</option>
            </select>
            <div className="flex justify-end gap-3">
              <button 
                onClick={() => setShowRejectModal(false)}
                className="px-4 py-2 text-sm font-semibold text-secondary hover:bg-mist rounded-lg"
              >
                Cancel
              </button>
              <button 
                onClick={handleRejectSubmit}
                disabled={!rejectReason}
                className="px-4 py-2 bg-danger text-white text-sm font-bold rounded-lg hover:bg-danger/90 disabled:opacity-50"
              >
                Submit Rejection
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}