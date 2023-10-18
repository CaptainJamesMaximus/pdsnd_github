#!/usr/bin/env python
# coding: utf-8

# In[7]:


import time
import pandas as pd
import numpy as np

# Define a dictionary mapping city names to their corresponding CSV file names
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for the city (chicago, new york city, washington)
    while True:
        city = input('Enter the name of the city (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name. Please enter a valid city.')

    # Get user input for the month (all, january, february, ..., june)
    while True:
        month = input('Enter the name of the month (all, january, february, ..., june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month name. Please enter a valid month.')

    # Get user input for the day of the week (all, monday, tuesday, ..., sunday)
    while True:
        day = input('Enter the name of the day of the week (all, monday, tuesday, ..., sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day name. Please enter a valid day.')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data from the specified CSV file
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' column
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month_num]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month_name = months[most_common_month - 1]
    print(f"The most common month for bike rentals is: {most_common_month_name}")

    # Display the most common day of the week
    most_common_day = df['Day of Week'].mode()[0]
    print(f"The most common day of the week for bike rentals is: {most_common_day}")

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print(f"The most common hour for bike rentals is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most common start station is: {most_common_start_station}")

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most common end station is: {most_common_end_station}")

    # Display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start and end station is: {most_common_trip[0]} to {most_common_trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time for all trips is: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time for all trips is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("Counts of User Types:")
    for user_type, count in user_type_counts.items():
        print(f"{user_type}: {count}")

    # Display counts of gender (if the 'Gender' column exists in your data)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")
    else:
        print("\nGender data is not available in the dataset.")

    # Display earliest, most recent, and most common year of birth (if the 'Birth Year' column exists in your data)
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print("\nBirth Year Statistics:")
        print(f"Earliest Birth Year: {int(earliest_birth_year)}")
        print(f"Most Recent Birth Year: {int(most_recent_birth_year)}")
        print(f"Most Common Birth Year: {int(most_common_birth_year)}")
    else:
        print("\nBirth Year data is not available in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Displays raw data upon user request in chunks of 5 rows.

    Args:
        df - Pandas DataFrame containing city data

    Returns:
        None
    """
    start_loc = 0
    while True:
        # Ask user if they want to see first 5 lines of raw data
        display_raw_data = input('Do you want to see 5 lines of raw data? Enter yes or no.\n')
        if display_raw_data.lower() == 'yes':
            # Display 5 lines of raw data based on the start_loc
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5  # Update the start_loc for the next iteration
        else:
            print('Exiting raw data display.')
            break
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask the user if they want to see raw data
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()


# In[ ]:




