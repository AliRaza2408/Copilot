function RecommendationCard({ recommendation }) {
    if (!recommendation) return null;
    return (
        <section className="recommendation-card">
            <h2>Recommended Supplier</h2>
            <h3>🥇 {recommendation.supplier}</h3>
            <p>Score: {recommendation.score}</p>
            <p>Confidence: {recommendation.confidence}</p>
            <button>View Evidence</button>
        </section>
    );
}
export default RecommendationCard;