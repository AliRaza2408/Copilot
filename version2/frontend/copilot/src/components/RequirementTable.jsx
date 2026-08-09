function RequirementTable({ requirements = [] }) {
    if (!requirements.length) return null;
    return (
        <section>
            <h2>Product Requirements</h2>
            <table>
                <thead>
                    <tr>
                        <th>Requirement</th>
                        <th>Operator</th>
                        <th>Required</th>
                        <th>Mandatory</th>
                    </tr>
                </thead>
                <tbody>
                    {requirements.map((req, index) => (
                        <tr key={index}>
                            <td>{req.name}</td>
                            <td>{req.operator}</td>
                            <td>{req.required_value}</td>
                            <td>{req.mandatory ? "Yes" : "No"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}
export default RequirementTable;