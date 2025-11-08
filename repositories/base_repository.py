from typing import TypeVar, Generic, List, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime

T = TypeVar('T')

class BaseRepository(Generic[T]):

    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    
    def get_all(self, active_only: bool = True) -> List[T]:
        query = self.session.query(self.model)
        if active_only:
            if hasattr(self.model, 'is_deleted'):
                query = query.filter(self.model.is_deleted.is_(False))
            if hasattr(self.model, 'deleted_at'):
                query = query.filter(self.model.deleted_at.is_(None))
        return query.all()

    def soft_delete(self, obj: T) -> T:
        if hasattr(obj, 'is_deleted'):
            obj.is_deleted = True
        if hasattr(obj, 'deleted_at'):
            obj.deleted_at = datetime.utcnow()
        return obj

    def restore(self, obj: T) -> T:
        if hasattr(obj, 'is_deleted'):
            obj.is_deleted = False
        if hasattr(obj, 'deleted_at'):
            obj.deleted_at = None
        return obj