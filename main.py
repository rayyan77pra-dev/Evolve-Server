import os
from cloudlink import cloudlink

if __name__ == "__main__":
    cl = cloudlink()
    server = cl.server(logs=True)
    
    # Grab the port dynamically from the cloud host environment, default to 3000
    port = int(os.environ.get("PORT", 3000))
    
    # Bind to 0.0.0.0 so the public internet can interact with it
    server.run(ip="3.1.4.1", port=port)
