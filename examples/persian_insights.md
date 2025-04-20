# Persian Market Insights

## Overview
This example demonstrates specialized analysis techniques for Persian financial markets, including sentiment analysis, market correlation, and trend detection in Persian language content.

## Example 1: Persian Market Sentiment

```python
from finsentrix import FinSentrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize analyzer
fsx = FinSentrix()

# Get sentiment data for Persian markets
persian_symbols = ['شاخص', 'فولاد', 'خودرو']
sentiment_data = {}

for symbol in persian_symbols:
    sentiment_data[symbol] = fsx.get_market_sentiment(
        market_type="stock",
        symbol=symbol,
        language="fa",  # Persian language
        start_date="1402-01-01",  # Persian calendar
        end_date="1402-12-29"
    )

# Create sentiment visualization
plt.figure(figsize=(15, 8))
for symbol, data in sentiment_data.items():
    plt.plot(data['timestamp'], data['sentiment_score'], 
             label=symbol, alpha=0.7)
plt.title('تحلیل احساسات بازار ایران')
plt.xlabel('تاریخ')
plt.ylabel('نمره احساسات')
plt.legend()
plt.grid(True)
plt.show()
```

![Persian Market Sentiment](assets/persian_sentiment.png)

## Example 2: Market Correlation Analysis

```python
# Calculate correlation matrix
correlation_data = pd.DataFrame()
for symbol, data in sentiment_data.items():
    correlation_data[symbol] = data['sentiment_score']

correlation_matrix = correlation_data.corr()

# Create correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
            vmin=-1, vmax=1)
plt.title('همبستگی احساسات بازار')
plt.show()

# Analyze market movements
price_data = fsx.get_market_data(
    market_type="stock",
    symbols=persian_symbols,
    language="fa",
    start_date="1402-01-01",
    end_date="1402-12-29"
)

# Create price-sentiment correlation
plt.figure(figsize=(15, 10))
for symbol in persian_symbols:
    plt.scatter(price_data[symbol]['price_change'],
                sentiment_data[symbol]['sentiment_change'],
                alpha=0.5, label=symbol)
plt.title('تغییر قیمت در مقابل تغییر احساسات')
plt.xlabel('تغییر قیمت (%)')
plt.ylabel('تغییر احساسات')
plt.legend()
plt.grid(True)
plt.show()
```

![Persian Market Correlation](assets/persian_correlation.png)

## Example 3: News Impact Analysis

```python
# Get news data
news_data = fsx.get_news_data(
    market_type="stock",
    language="fa",
    start_date="1402-01-01",
    end_date="1402-12-29"
)

# Analyze news impact
impact_data = fsx.analyze_news_impact(
    news_data=news_data,
    market_data=price_data,
    language="fa"
)

# Create impact visualization
plt.figure(figsize=(15, 8))
plt.plot(impact_data['timestamp'], impact_data['sentiment_impact'],
         label='تاثیر احساسات', color='blue')
plt.plot(impact_data['timestamp'], impact_data['price_impact'],
         label='تاثیر قیمت', color='red')
plt.title('تاثیر اخبار بر بازار')
plt.xlabel('تاریخ')
plt.ylabel('میزان تاثیر')
plt.legend()
plt.grid(True)
plt.show()

# Print key metrics
print(f"""
نتایج تحلیل:
- میانگین تاثیر احساسات: {impact_data['sentiment_impact'].mean():.2f}
- میانگین تاثیر قیمت: {impact_data['price_impact'].mean():.2f}
- همبستگی: {impact_data['correlation'].mean():.2f}
""")
```

![News Impact Analysis](assets/persian_news_impact.png)

## Key Insights

1. **Market Behavior**
   - تاثیر شدید اخبار سیاسی
   - نوسانات فصلی مشخص
   - تاثیر اخبار بین‌المللی
   - الگوهای معاملاتی خاص

2. **Sentiment Patterns**
   - احساسات مثبت در ابتدای هفته
   - تاثیر اخبار صبحگاهی
   - نوسانات پایان هفته
   - الگوهای فصلی

3. **Analysis Challenges**
   - تفاوت تقویم شمسی
   - اصطلاحات مالی خاص
   - منابع داده محدود
   - نوسانات بازار

## Best Practices

1. **Data Collection**
   - استفاده از منابع معتبر
   - در نظر گرفتن تعطیلات
   - پایش اخبار لحظه‌ای
   - تایید صحت داده‌ها

2. **Analysis**
   - استفاده از بازه‌های زمانی مناسب
   - در نظر گرفتن تعطیلات
   - تحلیل اخبار مهم
   - بررسی همبستگی‌ها

3. **Visualization**
   - استفاده از نمودارهای مناسب
   - نمایش روندها
   - برجسته‌سازی رویدادها
   - استفاده از رنگ‌های مناسب

## Implementation Tips

1. **Performance**
   - بهینه‌سازی برای داده‌های فارسی
   - مدیریت منابع
   - کش کردن نتایج
   - پردازش موازی

2. **Accuracy**
   - استفاده از منابع متعدد
   - تایید سیگنال‌ها
   - در نظر گرفتن عمق بازار
   - تحلیل نقدینگی

3. **User Experience**
   - رابط کاربری فارسی
   - به‌روزرسانی لحظه‌ای
   - هشدارهای مناسب
   - امکان شخصی‌سازی

## Next Steps

1. اضافه کردن نمادهای بیشتر
2. پیاده‌سازی تحلیل لحظه‌ای
3. اضافه کردن شاخص‌های فنی
4. توسعه مدل‌های پیش‌بینی 