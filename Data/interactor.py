import pandas as pd
import requests
from sqlalchemy import create_engine
from cleaning.Clean_Data import Clean

class DataLoader:
    def __init__(self):
        self.df = None

    def load_data(self, path, file_type="csv"):
        try:
            if file_type == "csv":
                self.df = pd.read_csv(path)
            elif file_type == "excel":
                self.df = pd.read_excel(path)
            elif file_type == "json":
                self.df = pd.read_json(path)
            else:
                raise ValueError("Unsupported file type.")
            print(f"Data loaded successfully from {file_type.upper()}!")
        except FileNotFoundError:
            print(f"File not found: {path}")
            self.df = None
        except ValueError as ve:
            print(f"Value error: {ve}")
            self.df = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = None

    def load_from_api(self, url):
        """Loads JSON data from an API endpoint"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                self.df = pd.DataFrame(data)

            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.df = pd.DataFrame(value)
                        break
            else:
                raise ValueError("Unsupported JSON format.")
            print(f"Data loaded successfully from API!")
        except Exception as e:
            print(f"Failed to load from API: {e}")
            self.df = None

    def load_from_mysql(self, user, password, host, database, query):
        """Loads data from MySQL using SQLAlchemy"""
        try:
            engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
            self.df = pd.read_sql_query(query, engine)
            print("Data loaded successfully from MySQL!")
        except Exception as e:
            print(f"Failed to load from MySQL: {e}")
            self.df = None

    def show_info(self):
        if self.df is not None:
            print("Head:")
            print(self.df.head())
            print("\nInfo:")
            print(self.df.info())
        else:
            print("No data loaded.")

    def clean(self, cleaner: Clean):
        if self.df is not None:
            self.df = cleaner.clean_dataframe(self.df)
            print("✨ Data cleaned!")
        else:
            print("⚠️ No data to clean.")
    def get_df(self):
        return self.df