import { useState } from "react";
import FileUpload from "../components/FileUpload";
import RequirementTable from "../components/RequirementTable";
import SupplierTable from "../components/SupplierTable";
import RecommendationCard from "../components/RecommendationCard";
import SensitivityAnalysis from "../components/SensitivityAnalysis";
import ConflictPanel from "../components/ConflictPanel";
import ReviewPanel from "../components/ReviewPanel";

function Dashboard() {
    // For now, we initialize with mock data structure. 
    // Later, this will be populated by calling evaluateDecision()
    const [data, setData] = useState(null);

    const handleUploadComplete = (result) => {
        // When upload finishes, we would normally call evaluateDecision()
        // For now, we just log it and set mock data to test UI rendering.
        console.log("Upload result:", result);
        
        // MOCK DATA TO PROVE UI WORKS:
        setData({
            requirements: [
                { name: "MOQ", operator: "<=", required_value: 1000, mandatory: true },
                { name: "Lead Time", operator: "<=", required_value: 30, mandatory: true }
            ],
            suppliers: [
                { supplier: "Supplier A", eligibility: "ELIGIBLE", score: 91.4 },
                { supplier: "Supplier B", eligibility: "INELIGIBLE", score: null },
                { supplier: "Supplier C", eligibility: "REQUIRES_REVIEW", score: null }
            ],
            recommendation: {
                supplier: "Supplier A",
                score: 91.4,
                confidence: "High"
            },
            sensitivity_analysis: {
                balanced: [{ supplier: "Supplier A", score: 91.4 }],
                speed_focused: [{ supplier: "Supplier A", score: 85.2 }]
            },
            conflicts: [
                {
                    field: "MOQ",
                    explanation: "Conflicting values found for MOQ.",
                    values: ["500", "1000"],
                    sources: ["Supplier_A.pdf", "Quotation_A.xlsx"]
                }
            ],
            review_items: [
                {
                    supplier: "Supplier C",
                    message: "Lead Time information missing."
                }
            ]
        });
    };

    return (
        <div className="dashboard">
            <header>
                <h1>AI Manufacturing Decision Copilot</h1>
                <p>Evidence-grounded supplier decision support</p>
            </header>

            <FileUpload onUploadComplete={handleUploadComplete} />

            {data && (
                <>
                    <RequirementTable requirements={data.requirements} />
                    <SupplierTable suppliers={data.suppliers} />
                    <RecommendationCard recommendation={data.recommendation} />
                    <SensitivityAnalysis data={data.sensitivity_analysis} />
                    <ConflictPanel conflicts={data.conflicts} />
                    <ReviewPanel reviewItems={data.review_items} />
                </>
            )}
        </div>
    );
}

export default Dashboard;