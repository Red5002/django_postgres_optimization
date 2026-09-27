# Django ORM & PostgreSQL Indexing Benchmarks

This repository contains a performance benchmarking suite built to evaluate execution time, query plan shifts, and buffer hits in Django ORM when querying unindexed vs. indexed PostgreSQL tables across **50,000 records**.

It covers single-column B-Tree indexes, composite indexes for filter-and-sort patterns, and PostgreSQL `JSONB` GIN indexes, analyzing each query with `EXPLAIN ANALYZE`.

---

## 📊 Benchmark Summary

| Test Scenario | Query Type | Unindexed Plan | Indexed Plan | Unindexed Time | Indexed Time | Speedup Factor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. B-Tree Index** | Single Column (`customer_email`) | `Seq Scan` | `Bitmap Index Scan` | **81.73 ms** | **2.69 ms** | **~30x Faster** |
| **2. Composite Index** | Filter + Sort (`status`, `-created_at`) | `Seq Scan` + `Sort` | `Index Scan` | **53.00 ms** | **0.76 ms** | **~70x Faster** |
| **3. GIN (Low Selectivity)** | `JSONB` Match (33.5% of dataset) | `Seq Scan` | `Bitmap Index Scan` | **79.36 ms** | **109.37 ms** | **~37% Slower** |
| **4. GIN (High Selectivity)**| `JSONB` Match (11.1% of dataset) | `Seq Scan` | `Bitmap Index Scan` | **132.93 ms** | **96.41 ms** | **~27% Faster** |

---

## 🚀 Key Takeaways

1. **B-Tree Lookups ($O(\log N)$):** Dropped shared buffer hits from **845 blocks** to **9 blocks** on single-column equality lookups.
2. **Composite Sorting:** Matching index direction (`status`, `-created_at`) eliminated in-memory `Top-N Heapsort` operations entirely, streaming sorted results straight from disk blocks.
3. **Django GIN Traps:** Direct ORM lookups like `metadata__plan="enterprise"` generate SQL equality (`->`) which bypasses standard GIN indexes. You must use `__contains` to trigger the `@>` containment operator.
4. **The Selectivity Threshold:** When a query matches >10–20% of total table records, constructing an in-memory index bitmap adds more overhead than a sequential table scan.

---

## 🛠️ Project Structure

```text
├── config/             # Django project configuration
├── orders/             # Application containing Indexed & Unindexed models
│   ├── models.py       # Model definitions and index declarations
│   └── migrations/     # Generated migrations
├── seed.py             # Script to bulk-insert 50,000 records per model
├── benchmark.py        # EXPLAIN ANALYZE execution suite
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

## Tech Stack & Prerequisites
​Python: 3.12+
​Framework: Django 6.1+
​Database: PostgreSQL 18+
​Database Driver: psycopg2-binary
​⚡ Quickstart & Setup

​1. Clone & Environment Setup

git clone [https://github.com/your-username/django-postgres-optimization.git](https://github.com/your-username/django-postgres-optimization.git)
cd django-postgres-optimization

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Configure Database Connection
​Update config/settings.py with your local PostgreSQL credentials:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_opt_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

3. Run Migrations & Seed Data

python manage.py makemigrations orders
python manage.py migrate

# Seeds 50,000 records into both UnindexedOrder and IndexedOrder tables
python seed.py

4. Run Benchmarks

python benchmark.py

License
​Distributed under the MIT License.
