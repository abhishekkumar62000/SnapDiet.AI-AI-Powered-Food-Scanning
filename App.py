### Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import json
import base64
import cv2  # Import OpenCV for image processing
from streamlit_webrtc import webrtc_streamer  # Import webrtc_streamer

# Set the page configuration (must be the first Streamlit command)
st.set_page_config(page_title="🤖 SnapDiet.AI App", layout="wide")

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Sidebar Images
AI_path = "AI.png"  # Ensure this file is in the same directory as your script
if os.path.exists(AI_path):
    st.sidebar.image(AI_path, caption="AI Assistant", use_container_width=True)
else:
    st.sidebar.warning("AI.png file not found. Please check the file path.")

image_path = "image.png"  # Ensure this file is in the same directory as your script
if os.path.exists(image_path):
    st.sidebar.image(image_path, caption="Stay Healthy!", use_container_width=True)
else:
    st.sidebar.warning("image.png file not found. Please check the file path.")

# Sidebar Navigation  
with st.sidebar:  
    st.header("⚙ App Features")  
    tab_selection = st.radio("Select a Feature:", [  
        "📊 Calorie Analysis",  
        "⚖️ BMI Calculator",  
        "💧 Water Intake Tracker",  
        "🥗 Meal Planner",  
        "📜 History",  
        "🚶‍♂️ Daily Step Tracker",  
        "😴 Sleep Tracker",  
        "😊 Mood Tracker",  
        "💪 Fitness Tips",  
        "🙏 Gratitude Journal",  
        "📸 Food Scanner",  
        "📅 Habit Tracker",  
        "🏋️‍♂️ Personalized Workout Plan",  
        "🧘‍♂️ Mindfulness Exercises",  
        "📈 Weekly Progress Report",  
        "🧠 Mental Health Check-In",
        "📸 AI Food Composition Analysis",  # New Feature
        "📊 AI-Powered Monthly Health Report",  # New Feature
        "🍽️ Intermittent Fasting Tracker",  # New Feature
        "👨‍⚕️ Virtual Dietitian Chatbot",  # New Feature
        "🔄 Auto-Adjust Meal Plans"  # New Feature
    ])

# Developer Information
st.sidebar.markdown("👨‍💻 **Developer:** Abhishek💖Yadav")

developer_path = "pic.jpg"  # Ensure this file is in the same directory as your script
if os.path.exists(developer_path):
    st.sidebar.image(developer_path, caption="Developer", use_container_width=True)
else:
    st.sidebar.warning("pic.jpg file not found. Please check the file path.")

# Display app name with emojis
st.markdown("<h1 style='text-align: center;'>🤖 SnapDiet.AI – AI-Powered Food Scanning</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: green;'>Snap. Scan. Stay Fit! 😋</h2>", unsafe_allow_html=True)

# Correctly define all tabs at once using st.tabs

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    try:
        # Ensure image is a list of parts
        if not isinstance(image, list):
            raise ValueError("Image data must be a list of parts.")
        
        # Use the updated model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input, image[0], prompt])
        
        # Safely access the response text
        if hasattr(response, 'text'):
            return response.text
        else:
            raise ValueError("Invalid response format from API.")
    except Exception as e:
        return f"Error: {str(e)}"

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Add this function to process the response and categorize food items
def categorize_food_items(response_text):
    categories = {"Carbohydrates": [], "Proteins": [], "Fats": []}
    # Example logic to parse response and categorize (you can refine this)
    for line in response_text.split("\n"):
        if "carb" in line.lower():
            categories["Carbohydrates"].append(line)
        elif "protein" in line.lower():
            categories["Proteins"].append(line)
        elif "fat" in line.lower():
            categories["Fats"].append(line)
    return categories

# Function to save history
def save_to_history(input_text, response_text):
    history_file = "history.json"
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(file)
    history.append({"input": input_text, "response": response_text})
    with open(history_file, "w") as file:
        json.dump(history, file)

# Function to load history
def load_history():
    history_file = "history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

# Function to suggest healthier alternatives
def suggest_healthier_alternatives(total_calories):
    if total_calories > 500:
        return "Consider reducing portion sizes or replacing high-calorie items with fruits or vegetables."
    elif total_calories < 200:
        return "You might need to add more nutritious items like nuts or lean proteins."
    else:
        return "This meal seems balanced!"

