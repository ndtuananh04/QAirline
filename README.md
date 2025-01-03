# QAirline - Hệ Thống Đặt Vé Máy Bay Tốt Nhất

## Tổng Quan
QAirline là một hệ thống đặt vé máy bay toàn diện cho phép người dùng tìm kiếm, đặt và quản lý vé máy bay. Hệ thống phân chia giao diện người dùng tách biệt, có hệ thống, đảm bảo đáp ứng các nhu cầu quản trị cũng như sử dụng tốt nhất.

## Tính Năng
- **Tính Năng Người Dùng**
  - Xem thông tin chung cũng như các thông tin về đặt vé máy bay 
  - Tìm kiếm và đặt vé
  - Đặt vé
  - Kiểm tra trạng thái chuyến bay
  - Hủy vé khi còn thời hạn
  - Cập nhật tin tức

- **Tính Năng Quản Trị**
  - Đăng thông báo về hãng, chuyến bay
  - Quản lý chuyến bay, máy bay, ghế (xem, thêm, sửa, xóa)
  - Thay đổi thời gian bay nếu cần
  - Thống kê hệ thống

## Công Nghệ Sử Dụng
### Frontend
- Framwork: SvelteKit
- SCSS
- JavaScript

### Backend
- Framework: Flask
- RESTful api
- ...

### Database
- MySQL (có thể sử dụng hệ quản trị dữ liệu khác)

## Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống
- Node.js (v14 trở lên)
- Python (v3.8 trở lên)
- PostgreSQL
  
### Cài Đặt Backend
```bash
cd back-end
python -m venv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Cài Đặt Frontend
```bash
cd front-end
npm install
npm run dev
```
### Hướng Dẫn Sử Dụng
- Khởi động máy chủ backend
- Chạy ứng dụng frontend
- Truy cập ứng dụng tại http://localhost:5173
- Cổng quản trị viên tại http://localhost:5173/admin
- 
## Tác giả

| Student ID | Full Name            | GitHub Profile                           |
|:----------:|:---------------------|:-----------------------------------------|
|  22028150  | Lê Bá Hoàng          | <https://github.com/lamhoang195>         |
|  22028136  | Nguyễn Đình Tuấn Anh | <https://github.com/ndtuananh04>         |
|  22028069  | Triệu Việt Hùng      | <https://github.com/kevintrieu04>        |
