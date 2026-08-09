function ReviewPanel({ reviewItems = [] }) {
    return (
        <section>
            <h2>Human Review Required</h2>
            {reviewItems.length === 0 ? (
                <p>No review items.</p>
            ) : (
                reviewItems.map((item, index) => (
                    <div key={index} className="review-item">
                        <h3>{item.supplier}</h3>
                        <p>{item.message}</p>
                        <button>View Evidence</button>
                    </div>
                ))
            )}
        </section>
    );
}
export default ReviewPanel;