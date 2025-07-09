import pandas as pd

class Clean:
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df.columns = df.columns.str.strip()

        df = df.dropna(how='any')

        columns_to_drop = []

        for col in df.columns:


            if pd.api.types.is_string_dtype(df[col]):

                stripped_col = df[col].astype(str).str.strip()


                empty_ratio = (stripped_col == "").mean()

                if empty_ratio > 0.7:
                    columns_to_drop.append(col)
                    continue


                df[col] = stripped_col.str.capitalize()

            elif pd.api.types.is_numeric_dtype(df[col]):
                if df[col].isnull().mean() > 0.7:
                    columns_to_drop.append(col)
                    continue


                mean_val = df[col].mean()
                df[col] = df[col].fillna(mean_val)


        df.drop(columns=columns_to_drop, inplace=True)
        if columns_to_drop:
            print(f"🗑️ Dropped columns with >70% missing: {columns_to_drop}")

        return df


if __name__ == '__main__':
    Clean().clean_dataframe(pd.read_csv(r"C:\Users\shuki\Desktop\Naivebayse\all_star.csv"))