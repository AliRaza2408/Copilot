const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function uploadDocuments(files) {
    const formData = new FormData();
    files.forEach((file) => {
        formData.append("files", file);
    });

    const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) throw new Error("Upload failed");
    return response.json();
}

export async function processDecision(files) {
    const formData = new FormData();
    files.forEach((file) => {
        formData.append("files", file);
    });

    const response = await fetch(`${API_BASE_URL}/api/decision/process`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) throw new Error("Decision processing failed");
    return response.json();
}

export async function askCopilot(question) {
    const response = await fetch(`${API_BASE_URL}/api/copilot/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) throw new Error("Failed to get AI response");
    return response.json();
}

export async function submitHumanReview(caseId, status, reason = null) {
    const response = await fetch(`${API_BASE_URL}/api/decision/${caseId}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_id: caseId, status: status, reason: reason }),
    });

    if (!response.ok) throw new Error("Failed to submit review");
    return response.json();
}