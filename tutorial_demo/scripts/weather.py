import pandas as pd
import numpy as np


def generate_synthetic_data(seed=42, output_path='../data/ksea_2024.csv'):
    """Generate a year of synthetic hourly SeaTac temperatures and save to CSV."""
    np.random.seed(seed)

    hours = pd.date_range('2024-01-01 00:00', '2024-12-31 23:00', freq='h', tz='UTC')

    doy = hours.dayofyear.to_numpy()
    seasonal = 9 + 11 * np.sin(2 * np.pi * (doy - 100) / 365.25)

    hod = hours.hour.to_numpy()
    diurnal = 5 * np.sin(2 * np.pi * (hod - 16) / 24)

    noise = np.random.normal(0, 1.8, len(hours))

    temp = seasonal + diurnal + noise

    df = pd.DataFrame({
        'timestamp': hours.tz_localize(None),
        'temp_c': temp,
    })

    df.to_csv(output_path, index=False)
    print(f'wrote {len(df)} rows')
    return df


def load_and_clean(path):
    """Load the CSV at path, parse the timestamp column, and set it as the index."""
    df = pd.read_csv(path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df


def compute_daily_stats(df):
    """Resample hourly DataFrame to daily mean, max, and min temperature."""
    return df['temp_c'].resample('D').agg(['mean', 'max', 'min'])


def compute_diurnal_pattern(df):
    """Return mean temperature grouped by hour of day across the full dataset."""
    df = df.copy()
    df['hour'] = df.index.hour
    by_hour = df.groupby('hour')['temp_c'].mean()
    print(f'peak hour: {by_hour.idxmax()}')
    print(f'coldest hour: {by_hour.idxmin()}')
    return by_hour


def forecast_next_day_max(daily, window=7):
    """Forecast tomorrow's max temperature as the mean of the last `window` daily maxes."""
    last_n = daily['max'].iloc[-window:]
    forecast = last_n.mean()
    print(f'last {window} daily maxes:')
    print(last_n)
    print(f'\nforecast for next day max: {forecast:.1f} C')
    return forecast
