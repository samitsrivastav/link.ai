import streamlit as st
import google.generativeai as genai
from util import logo
import json
import time

API_KEY = "AIzaSyAjrOrZB4_vfw-HpCQetMD1j5KE31WmSG8"

# Initialize Gemini API
genai.configure(api_key=API_KEY)

# Session state initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "field"
if 'field' not in st.session_state:
    st.session_state.field = None
if 'self_reported_level' not in st.session_state:
    st.session_state.self_reported_level = None
if 'current_level' not in st.session_state:
    st.session_state.current_level = None
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'courses' not in st.session_state:
    st.session_state.courses = None

# App title
st.title("Skill Assessment & Course Recommender")

# Sidebar for assessment info
with st.sidebar:
    logo()
    
    if st.session_state.assessment_complete:
        st.header("Assessment Results")
        st.write(f"Field: **{st.session_state.field}**")
        st.write(f"Self-reported level: **{st.session_state.self_reported_level}**")
        st.write(f"Assessed level: **{st.session_state.current_level}**")
        st.write(f"Questions answered correctly: **{st.session_state.correct_answers}/{st.session_state.questions_asked}**")

# Function to generate a question based on the field and level
def generate_question(field, level):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Generate an MCQ question to assess someone's knowledge in {field} at a {level} level.
    The question should be challenging but appropriate for this level.
    Return your response in the following JSON format:
    {{
        "question": "The question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "The correct option (exactly as written in options)",
        "explanation": "Brief explanation of why this is the correct answer"
    }}
    Only return the JSON, no other text.
    """

     
    response = model.generate_content(prompt)
    response_text = response.text  # or response.candidates[0].content if needed
   
    try:
        # Extract JSON from the response
        json_response = json.loads(response.text)
        return json_response
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the text
        try:
            json_str = response.text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            return {
                "question": "Error generating question. Please try again.",
                "options": ["Try again", "Continue", "Restart", "Exit"],
                "correct_answer": "Try again",
                "explanation": "There was an error parsing the response from the AI."
            }

# Function to get course recommendations
def get_course_recommendations(field, level):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Generate 5 LinkedIn Learning course recommendations for someone who is at a {level} level in {field}.
    For each course, provide a title, brief description, and why it's appropriate for this skill level.
    Return your response in the following JSON format:
    {{
        "courses": [
            {{
                "title": "Course title",
                "description": "Brief course description",
                "reason": "Why this course is appropriate for this level"
            }},
            ... (4 more courses)
        ],
        "general_advice": "General learning advice for someone at this level in this field"
    }}
    Only return the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Extract JSON from the response
        json_response = json.loads(response.text)
        return json_response
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the text
        try:
            json_str = response.text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            return {
                "courses": [
                    {
                        "title": "Error generating recommendations",
                        "description": "Please try again later",
                        "reason": "API error"
                    }
                ],
                "general_advice": "There was an error generating course recommendations."
            }

# Function to generate final assessment
def generate_assessment(field, self_reported_level, actual_level, correct_ratio):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Generate an assessment for someone in the {field} field.
    - They self-reported as a {self_reported_level} level
    - Based on their quiz performance, they are at a {actual_level} level
    - They answered {correct_ratio} of questions correctly
    
    Provide insights about their skill level, any gaps between their self-assessment and actual performance,
    and general advice for their skill development journey.
    
    Return your response in the following JSON format:
    {{
        "assessment": "Overall assessment paragraph",
        "strengths": "Identified strengths based on performance",
        "areas_for_improvement": "Areas that need more focus",
        "next_steps": "Recommended next steps for learning"
    }}
    Only return the JSON, no other text.
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Extract JSON from the response
        json_response = json.loads(response.text)
        return json_response
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the text
        try:
            json_str = response.text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            return {
                "assessment": "Error generating assessment. Please try again.",
                "strengths": "Unable to determine",
                "areas_for_improvement": "Unable to determine",
                "next_steps": "Please retry the assessment"
            }

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Main chat logic
# Add initial message if this is the first interaction
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("What field are you interested in?")
    st.session_state.messages.append({"role": "assistant", "content": "What field are you interested in?"})

# Get user input
if not st.session_state.assessment_complete:
    user_input = st.chat_input("Your response")
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process based on current stage
        if st.session_state.current_stage == "field":
            # Store the field and move to level question
            st.session_state.field = user_input
            st.session_state.current_stage = "level"
            
            with st.chat_message("assistant"):
                response = "What level do you think you are in this field? (Beginner, Intermediate, Advanced, or Expert)"
                st.write(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        elif st.session_state.current_stage == "level":
            # Store self-reported level and start questions
            st.session_state.self_reported_level = user_input
            
            # Map user input to standardized level
            level_map = {
                "beginner": "Beginner",
                "intermediate": "Intermediate",
                "advanced": "Advanced",
                "expert": "Expert"
            }
            
            # Try to map the input to a standard level
            reported_level_lower = user_input.lower()
            if any(level in reported_level_lower for level in level_map.keys()):
                for key, value in level_map.items():
                    if key in reported_level_lower:
                        st.session_state.self_reported_level = value
                        break
            
            # Set initial question level based on self-reported level
            st.session_state.current_level = st.session_state.self_reported_level
            st.session_state.current_stage = "questioning"
            
            # Generate first question
            with st.spinner("Generating question..."):
                question_data = generate_question(st.session_state.field, st.session_state.current_level)
            
            # Display the question
            with st.chat_message("assistant"):
                st.write(question_data["question"])
                options = question_data["options"]
                for i, option in enumerate(options):
                    st.write(f"{chr(65+i)}. {option}")
            
            # Store the question and correct answer
            st.session_state.messages.append({
                "role": "assistant", 
                "content": question_data["question"] + "\n" + "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
            })
            st.session_state.current_question = question_data
        
        elif st.session_state.current_stage == "questioning":
            # Process answer to current question
            current_question = st.session_state.current_question
            user_answer = user_input.strip()
            correct_answer = current_question["correct_answer"]
            
            # Standardize user answer format (handle both "A" and "Option A" formats)
            options = current_question["options"]
            correct_index = options.index(correct_answer)
            correct_letter = chr(65 + correct_index)
            
            # Check if answer is correct
            is_correct = False
            if user_answer.upper() == correct_letter:
                is_correct = True
            elif user_answer == correct_answer:
                is_correct = True
            elif any(user_answer.lower() in opt.lower() for opt in options) and user_answer.lower() in correct_answer.lower():
                is_correct = True
            
            # Update stats
            st.session_state.questions_asked += 1
            if is_correct:
                st.session_state.correct_answers += 1
            
            # Provide feedback
            with st.chat_message("assistant"):
                if is_correct:
                    st.write("✓ Correct!")
                else:
                    st.write(f"✗ Incorrect. The correct answer is: {correct_answer}")
                
                st.write(f"**Explanation**: {current_question['explanation']}")
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": (
                    "✓ Correct!" if is_correct else f"✗ Incorrect. The correct answer is: {correct_answer}"
                ) + f"\n\n**Explanation**: {current_question['explanation']}"
            })
            
            # Adjust difficulty if needed
            if is_correct and st.session_state.current_level != "Expert":
                level_progression = ["Beginner", "Intermediate", "Advanced", "Expert"]
                current_index = level_progression.index(st.session_state.current_level)
                # Only increase level if we have at least 2 questions and correct rate > 70%
                if st.session_state.questions_asked >= 2 and st.session_state.correct_answers / st.session_state.questions_asked > 0.7:
                    if current_index < len(level_progression) - 1:
                        st.session_state.current_level = level_progression[current_index + 1]
            
            elif not is_correct and st.session_state.current_level != "Beginner":
                level_progression = ["Beginner", "Intermediate", "Advanced", "Expert"]
                current_index = level_progression.index(st.session_state.current_level)
                # Only decrease level if we have at least 2 questions and correct rate < 30%
                if st.session_state.questions_asked >= 2 and st.session_state.correct_answers / st.session_state.questions_asked < 0.3:
                    if current_index > 0:
                        st.session_state.current_level = level_progression[current_index - 1]
            
            # Decide whether to continue questioning or finish assessment
            if st.session_state.questions_asked >= 5:
                # Complete the assessment
                st.session_state.current_stage = "complete"
                st.session_state.assessment_complete = True
                
                # Generate assessment
                with st.spinner("Analyzing your skill level..."):
                    correct_ratio = f"{st.session_state.correct_answers}/{st.session_state.questions_asked}"
                    assessment_data = generate_assessment(
                        st.session_state.field,
                        st.session_state.self_reported_level,
                        st.session_state.current_level,
                        correct_ratio
                    )
                
                # Generate course recommendations
                with st.spinner("Finding course recommendations..."):
                    st.session_state.courses = get_course_recommendations(
                        st.session_state.field,
                        st.session_state.current_level
                    )
                
                # Display assessment
                with st.chat_message("assistant"):
                    st.write("### Your Skill Assessment Results")
                    st.write(assessment_data["assessment"])
                    
                    st.write("**Strengths:**")
                    st.write(assessment_data["strengths"])
                    
                    st.write("**Areas for Improvement:**")
                    st.write(assessment_data["areas_for_improvement"])
                    
                    st.write("**Recommended Next Steps:**")
                    st.write(assessment_data["next_steps"])
                    
                    st.write("### Recommended LinkedIn Learning Courses")
                    for i, course in enumerate(st.session_state.courses["courses"], 1):
                        st.write(f"**{i}. {course['title']}**")
                        st.write(course["description"])
                        st.write(f"*Why this is recommended*: {course['reason']}")
                        st.write("---")
                    
                    st.write("**General Learning Advice:**")
                    st.write(st.session_state.courses["general_advice"])
                
                # Store final message
                assessment_message = f"### Your Skill Assessment Results\n\n{assessment_data['assessment']}\n\n"
                assessment_message += f"**Strengths:**\n{assessment_data['strengths']}\n\n"
                assessment_message += f"**Areas for Improvement:**\n{assessment_data['areas_for_improvement']}\n\n"
                assessment_message += f"**Recommended Next Steps:**\n{assessment_data['next_steps']}\n\n"
                assessment_message += "### Recommended LinkedIn Learning Courses\n\n"
                
                for i, course in enumerate(st.session_state.courses["courses"], 1):
                    assessment_message += f"**{i}. {course['title']}**\n"
                    assessment_message += f"{course['description']}\n"
                    assessment_message += f"*Why this is recommended*: {course['reason']}\n\n"
                
                assessment_message += f"**General Learning Advice:**\n{st.session_state.courses['general_advice']}"
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assessment_message
                })
                
            else:
                # Generate next question
                time.sleep(0.5)  # Brief pause before next question
                with st.spinner("Generating next question..."):
                    question_data = generate_question(st.session_state.field, st.session_state.current_level)
                
                # Display the question
                with st.chat_message("assistant"):
                    st.write(question_data["question"])
                    options = question_data["options"]
                    for i, option in enumerate(options):
                        st.write(f"{chr(65+i)}. {option}")
                
                # Store the question and correct answer
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": question_data["question"] + "\n" + "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
                })
                st.session_state.current_question = question_data
            
else:
    # If assessment is complete, provide option to restart
    if st.button("Start New Assessment"):
        # Reset all state
        st.session_state.messages = []
        st.session_state.current_stage = "field"
        st.session_state.field = None
        st.session_state.self_reported_level = None
        st.session_state.current_level = None
        st.session_state.questions_asked = 0
        st.session_state.correct_answers = 0
        st.session_state.assessment_complete = False
        st.session_state.courses = None
        st.rerun()