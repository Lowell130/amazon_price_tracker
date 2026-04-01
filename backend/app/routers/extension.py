import os
import zipfile
import io
from fastapi import APIRouter, Response, Request
from fastapi.responses import StreamingResponse
from datetime import datetime

router = APIRouter(
    prefix="/api/extension",
    tags=["extension"]
)

# Dynamically find the project root and the extension path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EXTENSION_PATH = os.path.join(BASE_DIR, "amazon-extension")

@router.get("/download")
async def download_extension(request: Request):
    """
    Bundles the chrome extension into a ZIP file and returns it.
    It dynamically patches the API URL based on where the extension is being downloaded from.
    """
    # Detect the current base URL (e.g., http://localhost:8000 or https://pricehub.it)
    # We remove the trailing slash if present to match the hardcoded version
    scheme = request.url.scheme
    netloc = request.url.netloc
    current_base_url = f"{scheme}://{netloc}"
    
    # The hardcoded URL to replace
    LOCALHOST_URL = "http://127.0.0.1:8000"

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk(EXTENSION_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, EXTENSION_PATH)
                
                # Check if this is a file we want to patch
                if file in ["manifest.json", "popup.js", "popup.html"]:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        # Perform the replacement
                        patched_content = content.replace(LOCALHOST_URL, current_base_url)
                        
                        # Add to ZIP
                        zip_file.writestr(rel_path, patched_content)
                        continue
                    except Exception as e:
                        # Fallback to original file if something goes wrong
                        print(f"Error patching {file}: {e}")
                
                # Default: write the original file
                zip_file.write(file_path, rel_path)
        
        # Add a README.md with installation instructions
        readme_content = f"""# Amazon Price Tracker Extension - Guida all'installazione

Questa estensione ti permette di monitorare i prezzi direttamente su Amazon.
Questa versione è stata configurata per connettersi a: {current_base_url}

## Come installare:

1. Estrai il contenuto di questo file ZIP in una cartella sul tuo computer.
2. Apri Google Chrome e vai all'indirizzo `chrome://extensions/`.
3. In alto a destra, attiva la **Modalità sviluppatore** (Developer mode).
4. Clicca sul pulsante **Carica estensione non pacchettizzata** (Load unpacked) in alto a sinistra.
5. Seleziona la cartella dove hai estratto i file dell'estensione.
6. L'estensione apparirà nella tua lista e sarà pronta all'uso!

---
© PriceHub.it (Generato il {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
"""
        zip_file.writestr("README_INSTALLAZIONE.md", readme_content)

    # Seek to the beginning of the buffer
    zip_buffer.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="amazon-extension-pricehub.zip"'
    }
    
    return StreamingResponse(
        zip_buffer, 
        media_type="application/x-zip-compressed",
        headers=headers
    )
