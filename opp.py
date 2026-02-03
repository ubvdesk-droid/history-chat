import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח - השתמשנו במפתח הישיר שלך כדי למנוע בעיות os.getenv
API_KEY = "AIzaSyDiFlWO0X3AFCmC5hehqzw3971B_FEBBQc"
genai.configure(api_key=API_KEY)

st.title("צ'אט היסטורי")

# 2. רשימת הדמויות
characters = {
    "יוליוס קיסר": "אתה יוליוס קיסר. ענה בעברית סמכותית.",
    "אלברט איינשטיין": "אתה אלברט איינשטיין. ענה בעברית כפיזיקאי סקרן.",
    "נפוליאון בונפרטה": "אתה נפוליאון. ענה בעברית כקיסר צרפת."
}

char_choice = st.sidebar.selectbox("בחר דמות:", list(characters.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת היסטוריית ההודעות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. קבלת קלט מהמשתמש
if prompt := st.chat_input("שאל אותי משהו..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # שימוש במודל יציב
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # התיקון הקריטי: הגדרת ה-contents בדיוק כפי שהמודל מצפה (כרשימה)
        instruction = characters[char_choice]
        response = model.generate_content([instruction, prompt])
        
        if response.text:
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            st.error("המודל לא החזיר תשובה, נסה שוב.")

    except Exception as e:
        st.error(f"שגיאה: {e}")

