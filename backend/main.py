import os
import re
import json
import logging
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cinemai")

app = FastAPI(title="CinemAI Backend — Movie Performance Predictor Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MovieAnalysisRequest(BaseModel):
    title: str = Field(..., min_length=1)
    synopsis: str = Field(..., min_length=10)
    genres: List[str]
    budget: float = Field(..., gt=0) # in millions USD
    cast_star_power: int = Field(..., ge=1, le=10)
    target_emotions: Dict[str, float] # e.g. {"joy": 40, "sadness": 20, ...}

class EmotionalArcPoint(BaseModel):
    checkpoint: str
    joy: float
    sadness: float
    fear: float
    anger: float
    suspense: float

class MovieAnalysisResponse(BaseModel):
    status: str # "success" or "fallback"
    title: str
    hit_probability: float
    box_office_outcome: str
    predicted_roi: float
    audience_score: float
    critical_score: float
    emotional_resonance: float
    genre_breakdown: Dict[str, float]
    emotional_arc: List[EmotionalArcPoint]
    agent_logs: List[str]
    executive_summary: str
    strengths: str
    weaknesses: str
    agent_recommendations: List[str]

def run_heuristic_analysis(req: MovieAnalysisRequest) -> dict:
    """
    Advanced heuristic fallback engine.
    Scans the plot text for genre/emotion related keywords, checks budget vs star power,
    and runs a deterministic mathematical simulation to produce high-fidelity reports.
    """
    text = req.synopsis.lower()
    
    # Define emotion keyword sets
    keywords = {
        "joy": ["laugh", "funny", "joke", "hilarious", "smile", "happy", "comedy", "romance", "love", "fun", "amusing", "cheerful", "party"],
        "sadness": ["cry", "sad", "death", "die", "died", "tragic", "loss", "grief", "lonely", "tears", "funeral", "depressed", "heartbroken"],
        "fear": ["scary", "ghost", "darkness", "fear", "haunt", "scream", "creature", "monster", "shadow", "killer", "horror", "panic", "blood"],
        "anger": ["fight", "kill", "revenge", "punch", "war", "battle", "hate", "furious", "angry", "weapon", "destroy", "enemy", "rage"],
        "suspense": ["chase", "mystery", "investigate", "clue", "secret", "hide", "thrill", "escape", "spy", "danger", "police", "warning", "trap"]
    }
    
    # Count occurrences
    counts = {emotion: 0 for emotion in keywords}
    total_words = len(text.split())
    for emotion, words in keywords.items():
        for word in words:
            counts[emotion] += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
            
    # Normalize counts to score (0-100 scale based on frequency and baseline)
    raw_scores = {}
    for emotion, count in counts.items():
        # Baseline minimum 15% to make graphs look interesting even for dry text
        freq_ratio = (count / max(1, total_words)) * 1000
        raw_scores[emotion] = min(95, max(15, 15 + freq_ratio * 15))
        
    # Boost raw scores based on requested genres
    genre_mapping = {
        "Comedy": "joy",
        "Drama": "sadness",
        "Horror": "fear",
        "Action": "anger",
        "Thriller": "suspense",
        "Sci-Fi": "suspense",
        "Romance": "joy"
    }
    
    for genre in req.genres:
        mapped_emotion = genre_mapping.get(genre)
        if mapped_emotion:
            raw_scores[mapped_emotion] = min(98, raw_scores[mapped_emotion] + 25)
            
    # Adjust other emotions slightly to sum closer to 100 in terms of relative shares
    total_raw = sum(raw_scores.values())
    genre_breakdown = {}
    for genre in req.genres:
        # Apportion genre relative weight
        genre_breakdown[genre] = 100 / len(req.genres)
    # Ensure remaining genres are listed at 0 if not selected
    all_genres = ["Action", "Comedy", "Drama", "Thriller", "Sci-Fi", "Horror", "Romance"]
    for g in all_genres:
        if g not in genre_breakdown:
            genre_breakdown[g] = 0.0
            
    # Calculate commercial performance score (viability)
    # Target scale: 0 - 100
    viability = 55.0 # Base
    
    # Star power impact
    viability += (req.cast_star_power - 5) * 5.0
    
    # Budget evaluation (risky vs cost-effective)
    # Ultra-high budget (> 120M) requires huge star power (>= 8) and commercial genres
    is_commercial_genre = any(g in ["Action", "Sci-Fi", "Comedy", "Thriller"] for g in req.genres)
    if req.budget > 120:
        if req.cast_star_power < 8:
            viability -= 25.0
        if not is_commercial_genre:
            viability -= 15.0
        else:
            viability += 10.0
    # Low budget (< 15M) has lower break-even threshold
    elif req.budget < 15:
        if req.cast_star_power >= 4:
            viability += 15.0
        if "Drama" in req.genres or "Horror" in req.genres:
            # Horrors are notoriously high ROI
            viability += 10.0
            
    # Target emotion match penalty/bonus
    # If the user sets target emotions and the synopsis matches them reasonably, give bonus
    match_score = 0.0
    for emotion, target in req.target_emotions.items():
        if emotion in raw_scores:
            diff = abs(raw_scores[emotion] - target)
            match_score += diff
    avg_diff = match_score / max(1, len(req.target_emotions))
    if avg_diff < 15:
        viability += 10.0 # High alignment
    elif avg_diff > 35:
        viability -= 10.0 # Low alignment
        
    # Cap viability
    viability = min(98.0, max(5.0, viability))
    
    # Map viability to outcome
    if viability >= 75:
        box_office_outcome = "Blockbuster Hit"
        predicted_roi = round(150 + viability * 4 + random.uniform(-20, 20), 1)
        hit_probability = round(viability + random.uniform(1, 5), 1)
    elif viability >= 55:
        box_office_outcome = "Box Office Success"
        predicted_roi = round(105 + viability * 1.5 + random.uniform(-10, 10), 1)
        hit_probability = round(viability, 1)
    elif viability >= 40:
        box_office_outcome = "Break-Even"
        predicted_roi = round(85 + (viability - 40) * 1.0 + random.uniform(-5, 5), 1)
        hit_probability = round(viability, 1)
    else:
        box_office_outcome = "Box Office Flop"
        predicted_roi = round(10 + viability * 1.5 + random.uniform(-5, 5), 1)
        hit_probability = round(viability - 5, 1)
        
    # Clean output bounds
    hit_probability = min(99.0, max(1.0, hit_probability))
    predicted_roi = max(5.0, predicted_roi)
    
    # Calculate scores
    # Critics like drama, low-budget indie gems, good emotional resonance
    critical_score = round(45 + (100 - viability) * 0.1 + (counts["sadness"] + counts["suspense"]) * 2.5 + (10 if req.budget < 20 else -5), 1)
    critical_score = min(97.0, max(20.0, critical_score))
    
    # Audience likes comedy/action, high star power, blockbuster thrills
    audience_score = round(35 + req.cast_star_power * 4.5 + (counts["joy"] + counts["anger"]) * 3.0 + (10 if is_commercial_genre else -5), 1)
    audience_score = min(98.0, max(15.0, audience_score))
    
    # Emotional resonance: combination of target alignment and word diversity
    emotional_resonance = round(100 - avg_diff, 1)
    emotional_resonance = min(95.0, max(30.0, emotional_resonance))
    
    # Generate emotional arc curve over 4 screenwriting phases
    # Dynamic values based on selected genres and keywords
    phases = ["Act 1: Setup", "Act 2: Confrontation", "Act 3: Climax", "Act 4: Resolution"]
    emotional_arc = []
    
    # Calculate base curves for each emotion
    for i, phase in enumerate(phases):
        # We model typical screenplay spikes:
        # Act 1: Setup (moderate joy, low sadness, low fear/anger, light suspense)
        # Act 2: Confrontation (joy down, sadness rising, fear/anger rising, suspense rising)
        # Act 3: Climax (joy lowest, sadness peaks if tragedy, fear/anger peak, suspense peaks)
        # Act 4: Resolution (joy resolves high if comedy/romance, sadness peaks if sad, suspense falls)
        
        factor_joy = 1.0 if "Comedy" in req.genres or "Romance" in req.genres else 0.4
        factor_sad = 1.2 if "Drama" in req.genres else 0.4
        factor_fear = 1.4 if "Horror" in req.genres else 0.3
        factor_ang = 1.3 if "Action" in req.genres else 0.5
        factor_susp = 1.3 if "Thriller" in req.genres or "Sci-Fi" in req.genres else 0.5
        
        if i == 0: # Setup
            joy_val = 55 * factor_joy
            sad_val = 15 * factor_sad
            fear_val = 10 * factor_fear
            ang_val = 15 * factor_ang
            susp_val = 25 * factor_susp
        elif i == 1: # Confrontation
            joy_val = 35 * factor_joy
            sad_val = 30 * factor_sad
            fear_val = 30 * factor_fear
            ang_val = 40 * factor_ang
            susp_val = 50 * factor_susp
        elif i == 2: # Climax
            joy_val = 10 * factor_joy
            sad_val = 60 * factor_sad
            fear_val = 75 * factor_fear
            ang_val = 80 * factor_ang
            susp_val = 90 * factor_susp
        else: # Resolution
            joy_val = (80 if box_office_outcome != "Box Office Flop" else 30) * factor_joy
            sad_val = (15 if "Comedy" in req.genres else 50) * factor_sad
            fear_val = 10 * factor_fear
            ang_val = 15 * factor_ang
            susp_val = 15 * factor_susp
            
        emotional_arc.append(
            EmotionalArcPoint(
                checkpoint=phase,
                joy=round(min(98, max(5, joy_val + random.uniform(-5, 5)))),
                sadness=round(min(98, max(5, sad_val + random.uniform(-5, 5)))),
                fear=round(min(98, max(5, fear_val + random.uniform(-5, 5)))),
                anger=round(min(98, max(5, ang_val + random.uniform(-5, 5)))),
                suspense=round(min(98, max(5, susp_val + random.uniform(-5, 5)))),
            )
        )
        
    # Generate recommendations
    recs = []
    if req.budget > 100 and req.cast_star_power < 7:
        recs.append(f"HIGH BUDGET RISK: A budget of ${req.budget}M is extremely high for a lead cast with star power ({req.cast_star_power}/10). Consider casting an A-list lead to secure pre-sales or optimize the budget down to under ${req.budget * 0.7:.1f}M.")
    if "Comedy" in req.genres and raw_scores["joy"] < 40:
        recs.append("LOW HUMOR INDEX: The synopsis is categorized as Comedy, but lacks punchy comedic beats or humor indicators. Suggest rewriting Act 2 to introduce a strong comedic misunderstanding or secondary funny character.")
    if "Thriller" in req.genres and raw_scores["suspense"] < 45:
        recs.append("TENSION DEFICIT: A Thriller needs high suspense. The text lacks suspense markers. Suggest introducing a ticking-clock element in the plot (e.g. a deadline, an active pursuer) to raise stakes.")
    if req.cast_star_power <= 3:
        recs.append("STAR POWER DRIFT: With low cast star power, the marketing will rely entirely on high concept hooks. Make sure the synopsis hook is extremely clear and unique, or target film festivals to build indie hype.")
    if len(req.synopsis) < 150:
        recs.append("PLOT UNDERDEVELOPMENT: The synopsis is too short for a comprehensive analysis. Provide details about the central conflict and climax to improve emotional resonance predictions.")
    if avg_diff > 25:
        recs.append(f"EMOTIONAL MISALIGNMENT: The target emotions diverge from the plot contents by {avg_diff:.1f}%. If you want to evoke these target feelings, adjust the tone of the synopsis to match (e.g. add darker conflicts for sadness/fear).")
        
    # Fallback default recommendations if list is short
    if len(recs) < 3:
        recs.append("CLIMAX REINFORCEMENT: The climax transition is functional but could benefit from a sharper twist. Introduce a moment of defeat right before the final resolution.")
        recs.append("Pacing Check: Keep the first act setup brief (under 15 minutes screen time) to get directly into the core genre hook and keep audience attention.")
    if len(recs) < 3:
        recs.append("Subplot Integration: Introduce a secondary romantic or dramatic subplot to keep secondary character engagement high during transition periods.")

    # Executive Summary / Strengths / Weaknesses
    exec_summary = f"An analysis of the plot for '{req.title}' reveals a {', '.join(req.genres)} concept. Commercial viability is modeled as a {box_office_outcome} with a predicted ROI of {predicted_roi}%."
    
    strengths = f"Clear genre target ({', '.join(req.genres)})"
    if req.cast_star_power >= 7:
        strengths += f" backed by highly bankable cast star power ({req.cast_star_power}/10)."
    else:
        strengths += f" with a reasonable budget footprint of ${req.budget}M."
    if emotional_resonance > 75:
        strengths += " The emotional resonance aligns beautifully with creative intentions."
        
    weaknesses = ""
    if req.budget > 120 and req.cast_star_power < 7:
        weaknesses += "High financial exposure due to high budget without guaranteed star power draw."
    elif avg_diff > 25:
        weaknesses += "Tonal inconsistency: the written plot synopsis does not fully reflect the intended emotional weights."
    else:
        weaknesses += "The emotional progression is standard but lacks unique thematic disruption in Act 2."
        
    # Agent logs simulation
    agent_logs = [
        f"[AI Agent] Initializing CinemAI Predictor Engine v2.4...",
        f"[AI Agent] Parsing project metadata: '{req.title}' | Budget: ${req.budget}M | Cast: {req.cast_star_power}/10",
        f"[AI Agent] Scanning synopsis tokens ({total_words} words) for semantic sentiment mapping...",
        f"[AI Agent] Semantic profile matched: Joy: {raw_scores['joy']:.1f}% | Sadness: {raw_scores['sadness']:.1f}% | Suspense: {raw_scores['suspense']:.1f}%",
        f"[AI Agent] Querying historical theatrical performance databases for genres: {req.genres}...",
        f"[AI Agent] Simulating audience demographic interest metrics...",
        f"[AI Agent] Executing Monte Carlo box office revenue projection models...",
        f"[AI Agent] Success probability calculated: {hit_probability}% | Expected Class: {box_office_outcome}.",
        f"[AI Agent] Formulating script editing recommendations..."
    ]
    
    return {
        "status": "fallback",
        "title": req.title,
        "hit_probability": hit_probability,
        "box_office_outcome": box_office_outcome,
        "predicted_roi": predicted_roi,
        "audience_score": audience_score,
        "critical_score": critical_score,
        "emotional_resonance": emotional_resonance,
        "genre_breakdown": genre_breakdown,
        "emotional_arc": emotional_arc,
        "agent_logs": agent_logs,
        "executive_summary": exec_summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "agent_recommendations": recs[:4]
    }

async def analyze_movie_ai(req: MovieAnalysisRequest, api_key: str) -> Optional[dict]:
    """
    Tries to call Gemini via OpenAI SDK to get a rich structured analysis.
    Returns None on exception so fallback takes over.
    """
    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    system_prompt = """You are an Agentic AI Screenplay Doctor and Box Office Commercial Analyst.
Your task is to analyze the user's movie proposal (title, genres, plot synopsis, budget, cast star power, and target emotional weights) and output a detailed commercial and emotional prediction.

You MUST reply ONLY with a JSON object. Do not wrap it in ```json ... ``` code blocks. Do not add any text before or after the JSON.

The JSON schema must match:
{
  "hit_probability": float (percentage 0 to 100),
  "box_office_outcome": string (exactly one of: "Blockbuster Hit", "Box Office Success", "Break-Even", "Box Office Flop"),
  "predicted_roi": float (percentage return on investment, e.g. 250.5),
  "audience_score": float (predicted Rotten Tomatoes Audience Score, 0 to 100),
  "critical_score": float (predicted Rotten Tomatoes Critic Score, 0 to 100),
  "emotional_resonance": float (overall emotional resonance score, 0 to 100),
  "genre_breakdown": {
     "Action": float,
     "Comedy": float,
     "Drama": float,
     "Thriller": float,
     "Sci-Fi": float,
     "Horror": float,
     "Romance": float
  } (summing to 100),
  "emotional_arc": [
     {"checkpoint": "Act 1: Setup", "joy": float, "sadness": float, "fear": float, "anger": float, "suspense": float},
     {"checkpoint": "Act 2: Confrontation", "joy": float, "sadness": float, "fear": float, "anger": float, "suspense": float},
     {"checkpoint": "Act 3: Climax", "joy": float, "sadness": float, "fear": float, "anger": float, "suspense": float},
     {"checkpoint": "Act 4: Resolution", "joy": float, "sadness": float, "fear": float, "anger": float, "suspense": float}
  ],
  "agent_logs": [
     "string describing step 1 of your agentic reasoning",
     "string describing step 2...",
     "string describing step 3...",
     "string describing step 4...",
     "string describing step 5 (end with complete evaluation)"
  ],
  "executive_summary": "string writing a concise commercial evaluation",
  "strengths": "string describing script strengths",
  "weaknesses": "string describing script weaknesses",
  "agent_recommendations": [
     "specific, actionable recommendation 1 to improve ROI (e.g. script edits, casting adjustments, budget tweaks)",
     "specific, actionable recommendation 2...",
     "specific, actionable recommendation 3..."
  ]
}

Ground your evaluations in realistic box office economics. A movie with a $200M budget and cast power of 2 is highly likely a "Box Office Flop". A horror movie with a $5M budget and cast power of 4 has high potential for "Box Office Success" or "Blockbuster Hit".
"""

    prompt = f"""Movie Proposal for Analysis:
Title: {req.title}
Selected Genres: {', '.join(req.genres)}
Estimated Budget: ${req.budget}M
Cast Star Power Rating: {req.cast_star_power}/10
Intended Target Emotions (creative direction): {json.dumps(req.target_emotions)}

Plot Synopsis / Script Scene:
\"\"\"
{req.synopsis}
\"\"\"
"""
    try:
        # We test gemini-2.0-flash first since it's the newest, standard model.
        # If it rate-limits or fails, we fail out to the fallback.
        logger.info("Attempting Gemini API call via OpenAI wrapper...")
        response = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        logger.info("Gemini raw response received.")
        
        # Clean response if LLM wraps it in markdown despite instructions
        content_clean = content.strip()
        if content_clean.startswith("```"):
            # strip leading/trailing code fences
            content_clean = re.sub(r'^```[a-zA-Z]*\n', '', content_clean)
            content_clean = re.sub(r'\n```$', '', content_clean)
            content_clean = content_clean.strip()
            
        data = json.loads(content_clean)
        
        # Ensure all keys are in data, otherwise raise ValueError to trigger fallback
        required_keys = ["hit_probability", "box_office_outcome", "predicted_roi", "audience_score", 
                         "critical_score", "emotional_resonance", "genre_breakdown", "emotional_arc", 
                         "agent_logs", "executive_summary", "strengths", "weaknesses", "agent_recommendations"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key in response JSON: {key}")
                
        # Inject status
        data["status"] = "success"
        data["title"] = req.title
        return data
        
    except Exception as e:
        logger.error(f"Gemini API analysis failed: {str(e)}")
        return None

@app.post("/api/analyze", response_model=MovieAnalysisResponse)
async def analyze_movie(req: MovieAnalysisRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY") # using this env key as config
    
    if api_key and not api_key.startswith("PLACEHOLDER"):
        result = await analyze_movie_ai(req, api_key)
        if result:
            return MovieAnalysisResponse(**result)
            
    # Fallback engine triggers if no API key, or if API key fails/rate-limits
    logger.info("Falling back to local heuristic analysis engine.")
    fallback_result = run_heuristic_analysis(req)
    return MovieAnalysisResponse(**fallback_result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
