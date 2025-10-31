from db import engine

try:
    conn = engine.connect()
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed:",e)