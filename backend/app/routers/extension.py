import os
import zipfile
import io
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from datetime import datetime

router = APIRouter(
    prefix="/extension",
    tags=["extension"]
)

# Dynamically find the project root and the extension path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EXTENSION_PATH = os.path.join(BASE_DIR, "amazon-extension")

@router.get("/download")
async def download_extension():
    """
    Bundles the chrome extension into a ZIP file and returns it.
    """
    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk(EXTENSION_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                # Create a relative path for the file in the ZIP
                rel_path = os.path.relpath(file_path, EXTENSION_PATH)
                zip_file.write(file_path, rel_path)
        
        # Add a README.md with installation instructions
        readme_content = """# Amazon Price Tracker Extension - Guida all'installazione

Questa estensione ti permette di monitorare i prezzi direttamente su Amazon.

## Come installare:

1. Estrai il contenuto di questo file ZIP in una cartella sul tuo computer.
2. Apri Google Chrome e vai all'indirizzo `chrome://extensions/`.
3. In alto a destra, attiva la **Modalità sviluppatore** (Developer mode).
4. Clicca sul pulsante **Carica estensione non pacchettizzata** (Load unpacked) in alto a sinistra.
5. Seleziona la cartella dove hai estratto i file dell'estensione.
6. L'estensione apparirà nella tua lista e sarà pronta all'uso!

---
© PriceHub.it
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
