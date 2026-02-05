# P6 – Insufficient Deletion of User Data

## Summary

Failure to properly delete user data on request or when no longer needed. Data persists in backups, logs, or third parties.

## Prevention

Implement secure deletion (including backups and replicas); honor deletion requests within SLA. Map data flows and storage; purge from all systems and processors; document process.

## Examples

### Wrong - Incomplete deletion

```python
@app.delete("/api/users/{user_id}/delete")
def delete_user(user_id: str):
    # Only deletes from main database
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return {"status": "deleted"}
    # Data still in: analytics, backups, search index, logs, third parties
```

### Right - Comprehensive deletion across all systems

```python
from dataclasses import dataclass
from typing import List

@dataclass
class DeletionResult:
    system: str
    status: str
    
def delete_user_data(user_id: str) -> List[DeletionResult]:
    results = []
    
    # 1. Primary database
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    results.append(DeletionResult("primary_db", "deleted"))
    
    # 2. Analytics database - anonymize or delete
    analytics_db.execute(
        "UPDATE events SET user_id = 'deleted' WHERE user_id = :uid",
        {"uid": user_id}
    )
    results.append(DeletionResult("analytics", "anonymized"))
    
    # 3. Search index
    search_index.delete(doc_id=f"user_{user_id}")
    results.append(DeletionResult("search_index", "deleted"))
    
    # 4. Cache
    cache.delete(f"user:{user_id}:*")
    results.append(DeletionResult("cache", "deleted"))
    
    # 5. Third-party services
    for service in THIRD_PARTY_PROCESSORS:
        service.request_deletion(user_id)
        results.append(DeletionResult(service.name, "requested"))
    
    # 6. Schedule backup purge
    backup_scheduler.schedule_deletion(user_id, delay_days=30)
    results.append(DeletionResult("backups", "scheduled"))
    
    # 7. Log deletion request for audit
    audit_log.record("user_deletion", user_id=user_id, results=results)
    
    return results

@app.delete("/api/users/{user_id}/delete")
def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403)
    
    results = delete_user_data(user_id)
    
    return {
        "status": "deletion_initiated",
        "results": [{"system": r.system, "status": r.status} for r in results],
        "complete_by": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
```

### Right - Data retention policy enforcement

```python
from datetime import datetime, timedelta

class DataRetentionService:
    RETENTION_PERIODS = {
        "user_data": timedelta(days=0),      # Delete immediately
        "order_history": timedelta(days=365), # Keep for 1 year (legal)
        "logs": timedelta(days=90),           # Keep for 90 days
        "backups": timedelta(days=30),        # Purge after 30 days
    }
    
    def process_deletion_request(self, user_id: str):
        deletion_date = datetime.utcnow()
        
        # Immediate deletions
        self.delete_user_profile(user_id)
        self.delete_preferences(user_id)
        
        # Scheduled deletions (legal retention requirements)
        for data_type, retention in self.RETENTION_PERIODS.items():
            scheduled_date = deletion_date + retention
            DeletionQueue.add(
                user_id=user_id,
                data_type=data_type,
                delete_after=scheduled_date
            )
        
        return {
            "immediate": ["profile", "preferences"],
            "scheduled": {
                dt: str(deletion_date + ret)
                for dt, ret in self.RETENTION_PERIODS.items()
            }
        }
```

### Deletion checklist

| System | Action | Timeline |
|--------|--------|----------|
| Primary database | Hard delete | Immediate |
| Analytics | Anonymize or delete | Immediate |
| Search index | Remove documents | Immediate |
| Cache/Redis | Invalidate keys | Immediate |
| Object storage | Delete files | Immediate |
| Third parties | Request deletion | Per DPA |
| Backups | Scheduled purge | 30 days |
| Logs | Anonymize user_id | 90 days |

## Testing

Request deletion and verify data is removed from primary and backup storage; check third-party processors.
