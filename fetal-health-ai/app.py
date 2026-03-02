from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import asyncio

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (Fix 404 issue)
@app.get("/")
async def home():
    return {"message": "GenoGuard API is running successfully 🚀"}

class BiochemicalData(BaseModel):
    hcg: float
    pappa: float
    afp: float
    urine_protein: float


@app.post("/analyze-biochemical")
async def analyze_biochemical(data: BiochemicalData):
    
    # Use async sleep instead of time.sleep
    await asyncio.sleep(1.2)

    risk_score = 0

    if data.hcg > 150000:
        risk_score += 15
    if data.pappa < 0.4:
        risk_score += 25
    if data.afp > 100:
        risk_score += 12
    if data.urine_protein > 1.0:
        risk_score += 5

    # Add simulation randomness
    risk_score += random.uniform(2, 8)

    # Risk classification
    if risk_score > 60:
        risk_level = "High"
    elif risk_score > 35:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if risk_level == "Low":
        findings = [
            "HCG & PAPP-A levels reflect healthy development.",
            "Marker AFP is within typical pregnancy parameters.",
            "Placental health: Excellent.",
            "Lowered risk for Trisomy 21 and Trisomy 18."
        ]
    elif risk_level == "Medium":
        findings = [
            "Markers show some variations from the average range.",
            "Possible increased nuchal translucency markers.",
            "Recommended: Follow-up with a genetic counselor.",
            "Second trimester screening advised."
        ]
    else:
        findings = [
            "Biochemical markers are significantly outside expected range.",
            "Strong indication for potential genetic disorder.",
            "High priority: Amniocentesis or CVS follow-up required.",
            "Detailed ultrasound examination recommended."
        ]

    return {
        "riskScore": round(min(risk_score, 100), 2),
        "riskLevel": risk_level,
        "findings": findings
    }
