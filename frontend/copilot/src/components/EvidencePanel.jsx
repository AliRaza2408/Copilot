function EvidencePanel({ evidence = [] }) {
    if (!evidence.length) return null;
    return (
        <section>
            <h2>Evidence</h2>
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