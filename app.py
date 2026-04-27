import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Health Calculator",
    page_icon="💪",
    layout="wide"
)

st.title("💪 Personal Health Calculator")
st.markdown("Calculate your BMI, daily calories, water intake "
            "and get personalised health insights.")
st.markdown("---")


st.sidebar.header("👤 Your Details")

name   = st.sidebar.text_input("Your name:", value="")
age    = st.sidebar.number_input("Age:", 10, 100, 20)
gender = st.sidebar.radio("Gender:", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm):", 100, 250, 170)
weight = st.sidebar.number_input("Weight (kg):", 30, 200, 65)

activity = st.sidebar.selectbox("Activity Level:", [
    "Sedentary (little or no exercise)",
    "Lightly active (1-3 days/week)",
    "Moderately active (3-5 days/week)",
    "Very active (6-7 days/week)",
    "Extra active (physical job)"
])

goal = st.sidebar.selectbox("Your Goal:", [
    "Lose Weight",
    "Maintain Weight",
    "Gain Muscle"
])


height_m = height / 100
bmi      = weight / (height_m ** 2)


if bmi < 18.5:
    bmi_cat   = "Underweight"
    bmi_color = "#3498db"
elif bmi < 25:
    bmi_cat   = "Normal Weight"
    bmi_color = "#2ecc71"
elif bmi < 30:
    bmi_cat   = "Overweight"
    bmi_color = "#f39c12"
else:
    bmi_cat   = "Obese"
    bmi_color = "#e74c3c"


if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161


activity_map = {
    "Sedentary (little or no exercise)":    1.2,
    "Lightly active (1-3 days/week)":       1.375,
    "Moderately active (3-5 days/week)":    1.55,
    "Very active (6-7 days/week)":          1.725,
    "Extra active (physical job)":          1.9
}
tdee = bmr * activity_map[activity]

if goal == "Lose Weight":
    cal_goal = tdee - 500
    goal_note = "500 calorie deficit for ~0.5kg/week loss"
elif goal == "Gain Muscle":
    cal_goal = tdee + 300
    goal_note = "300 calorie surplus for lean muscle gain"
else:
    cal_goal = tdee
    goal_note = "Maintain current weight"

water = weight * 35


ideal_min = 18.5 * (height_m ** 2)
ideal_max = 24.9 * (height_m ** 2)


tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BMI Analysis",
    "🍽️ Nutrition",
    "💧 Hydration",
    "📈 Progress Tracker"
])


with tab1:
    greeting = f"### Results for {name}" if name else "### Your Results"
    st.markdown(greeting)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("BMI",          f"{bmi:.1f}")
    col2.metric("Category",     bmi_cat)
    col3.metric("Ideal Weight", f"{ideal_min:.1f}–{ideal_max:.1f} kg")
    col4.metric("Height",       f"{height} cm")


    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.set_xlim(10, 45)
    ax.set_ylim(0, 1)
    ax.axis('off')

    bands = [
        (10,   18.5, '#3498db', 'Underweight'),
        (18.5, 25,   '#2ecc71', 'Normal'),
        (25,   30,   '#f39c12', 'Overweight'),
        (30,   45,   '#e74c3c', 'Obese')
    ]
    for start, end, color, label in bands:
        ax.barh(0.5, end - start, left=start,
                height=0.4, color=color, alpha=0.7)
        ax.text((start + end) / 2, 0.85, label,
                ha='center', fontsize=9, fontweight='bold')


    bmi_clamped = min(max(bmi, 10), 44)
    ax.annotate('', xy=(bmi_clamped, 0.3),
                xytext=(bmi_clamped, 0.05),
                arrowprops=dict(arrowstyle='->', color='black',
                                lw=2.5))
    ax.text(bmi_clamped, 0.0, f'YOU\n{bmi:.1f}',
            ha='center', fontsize=9, fontweight='bold')
    ax.set_title('Your BMI on the Scale', fontsize=13, pad=10)
    plt.tight_layout()
    st.pyplot(fig)


    st.markdown("### 💡 Health Insights")
    if bmi_cat == "Normal Weight":
        st.success(f"✅ Great job! Your BMI of {bmi:.1f} is in "
                   f"the healthy range.")
    elif bmi_cat == "Underweight":
        diff = ideal_min - weight
        st.info(f"📈 You are {diff:.1f} kg below the healthy "
                f"range. Consider increasing caloric intake.")
    elif bmi_cat == "Overweight":
        diff = weight - ideal_max
        st.warning(f"⚠️ You are {diff:.1f} kg above the healthy "
                   f"range. A calorie deficit can help.")
    else:
        diff = weight - ideal_max
        st.error(f"🚨 You are {diff:.1f} kg above the healthy "
                 f"range. Consult a healthcare professional.")


