import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orders.models import UnindexedOrder, IndexedOrder

def run_benchmarks():
    print("=" * 60)
    print("1. B-TREE INDEX: Single Column Lookup (customer_email)")
    print("=" * 60)
    print("\n--- UNINDEXED EMAIL LOOKUP ---")
    print(UnindexedOrder.objects.filter(customer_email="user_42@gmail.com").explain(analyze=True))
    
    print("\n--- INDEXED EMAIL LOOKUP (B-Tree) ---")
    print(IndexedOrder.objects.filter(customer_email="user_42@gmail.com").explain(analyze=True))

    print("\n" + "=" * 60)
    print("2. COMPOSITE INDEX: Filtering + Sorting (status & -created_at)")
    print("=" * 60)
    print("\n--- UNINDEXED COMPOSITE LOOKUP ---")
    print(UnindexedOrder.objects.filter(status="completed").order_by("-created_at")[:10].explain(analyze=True))

    print("\n--- INDEXED COMPOSITE LOOKUP ---")
    print(IndexedOrder.objects.filter(status="completed").order_by("-created_at")[:10].explain(analyze=True))

    # print("\n" + "=" * 60)
    # print("3. GIN INDEX: JSONB Metadata Field Lookup (metadata__plan)")
    # print("=" * 60)
    # print("\n--- UNINDEXED JSONB LOOKUP ---")
    # print(UnindexedOrder.objects.filter(metadata__plan="enterprise").explain(analyze=True))

    # print("\n--- INDEXED JSONB LOOKUP (GIN) ---")
    # print(IndexedOrder.objects.filter(metadata__plan="enterprise").explain(analyze=True))

    print("\n" + "=" * 60)
    print("3. GIN INDEX: JSONB Metadata Field Lookup (metadata__contains)")
    print("=" * 60)
    print("\n--- UNINDEXED JSONB LOOKUP ---")
    print(UnindexedOrder.objects.filter(metadata__contains={'plan': 'enterprise'}).explain(analyze=True))

    print("\n--- INDEXED JSONB LOOKUP (GIN) ---")
    print(IndexedOrder.objects.filter(metadata__contains={'plan': 'enterprise'}).explain(analyze=True))

if __name__ == '__main__':
    run_benchmarks()
