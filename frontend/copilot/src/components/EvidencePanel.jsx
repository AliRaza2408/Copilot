function EvidencePanel({ evidence = [], suppliers = [] }) {
    if (!evidence.length && !suppliers.length) return null;
    return (
        <section>
            <h2>Evidence</h2>

            {suppliers.length > 0 && (
                <div className="mb-6">
                    <h3>Extraction Verification</h3>
                    <p className="text-sm text-muted mb-2">
                        Each supplier field is checked against the source text. Values the AI
                        could not confirm in the document are flagged rather than presented as fact.
                    </p>
                    {suppliers.map((sup, i) => (
                        <div key={i} className="border border-line rounded-md p-3 mb-3">
                            <strong>{sup.name}</strong>
                            <ul className="mt-2 space-y-1">
                                {Object.entries(sup.verification_status || {}).map(([field, status]) => (
                                    <li key={field} className="text-sm flex items-center gap-2">
                                        {status === 'VERIFIED' ? (
                                            <span className="text-success font-bold">✓</span>
                                        ) : (
                                            <span className="text-danger font-bold">⚠</span>
                                        )}
                                        <span className="text-ink">{field.replace(/_/g, ' ')}</span>
                                        {status === 'VERIFIED' ? (
                                            <span className="text-success text-xs font-bold">Verified in source</span>
                                        ) : (
                                            <span className="text-danger text-xs font-bold">
                                                Unverified — not confirmed in source
                                            </span>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            )}

            {evidence.map((item, index) => (
                <div key={index}>
                    <strong>{item.source}</strong>
                    <p>Page: {item.page}</p>
                    <p>{item.text}</p>
                </div>
            ))}
        </section>
    );
}
export default EvidencePanel;
