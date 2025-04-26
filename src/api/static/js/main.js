document.addEventListener('DOMContentLoaded', function() {
    const analyzeForm = document.getElementById('analyzeForm');
    const resultDiv = document.getElementById('result');
    const sentimentAlert = document.getElementById('sentimentAlert');
    const sentimentResult = document.getElementById('sentimentResult');
    const confidenceResult = document.getElementById('confidenceResult');
    const detailsList = document.getElementById('detailsList');

    analyzeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const text = document.getElementById('text').value;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Show results
                resultDiv.style.display = 'block';
                
                // Update sentiment class
                sentimentAlert.className = 'alert alert-' + data.sentiment;
                
                // Update sentiment text
                const sentimentMap = {
                    'positive': 'مثبت',
                    'negative': 'منفی',
                    'neutral': 'خنثی'
                };
                sentimentResult.textContent = sentimentMap[data.sentiment];
                
                // Update confidence
                confidenceResult.textContent = (data.confidence * 100).toFixed(1) + '%';
                
                // Clear previous details
                detailsList.innerHTML = '';
                
                // Add new details
                for (const [term, score] of Object.entries(data.details)) {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    
                    const termSpan = document.createElement('span');
                    termSpan.textContent = term;
                    
                    const scoreSpan = document.createElement('span');
                    scoreSpan.className = `term-score ${score > 0 ? 'term-positive' : 'term-negative'}`;
                    scoreSpan.textContent = score > 0 ? '+' + score.toFixed(2) : score.toFixed(2);
                    
                    li.appendChild(termSpan);
                    li.appendChild(scoreSpan);
                    detailsList.appendChild(li);
                }
            } else {
                throw new Error(data.detail || 'خطا در تحلیل متن');
            }
        } catch (error) {
            alert('خطا: ' + error.message);
        }
    });
}); 