
import uvicorn
from app.main import app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Lê a porta do ambiente (Render usa $PORT)
    uvicorn.run(app, host="0.0.0.0", port=port) 