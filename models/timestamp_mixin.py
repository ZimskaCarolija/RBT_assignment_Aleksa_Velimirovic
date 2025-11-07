from datetime import datetime, timezone
from . import db

class TimestampMixin:
    created_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime, 
        default=lambda: None,  
        onupdate=lambda: datetime.now(timezone.utc) 
    )
    deleted_at = db.Column(db.DateTime, nullable=True)
