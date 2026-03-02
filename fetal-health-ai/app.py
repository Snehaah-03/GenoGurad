from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BiochemicalData(BaseModel):
    hcg: float
    pappa: float
    afp: float
    urine_protein: float

@app.post("/analyze-biochemical")
async def analyze_biochemical(data: BiochemicalData):
    # Simulate processing delay
    time.sleep(1.2)
    
    # Simple risk logic (Simulation)
    risk_score = 0
    
    if data.hcg > 150000: risk_score += 15
    if data.pappa < 0.4: risk_score += 25
    if data.afp > 100: risk_score += 12
    if data.urine_protein > 1.0: risk_score += 5
    
    # Add some randomness for simulation
    risk_score += random.uniform(2, 8)
    
    risk_level = "Low"
    if risk_score > 35: risk_level = "Medium"
    if risk_score > 60: risk_level = "High"
    
    findings = []
    if risk_level == "Low":
        findings = [
            "HCG & PAPP-A levels reflect healthy development.",
            "Marker AFP is within typical pregnancy parameters.",
            "Placental health: Excellent.",
            "Lowered risk for Trisomy 21 (Down Syndrome) and 18 (Edward's Syndrome)."
        ]
    elif risk_level == "Medium":
        findings = [
            "Markers show some variations from the average range.",
            "Increased nuchal translucency markers could be present.",
            "Recommended: Follow-up with a genetic counselor.",
            "Second trimester screening might provide more clarity."
        ]
    else:
        findings = [
            "Biochemical markers are significantly outside the expected range.",
            "Strong indication for potential genetic disorder.",
            "High priority: Amniocentesis or CVS follow-up required.",
            "Ultrasound should focus on nuchal thickness and nasal bone presence."
        ]

    return {
        "riskScore": min(risk_score, 100),
        "riskLevel": risk_level,
        "findings": findings
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
