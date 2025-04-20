"""
Script to create a sample dataset for training the sentiment analysis model.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_dataset(size: int = 1000) -> pd.DataFrame:
    """
    Create a sample dataset with Persian financial text and sentiment labels.
    
    Args:
        size (int): Number of samples to create
        
    Returns:
        pd.DataFrame: Generated dataset
    """
    # Positive sentiment samples
    positive_samples = [
        "سهام شرکت فولاد امروز با افزایش قیمت مواجه شد",
        "تحلیل‌گران پیش‌بینی می‌کنند که این روند ادامه خواهد داشت",
        "سودآوری شرکت در سه ماهه اول افزایش یافته است",
        "بازار بورس امروز روند صعودی داشت",
        "شرکت در زمینه صادرات پیشرفت خوبی داشته است",
        "سود هر سهم بیشتر از پیش‌بینی‌ها بود",
        "رشد فروش شرکت امیدوارکننده است",
        "تحلیل تکنیکال نشان‌دهنده روند صعودی است",
        "سهام شرکت پتانسیل رشد خوبی دارد",
        "بازدهی سهام در مقایسه با شاخص کل بهتر بود"
    ]
    
    # Negative sentiment samples
    negative_samples = [
        "بازار بورس امروز روند نزولی داشت",
        "سودآوری شرکت کاهش یافته است",
        "تحلیل‌گران نسبت به آینده بدبین هستند",
        "شرکت با مشکلات مالی مواجه شده است",
        "سهام شرکت امروز با کاهش قیمت مواجه شد",
        "پیش‌بینی‌ها نسبت به آینده خوشبینانه نیست",
        "رشد فروش شرکت کمتر از انتظارات بود",
        "تحلیل تکنیکال نشان‌دهنده روند نزولی است",
        "سهام شرکت ریسک بالایی دارد",
        "بازدهی سهام در مقایسه با شاخص کل ضعیف بود"
    ]
    
    # Neutral sentiment samples
    neutral_samples = [
        "شرکت امروز گزارش عملکرد خود را منتشر کرد",
        "تحلیل‌گران در مورد آینده سهام نظرات مختلفی دارند",
        "قیمت سهام امروز بدون تغییر بود",
        "شرکت در حال بررسی طرح‌های توسعه است",
        "مجمع عمومی شرکت هفته آینده برگزار می‌شود",
        "شرکت در حال مذاکره با سرمایه‌گذاران جدید است",
        "قیمت سهام در محدوده مقاومت قرار دارد",
        "شرکت در حال به‌روزرسانی استراتژی‌های خود است",
        "تحلیل‌گران در انتظار انتشار گزارش مالی هستند",
        "شرکت در حال بررسی گزینه‌های مختلف است"
    ]
    
    # Create dataset
    data = []
    labels = []
    
    # Add positive samples
    for _ in range(size // 3):
        text = np.random.choice(positive_samples)
        data.append(text)
        labels.append(1)  # 1 for positive
        
    # Add negative samples
    for _ in range(size // 3):
        text = np.random.choice(negative_samples)
        data.append(text)
        labels.append(0)  # 0 for negative
        
    # Add neutral samples
    for _ in range(size // 3):
        text = np.random.choice(neutral_samples)
        data.append(text)
        labels.append(2)  # 2 for neutral
        
    # Create DataFrame
    df = pd.DataFrame({
        'text': data,
        'sentiment': labels
    })
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def save_dataset(df: pd.DataFrame, output_path: str):
    """
    Save the dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): Dataset to save
        output_path (str): Path to save the dataset
    """
    df.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Dataset saved to {output_path}")
    logger.info(f"Dataset size: {len(df)} samples")
    logger.info(f"Sentiment distribution:\n{df['sentiment'].value_counts()}")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = Path("data/raw/sample")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create and save dataset
    dataset = create_sample_dataset(size=1000)
    save_dataset(dataset, output_dir / "sample_dataset.csv")
    
    # Print sample of the dataset
    print("\nSample of the dataset:")
    print(dataset.head())
    print("\nSentiment distribution:")
    print(dataset['sentiment'].value_counts()) 