with tab2:
    st.markdown("### 🍽️ Daily Calorie Needs")

    col1, col2, col3 = st.columns(3)
    col1.metric("BMR (Base)",    f"{bmr:.0f} kcal")
    col2.metric("TDEE (Active)", f"{tdee:.0f} kcal")
    col3.metric("Your Goal",     f"{cal_goal:.0f} kcal",
                goal_note)

  
    protein = weight * 2.0
    fat     = cal_goal * 0.25 / 9
    carbs   = (cal_goal - protein * 4 - fat * 9) / 4

    st.markdown("### 🥗 Recommended Daily Macros")
    m1, m2, m3 = st.columns(3)
    m1.metric("Protein", f"{protein:.0f}g",
              f"{protein*4:.0f} kcal")
    m2.metric("Carbs",   f"{carbs:.0f}g",
              f"{carbs*4:.0f} kcal")
    m3.metric("Fat",     f"{fat:.0f}g",
              f"{fat*9:.0f} kcal")

    fig, ax = plt.subplots(figsize=(6, 5))
    sizes  = [protein * 4, carbs * 4, fat * 9]
    labels = [f'Protein\n{protein:.0f}g',
              f'Carbs\n{carbs:.0f}g',
              f'Fat\n{fat:.0f}g']
    colors = ['#3498db', '#2ecc71', '#f39c12']
    ax.pie(sizes, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90,
           wedgeprops={'edgecolor': 'black'})
    ax.set_title('Daily Macro Distribution', fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)


    st.markdown("### 🍳 Suggested Meal Split")
    meals = pd.DataFrame({
        'Meal':     ['Breakfast', 'Lunch',
                     'Snack', 'Dinner'],
        'Calories': [
            round(cal_goal * 0.25),
            round(cal_goal * 0.35),
            round(cal_goal * 0.10),
            round(cal_goal * 0.30)
        ],
        'Protein (g)': [
            round(protein * 0.25),
            round(protein * 0.35),
            round(protein * 0.10),
            round(protein * 0.30)
        ]
    })
    st.dataframe(meals, use_container_width=True,
                 hide_index=True)


with tab3:
    st.markdown("### 💧 Daily Water Intake")

    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Water",  f"{water:.0f} ml")
    col2.metric("In Litres",    f"{water/1000:.2f} L")
    col3.metric("Glasses (250ml)", f"{water/250:.0f}")


    st.markdown("### ⏰ Hydration Schedule")
    schedule = pd.DataFrame({
        'Time':   ['Wake up (6AM)', 'Morning (8AM)',
                   'Before lunch (12PM)', 'Afternoon (3PM)',
                   'Evening (6PM)', 'Before bed (9PM)'],
        'Amount': ['500 ml', f'{water*0.15:.0f} ml',
                   '500 ml', f'{water*0.20:.0f} ml',
                   f'{water*0.15:.0f} ml', '250 ml'],
        'Tip':    [
            'Kickstart metabolism',
            'Stay ahead of thirst',
            'Aid digestion',
            'Beat afternoon slump',
            'Post workout hydration',
            'Support overnight recovery'
        ]
    })
    st.dataframe(schedule, use_container_width=True,
                 hide_index=True)


    glasses_needed = int(water / 250)
    fig, ax = plt.subplots(figsize=(10, 3))
    for i in range(min(glasses_needed, 16)):
        color = '#3498db' if i < glasses_needed else '#ecf0f1'
        ax.bar(i, 1, color=color,
               edgecolor='white', width=0.8)
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(0, 1.3)
    ax.axis('off')
    ax.set_title(f'Daily Water Goal: '
                 f'{glasses_needed} glasses of 250ml',
                 fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)


with tab4:
    st.markdown("### 📈 Simulate Your Weight Progress")

    weeks = st.slider("Weeks to simulate:", 4, 52, 12)
    weekly_change = -0.5 if goal == "Lose Weight" else \
                    (0.25 if goal == "Gain Muscle" else 0)

    projected = [weight + (i * weekly_change)
                 for i in range(weeks + 1)]
    week_labels = list(range(weeks + 1))

    fig, ax = plt.subplots(figsize=(10, 5))
    color = '#2ecc71' if goal == "Gain Muscle" else \
            '#e74c3c' if goal == "Lose Weight" else '#3498db'
    ax.plot(week_labels, projected,
            color=color, linewidth=2.5,
            marker='o', markersize=4)
    ax.fill_between(week_labels, projected,
                    projected[0], alpha=0.15, color=color)
    ax.axhline(y=ideal_min, color='#2ecc71',
               linestyle='--', alpha=0.7,
               label=f'Ideal min ({ideal_min:.1f}kg)')
    ax.axhline(y=ideal_max, color='#f39c12',
               linestyle='--', alpha=0.7,
               label=f'Ideal max ({ideal_max:.1f}kg)')
    ax.set_title(f'Projected Weight Over {weeks} Weeks',
                 fontsize=14)
    ax.set_xlabel('Week')
    ax.set_ylabel('Weight (kg)')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    final_weight = projected[-1]
    total_change = final_weight - weight
    st.info(f"📊 After {weeks} weeks: "
            f"**{final_weight:.1f} kg** "
            f"({total_change:+.1f} kg from now)")

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "For educational purposes only — "
    "consult a healthcare professional for medical advice."
)