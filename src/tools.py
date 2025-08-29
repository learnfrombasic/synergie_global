import pandas as pd

from datetime import datetime, timedelta
from typing import Any, Dict, List


from src.configs import settings


def read_reprompts(file_path: str) -> List[Dict[str, str]]:
    try:
        df = pd.read_excel(file_path)
        dialogue_cols = [
            col
            for col in df.columns
            if col.startswith("Dialogue") or col.startswith("Unnamed")
        ]
        df["Dialogue"] = df[dialogue_cols].astype(str).agg(" ".join, axis=1)

        # Drop the extras
        df = df[["Speaker", "Dialogue"]]
        df["Dialogue"] = df["Dialogue"].str.strip()
        return df.to_dict("records")
    except FileNotFoundError:
        return []


def seed_slots_for(address: str, slots_db: Dict[str, List[str]]) -> List[str]:
    """Create fake availability for the next 3 days at 11:00 and 15:00."""
    if address not in slots_db:
        today = datetime.now()
        avail = []
        for d in range(1, 4):
            day = today + timedelta(days=d)
            day_str = day.strftime("%A, %Y-%m-%d")
            avail.append(f"{day_str} 11:00 AM")
            avail.append(f"{day_str} 03:00 PM")
        slots_db[address] = avail
    return slots_db[address]


def tool_check_coverage(address: str) -> Dict[str, Any]:
    if not address or len(address.strip()) < 5:
        return {"is_covered": False, "reason": "Address missing or invalid."}
    is_covered = (hash(address) % 10) != 0  # ~90% covered
    return {
        "is_covered": is_covered,
        "reason": "Coverage confirmed." if is_covered else "Outside service area.",
    }


def tool_get_available_slots(address: str, slots_db: Dict[str, List[str]]) -> List[str]:
    return seed_slots_for(address, slots_db)


def tool_book_appointment(
    name: str,
    address: str,
    phone: str,
    email: str,
    service_request: str,
    slot: str,
    slots_db: Dict[str, List[str]],
    bookings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    avail = seed_slots_for(address, slots_db)
    if slot not in avail:
        return {
            "success": False,
            "confirmation_id": "",
            "message": "Requested slot no longer available.",
        }
    avail.remove(slot)
    confirmation_id = f"JAC-{abs(hash((name, address, slot))) % 1_000_000:06d}"
    bookings.append(
        {
            "confirmation_id": confirmation_id,
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "service_request": service_request,
            "slot": slot,
        }
    )
    return {
        "success": True,
        "confirmation_id": confirmation_id,
        "message": "Appointment booked.",
    }


TOOLS = {
    "check_coverage": tool_check_coverage,
    "get_available_slots": tool_get_available_slots,
    "book_appointment": tool_book_appointment,
}
