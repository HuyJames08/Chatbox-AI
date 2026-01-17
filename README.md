# 🤖 Chatbox AI - Streamlit + Gemini

Một chatbot AI thân thiện được xây dựng bằng **Google Gemini API** và **Streamlit**.  
Hỗ trợ tiếng Việt, giao diện đẹp, có lưu lịch sử hội thoại ra file `.json`, tự động retry khi API quá tải.

---

## ✨ Tính năng

- 💬 **Chat AI bằng tiếng Việt** - Trợ lý AI tên StreamlitBot, thân thiện và chuyên nghiệp
- 🤖 **Gemini 2.5 Flash** - Model AI mạnh mẽ, nhanh và tiết kiệm chi phí
- 💾 **Lưu lịch sử hội thoại** - Tự động lưu vào file `chat_history.json` (JSON format)
- 🔁 **Tự động retry thông minh** - Khi API quá tải, hệ thống tự retry tối đa 5 lần với exponential backoff
- 🗑️ **Quản lý lịch sử** - Nút xóa lịch sử chat trên giao diện
- 🎨 **Giao diện 2 cột** - Sidebar với logo, thông tin; chat area chính
- 🔒 **Bảo mật** - Sử dụng `.env` file cho API key, không push lên GitHub
- 📝 **Logging chi tiết** - Ghi lỗi vào file `gemini_errors.log`

---

## 🗂️ Cấu trúc thư mục

```
Chatbox-AI/
│
├── app.py                    # File ứng dụng chính
├── requirements.txt          # Các thư viện cần cài đặt
├── chat_history.json         # Lịch sử chat (tự tạo khi chạy)
├── gemini_errors.log         # Log lỗi API (tự tạo)
├── README.md                 # File hướng dẫn này
├── .env                      # Biến môi trường (KHÔNG push GitHub)
├── .gitignore                # Các file bỏ qua khi push GitHub
└── data/                     # Thư mục dữ liệu (nếu cần)
```

---

## 🛠️ Yêu cầu hệ thống

- **Python 3.9+** (khuyến cáo 3.10 hoặc cao hơn)
- **Tài khoản Google AI** với Gemini API Key (lấy tại [Google AI Studio](https://aistudio.google.com/app/apikey))
- **Hệ điều hành**: Windows / macOS / Linux
- **Internet connection** (để kết nối API Gemini)

---

## 📥 Hướng dẫn cài đặt

### **Bước 1️⃣: Cài đặt Python**

Tải Python từ: 👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

**Khi cài đặt, bắt buộc tick** ☑ **Add Python to PATH**

Kiểm tra cài đặt:
```bash
python --version
```

---

### **Bước 2️⃣: Clone hoặc Download dự án**

**Tùy chọn A - Nếu dự án đã trên GitHub:**
```bash
git clone https://github.com/HuyJames08/Chatbox-AI.git
cd Chatbox-AI
```

**Tùy chọn B - Nếu chưa có Git:**
- Download file ZIP từ GitHub
- Giải nén vào thư mục bất kỳ
- Mở PowerShell/Terminal tại thư mục đó

---

### **Bước 3️⃣: Cài đặt các thư viện**

Trong thư mục dự án, chạy lệnh:
```bash
pip install -r requirements.txt
```

**Thư viện sẽ được cài đặt:**
- `streamlit` - Framework web app
- `google-genai` - Google Gemini API client
- `python-dotenv` - Quản lý biến môi trường

---

### **Bước 4️⃣: Thiết lập API Key Gemini**

1. Truy cập 👉 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Đăng nhập bằng tài khoản Google
3. Nhấn **"Create API key"** → **"Create API key in new project"**
4. Copy API key (dạng `AIza...`)

5. Tạo file `.env` trong thư mục dự án:
```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

**Thay `YOUR_API_KEY_HERE` bằng API key của bạn**

⚠️ **Không bao giờ share file `.env` hoặc commit lên GitHub!**

---

## 🚀 Chạy ứng dụng

Mở PowerShell/Terminal tại thư mục dự án và chạy:

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở ở `http://localhost:8501` trên trình duyệt của bạn.

---

## 💬 Cách sử dụng

1. **Nhập câu hỏi** vào ô chat input
2. **Đợi trợ lý AI** trả lời (có loading spinner)
3. **Lịch sử chat** tự động lưu vào `chat_history.json`
4. **Xóa lịch sử** bằng nút 🗑️ trên sidebar
5. **Reload lại trang** sẽ hiển thị các tin nhắn cũ

---

## 🔧 Các tính năng chi tiết

### **Hệ thống Retry thông minh**
- Khi API quá tải → Tự retry tối đa 5 lần
- Thời gian chờ tăng dần (exponential backoff): 1s → 2s → 4s → 8s → 16s
- Thêm random jitter để tránh thundering herd problem

### **Logging & Error Handling**
- Tất cả lỗi được ghi vào `gemini_errors.log`
- Hiển thị lỗi thân thiện cho người dùng
- Nút "Thử lại" khi API quá tải

### **Lưu lịch sử**
- Mỗi khi chat, tự động lưu vào `chat_history.json`
- Format: JSON array với các object `{role, content}`
- Khi tải lại app, lịch sử được khôi phục

---

## 📋 System Instruction của AI

Trợ lý AI được cấu hình với instruction:
```
Bạn là 'StreamlitBot' — một trợ lý AI thân thiện và chuyên nghiệp, 
trả lời bằng tiếng Việt. Hãy ngắn gọn, tự nhiên, và nếu không chắc 
chắn, hãy nói 'Tôi chưa rõ lắm về điều đó'.
```

Bạn có thể chỉnh sửa instruction trong file `app.py` (dòng `SYSTEM_INSTRUCTION`)







## 👨‍💻 Tác giả

Made with ❤️ bằng Streamlit + Google Gemini API

---




