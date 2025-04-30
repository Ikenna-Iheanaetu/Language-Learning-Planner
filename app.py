
from flask import Flask, render_template, request, jsonify
import os
import json
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_secret_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get JSON data from request
        user_data = request.json
        if not user_data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate required fields
        required_fields = ['target_language', 'native_language', 'proficiency_level', 
                          'learning_goal', 'weekly_time', 'available_days']
        for field in required_fields:
            if field not in user_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Call Gemini integration
        schedule_data = generate_learning_schedule(user_data)
        
        if not schedule_data:
            return jsonify({'error': 'Failed to generate schedule'}), 500
            
        return jsonify(schedule_data)
        
    except Exception as e:
        print(f"Error in generate endpoint: {e}")
        return jsonify({'error': str(e)}), 500
    
def generate_learning_schedule(user_data):
    """Generate a personalized learning schedule using Gemini API"""
    try:
        # Try using Gemini API first
        schedule = generate_schedule_with_gemini(user_data)
        return schedule
    except Exception as e:
        print(f"Gemini API failed: {e}")
        # Fall back to backup plan
        return generate_backup_schedule(user_data)

def generate_schedule_with_gemini(user_data):
    """Generate a personalized learning schedule using Gemini API"""
    
    # Extract user preferences
    target_language = user_data['target_language']
    native_language = user_data['native_language']
    proficiency_level = user_data['proficiency_level']
    learning_goal = user_data['learning_goal']
    weekly_time = user_data['weekly_time']
    available_days = user_data['available_days']
    
    # Calculate time distribution across available days
    num_days = len(available_days)
    time_per_day = weekly_time // num_days
    
    # Map day names to day numbers for consistent ordering
    day_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                  "Friday": 4, "Saturday": 5, "Sunday": 6}
    available_day_numbers = [day_mapping[day] for day in available_days]
    
    # Create prompt for Gemini
    prompt = f"""
    Generate a personalized weekly language learning schedule based on spaced repetition principles.
    
    User Profile:
    - Target Language: {target_language}
    - Native Language: {native_language}
    - Proficiency Level: {proficiency_level}
    - Learning Goal: {learning_goal}
    - Weekly Time Commitment: {weekly_time} minutes
    - Available Days: {', '.join(available_days)}
    
    Based on spaced repetition research and language acquisition principles:
    1. Create a balanced schedule between new learning and revision
    2. Distribute the time commitment of {weekly_time} minutes across {num_days} days
    3. Target approximately {time_per_day} minutes per day
    4. Vary activity types (vocabulary, grammar, speaking, listening, reading, writing)
    5. Apply appropriate intervals for reviewing content based on proficiency level
    6. Include specific activities with durations for each day
    
    For beginners, focus more on vocabulary acquisition and basic grammatical structures.
    For intermediate learners, balance vocabulary expansion with more complex grammar and conversation practice.
    For advanced learners, emphasize authentic materials, subtle grammar points, and fluency development.
    
    Each learning activity should have a specific focus related to the learning goal of {learning_goal}.
    
    Return the schedule in JSON format with this exact structure:
    {{
        "week_starting": "2025-04-22",
        "target_language": "{target_language}",
        "proficiency_level": "{proficiency_level}",
        "daily_plans": [
            {{
                "day": "Day name",
                "day_number": 0-6 (where 0 is Monday),
                "activities": [
                    {{
                        "activity_type": "Learning" or "Review" or "Practice",
                        "content_type": "Vocabulary" or "Grammar" or "Listening" or "Speaking" or "Reading" or "Writing",
                        "duration_minutes": integer,
                        "description": "Detailed description of the activity"
                    }}
                ]
            }}
        ]
    }}
    
    Include ONLY the days that are in the available days list: {available_days}.
    Ensure the total duration across all days equals {weekly_time} minutes.
    Return ONLY valid JSON with no additional text or explanation.
    """
    
    # Call Gemini API
    if not api_key:
        raise ValueError("Gemini API key not configured")
        
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Extract JSON content (may be in markdown code block)
    if "```json" in response_text:
        json_content = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        json_content = response_text.split("```")[1].strip()
    else:
        json_content = response_text.strip()
        
    # Parse and validate the JSON
    schedule_data = json.loads(json_content)
    
    # Validate structure
    validate_schedule_structure(schedule_data)
    
    return schedule_data

def validate_schedule_structure(schedule_data):
    """Validate the structure of the generated schedule"""
    
    # Check required top-level fields
    required_fields = ['week_starting', 'target_language', 'proficiency_level', 'daily_plans']
    for field in required_fields:
        if field not in schedule_data:
            raise ValueError(f"Missing required field in schedule: {field}")
    
    # Check daily plans
    if not isinstance(schedule_data['daily_plans'], list):
        raise ValueError("daily_plans must be a list")
    
    # Check each day
    total_minutes = 0
    for day_plan in schedule_data['daily_plans']:
        # Check day fields
        if 'day' not in day_plan or 'day_number' not in day_plan or 'activities' not in day_plan:
            raise ValueError(f"Missing required field in day plan: {day_plan}")
        
        # Check activities
        if not isinstance(day_plan['activities'], list):
            raise ValueError("activities must be a list")
        
        # Check each activity
        for activity in day_plan['activities']:
            required_activity_fields = ['activity_type', 'content_type', 'duration_minutes', 'description']
            for field in required_activity_fields:
                if field not in activity:
                    raise ValueError(f"Missing required field in activity: {field}")
            
            # Count total minutes
            total_minutes += activity['duration_minutes']

def generate_backup_schedule(user_data):
    """A backup schedule if Gemini API fails"""
    
    # Extract user preferences
    target_language = user_data['target_language']
    proficiency_level = user_data['proficiency_level']
    available_days = user_data['available_days']
    weekly_time = user_data['weekly_time']
    
    # Map day names to day numbers
    day_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                  "Friday": 4, "Saturday": 5, "Sunday": 6}
    
    # Sort available days by their day number
    available_days.sort(key=lambda x: day_mapping[x])
    
    # Calculate minutes per day
    minutes_per_day = weekly_time // len(available_days)
    
    # Basic activity templates based on proficiency level
    activity_templates = {
        "Beginner": [
            {"activity_type": "Learning", "content_type": "Vocabulary", "description": "Learn 10 new basic words"},
            {"activity_type": "Practice", "content_type": "Speaking", "description": "Practice pronunciation"},
            {"activity_type": "Review", "content_type": "Vocabulary", "description": "Review previous vocabulary"}
        ],
        "Intermediate": [
            {"activity_type": "Learning", "content_type": "Grammar", "description": "Study new grammar concept"},
            {"activity_type": "Practice", "content_type": "Listening", "description": "Listen to short dialogues"},
            {"activity_type": "Review", "content_type": "Grammar", "description": "Review previous grammar concepts"}
        ],
        "Advanced": [
            {"activity_type": "Practice", "content_type": "Reading", "description": "Read authentic materials"},
            {"activity_type": "Practice", "content_type": "Writing", "description": "Write short essay"},
            {"activity_type": "Review", "content_type": "Speaking", "description": "Practice conversation"}
        ]
    }
    
    # Select appropriate templates
    templates = activity_templates.get(proficiency_level, activity_templates["Beginner"])
    
    # Generate daily plans
    daily_plans = []
    for day in available_days:
        # Select 2 activities from templates for this day
        day_activities = []
        

if __name__ == '__main__':
    app.run(debug=True)