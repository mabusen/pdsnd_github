import time
import pandas as pd
import numpy as np

#Defining dictionary containing the three csv files

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
    print('Hello! Let\'s explore some US bikeshare data together!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("What\'s the city you want to analyze? You can choose between chicago, new york city or washington.\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("\n You must enter one of the three cities in the prompt as it is written.")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("What\'s month you want to analyze? You can choose between january, february, march, april, may, june or all of them. If you want to analyze, type all.\n").lower()
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            break
        else:
            print("\n Please choose a month in the first half of the year and please do not use any abbreviations.\n If you want to see data for all months January through June, type \"all\".")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day of the week would you like to explore? If you want to see data for all seven days, type \"all\" .\n").lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        else:
            print("Please select a valid day of the week or select ""all"" if you want to analyze all days.")

    print("\n Thank you! We'll be exploring data from {} in month: {} and on day: {}".format(city.title(), month.title(), day.title()))
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
    df = pd.read_csv(CITY_DATA.get(city))

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int (remember input is str, in df it is int)
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month.lower()) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month_num]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe, use .title() because dt.weekday_name returns day capitalized
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_num = df['month'].mode()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[int(common_month_num - 1)].title()
    print("The most common month for rides: ", common_month)

    # TO DO: display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
    print("The most common week day for rides: ", common_week_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common starting hour for rides: ", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station for rides: ", common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station for rides: ", common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['combined_journey'] = df['Start Station'] + ' to ' + df['End Station']
    common_journey = df['combined_journey'].mode()[0]
    common_journey_freq = len(df[df['combined_journey'] == common_journey])
    print("Most commonly taken trip is from {} with {} occurences.\n".format(common_journey, common_journey_freq))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time for rides is: ", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time for rides is: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Here's a table showing the count for each user type.")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("\nA table showing the count for each user gender.")
        nan_num = df['Gender'].isnull().sum()
        print("{} people did not specify their gender.".format(nan_num))
        print(df['Gender'].value_counts())
    else:
        print("This city has not provided gender data.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBirth year statistics:")
        print("The most recent birth year on record is {}.".format(int(df['Birth Year'].max())))
        print("The earliest birth year on record is {}.".format(int(df['Birth Year'].min())))
        print("The most common birth year among users is {}.".format(int(df['Birth Year'].mode())))
    else:
        print("This city has not provided birth year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Defining a function that allows the user to restart the flow

def restart():
    """Allows users to choose to restart or quit tool"""
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
        print("Okay, bye, and please come back soon. The program is only getting better and we need to save the planet!")
        quit()
    else:
        main()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw = input("Would you like to see the first 10 rows of data?\n")
        if raw.lower() == 'no':
            restart()
        elif raw.lower() == 'yes':
            print(df.head(10))
            i = 10
            while True:
                ten = input("10 more rows of data? Yes or no.")
                if ten.lower() == 'no':
                    restart()
                elif ten.lower() == 'yes':
                    print(df[i:i+10])
                    i += 10
                else:
                    print("Your input must be yes or no.")
            restart()
        else:
            print("Your input must be yes or no.")


if __name__ == "__main__":
	main()
