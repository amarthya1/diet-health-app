"""
Data Models - Dataclasses representing core domain entities
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class User:
    id: str
    name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None          # 'male' | 'female'
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class MealEntry:
    user_id: str
    meal_name: str
    calories: int
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class VitalsEntry:
    user_id: str
    date: str
    weight_kg: Optional[float] = None
    blood_pressure: Optional[str] = None  # e.g. "120/80"
    blood_sugar_mmol: Optional[float] = None
    heart_rate_bpm: Optional[int] = None


@dataclass
class HealthGoal:
    user_id: str
    goal_type: str                         # 'lose' | 'maintain' | 'gain'
    target_weight_kg: Optional[float] = None
    daily_calorie_target: Optional[int] = None
    dietary_restrictions: List[str] = field(default_factory=list)  # e.g. ['vegan', 'gluten-free']


@dataclass
class FoodItem:
    id: str
    name: str
    calories_per_100g: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    vitamin_c_mg: float = 0.0
    vitamin_d_iu: float = 0.0
    calcium_mg: float = 0.0
    iron_mg: float = 0.0
