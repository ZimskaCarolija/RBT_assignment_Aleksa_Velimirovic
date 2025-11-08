import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_user_import_file(file) -> pd.DataFrame:
    """
    Expects a file where each row contains:
    email    password
    Returns a cleaned DataFrame with columns: [email, password]
    """
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, header=None)
        else:
            df = pd.read_csv(file, header=None, sep=r'\s+', engine='python', on_bad_lines='skip')

        if df.empty:
            raise ValueError("File is empty")

        if df.shape[1] < 2:
            raise ValueError("Each row must contain email and password (2 columns)")

        df = df.iloc[:, :2].copy()
        df.columns = ['email', 'password']

        df['email'] = df['email'].astype(str).str.strip().str.lower()
        df['password'] = df['password'].astype(str).str.strip()

        df = df[df['email'] != '']
        df = df[df['password'] != '']
        df = df[df['email'].str.contains('@', na=False)]

        if df.empty:
            raise ValueError("No valid users found after cleaning")

        df = df.reset_index(drop=True)
        logger.info(f"Cleaned {len(df)} users from file {file.filename}")
        return df

    except Exception as e:
        logger.error(f"Error cleaning file: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")
    

def clean_vacation_records_file(file) -> pd.DataFrame:
    """
    Cleans vacation file and adds:
    - 'year': start_date.year
    - 'days': (end_date - start_date).days + 1
    """
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, header=None)
        else:
            df = pd.read_csv(file, header=None, sep=r'\s{2,}', engine='python', on_bad_lines='skip')

        if df.empty or df.shape[1] < 3:
            raise ValueError("File must have at least 3 columns: email, start_date, end_date")

        df = df.iloc[:, :3].copy()
        df.columns = ['email', 'start_date_str', 'end_date_str']

        # Clean email
        df['email'] = df['email'].astype(str).str.strip().str.lower()

        # Parse dates
        def parse_date(date_str):
            date_str = str(date_str).strip()
            for fmt in (
                "%A, %B %d, %Y",
                "%A, %d %B %Y",
                "%Y-%m-%d",
                "%d/%m/%Y"
            ):
                try:
                    return datetime.strptime(date_str, fmt).date()
                except:
                    continue
            raise ValueError(f"Invalid date: {date_str}")

        df['start_date'] = df['start_date_str'].apply(parse_date)
        df['end_date'] = df['end_date_str'].apply(parse_date)

        # Calculate year and days
        df['year'] = df['start_date'].apply(lambda d: d.year)
        df['days'] = (df['end_date'] - df['start_date']).dt.days + 1

        # Validate
        if (df['days'] < 1).any():
            raise ValueError("End date must be on or after start date")

        df = df[df['email'].str.contains('@', na=False)]
        df = df.reset_index(drop=True)

        logger.info(f"Cleaned {len(df)} vacation records with year and days")
        return df

    except Exception as e:
        logger.error(f"Error cleaning vacation file: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")
    
def clean_entitlement_file(file) -> tuple[pd.DataFrame, int]:
    """
    Cleans entitlement file:
    Vacation year 2021
    Employee Total vacation days
    user1@rbt.rs 20
    ...
    Returns (DataFrame with email/total_days, year)
    """
    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, header=None)
        else:
            df = pd.read_csv(file, header=None, sep=r'\s{2,}', engine='python', on_bad_lines='skip')

        if df.empty or df.shape[1] < 2:
            raise ValueError("File must have at least 2 columns")

        # 1. Extract year from first row
        first_row = str(df.iloc[0, 0])
        if not first_row.startswith("Vacation year"):
            raise ValueError("First row must be 'Vacation year YYYY'")
        try:
            year = int(first_row.split()[-1])
        except:
            raise ValueError("Invalid year in first row")

        # 2. Skip first two rows (header)
        data_df = df.iloc[2:].copy()
        data_df = data_df.iloc[:, :2]
        data_df.columns = ['email', 'total_days']

        # 3. Clean
        data_df['email'] = data_df['email'].astype(str).str.strip().str.lower()
        data_df['total_days'] = pd.to_numeric(data_df['total_days'], errors='coerce')

        # 4. Validate
        if data_df['total_days'].isna().any():
            raise ValueError("Invalid total_days value")
        if not data_df['email'].str.contains('@', na=False).all():
            raise ValueError("Invalid email format")

        data_df = data_df.reset_index(drop=True)
        logger.info(f"Cleaned {len(data_df)} entitlements for year {year}")
        return data_df, year

    except Exception as e:
        logger.error(f"Error cleaning entitlement file: {e}")
        raise ValueError(f"Invalid file format: {str(e)}")