from django.db import models
from django.contrib.postgres.indexes import GinIndex

class UnindexedOrder(models.Model):
    customer_email = models.EmailField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

class IndexedOrder(models.Model):
    customer_email = models.EmailField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [
            # Standard B-Tree index on email
            models.Index(fields=['customer_email'], name='idx_customer_email'),
            
            # Composite index for status + creation date
            models.Index(fields=['status', '-created_at'], name='idx_status_created'),
            
            # GIN index for fast JSONB querying in PostgreSQL
            GinIndex(fields=['metadata'], name='idx_order_metadata_gin'),
        ]
