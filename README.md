# Information_Retrieval - Truy Vấn Thông Tin
Xây dựng hệ thông tìm kiếm trên máy tính dựa trên tập dữ liệu mẫu Cranfield

## Bắt đầu
Python 3.7.3 hoặc bất kỳ phiên bản nào khác <br>

### Cài đặt môi trường
   1. Cài đặt Python: [Python 3.7.3] (https://www.python.org/downloads/release/python-373/) <br>
   2. Cài đặt môi trường:
      2.1. Mở ```Edit the system environment variables``` (Bấm WIN và tìm environment - Win 10)
      2.2. Chọn ``` Environment Variables...```
      2.3. Chọn Path >> Edit... >> New
      2.4. Chèn đường dẫn đến folder Python và folder Scripts trong Python
   3. Cài đặt thư viện hỗ trợ python. (Nếu dùng anaconda thì không cần cài vì đã được tích hợp sẵn)

### Sử dụng
Download chương trình về máy tính bằng GIT hoặc ZIP trong ```Clone or download```
Chạy chương trình:
   - Mở CMD (WIN + R)
   - Di chuyển đến folder chương trình: ```cd duong-dan```
   - Chạy chương trình: ```python BM25.py duong-dan-1 duong-dan-2```
      + duong-dan-1: Path folder tập tài liệu
      + duong-dan-2: Path file query
      + Chương trình sẽ tạo 1 folder mới tên là Resuals chứa các file id-query.txt ghi tài liệu trả về theo theo câu truy vấn
   - So sánh kết quả: ```python compand duong-dan-tai-lieu-tra-ve duong-dan-tai-lieu-lien-quan```
      + duong-dan-tai-lieu-tra-ve: Path tới folder Resuals vừa tạo trước. (Mỗi file chỉ có 1 số - id tài liệu)
      + duong-dan-tai-lieu-lien-quan: Path tới folder tập tài liệu liên quan giống trong tập dữ liệu Cranfield (Mỗi dòng trong file có 3 chỉ số và lấy chỉ số thứ 2 - id tài liệu)
      + Chương trình sẽ in ra CMD độ phủ và độ chính xác của tập dữ liệu trả về.
          
### Sinh viên thực hiện
  - Võ Nguyễn Hoàng Triều – 13520930
  - Bùi Quang Vũ – 13521047
  - Trần Hà Phan – 15520598
