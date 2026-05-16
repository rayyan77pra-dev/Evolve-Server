import os
from cloudlink import server

if __name__ == "__main__":
    server_app = server()
    
    # Render explicitly requires reading its assigned PORT environment variable
    # If it is missing, fallback to 10000 (Render's default fallback port)
    port = int(os.environ.get("PORT", 10000))
    
    # Bind directly to 0.0.0.0 so Render's internal proxy maps it to your public URL
    server_app.run(ip="0.0.0.0", port=port)
