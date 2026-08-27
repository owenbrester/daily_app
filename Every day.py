
user_state = {
    "screentime": 0,
    "screentime_elo" : 0,
    "gym_elo": 0,
    "streak": 0,
    "rest_used": False,
    "last_workouts": [],
    "student" : False,
    "study_time": 0,
    "study_elo": 0,
    "classes": [],
    "class_intensity": []
}

def screentime_point_function(minutes):
    if minutes <= 30:
        return 17.5
    elif minutes <= 45:
        return 12.5
    elif minutes <= 60:
        return 7.5
    elif minutes <= 90:
        return 5
    elif minutes <= 120:
        return 0
    elif minutes <= 150:
        return -5
    elif minutes <= 180:
        return -7.5
    elif minutes <= 210:
        return -12.5
    else :
        return -17.5

def study_time_point_function(minutes):
    if user_state["class_intensity"] == ["high"]:
        if minutes < 30:
            return -17.5
        elif minutes <= 60:
            return -12.5
        elif minutes <= 120:
            return -7.5
        elif minutes <= 180:
            return -5
        elif minutes <= 240:
            return -2.5
        elif minutes <= 300:
            return 8.75
        elif minutes < 360:
            return 12.5
        else :
            return 17.5
    elif user_state["class_intensity"] == ["medium"]:
        if minutes < 30:
            return -17.5
        elif minutes <= 45:
            return -12.5
        elif minutes <= 60:
            return -7.5
        elif minutes <= 120:
            return -2.5
        elif minutes <= 180:
            return 7.5
        elif minutes < 240:
            return 12.5
        else :
            return 17.5
    elif user_state["class_intensity"] == ["low"]:
        if minutes < 30:
            return -17.5
        elif minutes <= 45:
            return 2.5
        elif minutes <= 60:
            return 7.5
        elif minutes < 120:
            return 12.5
        else :
            return 17.5
    else :
        return 0


def time_points(minutes):
    return min(minutes, 17.5)

def rotation_bonus(workout, history):
    if workout not in history:
        return 17.5
    elif history.count(workout) == 1:
        return 5
    else:
        return -15

def handle_streak(state, went):
    if went:
        state["streak"] += 1
        state["rest_used"] = False
        return 0

    if state["streak"] >= 5 and not state["rest_used"]:
        state["rest_used"] = True
        state["streak"] = 0
        return 0 #rest day

    state["streak"] = 0
    return -40 #skipping penalty

def rank_multiplier(elo):
    if elo < 100: return 2
    if elo < 200: return 1.82142857143
    if elo < 300: return 1.64285714286
    if elo < 400: return 1.46428571429
    if elo < 500: return 1.28571428571
    if elo < 600: return 1.10714285714
    if elo < 700: return 0.92857142857
    if elo < 800: return 0.75000000000
    return .57142857142

#variables
rank = ["iron", "bronze", "silver", "gold", "platinum", "diamond", "ascendant", "immortal", "radiant"]

today_points = 0

#elo mapping
elo = {}

start = 0
step = 100

for i in range(len(rank)):
    elo[rank[i]] = start + i * step

#user input
screentime = input("Enter today's screen time (HH:MM): ")
h, m = screentime.split(":")
total_screentime = int(h) * 60 + int(m)

base_screentime = screentime_point_function(total_screentime)
base_screentime *= rank_multiplier(user_state["screentime_elo"])

#gym input
gym_input = input("Did you go to the gym today? (y/n): ").lower()
went_to_gym = gym_input == "y"

gym_minutes = 0
gym_workout = ""

if went_to_gym:
    gym_time = input("How long did you workout (HH:MM): ")
    h, m = gym_time.split(":")
    gym_minutes = int(h) * 60 +int(m)

    gym_workout = input("What did you work out today? (arms, legs, chest, back, core): ").lower()

    print("Workout logged")

else:
    print("No gym today.")

if went_to_gym:
    base = time_points(gym_minutes)
    rotation = rotation_bonus(gym_workout, user_state["last_workouts"])
    today_points = (base + rotation) / 2
else:
    today_points = handle_streak(user_state, False)

#streak bonus if went to gym
if went_to_gym:
    today_points += handle_streak(user_state, True)

today_points *= rank_multiplier(user_state["gym_elo"])

user_state["gym_elo"] += int(today_points)
user_state["gym_elo"] = max(0, user_state["gym_elo"])

if went_to_gym:
    user_state["last_workouts"].append(gym_workout)
    if len(user_state["last_workouts"]) > 3:
        user_state["last_workouts"].pop(0) #reset cycle for what area was worked out

student_bool = input("Are you a student? (y/n): ").lower()
student_today = student_bool == "y"

if student_today:
    user_state["student"] = True
    classes_base = input("What classes did you have today: ").lower()
    user_state["classes"].append(classes_base)

student_intensity = input("How intense is the workload today? (h/m/l): ").lower()
high_intensity = student_intensity == "h"
medium_intensity = student_intensity == "m"
low_intensity = student_intensity == "l"

if high_intensity:
    user_state["class_intensity"].append("high")
if medium_intensity:
    user_state["class_intensity"].append("medium")
if low_intensity:
    user_state["class_intensity"].append("low")

study_time = input("How much time did you study today (HH:MM): ").lower()
h, m = study_time.split(":")
study_minutes = int(h) * 60 + int(m)

user_state["study_time"] = study_minutes
user_state["study_time"] = max(0, user_state["study_time"])

study_points = study_time_point_function(user_state["study_time"])
study_points *= rank_multiplier(user_state["study_elo"])
user_state["study_elo"] = study_points

#print("Screentime points today:", float(base_screentime))
#print("Gym points today:", int(today_points))
#print("Gym ELO:", user_state["gym_elo"])
#print("Workout history:", user_state["last_workouts"])
#print("Streak:", user_state["streak"])
#print("Classes today: ", user_state["classes"])
#print("Study Points today: ", user_state["study_elo"])


