import streamlit as st
import re
import random
import string

# Set full page configuration
st.set_page_config(page_title="🔐 Advanced Password Strength Meter", page_icon="🔑", layout="wide")

# Sidebar for advanced options
st.sidebar.title("Advanced Options")
gen_length = st.sidebar.slider("Generator Length", min_value=8, max_value=32, value=16)
include_upper = st.sidebar.checkbox("Include Uppercase", value=True)
include_lower = st.sidebar.checkbox("Include Lowercase", value=True)
include_digits = st.sidebar.checkbox("Include Digits", value=True)
include_special = st.sidebar.checkbox("Include Special Characters", value=True)

# Custom CSS
st.markdown("""
    <style>
    body { background-color: #f8f9fa; }
    .stApp { background-color: #f8f9fa; padding: 20px; }
    .title { text-align: center; color: #4A90E2; font-size: 36px; font-weight: bold; }
    .subtitle { text-align: center; color: #555; font-size: 20px; }
    .weak { color: red; font-weight: bold; }
    .moderate { color: orange; font-weight: bold; }
    .strong { color: green; font-weight: bold; }
    .container { padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    .copy-button { background: #4A90E2; color: white; border-radius: 5px; padding: 8px 15px; cursor: pointer; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("<h1 class='title'>🔐 Advanced Password Strength Meter</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Make your passwords as secure as your data.</p>", unsafe_allow_html=True)

# List of common weak passwords to blacklist
COMMON_PASSWORDS = {"password", "123456", "123456789", "qwerty", "abc123", "password1", "12345", "12345678", "admin"}

# Function to evaluate password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in COMMON_PASSWORDS:
        return "Weak", "❌ Too common! Choose a unique password."

    # Length Evaluation
    if len(password) >= 20:
        score += 3
    elif len(password) >= 16:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ At least 8 characters needed.")

    # Check for both uppercase and lowercase letters
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Check for digits
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one digit (0-9).")

    # Check for special characters
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Return rating based on score
    if score >= 7:
        return "Strong", "✅ Your password is extremely strong!"
    elif score >= 4:
        return "Moderate", "⚠️ Your password is moderate.\n" + "\n".join(feedback)
    else:
        return "Weak", "❌ Your password is weak!\n" + "\n".join(feedback)

# Function to generate a strong password based on options
def generate_strong_password(length, upper, lower, digits, special):
    char_pool = ""
    if upper:
        char_pool += string.ascii_uppercase
    if lower:
        char_pool += string.ascii_lowercase
    if digits:
        char_pool += string.digits
    if special:
        char_pool += "!@#$%^&*"
    if not char_pool:
        return "Please select at least one character type for generation."
    return ''.join(random.choice(char_pool) for _ in range(length))

# Main Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔑 Password Strength Checker")
    user_password = st.text_input("Enter your password", type="password", placeholder="Type your password here...")
    
    if user_password:
        rating, rating_feedback = check_password_strength(user_password)
        color_class = "strong" if rating == "Strong" else "moderate" if rating == "Moderate" else "weak"
        # Replace newlines with <br> for HTML display
        feedback_html = rating_feedback.replace("\n", "<br>")
        st.markdown(f"<h3 class='{color_class}'>🔹 {rating} Password</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='{color_class}'>{feedback_html}</p>", unsafe_allow_html=True)
        meter_value = 100 if rating == "Strong" else 60 if rating == "Moderate" else 20
        st.progress(meter_value / 100)

with col2:
    st.subheader("🔑 Password Generator")
    if st.button("Generate Password"):
        new_pass = generate_strong_password(gen_length, include_upper, include_lower, include_digits, include_special)
        st.text_input("💡 Suggested Password", new_pass, key="generated_password")
        st.code(new_pass, language="bash")
        st.markdown(f"<button class='copy-button' onclick='navigator.clipboard.writeText(\"{new_pass}\")'>📋 Copy</button>", unsafe_allow_html=True)

# Additional Features & Security Tips Section
st.markdown("---")
st.subheader("📈 Advanced Features & Security Tips")
st.markdown("""
- **Live Feedback:** See instant strength updates as you type.
- **Custom Generator Options:** Adjust length and character types from the sidebar.
- **Security Best Practices:**  
  - Use at least **20 characters** for high security.  
  - Mix **uppercase, lowercase, numbers, and symbols**.  
  - Avoid common or predictable passwords.  
  - Use a **password manager** and enable **2FA** for enhanced security.  
- **Responsive UI:** Enjoy a full-width, professional design with smooth interactions.
""")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>🔐 Secure your digital life with advanced security practices!</p>", unsafe_allow_html=True)
