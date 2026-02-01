import streamlit as st
import google.generativeai as genai

# הגדרת המפתח והחיבור
API_KEY = "AIzaSyDiFlWO0X3AFCmC5hehqzw3971B_FEBBQc"
genai.configure(api_key=API_KEY)

st.title("צ'אט היסטורי")

# רשימת הדמויות
characters = {
    "יוליוס קיסר": "אתה יוליוס קיסר. ענה בעברית סמכותית.",
    "אלברט איינשטיין": "אתה אלברט איינשטיין. ענה בעברית כפיזיקאי סקרן.",
    "נפוליאון בונפרטה": "אתה נפוליאון. ענה בעברית כקיסר צרפת."
}

char_choice = st.sidebar.selectbox("בחר דמות:", list(characters.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("שאל אותי משהו..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # שימוש במודל היציב ביותר למניעת 404
        model = genai.GenerativeModel('gemini-pro')
        
        # שליחת ההנחיה והשאלה יחד
        full_prompt = f"{characters[char_choice]}\n\n{prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"שגיאה: {e}")
