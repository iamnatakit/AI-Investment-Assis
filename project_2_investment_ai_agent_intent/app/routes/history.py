from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from shared.database.db import get_db
from shared.database.models import ChatMessage, BillingLedger
from sqlalchemy import func

router = APIRouter()

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id,
        ChatMessage.project_name == "project_2_intent"
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return {
        "session_id": session_id,
        "history": [
            {
                "message_id": msg.message_id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@router.get("/report")
async def get_usage_report(db: Session = Depends(get_db)):
    # Calculate totals from BillingLedger
    total_tokens = db.query(func.sum(BillingLedger.total_tokens)).scalar() or 0
    total_cost_usd = db.query(func.sum(BillingLedger.cost_usd)).scalar() or 0.0
    total_cost_thb = db.query(func.sum(BillingLedger.cost_thb)).scalar() or 0.0

    # Group by project_name
    projects = db.query(
        BillingLedger.project_name,
        func.sum(BillingLedger.total_tokens).label("tokens"),
        func.sum(BillingLedger.cost_usd).label("usd"),
        func.count(BillingLedger.billing_id).label("requests")
    ).group_by(BillingLedger.project_name).all()

    project_stats = []
    for p in projects:
        project_stats.append({
            "project_name": p.project_name,
            "total_tokens": int(p.tokens) if p.tokens else 0,
            "cost_usd": float(p.usd) if p.usd else 0.0,
            "total_requests": int(p.requests) if p.requests else 0
        })

    return {
        "overall": {
            "total_tokens": int(total_tokens),
            "total_cost_usd": float(total_cost_usd),
            "total_cost_thb": float(total_cost_thb)
        },
        "by_project": project_stats
    }
