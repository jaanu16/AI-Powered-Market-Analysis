# AI-Powered-Market-Analysis
The Trade Opportunities API is a FastAPI-based application that analyzes Indian market sectors using AI-driven insights. It validates input, enforces security and rate limiting, gathers market data, and generates structured Markdown reports highlighting trade opportunities, risks, and market outlook.
# Trade Opportunities API

A FastAPI-based service that analyzes Indian market sectors and returns
AI-powered trade opportunity insights in Markdown format.

## Features
- FastAPI backend
- Input validation
- Authentication
- Rate limiting
- In-memory storage
- Markdown report generation
- Gemini API ready

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
