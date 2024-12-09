#Anaconda prompt: 

#conda activate webapi
#cd C:\Projects_WebDiv\backend_Uebung02\api
#fastapi dev 01transformer.py

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from pyproj import Transformer
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für die Entwicklung offen lassen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Transformer für die Koordinatentransformation
wgs84_to_lv95 = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)

@app.post("/transform-csv/")
async def transform_csv(file: UploadFile = File(...)):
    """
    CSV-Datei mit WGS84-Koordinaten hochladen und transformieren.
    """
    try:
        # CSV lesen
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Überprüfen, ob notwendige Spalten vorhanden sind
        if "lng" not in df.columns or "lat" not in df.columns:
            raise HTTPException(
                status_code=400, detail="CSV muss die Spalten 'lng' und 'lat' enthalten."
            )

        # Transformation durchführen
        transformed = df.copy()
        transformed["east"], transformed["north"] = wgs84_to_lv95.transform(
            transformed["lng"].values, transformed["lat"].values
        )

        # Transformierte CSV erstellen
        output = io.StringIO()
        transformed.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=transformed_coordinates.csv"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler bei der Verarbeitung: {e}")
