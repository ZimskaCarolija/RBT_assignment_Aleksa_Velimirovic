# services/import_service.py
import logging
from typing import List
from dto import ImportResult
from utils.import_helper import clean_user_import_file,clean_entitlement_file,clean_vacation_records_file
from dto import CreateUserRequest,VacationRecordDTO,CreateVacationRequest,VacationEntitlement
from container import container
from models import VacationEntitlement
from datetime import datetime
logger = logging.getLogger(__name__)

class ImportService:
    def __init__(self, session):
        self.session = session
        self.user_service = container.user_service
        self.vacation_service = container.vacation_service  # Add to container

    def import_users_from_file(self, file, chunk_size: int = 100) -> ImportResult:
        result = ImportResult(
            success=True,
            message="",
            imported=0,
            errors=[],
            details={}
        )
        try:
            df = clean_user_import_file(file)
            total_rows = len(df)
            imported = 0
            errors = []

            for start in range(0, total_rows, chunk_size):
                chunk = df.iloc[start:start + chunk_size]

                for idx, row in chunk.iterrows():
                    email = row['email']
                    password = row['password']

                    try:
                        create_req = CreateUserRequest(
                            email=email,
                            password=password,
                        )
                    except Exception as e:
                        errors.append(f"Row {idx + 1}: Invalid data - {str(e)}")
                        continue

                    try:
                        user_dto = self.user_service.create_user(create_req)
                        imported += 1
                        logger.debug(f"Created user: {email} (ID: {user_dto.id})")
                    except ValueError as ve:
                        errors.append(f"Row {idx + 1}: {email} - {str(ve)}")
                    except Exception as e:
                        errors.append(f"Row {idx + 1}: {email} - Unexpected error: {str(e)}")

                try:
                    self.session.flush()
                except Exception as e:
                    self.session.rollback()
                    errors.append(f"Database error in chunk (rows {start+1}-{min(start+chunk_size, total_rows)}): {e}")
                    continue  # Continue to next chunk

            self.session.commit()

            result.imported = imported
            result.errors = errors[:50]
            result.details = {
                "total_processed": total_rows,
                "chunk_size": chunk_size
            }
            result.message = f"Imported {imported} out of {total_rows} users successfully."

        except Exception as e:
            self.session.rollback()
            result.success = False
            result.message = f"Import failed: {str(e)}"
            logger.error(f"User import error: {e}", exc_info=True)

        return result

    def import_vacation_records_from_file(self, file, chunk_size: int = 100) -> ImportResult:
        """
        Imports vacation records from file with calculated 'year' and 'days' columns.
        Uses existing repositories and VacationService for full validation.
        """
        result = ImportResult(
            success=True,
            message="",
            imported=0,
            errors=[],
            details={}
        )
        try:
            # 1. Clean file and calculate year + days
            df = clean_vacation_records_file(file)
            total_rows = len(df)
            imported = 0
            errors = []

            record_repo = container.vacation_record_repository
            entitlement_repo = container.vacation_entitlement_repository

            for start in range(0, total_rows, chunk_size):
                chunk = df.iloc[start:start + chunk_size]

                for idx, row in chunk.iterrows():
                    email = row['email']
                    start_date = row['start_date']
                    end_date = row['end_date']
                    year = row['year']
                    days = row['days']

                    user = container.user_repository.get_by_email(email)
                    if not user:
                        errors.append(f"Row {idx + 1}: User not found - {email}")
                        continue

                    if record_repo.has_overlap(user.id, start_date, end_date):
                        errors.append(f"Row {idx + 1}: Overlap for {email}: {start_date} - {end_date}")
                        continue

                    available_days = self.vacation_service.get_available_days(user.id,year)

                    if days > available_days:
                        errors.append(
                            f"Row {idx + 1}: Not enough days for {email}. "
                            f"Needed: {days}, Available: {available_days}"
                        )
                        continue

                    try:
                        req = CreateVacationRequest(
                            start_date=start_date,
                            end_date=end_date,
                            note="Imported from file"
                        )
                        self.vacation_service.create_vacation_record(user.id, req)
                        imported += 1
                    except ValueError as ve:
                        errors.append(f"Row {idx + 1}: {email} - {str(ve)}")
                    except Exception as e:
                        errors.append(f"Row {idx + 1}: {email} - DB error: {str(e)}")

                try:
                    self.session.flush()
                except Exception as e:
                    self.session.rollback()
                    errors.append(f"Chunk error (rows {start+1}-{min(start+chunk_size, total_rows)}): {e}")
                    continue

            self.session.commit()

            result.imported = imported
            result.errors = errors[:50]
            result.details = {
                "total_processed": total_rows,
                "chunk_size": chunk_size
            }
            result.message = f"Imported {imported} vacation records."

        except Exception as e:
            self.session.rollback()
            result.success = False
            result.message = f"Import failed: {str(e)}"
            logger.error(f"Vacation import error: {e}", exc_info=True)

        return result
    
def import_vacation_entitlements_from_file(self, file, chunk_size: int = 100) -> ImportResult:
        """
        Imports vacation entitlements from file:
        Vacation year 2021
        Employee Total vacation days
        user1@rbt.rs 20
        ...
        """
        result = ImportResult(
            success=True,
            message="",
            imported=0,
            errors=[],
            details={}
        )
        try:
            # 1. Clean file and extract year + total_days
            df, year = clean_entitlement_file(file)
            total_rows = len(df)
            imported = 0
            errors = []

            entitlement_repo = container.vacation_entitlement_repository

            for start in range(0, total_rows, chunk_size):
                chunk = df.iloc[start:start + chunk_size]

                for idx, row in chunk.iterrows():
                    email = row['email']
                    total_days = int(row['total_days'])

                    # Find user
                    user = container.user_repository.get_by_email(email)
                    if not user:
                        errors.append(f"Row {idx + 3}: User not found - {email}")
                        continue

                    # Get or create entitlement
                    try:
                        existing = entitlement_repo.get_by_user_year(user.id, year)
                        if existing:
                            if existing.total_days != total_days:
                                existing.total_days = total_days
                                existing.updated_at = datetime.now(datetime.timezone.utc)
                            imported += 1
                        else:
                            entitlement = entitlement_repo.create_vacation_entitlement(
                                user_id=user.id,
                                year=year,
                                total_days=total_days
                            )
                            self.session.add(entitlement)
                            imported += 1
                    except Exception as e:
                        errors.append(f"Row {idx + 3}: DB error for {email} - {str(e)}")

                try:
                    self.session.flush()
                except Exception as e:
                    self.session.rollback()
                    errors.append(f"Chunk error (rows {start+3}-{min(start+chunk_size+2, total_rows+2)}): {e}")
                    continue

            self.session.commit()

            result.imported = imported
            result.errors = errors[:50]
            result.details = {
                "year": year,
                "total_processed": total_rows
            }
            result.message = f"Imported {imported} entitlements for year {year}."

        except Exception as e:
            self.session.rollback()
            result.success = False
            result.message = f"Import failed: {str(e)}"
            logger.error(f"Entitlement import error: {e}", exc_info=True)

        return result