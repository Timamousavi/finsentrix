document.addEventListener('DOMContentLoaded', function() {
    const batchAnalyzeForm = document.getElementById('batchAnalyzeForm');
    const batchResults = document.getElementById('batchResults');

    // Update market data every 5 seconds
    updateMarketData();
    setInterval(updateMarketData, 5000);

    // Handle batch analysis form submission
    batchAnalyzeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const texts = document.getElementById('batchText').value
            .split('\n')
            .filter(text => text.trim().length > 0);
        
        if (texts.length === 0) {
            alert('لطفاً حداقل یک متن وارد کنید');
            return;
        }
        
        try {
            const response = await fetch('/analyze/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ texts: texts })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayBatchResults(data.results);
            } else {
                throw new Error(data.detail || 'خطا در تحلیل متن‌ها');
            }
        } catch (error) {
            alert('خطا: ' + error.message);
        }
    });
});

async function updateMarketData() {
    try {
        const response = await fetch('/api/dashboard/real-time');
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            const marketData = data.data.market_data;
            
            // Update TSE Index
            document.getElementById('tseIndex').textContent = numberWithCommas(marketData.tse_index.value);
            updateChangeBadge('tseChange', marketData.tse_index.change);
            
            // Update IFX Index
            document.getElementById('ifxIndex').textContent = numberWithCommas(marketData.ifx_index.value);
            updateChangeBadge('ifxChange', marketData.ifx_index.change);
            
            // Update Volumes
            document.getElementById('tseVolume').textContent = numberWithCommas(marketData.tse_index.volume);
            document.getElementById('ifxVolume').textContent = numberWithCommas(marketData.ifx_index.volume);
        }
    } catch (error) {
        console.error('Error updating market data:', error);
    }
}

function updateChangeBadge(elementId, change) {
    const element = document.getElementById(elementId);
    const changeText = (change >= 0 ? '+' : '') + change.toFixed(2) + '%';
    element.textContent = changeText;
    element.className = 'change-badge ' + (change >= 0 ? 'change-positive' : 'change-negative');
}

function displayBatchResults(results) {
    batchResults.innerHTML = '';
    
    results.forEach((result, index) => {
        const card = document.createElement('div');
        card.className = 'card mt-3';
        
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        
        // Add text
        const text = document.createElement('p');
        text.className = 'mb-3';
        text.textContent = result.text;
        
        // Add sentiment and confidence
        const sentimentDiv = document.createElement('div');
        sentimentDiv.className = `alert alert-${result.sentiment} mb-3`;
        
        const sentimentMap = {
            'positive': 'مثبت',
            'negative': 'منفی',
            'neutral': 'خنثی'
        };
        
        sentimentDiv.innerHTML = `
            <strong>احساس:</strong> ${sentimentMap[result.sentiment]}<br>
            <strong>اطمینان:</strong> ${(result.confidence * 100).toFixed(1)}%
        `;
        
        // Add details
        const detailsList = document.createElement('ul');
        detailsList.className = 'list-group';
        
        for (const [term, score] of Object.entries(result.details)) {
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
        
        cardBody.appendChild(text);
        cardBody.appendChild(sentimentDiv);
        cardBody.appendChild(detailsList);
        card.appendChild(cardBody);
        batchResults.appendChild(card);
    });
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
} 