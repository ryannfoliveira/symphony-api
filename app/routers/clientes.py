from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])