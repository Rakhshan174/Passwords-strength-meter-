import streamlit as st
import random
import string
from zxcvbn import zxcvbn  # ✅ Import zxcvbn for password strength analysis

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
    }
    .generated-password {
        font-size: 18px;
        font-weight: bold;
        color: #2a5298;
        background: #d1ecf1;
        padding: 5px;
        border-radius: 5px;
    }
    .strength-meter {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        padding: 5px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Function to generate a strong password
def generate_password(length=12, use_letters=True, use_digits=True, use_specials=True):
    chars = ""
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_specials:
        chars += string.punctuation
    if not chars:
        return "⚠️ Select at least one option!"
    return ''.join(random.choice(chars) for _ in range(length))

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: black;'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)
password = st.text_input("Enter your password:", type="password")

if password:
    result = zxcvbn(password)  # ✅ Now using zxcvbn for strength calculation
    score = result["score"]
    feedback = result["feedback"].get("suggestions", ["Looks good!"])
    crack_time = result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]

    # Define strength levels
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    colors = ["#FF4B4B", "#FFA500", "#FFD700", "#9ACD32", "#32CD32"]

    # Show strength level
    strength_text = strength_levels[score]
    color = colors[score]
    strength_percentage = (score + 1) * 20

    st.markdown(f"<h3 style='color: {color};'>Strength Score: {score} / 4 ({strength_text})</h3>", unsafe_allow_html=True)
    st.progress(strength_percentage / 100)
    st.markdown(f"<div class='strength-meter' style='background: {color}; color: white;'>{strength_text} ({strength_percentage}%)</div>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: darkgreen;'>🔓 Crack Time Estimate: `{crack_time}`</h4>", unsafe_allow_html=True)

    # Display feedback
    if feedback:
        for msg in feedback:
            st.warning(msg)

# Password Generator Section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>🔑 Custom Password Generator</h3>", unsafe_allow_html=True)

length = st.slider("Select password length:", min_value=6, max_value=24, value=12)
use_letters = st.checkbox("Include Letters (A-Z, a-z)", value=True)
use_digits = st.checkbox("Include Numbers (0-9)", value=True)
use_specials = st.checkbox("Include Special Characters (!@#$%^&*)", value=True)

if st.button("Generate Custom Password"):
    strong_password = generate_password(length, use_letters, use_digits, use_specials)
    st.markdown(f"<p class='generated-password'>🔒 {strong_password}</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>Built with ❤️ using Streamlit</h5>", unsafe_allow_html=True)
