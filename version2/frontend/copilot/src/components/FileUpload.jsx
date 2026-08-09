import { useState } from "react";
import { uploadDocuments } from "../services/api";

function FileUpload({ onUploadComplete }) {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        setFiles(Array.from(event.target.files));
        setError("");
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setError("Please select files.");
            return;
        }
        try {
            setLoading(true);
            const result = await uploadDocuments(files);
            onUploadComplete(result);
        } catch (err) {
            setError("Unable to upload documents.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-card">
            <h2>Upload Challenge Pack</h2>
            <input type="file" multiple onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading..." : "Upload Documents"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
}

export default FileUpload;