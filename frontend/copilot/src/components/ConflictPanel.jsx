function ConflictPanel({ conflicts = [] }) {
    return (
        <section>
            <h2>⚠ Evidence Conflicts</h2>
            {conflicts.length === 0 ? (
                <p>No conflicts detected.</p>
            ) : (
                conflicts.map((conflict, index) => (
                    <div key={index} className="conflict">
                        <h3>{conflict.field}</h3>
                        <p>{conflict.explanation}</p>
                        <p>Values: {conflict.values.join(" vs ")}</p>
                        <p>Sources: {conflict.sources.join(", ")}</p>
                    </div>
                ))
            )}
        </section>
    );
}
export default ConflictPanel;