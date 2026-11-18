"""CraveMatch — FastAPI + Jinja2 restaurant discovery application."""
from pathlib import Path
import os
import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from recommender import recommend_restaurants

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed_restaurants.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Restaurant dataset not found: {DATA_PATH}")

restaurants_df = pd.read_csv(DATA_PATH)
required_columns = {"Restaurant Name", "City", "Locality", "Cuisines", "Aggregate rating"}
missing = required_columns - set(restaurants_df.columns)
if missing:
    raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")

cities = sorted(restaurants_df["City"].dropna().astype(str).unique().tolist())
cuisine_set = set()
for cuisine_list in restaurants_df["Cuisines"].dropna().astype(str):
    cuisine_set.update(item.strip() for item in cuisine_list.split(",") if item.strip())
cuisines = sorted(cuisine_set)

app = FastAPI(title="CraveMatch", description="AI-powered restaurant discovery", version="2.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

FOOD_IMAGES = {
    "indian": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=900&q=85",
    "pizza": "https://images.unsplash.com/photo-157 pizza?auto=format&fit=crop&w=900&q=85",
    "italian": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=85",
    "chinese": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=900&q=85",
    "cafe": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=900&q=85",
    "default": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=900&q=85",
}
# Correct the pizza image URL separately (kept as a valid static URL).
FOOD_IMAGES["pizza"] = "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=85"

CUISINE_CATEGORIES = [
    {"name": "All", "emoji": "▦"}, {"name": "Indian", "emoji": "🍛"},
    {"name": "Chinese", "emoji": "🍜"}, {"name": "Italian", "emoji": "🍕"},
    {"name": "Continental", "emoji": "🥘"}, {"name": "Mexican", "emoji": "🌮"},
    {"name": "Desserts", "emoji": "🧁"}, {"name": "Beverages", "emoji": "🥤"},
]


def clean_value(value: str | None):
    value = (value or "").strip()
    return None if not value or value.lower() in {"any", "all", "all cuisines", "any price"} else value


def image_for(cuisines_text: str) -> str:
    text = (cuisines_text or "").lower()
    for key in ("indian", "pizza", "italian", "chinese", "cafe"):
        if key in text:
            return FOOD_IMAGES[key]
    return FOOD_IMAGES["default"]


def serialize_results(frame: pd.DataFrame):
    records = frame.to_dict(orient="records") if frame is not None and not frame.empty else []
    output = []
    for row in records:
        rating = row.get("Aggregate rating", 0)
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            rating = 0.0
        score = row.get("Match Percentage", "")
        try:
            match = float(str(score).replace("%", ""))
        except (TypeError, ValueError):
            match = min(99, max(70, round(rating / 5 * 100)))
        price = row.get("Price range", "—")
        try:
            price = "₹" * max(1, int(price))
        except (TypeError, ValueError):
            price = "₹₹"
        votes = row.get("Votes", 0)
        try:
            votes = f"{int(votes):,}"
        except (TypeError, ValueError):
            votes = "—"
        output.append({
            "name": row.get("Restaurant Name", "Restaurant"),
            "city": row.get("City", ""), "locality": row.get("Locality", ""),
            "cuisines": row.get("Cuisines", "Restaurant"), "rating": rating,
            "votes": votes, "price": price,
            "cost": row.get("Average Cost for two", "—"),
            "match": round(match), "image": image_for(str(row.get("Cuisines", ""))),
            "booking": row.get("Has Table booking", "No"),
            "delivery": row.get("Has Online delivery", "No"),
        })
    return output


def page_context(request: Request, **extra):
    context = {"request": request, "cities": cities, "cuisines": cuisines,
               "categories": CUISINE_CATEGORIES, "restaurants": [], "selected": {},
               "searched": False, "error": None}
    context.update(extra)
    return context


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Initial page shows popular, highly rated restaurants from the real dataset.
    popular = restaurants_df.sort_values(["Aggregate rating", "Votes"], ascending=[False, False]).head(6)
    return templates.TemplateResponse("index.html", page_context(request, restaurants=serialize_results(popular)))


@app.post("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    city: str = Form("Chennai"), cuisine: str = Form("Any"),
    price_range: str = Form("Any"), min_rating: str = Form("Any"),
    restaurant_type: str = Form(""), table_booking: str = Form("Any"),
    online_delivery: str = Form("Any"), top_n: int = Form(6),
):
    selected = {"city": city, "cuisine": cuisine, "price_range": price_range,
                "min_rating": min_rating, "restaurant_type": restaurant_type,
                "table_booking": table_booking, "online_delivery": online_delivery}
    try:
        frame = recommend_restaurants(
            cuisine=clean_value(cuisine), city=clean_value(city),
            price_range=clean_value(price_range), min_rating=clean_value(min_rating),
            restaurant_type=clean_value(restaurant_type),
            table_booking=clean_value(table_booking), online_delivery=clean_value(online_delivery),
            top_n=max(1, min(int(top_n), 20)),
        )
        results = serialize_results(frame)
        return templates.TemplateResponse("index.html", page_context(
            request, restaurants=results, selected=selected, searched=True,
            result_count=len(results),
            search_summary=f"Showing {len(results)} restaurant matches for your preferences." if results else "No exact matches found. Try changing a filter."
        ))
    except Exception as exc:
        return templates.TemplateResponse("index.html", page_context(
            request, restaurants=[], selected=selected, searched=True,
            error=f"We couldn't complete that search: {exc}"
        ), status_code=500)


@app.get("/health")
async def health():
    return {"status": "healthy", "app": "CraveMatch", "restaurants": int(len(restaurants_df))}


@app.get("/api/cuisines")
async def cuisine_list():
    return JSONResponse({"cuisines": cuisines, "cities": cities})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
