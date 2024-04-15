from datetime import datetime


def datetime_to_iso(dt):
    return dt.isoformat() if isinstance(dt, datetime) else dt


def serialize_banners(banners):
    return [{
        '_id': banner['_id'] if isinstance(banner['_id'], int) else banner.get("prev_id"),
        'tag_ids': banner['tag_ids'],
        'feature_id': banner['feature_id'],
        'content': banner['content'],
        'is_active': banner['is_active'],
        'created_at': datetime_to_iso(banner['created_at']),
        'updated_at': datetime_to_iso(banner['updated_at'])
    } for banner in banners]
