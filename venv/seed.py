import os
import django
import random

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orders.models import UnindexedOrder, IndexedOrder

def seed_database():
    statuses = ['pending', 'processing', 'completed', 'cancelled']
    domains = ['gmail.com', 'yahoo.com', 'enterprise.io', 'techcorp.org']
    plans = ['free', 'pro', 'enterprise']
    
    unindexed_batch = []
    indexed_batch = []

    print("Generating 50,000 records for each model...")
    for i in range(50000):
        email = f"user_{i % 1500}@{random.choice(domains)}"
        status = random.choice(statuses)
        meta = {
            "plan": random.choice(plans),
            "active": True,
            "region": random.choice(["US", "EU", "AP"])
        }

        unindexed_batch.append(UnindexedOrder(customer_email=email, status=status, metadata=meta))
        indexed_batch.append(IndexedOrder(customer_email=email, status=status, metadata=meta))

    print("Bulk inserting into UnindexedOrder table...")
    UnindexedOrder.objects.bulk_create(unindexed_batch, batch_size=5000)

    print("Bulk inserting into IndexedOrder table...")
    IndexedOrder.objects.bulk_create(indexed_batch, batch_size=5000)

    print("Database seeding successfully completed!")

if __name__ == '__main__':
    seed_database()
