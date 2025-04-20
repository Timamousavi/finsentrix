# FinSentrix (FSX) Global Market Sentiment Analysis Dataset

## Overview
This dataset is designed for training and evaluating sentiment analysis models for global financial markets, with a focus on multi-language support including English and Persian.

## License Information
This dataset is available under a dual-license structure:

### Academic License
- Free for academic and research purposes
- Requires proper citation
- No redistribution allowed without permission
- Contact for academic use: fatemehmousavy@ut.ac.ir

### Commercial License
- Requires a separate commercial license agreement
- Available for business and commercial use
- Includes technical support options
- Custom terms and pricing available
- Contact for commercial inquiries: fatemehmousavy@ut.ac.ir

For detailed license terms, please refer to the LICENSE file.

## Dataset Structure
The dataset is stored in CSV format with the following columns:

- `text`: Persian financial text (UTF-8 encoded)
- `sentiment`: Sentiment label (0: negative, 1: positive, 2: neutral)

## Data Collection Methodology
The dataset was created using a combination of:
1. Manually curated financial statements
2. Common stock market phrases
3. Financial news headlines
4. Forum discussions

## Data Categories

### Positive Sentiment (1)
Examples of positive financial statements:
- Stock price increases
- Good financial performance
- Positive analyst predictions
- Growth indicators

### Negative Sentiment (0)
Examples of negative financial statements:
- Stock price decreases
- Poor financial performance
- Negative analyst predictions
- Risk indicators

### Neutral Sentiment (2)
Examples of neutral financial statements:
- Company announcements
- General updates
- Routine reports
- Market status updates

## Usage
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('sample_dataset.csv', encoding='utf-8')

# View sample data
print(df.head())

# Check sentiment distribution
print(df['sentiment'].value_counts())
```

## Data Statistics
- Total samples: 1000
- Positive samples: 333
- Negative samples: 333
- Neutral samples: 333

## Limitations
1. This is a sample dataset and may not represent real-world distribution
2. Limited to common financial phrases and statements
3. May not cover all financial scenarios
4. Needs to be supplemented with real-world data

## Future Improvements
1. Add more diverse financial statements
2. Include real-world data from financial websites
3. Add more specific financial terms
4. Include company-specific information

## Citation
If you use this dataset in your research, please cite:
```
FinSentrix (FSX) Global Market Sentiment Analysis Dataset
Tima Mousavi
2024
```

## Commercial Use
For commercial use of this dataset, please contact:
- Name: Tima Mousavi
- Email: fatemehmousavy@ut.ac.ir

Commercial license options include:
- Standard commercial license
- Enterprise license
- Custom integration services
- Technical support packages

## Contact
For questions or suggestions, please contact:
- Academic inquiries: fatemehmousavy@ut.ac.ir
- Commercial inquiries: fatemehmousavy@ut.ac.ir
- General questions: fatemehmousavy@ut.ac.ir 