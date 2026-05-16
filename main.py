import os
from cloudlink import server

if __name__ == "__main__":
    # Instantiate the server object directly using the updated module format
    server_app = server()
    
    # Grab the port dynamically from Render's environment
    port = int(os.environ.get("PORT", 3000))
    
    # Run the server
    server_app.run(ip="0.0.0.0", port=port)
