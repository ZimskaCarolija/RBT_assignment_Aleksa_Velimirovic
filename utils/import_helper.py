# utils/import_helper.py
import pandas as pd
import logging
from datetime import datetime
from typing import Tuple

logger = logging.getLogger(__name__)

def clean_user_import_file(file_path: str) -> pd.DataFrame:
    """
    Vacation year,2019
    Employee Email,Employee Password
    user1@rbt.rs,Abc!@#$
    ...
    """
    try:
        df = load_dataframe(file_path)

        if df.empty:
            raise ValueError("File is empty")
        if df.shape[0] < 3:
            raise ValueError("File must have at least 3 rows (header + data)")
        df = df.iloc[2:].copy()

        df = df.iloc[:, :2].copy()
        df.columns = ['email', 'password']

        df['email'] = df['email'].astype(str).str.strip().str.lower()
        df['password'] = df['password'].astype(str).str.strip()

        df['full_name'] = df['email'].str.split('@').str[0].str.replace('.', ' ').str.replace('_', ' ').str.title()

        df = df[df['email'].str.contains('@', na=False)]
        df = df[df['email'] != '']
        df = df[df['password'] != '']

        if df.empty:
            raise ValueError("No valid users found after cleaning")

        df = df[['email', 'full_name', 'password']].reset_index(drop=True)
        logger.info(f"Cleaned {len(df)} users from {file_path}")
        return df

    except Exception as e:
        logger.error(f"Error cleaning file {file_path}: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")


def clean_vacation_records_file(file_path: str) -> pd.DataFrame:
    """
    return df with ['email', 'start_date', 'end_date', 'year', 'days']
    """
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, header=None)
        else:
            df = pd.read_csv(
                file_path,
                header=None,
                sep=',',
                engine='python',
                on_bad_lines='skip',
                encoding='utf-8',
                skipinitialspace=True  
            )

        if df.empty:
            raise ValueError("File is empty or no data could be parsed")

        if df.shape[1] < 3:
            raise ValueError("File must have at least 3 columns: email, start_date, end_date")

        df = df.iloc[1:, :3].copy()
        if df.empty:
            raise ValueError("No data rows after skipping header")

        df.columns = ['email', 'start_date_str', 'end_date_str']

        df['email'] = df['email'].astype(str).str.strip().str.lower()

        def parse_date(date_str):
            date_str = str(date_str).strip()
            formats = (
                "%A, %B %d, %Y",  # 'Friday, August 30, 2019'
                "%A, %d %B %Y",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d.%m.%Y",
                "%m/%d/%Y"
            )
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt) 
                except ValueError:
                    continue
            raise ValueError(f"Invalid date: {date_str}")

        df['start_date'] = pd.to_datetime(df['start_date_str'].apply(parse_date))
        df['end_date'] = pd.to_datetime(df['end_date_str'].apply(parse_date))

        df['year'] = df['start_date'].dt.year
        df['days'] = (df['end_date'] - df['start_date']).dt.days + 1 

        if (df['days'] < 1).any():
            raise ValueError("End date must be on or after start date")

        df = df[df['email'].str.contains('@', na=False)]
        df = df[['email', 'start_date', 'end_date', 'year', 'days']]
        df = df.reset_index(drop=True)

        logger.info(f"Cleaned {len(df)} vacation records from {file_path}")
        return df

    except Exception as e:
        logger.error(f"Error cleaning vacation file {file_path}: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")

def clean_entitlement_file(file_path: str) -> Tuple[pd.DataFrame, int]:
    """
    returns : (DataFrame with ['email', 'total_days'], year)
    """
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, header=None)
        else:
            df = pd.read_csv(
                file_path,
                header=None,
                sep=',',
                engine='python',
                on_bad_lines='skip',
                encoding='utf-8'
            )

        if df.empty or df.shape[1] < 2:
            raise ValueError("File must have at least 2 columns")

        header_cell = str(df.iloc[0, 0]).strip().lower()
        if not header_cell.startswith("vacation year"):
            raise ValueError("First row must start with 'Vacation year'")

        try:
            year = int(df.iloc[0, 1]) 
        except (ValueError, TypeError):
            raise ValueError("Invalid year in first row, second column")

        data_df = df.iloc[2:, :2].copy()
        if data_df.empty:
            raise ValueError("No data rows found")

        data_df.columns = ['email', 'total_days']
        data_df = data_df.dropna(how='all').reset_index(drop=True)

        data_df['email'] = data_df['email'].astype(str).str.strip().str.lower()
        data_df['total_days'] = pd.to_numeric(data_df['total_days'], errors='coerce')

        if data_df['total_days'].isna().any():
            raise ValueError("Some total_days values are not numeric")
        if not data_df['email'].str.contains('@', na=False).all():
            raise ValueError("Some emails are invalid (missing @)")

        logger.info(f"Cleaned {len(data_df)} entitlements for year {year} from {file_path}")
        return data_df, year

    except Exception as e:
        logger.error(f"Error cleaning entitlement file {file_path}: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")
    
def load_dataframe(file_path: str) -> pd.DataFrame:
    """
    Učitava CSV ili XLSX fajl.
    Podržava: .csv (zarez), .xlsx
    Vraća: pd.DataFrame (bez header-a)
    """
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path, header=None)
    elif file_path.endswith('.csv'):
        return pd.read_csv(
            file_path,
            header=None,
            sep=',',
            engine='python',
            on_bad_lines='skip'
        )
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")