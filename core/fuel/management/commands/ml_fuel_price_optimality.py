import os

import joblib
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from core.project.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Create and Save Machine Learning Model'  # noqa: A003

    def handle(self, *args, **options):

        try:
            ml_pickle_file_exists = os.path.join(BASE_DIR, 'core/fuel/utils/fuel_stop_model.pkl')

            if not os.path.isfile(ml_pickle_file_exists):

                self.stdout.write(self.style.WARNING('About to create Machine Learning Model'))
                self.stdout.write(self.style.SUCCESS('Creating and saving Machine Learning Model ...'))

                # load and read csv file
                file_path = os.path.join(BASE_DIR, 'core/fuel/utils/update_fuel-prices-for-be-assessment.csv')
                df = pd.read_csv(file_path)

                # perform basic file cleaning
                # remove duplicate rows
                df = df.drop_duplicates()
                # drop missing rows for Retail Price, Latitude,  Longitude
                # note will have been added to cv using csv_lat_long_addition utility
                df = df.dropna(subset=['Retail Price', 'Latitude', 'Longitude'])

                # calculate the average fuel price for each state serving as a benchmark
                df['state_avg_price'] = df.groupby('State')['Retail Price'].transform('mean')
                # guess and compute the distance to the next stop
                # this done using difference in fuel price between consecutive rows.
                # also the missing values is filled with the median fuel price by
                # taking absoulte fuel value
                df['distance_to_next_stop'] = df['Retail Price'].diff().fillna(df['Retail Price'].median()).abs()

                # features and label
                X = df[['Retail Price', 'state_avg_price', 'distance_to_next_stop']].values
                y = (df['Retail Price'] < 3.5).astype(int)

                # train and test (80/20)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # use Random Forest classifier
                clf = RandomForestClassifier(n_estimators=100, random_state=42)
                clf.fit(X_train, y_train)

                # save model for later use
                model_path = os.path.join(BASE_DIR, 'core/fuel/utils/fuel_stop_model.pkl')
                joblib.dump(clf, model_path)

                self.stdout.write(self.style.SUCCESS('Machine Learning Model Saved Successfully'))
            else:
                self.stdout.write(self.style.SUCCESS('Great, ML pickle file already exists, skipping training.'))
        except Exception:
            raise CommandError('Failed create Machine Learning Model')
