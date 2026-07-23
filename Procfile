# Railway injects PORT; domain targetPort must match (pinned to 8080).
web: gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 4 --timeout 120
