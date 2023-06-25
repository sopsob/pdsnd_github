# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 17:17:25 2023

@author: SOBA010
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # defines valid cities
    valid_cities = ["chicago", "new york city", "washington"]
    #asks user for city input and changes it to lower case string
    while True:
        city = input("Which city do you want to explore (Chicago, New York City, or Washington): ").lower()

        if city in valid_cities:
            break
        else:
            print("Invalid input. Please enter a valid city.")

    # get user input for month (all, january, february, ... , june)
    valid_months = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = input("Please choose a month (January, February, March, April, May, June or all): ").lower()

        if month in valid_months:
            break
        else:
            print("Invalid input. Please enter a valid month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    while True:
        day = input("Please choose a day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all): ").lower()

        if day in valid_days:
            break
        else:
            print("Invalid input. Please enter a valid weekday.")
 
    print("Data Selection city: {}/ month: {}/ day: {}".format(city, month, day).title()) 

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start+End Time column to datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extracts the most common value of the column month
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts()[popular_month]
    # display the most common month
    print('Most Popular Month {} Count {}'.format(popular_month, popular_month_count))
    # extracts the most common value of the column day_of_week
    popular_weekday = df['day_of_week'].mode()[0]
    # display the most common day of week
    print('Most Popular Weekday:', popular_weekday)
    # extracts the most common value of the column hour
    popular_hour = df['hour'].mode()[0]
    # display the most common start hour
    print('Most Popular Start Hour:', popular_hour)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # extracts the most common value of for Start station
    popular_start_station = df['Start Station'].mode()[0]
    # display most commonly used start station
    print('Most Popular Start Station(s):', popular_start_station)

    # display least commonly used start station
    count_start = df['Start Station'].value_counts()
    #extracts minimum count for popolar start stations and returns as a list
    least_polular_starts = count_start[count_start == count_start.min()].index.tolist()
    print('Least popular Start Station(s):', least_polular_starts)
    
    # display most commonly used end station
    # extracts the most common value of for End station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['station_combi'] = df['Start Station'] + df['End Station']
    popular_station_combi = df['station_combi'].mode()[0]
    print('Most Popular Trip:', popular_station_combi)    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time", df['Trip Duration'].sum())
    #calculate mean of column Trip Duration
    #mean_duration = df['Trip Duration'].mean()
    # display mean travel time
    print("Average Travel Time", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Type", df['User Type'].value_counts())
    # Checks city = Washington, as Gender and Birth Year not available for Washinton
    try:    
        # Display counts of gender
        print("Counts of Gender", df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print("Earliest Birth Year", df['Birth Year'].min())
        print("Most recent Birth Year", df['Birth Year'].max())
        print("Most common Birth Year", df['Birth Year'].mode()[0])
    except:
        print("Sorry, Gender and Birth Year are not available for Washington")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def show_raw_data(df, batch_size=5):
    """Displays 5 lines of raw data from bikeshare dataframe"""
    #defines total length of data
    data_length = len(df)
    #sets start count to 0
    row_count = 0

    while row_count < data_length:
        #asks if user wants to see 5 lines of raw data
        user_input = input("Do you want to see 5 lines of raw data? (yes/no): ").lower()
        # dispays 5 lines of data
        if user_input == 'yes':
            for i in range(row_count, min(row_count + batch_size, data_length)):
                print(df.iloc[i])
            #increase row count by batch size (5)
            row_count += batch_size
            #runs if not reached the end of the data yet
            if row_count < data_length:
                #ask user if they want to see 5 further lines 
                user_input = input("Do you want to see the next 5 lines? (yes/no): ").lower()
                if user_input != 'yes':
                    break
        elif user_input == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:       
        while True:
            city, month, day = get_filters()

            #ask user if filters need to be changed and restarts if yes
            changefilter = input('\nWould you like to change your filter? Enter yes or no.\n')
            if changefilter.lower() != 'yes':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
