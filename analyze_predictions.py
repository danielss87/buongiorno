"""
Analyze prediction accuracy for Buongiorno gold price predictions
"""
import pandas as pd
import sys
import io

# Set encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load predictions history
predictions = pd.read_csv('backend/pipeline/data/predictions/predictions_history.csv')
predictions['target_date'] = pd.to_datetime(predictions['target_date'])
predictions['prediction_date'] = pd.to_datetime(predictions['prediction_date'])

# Load actual gold prices
gold_prices = pd.read_csv('backend/pipeline/data/raw/gold_prices.csv')
gold_prices['Date'] = pd.to_datetime(gold_prices['Date'])
gold_prices = gold_prices.set_index('Date')

print('=' * 80)
print('BUONGIORNO - PREDICTION ACCURACY ANALYSIS')
print('=' * 80)

print('\n=== PREDICTION HISTORY ===\n')
for idx, row in predictions.iterrows():
    pred_date = row['prediction_date'].strftime('%Y-%m-%d')
    target_date = row['target_date'].strftime('%Y-%m-%d')

    print(f"{idx+1}. Predicted on {pred_date} for {target_date}")
    print(f"   Current Price: ${row['current_price']:.2f}")
    print(f"   Predicted Price: ${row['predicted_price']:.2f}")
    print(f"   Expected Change: ${row['change_abs']:.2f} ({row['change_pct']:.2f}%)")
    print(f"   Trend: {row['trend']}")
    print(f"   Model: {row['model_used'].upper()} | MAPE: {row['model_mape']:.2f}%")
    print()

print('\n' + '=' * 80)
print('COMPARING PREDICTIONS VS ACTUAL PRICES')
print('=' * 80 + '\n')

# For each prediction, find the actual price on target date
results = []
for idx, row in predictions.iterrows():
    target_date = row['target_date']
    pred_date = row['prediction_date']

    # Get actual price on target date (if available)
    if target_date in gold_prices.index:
        actual_price = gold_prices.loc[target_date, 'Close']
        predicted_price = row['predicted_price']
        current_price = row['current_price']

        # Calculate actual change
        actual_change = actual_price - current_price
        actual_change_pct = (actual_change / current_price) * 100

        # Calculate prediction error
        price_error = predicted_price - actual_price
        price_error_pct = abs(price_error / actual_price) * 100

        # Determine if trend was correct
        predicted_trend = 'up' if row['change_abs'] > 0 else 'down' if row['change_abs'] < 0 else 'stable'
        actual_trend = 'up' if actual_change > 0 else 'down' if actual_change < 0 else 'stable'
        trend_correct = predicted_trend == actual_trend

        results.append({
            'prediction_date': pred_date.strftime('%Y-%m-%d'),
            'target_date': target_date.strftime('%Y-%m-%d'),
            'model': row['model_used'],
            'current_price': current_price,
            'predicted_price': predicted_price,
            'actual_price': actual_price,
            'predicted_change_pct': row['change_pct'],
            'actual_change_pct': actual_change_pct,
            'price_error': price_error,
            'price_error_pct': price_error_pct,
            'predicted_trend': predicted_trend,
            'actual_trend': actual_trend,
            'trend_correct': trend_correct
        })

if len(results) == 0:
    print("⚠️  NO COMPARABLE DATA FOUND")
    print("The predictions are for future dates that haven't occurred yet.")
    print("\nMost recent prediction:")
    latest = predictions.iloc[-1]
    print(f"  - Target Date: {latest['target_date'].strftime('%Y-%m-%d')}")
    print(f"  - Predicted Price: ${latest['predicted_price']:.2f}")
    print(f"  - Expected Change: {latest['change_pct']:.2f}%")
    print(f"  - Model: {latest['model_used'].upper()}")
else:
    # Display results
    for i, result in enumerate(results, 1):
        status = '✓' if result['trend_correct'] else '✗'
        print(f"{i}. {result['prediction_date']} → {result['target_date']} ({result['model'].upper()})")
        print(f"   Current: ${result['current_price']:.2f}")
        print(f"   Predicted: ${result['predicted_price']:.2f} | Actual: ${result['actual_price']:.2f}")
        print(f"   Predicted Change: {result['predicted_change_pct']:+.2f}% | Actual: {result['actual_change_pct']:+.2f}%")
        print(f"   Price Error: ${result['price_error']:+.2f} ({result['price_error_pct']:.2f}%)")
        print(f"   Trend: {result['predicted_trend'].upper()} → {result['actual_trend'].upper()} {status}")
        print()

    # Summary statistics
    print('\n' + '=' * 80)
    print('SUMMARY STATISTICS')
    print('=' * 80 + '\n')

    total = len(results)
    correct_trends = sum(1 for r in results if r['trend_correct'])
    avg_price_error = sum(abs(r['price_error']) for r in results) / total
    avg_error_pct = sum(r['price_error_pct'] for r in results) / total

    print(f"Total Predictions Analyzed: {total}")
    print(f"Trend Accuracy: {correct_trends}/{total} ({(correct_trends/total)*100:.1f}%)")
    print(f"Average Price Error: ${avg_price_error:.2f}")
    print(f"Average Error Percentage: {avg_error_pct:.2f}%")

    # Breakdown by model
    print("\n--- By Model ---")
    for model in set(r['model'] for r in results):
        model_results = [r for r in results if r['model'] == model]
        model_correct = sum(1 for r in model_results if r['trend_correct'])
        model_total = len(model_results)
        print(f"{model.upper()}: {model_correct}/{model_total} trends correct ({(model_correct/model_total)*100:.1f}%)")

print('\n=== RECENT ACTUAL GOLD PRICES (Last 10 days) ===\n')
recent = gold_prices.tail(10)[['Close']]
for date, row in recent.iterrows():
    # Calculate daily change
    prev_date = gold_prices.index[gold_prices.index.get_loc(date) - 1] if gold_prices.index.get_loc(date) > 0 else None
    if prev_date:
        prev_price = gold_prices.loc[prev_date, 'Close']
        change = row['Close'] - prev_price
        change_pct = (change / prev_price) * 100
        trend_symbol = '↗' if change > 0 else '↘' if change < 0 else '→'
        print(f"{date.strftime('%Y-%m-%d')}: ${row['Close']:.2f} ({change:+.2f}, {change_pct:+.2f}%) {trend_symbol}")
    else:
        print(f"{date.strftime('%Y-%m-%d')}: ${row['Close']:.2f}")

print('\n' + '=' * 80)
