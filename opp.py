import streamlit as st
import google.generativeai as genai

# הגדרת המפתח - וודא שהמפתח החדש שלך כאן
API_KEY = "AIzaSyDiFlWO0X3AFCmC5hehqzw3971B_FEBBQc"

st.title("צ'אט היסטורי")

# רשימת הדמויות
characters = {
    "יוליוס קיסר": "אתה יוליוס קיסר, קיסר רומא. ענה בעברית קולחת וסמכותית.",
    "אלברט איינשטיין": "אתה אלברט איינשטיין. ענה בעברית, היה חכם וסקרן.",
    "נפוליאון בונפרטה": "אתה נפוליאון. ענה בעברית כקיסר צרפת הגאה."
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
        # שימוש במודל עם הגדרות מלאות למניעת NotFound
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([characters[char_choice], prompt])
        
        full_response = response.text
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"שגיאה: {e}")

