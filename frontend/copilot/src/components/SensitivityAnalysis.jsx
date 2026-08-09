function SensitivityAnalysis({ data = {} }) {
    const scenarios = Object.entries(data);
    if (!scenarios.length) return null;

    return (
        <section>
            <h2>Ranking Sensitivity</h2>
            {scenarios.map(([scenario, suppliers]) => (
                <div key={scenario} style={{ marginBottom: "1rem" }}>
                    <h3 style={{ textTransform: "Capitalize" }}>{scenario}</h3>
                    <ol>
                        {suppliers.map((sup) => (
                            <li key={sup.supplier}>
                                {sup.supplier} — Score: {sup.score}
                            </li>
                        ))}
                    </ol>
                </div>
            ))}
        </section>
    );
}
export default SensitivityAnalysis;