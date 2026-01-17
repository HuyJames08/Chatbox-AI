# app.py
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import time
import random
import json
import logging
from google import genai
from google.genai.errors import APIError
from google.genai.types import GenerateContentConfig

# --- Cấu hình trang ---
st.set_page_config(page_title="Streamlit AI Chatbot ✨", layout="wide")

# --- Cấu hình Logging ---
logging.basicConfig(
    filename="gemini_errors.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Lấy API key từ môi trường ---
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Khởi tạo client Gemini ---
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"⚠️ Lỗi khởi tạo Gemini Client: {e}")
else:
    client = None

MODEL_NAME = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = """Bạn là 'StreamlitBot' — một trợ lý AI thân thiện và chuyên nghiệp, trả lời bằng tiếng Việt. 
Hãy ngắn gọn, tự nhiên, và nếu không chắc chắn, hãy nói 'Tôi chưa rõ lắm về điều đó'."""

# --- Đường dẫn file lưu hội thoại ---
HISTORY_FILE = "chat_history.json"


# --- Hàm xử lý lưu/đọc JSON ---
def load_history():
    """Đọc file JSON chứa hội thoại cũ."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            return []
    return []

def save_history(messages):
    """Ghi toàn bộ lịch sử hội thoại ra file JSON."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Lỗi lưu hội thoại JSON: {e}")

def clear_history():
    """Xóa file lịch sử và session."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.session_state.clear()
    st.rerun()


# --- Hàm gọi API Gemini với retry ---
def get_gemini_response(prompt_history, current_user_prompt,
                        model_name=MODEL_NAME,
                        system_instruction=SYSTEM_INSTRUCTION,
                        max_retries=5, base_delay=1.0):
    if not client:
        return "⚠️ Chưa có API Key. Vui lòng thiết lập biến môi trường GEMINI_API_KEY."

    contents = []
    for msg in prompt_history:
        role_map = {"user": "user", "assistant": "model"}
        contents.append({
            "role": role_map[msg["role"]],
            "parts": [{"text": msg["content"]}]
        })
    contents.append({"role": "user", "parts": [{"text": current_user_prompt}]})

    config = GenerateContentConfig(system_instruction=system_instruction)

    attempt = 0
    while attempt < max_retries:
        try:
            attempt += 1
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            return response.text  # ✅ Thành công

        except APIError as e:
            logging.warning(f"Attempt {attempt}/{max_retries} - APIError: {e}")
            if attempt >= max_retries:
                logging.error(f"Max retries reached. APIError final: {e}")
                break
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, 0.5 * delay)
            time.sleep(delay + jitter)
            continue

        except Exception as e:
            logging.exception(f"Attempt {attempt}/{max_retries} - Unexpected error: {e}")
            if attempt >= max_retries:
                break
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, 0.5 * delay)
            time.sleep(delay + jitter)
            continue

    fallback = (
        "⚠️ Hiện tại không thể kết nối tới Gemini (mô hình có thể đang quá tải). "
        "Vui lòng thử lại sau vài phút.\n\n"
        "👉 Gợi ý: Nhấn **Thử lại**, hoặc kiểm tra lại API Key / quota tài khoản."
    )
    return fallback


# --- Hiển thị tin nhắn đẹp ---
def render_message(role, content):
    avatar = "🤖" if role == "assistant" else "🧍‍♂️"
    bg_color = "#F0F2F6" if role == "assistant" else "#DCF8C6"
    align = "left" if role == "assistant" else "right"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: {align}; margin: 8px 0;'>
            <div style='background-color:{bg_color}; padding:10px 15px; border-radius:15px; max-width:70%;'>
                <b>{avatar} {'StreamlitBot' if role == 'assistant' else 'Bạn'}:</b><br>{content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Giao diện chính ---
def main():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712100.png", width=160)
        st.markdown("### 🤖 StreamlitBot")
        st.write("Trợ lý AI powered by **Gemini 2.5 Flash**.")
        st.write("Hỏi tôi bất cứ điều gì bằng tiếng Việt 💬")
        st.markdown("---")
        if st.button("🗑️ Xóa lịch sử chat"):
            clear_history()

    with col2:
        st.title("💭 Chat cùng AI")
        if not client:
            st.warning("⚠️ Vui lòng thiết lập biến môi trường GEMINI_API_KEY để ứng dụng hoạt động.")
            return

        # --- Khởi tạo hoặc nạp lại lịch sử ---
        if "messages" not in st.session_state:
            saved_msgs = load_history()
            if saved_msgs:
                st.session_state["messages"] = saved_msgs
            else:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "Xin chào! Tôi là StreamlitBot 😊. Tôi có thể giúp gì cho bạn hôm nay?"}
                ]

        # --- Hiển thị hội thoại ---
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])

        # --- Nhập câu hỏi ---
        if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            render_message("user", prompt)

            with st.spinner("StreamlitBot đang suy nghĩ..."):
                history = st.session_state.messages[:-1]
                response = get_gemini_response(history, prompt)

            # --- Nếu lỗi ---
            if response.startswith("⚠️"):
                st.error(response)
                if st.button("🔁 Thử lại"):
                    with st.spinner("Đang thử lại..."):
                        response2 = get_gemini_response(history, prompt)
                    render_message("assistant", response2)
                    st.session_state.messages.append({"role": "assistant", "content": response2})
                    save_history(st.session_state.messages)
            else:
                render_message("assistant", response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            # --- Lưu lại hội thoại mới ---
            save_history(st.session_state.messages)


if __name__ == "__main__":
    main()
