import streamlit as st
import google.generativeai as genai

# 1. הגדרת המפתח והחיבור
API_KEY = "AIzaSyDiFlWO0X3AFCmC5hehqzw3971B_FEBBQc"
genai.configure(api_key=API_KEY)

st.title("צ'אט היסטורי")

# 2. הגדרת דמויות
characters = {
    "יוליוס קיסר": "אתה יוליוס קיסר, קיסר רומא. ענה בעברית סמכותית.",
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
        # 3. שימוש במודל היציב ביותר (1.0 Pro) שעובד כמעט תמיד כש-1.5 נותן 404
        model = genai.GenerativeModel('gemini-pro')
        
        # בניית השאלה עם ההנחיה בתוכה
        full_prompt = f"{characters[char_choice]}\n\nהמשתמש שואל: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # ניסיון אחרון עם המודל החדש אם הפרו נכשל
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{characters[char_choice]}\n\n{prompt}")
            st.markdown(response.text)
        except:
            st.error("גוגל עדיין לא מאשרת את המודל. נסה לעשות Reboot לאפליקציה ב-Streamlit.")
