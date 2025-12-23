from sqlalchemy.orm import Session
from core.models import Asset


def get_assets(
    db: Session,
    limit: int = 10,
    offset: int = 0
):
    return (
        db.query(Asset)
        .order_by(Asset.updated_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
