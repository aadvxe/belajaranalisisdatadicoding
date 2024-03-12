import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Bike Sharing Dataset Dashboard')

hour_df = pd.read_csv('hour.csv')
day_df = pd.read_csv('day.csv')

st.sidebar.title('Bike Sharing Dataset')

min_date = pd.to_datetime(hour_df['dteday']).min().date()
max_date = pd.to_datetime(hour_df['dteday']).max().date()

start_date, end_date = st.sidebar.date_input(
    label='Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

hour_df_filtered = hour_df[(pd.to_datetime(hour_df['dteday']).dt.date >= start_date) & 
                           (pd.to_datetime(hour_df['dteday']).dt.date <= end_date)]
day_df_filtered = day_df[(pd.to_datetime(day_df['dteday']).dt.date >= start_date) & 
                         (pd.to_datetime(day_df['dteday']).dt.date <= end_date)]

st.header('Hourly and Daily Distribution')

fig_hour_hist, ax_hour_hist = plt.subplots(figsize=(10, 6))
sns.histplot(hour_df_filtered['cnt'], bins=30, kde=True, ax=ax_hour_hist)
ax_hour_hist.set_title('Hourly Bike Rentals Distribution')
ax_hour_hist.set_xlabel('Number of Bike Rentals')
ax_hour_hist.set_ylabel('Frequency')
st.pyplot(fig_hour_hist)

fig_day_hist, ax_day_hist = plt.subplots(figsize=(10, 6))
sns.histplot(day_df_filtered['cnt'], bins=30, kde=True, ax=ax_day_hist)
ax_day_hist.set_title('Daily Bike Rentals Distribution')
ax_day_hist.set_xlabel('Number of Bike Rentals')
ax_day_hist.set_ylabel('Frequency')
st.pyplot(fig_day_hist)

st.header('Hourly Bike Rentals on Weekdays')

hourly_workday_rentals = hour_df_filtered[hour_df_filtered['workingday'] == 1].groupby(['weekday', 'hr'])['cnt'].mean().reset_index()

fig_hourly_heatmap, ax_hourly_heatmap = plt.subplots(figsize=(12, 8))
heatmap_data = hourly_workday_rentals.pivot(index='weekday', columns='hr', values='cnt')
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.5, ax=ax_hourly_heatmap)
ax_hourly_heatmap.set_title('Hourly Bike Rentals on Weekdays')
ax_hourly_heatmap.set_xlabel('Hour (hr)')
ax_hourly_heatmap.set_ylabel('Weekday')
ax_hourly_heatmap.set_xticklabels(ax_hourly_heatmap.get_xticklabels(), rotation=45)
ax_hourly_heatmap.set_yticks(ticks=[0, 1, 2, 3, 4])
ax_hourly_heatmap.set_yticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
st.pyplot(fig_hourly_heatmap)
