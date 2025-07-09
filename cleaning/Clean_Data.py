import pandas as pd

class Clean:
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        ניקוי בסיסי:
        - הסרת רווחים משמות עמודות
        - ניקוי ערכי טקסט: הסרת רווחים והכנסת אות ראשונה גדולה
        - הסרת שורות עם ערכי null בכלל
        - מילוי ערכים חסרים בעמודות מספריות (אם נשארו)
        """

        df = df.copy()

        # ניקוי שמות עמודות
        df.columns = df.columns.str.strip()

        # הסרת שורות עם כל null (לפי דרישתך)
        df = df.dropna(how='any')

        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip().str.capitalize()
            elif pd.api.types.is_numeric_dtype(df[col]):
                if df[col].isnull().any():
                    mean_val = df[col].mean()
                    df[col] = df[col].fillna(mean_val)

        return df
