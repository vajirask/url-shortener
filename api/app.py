from flask import Flask, request, redirect, jsonify
import psycopg2
import redis
import string
import random
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'urlshortener'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

# Redis connection
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            short_code VARCHAR(10) UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Generate random short code
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def home():
    return jsonify({"message": "URL Shortener API is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
        (short_code, original_url)
    )
    conn.commit()
    cur.close()
    conn.close()

    # Cache it
    redis_client.set(short_code, original_url)

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}",
        "original_url": original_url
    })

@app.route('/<short_code>')
def redirect_url(short_code):
    # Check cache first
    cached_url = redis_client.get(short_code)
    if cached_url:
        return redirect(cached_url)

    # If not in cache, check database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        original_url = result[0]
        redis_client.set(short_code, original_url)
        return redirect(original_url)

    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)