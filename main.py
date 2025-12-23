from fastapi import FastAPI, Depends, HTTPException, Header
from enum import Enum
import time

app = FastAPI(
    title="Trade Opportunities API",
    description="AI-powered market analysis for Indian sectors",
    version="1.0.0"
)

# -------------------------------
# Input Validation
# -------------------------------
class SectorEnum(str, Enum):
    pharmaceuticals = "pharmaceuticals"
    technology = "technology"
    agriculture = "agriculture"


# -------------------------------
# Authentication (Simple)
# -------------------------------
def verify_user(authorization: str = Header(default="guest")):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization


# -------------------------------
# Rate Limiting (In-Memory)
# -------------------------------
RATE_LIMIT = {}
MAX_REQUESTS = 5
WINDOW_SECONDS = 60

def rate_limit(user_id: str = Depends(verify_user)):
    now = time.time()
    RATE_LIMIT.setdefault(user_id, [])

    RATE_LIMIT[user_id] = [
        t for t in RATE_LIMIT[user_id] if now - t < WINDOW_SECONDS
    ]

    if len(RATE_LIMIT[user_id]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    RATE_LIMIT[user_id].append(now)


# -------------------------------
# Market Data Collection (Mock)
# -------------------------------
async def fetch_market_data(sector: str) -> str:
    return f"Latest Indian market trends, news, and policies related to {sector} sector."


# -------------------------------
# AI Analysis (Gemini Placeholder)
# -------------------------------
async def analyze_sector(sector: str, data: str) -> dict:
    # Gemini / LLM API can be integrated here
    return {
        "opportunities": [
            "Growing export demand",
            "Government policy support"
        ],
        "risks": [
            "Regulatory uncertainty",
            "Global market volatility"
        ],
        "outlook": "The sector shows positive growth potential over the next 6–12 months."
    }


# -------------------------------
# Markdown Report Generator
# -------------------------------
def generate_md_report(sector: str, analysis: dict) -> str:
    return f"""
# 📊 {sector.title()} Sector Trade Analysis

## 🚀 Opportunities
- {analysis['opportunities'][0]}
- {analysis['opportunities'][1]}

## ⚠️ Risks
- {analysis['risks'][0]}
- {analysis['risks'][1]}

## 📈 Market Outlook
{analysis['outlook']}
"""


# -------------------------------
# Main API Endpoint
# -------------------------------
@app.get("/analyze/{sector}")
async def analyze_sector_api(
    sector: SectorEnum,
    user: str = Depends(verify_user),
    _: None = Depends(rate_limit)
):
    try:
        market_data = await fetch_market_data(sector.value)
        analysis = await analyze_sector(sector.value, market_data)
        report = generate_md_report(sector.value, analysis)

        return {
            "sector": sector.value,
            "markdown_report": report
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
