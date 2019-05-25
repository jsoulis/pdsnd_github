import time
import pandas as pd
import numpy as np
import datetime as dt

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
    cities = ['chicago', 'new york city', 'washington']
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
    days = {'mon':'monday', 'tue':'tuesday', 'wed':'wednesday', 'thu':'thursday', 'fri':'friday', 'sat':'saturday', 'sun':'sunday'}
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter a city! Choose between Chicago, New York City and Washington: ')
        city = city.strip().lower()
        if city in cities:
            break
        else: 
            print('I\'m sorry, I didn\'t get that. Please enter a valid city.')
            continue
        
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter a month to filter on. Please choose "all" or Jan, Feb, Mar, Apr, May, or Jun: ')
        month = month.strip().lower()
        if month in months or month == 'all':
            break
        else:
            print('Please choose a month by its 3 letter abreviation or select "all" to not filter based on month.')
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter a day to filter on. Please choose "all" or Mon, Tue, Wed, Thu, Fri, Sat or Sun: ')
        day = day.strip().lower()
        if day in days or day == 'all':
            if day != 'all':
                day = days[day]
            break
        else:
            print('Please choose a day by entering its 3 letter abreviation or select "all" to not filter based on day of the week.')
            continue

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
    df = pd.read_csv(CITY_DATA[city], index_col=0)
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months  = ['January', 'February', 'March', 'April', 'May', 'June']

    # display the most common month
    if month == 'all':
        print("Most popular month: {}".format(months[df['month'].mode()[0]-1]))

    # display the most common day of week
    if day == 'all':
        print("Most popular day of week: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("Most popular start hour: {}".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most commonly used end station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip

    #organize routes to get a count on the most popular one
    df['route'] = df['Start Station'] + ' -> ' + df['End Station']

    print("Most frequent route: {}".format(df['route'].mode()[0]))
    print("This route was frequented {} time[s]!".format(df.groupby(['route']).count().max()[0]))
    
    # remove new column from raw data
    df.drop("route", axis=1, inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = dt.timedelta(seconds=float(df['Trip Duration'].sum()))
    print("The total travel time is: {}".format(total_time))

    # display mean travel time
    avg_time = dt.timedelta(seconds=float(df['Trip Duration'].mean()))
    print("The mean travel time is: {}".format(avg_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("There were {} Customers and {} Subscribers".format(user_types['Customer'],user_types['Subscriber'] ))

    # Display counts of gender
    if city == 'washington':
        print("No gender information available for Washington")
    else:
        gender = df['Gender'].value_counts()
        print("There were {} Female and {} Male riders".format(gender['Female'], gender['Male']))

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print("There is no date of birth information available for Washington")
    else:
        print("The earliest born rider was born in: {}".format(int(df['Birth Year'].min())))
        print("The most recent born rider was born in: {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth was in: {}".format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    status = 'no'
    status = input('\nWould you like to see 5 lines of raw data? Enter yes or no\n')
    index = 0
    #end is the number of rows
    end = df.shape[0]

    while status == 'yes' and index < end:
        index_end = index + 5
        if index_end > end:
            index_end = end - 1
        while index < index_end:
            print("{}\n".format(df.iloc[index]))
            index += 1
        index = index_end
        status = input('\nWould you like to see 5 more lines of raw data? Enter yes or no\n')
        
        
            


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
    
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