# Function to export results
def export_results(response_text):
    b64 = base64.b64encode(response_text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="analysis.txt">Download Analysis</a>'
    return href

# Function to analyze food image
def analyze_food_image(image_data):
    input_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and provide:
    1. Calories
    2. Fats
    3. Proteins
    4. Carbohydrates
    Also, suggest if this food is beneficial for the user based on their health goals.
    """
    try:
        # Use Google Gemini Pro Vision API
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Pass image_data to the generate_content method
        response = model.generate_content([input_prompt, image_data])
        return response.text  # Adjust based on the actual response structure
    except Exception as e:
        return f"Error: {str(e)}"

# Correctly define all tabs at once using st.tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs([
    "Calorie Analysis", 
    "BMI Calculator", 
    "Water Intake Tracker", 
    "Meal Planner",
    "History",
    "Daily Step Tracker", 
    "Sleep Tracker", 
    "Mood Tracker", 
    "Fitness Tips", 
    "Gratitude Journal",
    "Food Scanner",  # Fixed missing comma
    "Habit Tracker",
    "Personalized Workout Plan",
    "Mindfulness Exercises",
    "Weekly Progress Report",
    "Mental Health Check-In",
])

# Tab 1: Calorie Analysis
with tab1:
    st.header("Calorie Analysis")
    input = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)

    daily_goal = st.number_input("Enter your daily calorie goal:", min_value=0, step=50, key="calorie_goal")
    submit = st.button("Tell me the total calories")

    input_prompt = """
    You are an expert in nutritionist where you need to see the food items from the image
                   and calculate the total calories, also provide the details of every food items with calories intake
                   is below format

                   1. Item 1 - no of calories
                   2. Item 2 - no of calories
                   ----
                   ----
    """

    if submit:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.subheader("The Response is")
            st.write(response)
            save_to_history(input, response)

            # Add export option
            st.markdown(export_results(response), unsafe_allow_html=True)

            # Extract total calories and provide suggestions
            total_calories = sum([int(word) for word in response.split() if word.isdigit()])
            st.write(f"**Total Calories in this meal:** {total_calories}")
            suggestion = suggest_healthier_alternatives(total_calories)
            st.write(f"**Suggestion:** {suggestion}")

            if daily_goal > 0:
                st.write(f"**Remaining Calories for the Day:** {daily_goal - total_calories}")

            # Categorize and display food items
            categories = categorize_food_items(response)
            st.subheader("Nutritional Breakdown")
            for category, items in categories.items():
                st.write(f"**{category}:**")
                for item in items:
                    st.write(f"- {item}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Tab 2: BMI Calculator
with tab2:
    st.header("BMI Calculator")
    weight = st.number_input("Enter your weight (kg):", min_value=0.0, step=0.1, key="weight")
    height = st.number_input("Enter your height (m):", min_value=0.0, step=0.01, key="height")

    if st.button("Calculate BMI"):
        if height > 0:
            bmi = weight / (height ** 2)
            st.write(f"**Your BMI is:** {bmi:.2f}")
            if bmi < 18.5:
                st.write("You are underweight. Consider consulting a nutritionist.")
            elif 18.5 <= bmi < 24.9:
                st.write("You have a normal weight. Keep up the good work!")
            elif 25 <= bmi < 29.9:
                st.write("You are overweight. Consider a balanced diet and exercise.")
            else:
                st.write("You are obese. Please consult a healthcare professional.")
        else:
            st.write("Please enter a valid height.")

# Tab 3: Water Intake Tracker
with tab3:
    st.header("Water Intake Tracker")
    water_goal = st.number_input("Enter your daily water intake goal (liters):", min_value=0.0, step=0.1, key="water_goal")
    water_consumed = st.number_input("Enter the amount of water you've consumed today (liters):", min_value=0.0, step=0.1, key="water_consumed")

    if st.button("Track Water Intake"):
        if water_goal > 0:
            remaining_water = water_goal - water_consumed
            if remaining_water > 0:
                st.write(f"You need to drink {remaining_water:.2f} liters more water today.")
            else:
                st.write("Congratulations! You've met your daily water intake goal.")
        else:
            st.write("Please set a valid water intake goal.")

# Tab 4: Meal Planner
with tab4:
    st.header("Meal Planner")
    if st.button("Generate Meal Plan"):
        st.write("**Suggested Meal Plan:**")
        st.write("- Breakfast: Oatmeal with fruits (300 calories)")
        st.write("- Lunch: Grilled chicken salad (400 calories)")
        st.write("- Snack: Greek yogurt with nuts (200 calories)")
        st.write("- Dinner: Steamed vegetables with quinoa (400 calories)")
        st.write("Total Calories: 1300 (adjust portions as needed)")

# Tab 5: History
with tab5:
    st.header("History")
    history = load_history()
    for entry in history:
        st.write(f"**Input:** {entry['input']}")
        st.write(f"**Response:** {entry['response']}")
        st.write("---")

# Tab 6: Daily Step Tracker
with tab6:
    st.header("Daily Step Tracker")
    step_goal = st.number_input("Enter your daily step goal:", min_value=0, step=100, key="step_goal")
    steps_taken = st.number_input("Enter the number of steps you've taken today:", min_value=0, step=100, key="steps_taken")

    if st.button("Track Steps"):
        if step_goal > 0:
            remaining_steps = step_goal - steps_taken
            if remaining_steps > 0:
                st.write(f"You need to take {remaining_steps} more steps to reach your goal.")
            else:
                st.write("Congratulations! You've reached your daily step goal.")
        else:
            st.write("Please set a valid step goal.")

# Tab 7: Sleep Tracker
with tab7:
    st.header("Sleep Tracker")
    sleep_goal = st.number_input("Enter your daily sleep goal (hours):", min_value=0.0, step=0.5, key="sleep_goal")
    sleep_duration = st.number_input("Enter the number of hours you slept last night:", min_value=0.0, step=0.5, key="sleep_duration")

    if st.button("Track Sleep"):
        if sleep_goal > 0:
            remaining_sleep = sleep_goal - sleep_duration
            if remaining_sleep > 0:
                st.write(f"You need {remaining_sleep:.1f} more hours of sleep to meet your goal.")
            else:
                st.write("Great! You've met your daily sleep goal.")
    st.header("Mood Tracker")
    mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Stressed", "Tired", "Excited"], key="mood")

    if st.button("Log Mood"):
        if mood == "Happy":
            st.write("That's great! Keep spreading positivity!")
        elif mood == "Sad":
            st.write("It's okay to feel sad sometimes. Consider talking to a friend or doing something you enjoy.")
        elif mood == "Stressed":
            st.write("Take a deep breath. Try meditation or a short walk to relax.")
        elif mood == "Tired":
            st.write("Make sure to get some rest and stay hydrated.")
        elif mood == "Excited":
            st.write("Awesome! Channel your energy into something productive!")

# Tab 9: Fitness Tips
with tab9:
    st.header("Fitness Tips")
    tips = [
        "Drink plenty of water throughout the day.",
        "Incorporate strength training into your workout routine.",
        "Take short breaks to stretch if you sit for long periods.",
        "Aim for at least 30 minutes of physical activity daily.",
        "Get enough sleep to allow your body to recover."
    ]

    if st.button("Get a Fitness Tip"):
        import random
        st.write(f"**Tip:** {random.choice(tips)}")

# Tab 10: Gratitude Journal
with tab10:
    st.header("Gratitude Journal")
    gratitude_entry = st.text_area("Write down three things you're grateful for today:", key="gratitude_entry")

    if st.button("Save Gratitude Entry"):
        if gratitude_entry.strip():  # Check if the input is not empty after stripping whitespace
            st.write("Thank you for sharing! Reflecting on gratitude can improve your mental well-being.")
        else:
            st.write("Please write something before saving.")
            
# Tab 11: Food Scanner
with tab11:
    st.header("Food Scanner")

    # Option to use camera or upload an image
    use_camera = st.radio("Choose input method:", ["Upload Image", "Use Camera"], key="food_scanner_method")

    if use_camera == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image of food:", type=["jpg", "jpeg", "png"], key="food_scanner_upload")
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Food Image", use_container_width=True)

            if st.button("Analyze Food", key="analyze_food_button"):
                # Convert image to bytes
                image_data = input_image_setup(uploaded_file)
                result = analyze_food_image(image_data)

                st.subheader("Analysis Result")
                st.write(result)

                # Suggest if the food is beneficial
                if "calories" in result.lower():
                    total_calories = sum([int(word) for word in result.split() if word.isdigit()])
                    suggestion = suggest_healthier_alternatives(total_calories)
                    st.write(f"**Total Calories:** {total_calories}")
                    st.write(f"**Suggestion:** {suggestion}")

# Tab 12: Habit Tracker
with tab12:
    st.header("Habit Tracker")
    st.write("Track your daily habits to build consistency.")

    habits = st.text_input("Enter the habit you want to track (e.g., Exercise, Reading):", key="habit_name")
    progress = st.slider(f"How much progress did you make today for '{habits}'?", 0, 100, key="habit_progress")

    if st.button("Save Habit Progress"):
        st.write(f"Great job! You've completed {progress}% of your habit '{habits}' today.")

# Tab 13: Personalized Workout Plan
with tab13:
    st.header("Personalized Workout Plan")
    st.write("Get a workout plan tailored to your fitness level and goals.")

    fitness_level = st.selectbox("Select your fitness level:", ["Beginner", "Intermediate", "Advanced"], key="fitness_level")
    goal = st.selectbox("What is your fitness goal?", ["Lose Weight", "Build Muscle", "Improve Endurance"], key="fitness_goal")

    if st.button("Generate Workout Plan"):
        st.write("**Your Personalized Workout Plan:**")
        if fitness_level == "Beginner":
            st.write("- 10 minutes of stretching")
            st.write("- 20 minutes of brisk walking")
            st.write("- 10 minutes of bodyweight exercises (e.g., squats, push-ups)")
        elif fitness_level == "Intermediate":
            st.write("- 10 minutes of dynamic warm-up")
            st.write("- 30 minutes of jogging or cycling")
            st.write("- 20 minutes of strength training")
        else:
            st.write("- 15 minutes of advanced warm-up")
            st.write("- 45 minutes of high-intensity interval training (HIIT)")
            st.write("- 30 minutes of weightlifting")

# Tab 14: Mindfulness Exercises
with tab14:
    st.header("Mindfulness Exercises")
    st.write("Practice mindfulness to reduce stress and improve focus.")

    exercise = st.selectbox("Choose a mindfulness exercise:", ["Deep Breathing", "Body Scan Meditation", "Gratitude Reflection"], key="mindfulness_exercise")

    if st.button("Start Exercise"):
        if exercise == "Deep Breathing":
            st.write("**Deep Breathing Exercise:**")
            st.write("1. Inhale deeply for 4 seconds.")
            st.write("2. Hold your breath for 7 seconds.")
            st.write("3. Exhale slowly for 8 seconds.")
            st.write("Repeat this cycle for 5 minutes.")
        elif exercise == "Body Scan Meditation":
            st.write("**Body Scan Meditation:**")
            st.write("1. Sit or lie down in a comfortable position.")
            st.write("2. Close your eyes and focus on your breathing.")
            st.write("3. Gradually bring your attention to each part of your body, starting from your toes to your head.")
        else:
            st.write("**Gratitude Reflection:**")
            st.write("1. Think of three things you are grateful for today.")
            st.write("2. Reflect on why these things are meaningful to you.")

# Tab 15: Weekly Progress Report
with tab15:
    st.header("Weekly Progress Report")
    st.write("View a summary of your progress over the past week.")

    calories_burned = st.number_input("Enter total calories burned this week:", min_value=0, key="weekly_calories")
    steps_taken = st.number_input("Enter total steps taken this week:", min_value=0, key="weekly_steps")
    hours_slept = st.number_input("Enter total hours slept this week:", min_value=0.0, step=0.1, key="weekly_sleep")

    if st.button("Generate Weekly Report"):
        st.write("**Your Weekly Progress Report:**")
        st.write(f"- Total Calories Burned: {calories_burned}")
        st.write(f"- Total Steps Taken: {steps_taken}")
        st.write(f"- Total Hours Slept: {hours_slept}")
        st.write("Keep up the great work!")
        
# Tab 16: Mental Health Check-In (Correctly placed under its own tab)
with tab16:
    st.header("Mental Health Check-In")
    st.write("Answer the following questions to assess your mental well-being:")

    q1 = st.radio("How often have you felt stressed in the past week?", ["Never", "Sometimes", "Often", "Always"], key="stress")
    q2 = st.radio("How often have you felt happy in the past week?", ["Never", "Sometimes", "Often", "Always"], key="happiness")
    q3 = st.radio("How often have you felt anxious in the past week?", ["Never", "Sometimes", "Often", "Always"], key="anxiety")

    if st.button("Submit Mental Health Check-In"):
        st.write("Thank you for sharing. Based on your responses:")
        if q1 == "Always" or q3 == "Always":
            st.write("You might be experiencing high levels of stress or anxiety. Consider seeking professional help.")
        elif q2 == "Never":
            st.write("It seems you might not be feeling happy often. Try engaging in activities you enjoy.")
        else:
            st.write("Your mental health seems balanced. Keep taking care of yourself!")

# Tab 17: AI Food Composition Analysis
with st.tabs(["AI Food Composition Analysis"])[0]:
    st.header("📸 AI Food Composition Analysis")
    st.write("Detect food ingredients, allergens, and nutrition values from images.")

    uploaded_file = st.file_uploader("Upload an image of food:", type=["jpg", "jpeg", "png"], key="food_composition_upload")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Food Image", use_container_width=True)

        if st.button("Analyze Food Composition", key="analyze_composition_button"):
            # Simulate AI analysis (replace with actual AI model call)
            st.write("**Detected Ingredients:** Rice, Chicken, Broccoli")
            st.write("**Allergens:** None")
            st.write("**Nutrition Values:**")
            st.write("- Calories: 450 kcal")
            st.write("- Proteins: 30g")
            st.write("- Carbohydrates: 50g")
            st.write("- Fats: 10g")

# Tab 18: AI-Powered Monthly Health Report
with st.tabs(["AI-Powered Monthly Health Report"])[0]:
    st.header("📊 AI-Powered Monthly Health Report")
    st.write("Generate a personalized report with progress tracking and health tips.")

    if st.button("Generate Monthly Report"):
        # Simulate report generation (replace with actual logic)
        st.write("**Your Monthly Health Report:**")
        st.write("- Total Calories Burned: 12,000 kcal")
        st.write("- Total Steps Taken: 150,000 steps")
        st.write("- Average Sleep Duration: 7.5 hours/day")
        st.write("**Health Tips:** Stay consistent with your exercise routine and maintain a balanced diet.")

# Tab 19: Intermittent Fasting Tracker
with st.tabs(["Intermittent Fasting Tracker"])[0]:
    st.header("🍽️ Intermittent Fasting Tracker")
    st.write("Track your fasting windows and eating schedules.")

    fasting_start = st.time_input("Enter your fasting start time:", key="fasting_start")
    fasting_end = st.time_input("Enter your fasting end time:", key="fasting_end")

    if st.button("Track Fasting"):
        st.write(f"**Fasting Window:** {fasting_start} to {fasting_end}")
        st.write("Keep up with your fasting schedule for better health!")

# Tab 20: Virtual Dietitian Chatbot
with st.tabs(["Virtual Dietitian Chatbot"])[0]:
    st.header("👨‍⚕️ Virtual Dietitian Chatbot")
    st.write("Chat with an AI-powered dietitian for personalized nutrition and health guidance.")

    user_query = st.text_input("Ask the Virtual Dietitian:", key="dietitian_query")
    if st.button("Get Advice"):
        # Simulate chatbot response (replace with actual AI model call)
        st.write("**Dietitian's Advice:** Based on your query, I recommend including more leafy greens and lean proteins in your diet.")

# Tab 21: Auto-Adjust Meal Plans
with st.tabs(["Auto-Adjust Meal Plans"])[0]:
    st.header("🔄 Auto-Adjust Meal Plans")
    st.write("Dynamically updates diet plans based on weight changes and goals.")

    current_weight = st.number_input("Enter your current weight (kg):", min_value=0.0, step=0.1, key="current_weight")
    goal_weight = st.number_input("Enter your goal weight (kg):", min_value=0.0, step=0.1, key="goal_weight")

    if st.button("Adjust Meal Plan"):
        if current_weight > goal_weight:
            st.write("**Suggested Meal Plan:** Focus on a calorie deficit diet with high protein and low carbs.")
        elif current_weight < goal_weight:
            st.write("**Suggested Meal Plan:** Focus on a calorie surplus diet with balanced macros.")
        else:
            st.write("**Suggested Meal Plan:** Maintain your current diet to sustain your weight.")
