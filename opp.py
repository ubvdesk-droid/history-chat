import streamlit as st
import google.generativeai as genai

# הגדרת כותרת האתר
st.set_page_config(page_title="צ'אט עם ההיסטוריה", layout="wide")

# כאן תכניס את ה-API Key שקיבלת מגוגל
API_KEY = "AIzaSyC1w7s22qrk5WQXa2GoYSEyrdEMeqRXk_A"
genai.configure(api_key=API_KEY)

# תפריט בחירת דמויות
st.sidebar.title("בחר דמות:")
char_choice = st.sidebar.selectbox("", ["יוליוס קיסר", "נפוליאון", "אלברט איינשטיין"])

# הגדרות לכל דמות
characters = {
    "יוליוס קיסר": "אתה יוליוס קיסר. ענה תמיד בעברית גבוהה וסמכותית. אתה מנהיג רומאי.",
    "נפוליאון": "אתה נפוליאון בונפרטה. ענה בעברית רהוטה עם ביטחון עצמי של קיסר צרפתי.",
    "אלברט איינשטיין": "אתה אלברט איינשטיין. ענה בעברית סבלנית, חכמה ומלאת סקרנות."
}

st.title(f"שיחה עם {char_choice}")

# ניהול הזיכרון של הצ'אט
if "messages" not in st.session_state or st.sidebar.button("נקה צ'אט"):
    st.session_state.messages = []

# הצגת ההודעות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# תיבת קלט מהמשתמש
if prompt := st.chat_input("כתוב משהו..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # שליחה למודל של גוגל
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})






