"""
Utilities - Helper functions used across the backend
"""


def validate_required_fields(data: dict, required: list) -> tuple[bool, str]:
    """Check that all required fields exist in a dict."""
    for field in required:
        if field not in data:
            return False, f"Missing required field: '{field}'"
    return True, ""


def format_success(data: dict, message: str = "Success") -> dict:
    """Standard success response wrapper."""
    return {"success": True, "message": message, "data": data}


def format_error(message: str, code: int = 400) -> dict:
    """Standard error response wrapper."""
    return {"success": False, "error": message, "code": code}


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def calculate_macro_calories(protein_g: float, carbs_g: float, fat_g: float) -> int:
    """Convert macronutrients to total calories (4-4-9 rule)."""
    return round(protein_g * 4 + carbs_g * 4 + fat_g * 9)
