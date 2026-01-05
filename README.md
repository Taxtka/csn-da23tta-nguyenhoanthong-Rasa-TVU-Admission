# csn-da23tta-nguyenhoanthong-Rasa-TVU-Admission
# Đồ án Cơ sở ngành: Chatbot Tư vấn Tuyển sinh Trường Đại học Trà Vinh (TVU)
![Rasa](https://img.shields.io/badge/rasa-3.x-purple)
![Python](https://img.shields.io/badge/python-3.10.11-blue)
![Status](https://img.shields.io/badge/status-final-green)
> **Mô tả:** Hệ thống Chatbot AI hỗ trợ tư vấn tuyển sinh tự động 24/7, được xây dựng trên nền tảng Rasa Framework, tích hợp xử lý ngôn ngữ tự nhiên (NLP) tiếng Việt và triển khai trên giao diện Web thông qua Socket.IO.
---
## 🚀 Giới thiệu
Dự án được thực hiện nhằm giải quyết bài toán quá tải trong công tác tư vấn tuyển sinh tại Trường Đại học Trà Vinh. Chatbot có khả năng trả lời các câu hỏi thường gặp của thí sinh về ngành học, học phí, thời gian đào tạo và phương thức xét tuyển với tốc độ phản hồi tức thì.
### ✨ Tính năng nổi bật
* **Hiểu ngôn ngữ tự nhiên (NLU):** Phân loại chính xác ý định (Intent) và trích xuất thực thể (Entity) tiếng Việt.
* **Quản lý hội thoại theo ngữ cảnh (Contextual Memory):** Ghi nhớ thông tin ngành học đang thảo luận để trả lời các câu hỏi nối tiếp (VD: Hỏi "Học phí bao nhiêu?" mà không cần nhắc lại tên ngành).
* **Xử lý lỗi chính tả (Fuzzy Matching):** Tự động nhận diện đúng tên ngành ngay cả khi người dùng viết tắt hoặc sai chính tả (VD: "CNTT", "Thú i").
* **Tốc độ cao:** Sử dụng cấu trúc dữ liệu Dictionary (Hash Map) để truy xuất thông tin O(1), không phụ thuộc vào Database cồng kềnh.
* **Giao diện hiện đại:** Webchat tích hợp hiệu ứng Glassmorphism và kết nối Real-time.
---
## 🛠 Công nghệ sử dụng
* **Core AI:** Rasa Open Source (v3.x).
* **Ngôn ngữ lập trình:** Python 3.10.11.
* **IDE:** Visual Studio Code.
* **Giao diện (Frontend):** HTML5, CSS3, JavaScript (rasa-webchat).
* **Giao thức kết nối:** Socket.IO.
* **Xử lý dữ liệu:** Python Dictionary & Algorithms.
---
## Cấu trúc thư mục
```text
TVU-Admissions-Chatbot/
├── actions/                 # Chứa logic xử lý nghiệp vụ (Custom Actions)
│   ├── __init__.py
│   └── actions.py           # Code Python xử lý tra cứu ngành, Fuzzy Matching
├── data/                    # Dữ liệu huấn luyện
│   ├── nlu.yml              # Dữ liệu mẫu câu huấn luyện NLU
│   ├── stories.yml          # Các kịch bản hội thoại mẫu
│   └── rules.yml            # Các luật hội thoại cố định
├── models/                  # Chứa các file mô hình đã huấn luyện
├── tests/                   # Các kịch bản kiểm thử
├── progress-report/         # Chứa báo cáo đồ án (Word/PDF)
├── config.yml               # Cấu hình Pipeline NLU và Policies
├── domain.yml               # Định nghĩa Intent, Entity, Slot, Response
├── endpoints.yml            # Cấu hình kết nối Action Server
├── credentials.yml          # Cấu hình kết nối Socket.IO
├── index.html               # File chạy giao diện Web Chatbot
└── README.md                # Tài liệu hướng dẫn này
```
---
## Hướng dẫn cài đặt & Chạy dự án
Do giới hạn về dung lượng, repository này không bao gồm thư viện (folder venv). Vui lòng thực hiện các bước sau để chạy chương trình:
1. Yêu cầu hệ thống
Python 3.10 (Khuyến nghị bản 3.10.11).
Visual Studio Code.
2. Cài đặt môi trường
Mở Terminal tại thư mục gốc của dự án và chạy các lệnh sau:
``` text
# Tạo môi trường ảo
python -m venv venv
# Kích hoạt môi trường ảo (Windows)
.\venv\Scripts\activate
# Cài đặt Rasa và các thư viện phụ thuộc
pip install rasa
```
3. Huấn luyện mô hình (Training)
Nếu bạn thay đổi dữ liệu trong folder data/, hãy chạy lệnh sau để huấn luyện lại:
``` rasa train ```
4. Khởi chạy hệ thống
Bạn cần mở 2 cửa sổ Terminal riêng biệt:
Terminal 1: Chạy Action Server (Xử lý logic)
``` rasa run actions ```
Terminal 2: Chạy Rasa Core (API & Socket)
``` rasa run --enable-api --cors "*" ```
5. Sử dụng
Mở file index.html bằng trình duyệt web (Chrome/Edge).
Nhấn vào biểu tượng chat ở góc dưới màn hình để bắt đầu trò chuyện.
Tác giả
Sinh viên: Nguyễn Hoàn Thông
MSSV: 110123050
Lớp: DA23TTA
GVHD: ThS. Phạm Thị Trúc Mai
