function SupplierTable({ suppliers = [] }) {
    if (!suppliers.length) return null;
    return (
        <section>
            <h2>Supplier Eligibility</h2>
            <table>
                <thead>
                    <tr>
                        <th>Supplier</th>
                        <th>Eligibility</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {suppliers.map((sup, index) => (
                        <tr key={index}>
                            <td>{sup.supplier}</td>
                            <td>{sup.eligibility}</td>
                            <td>{sup.score ?? "-"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}
export default SupplierTable;