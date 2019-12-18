# Logo Recognizer
Nhận dạng logo sử dụng Naive Bayes Nearest Neighbor

## Getting Started
### Prerequisites

Cài đặt các thư viện cần thiết bằng command này

Windows:
```
python -m pip install -r requirements.txt
```
Linux:
```
python3 -m pip install -r requirements.txt
```
Sau đó tải file [này](https://studenthcmupedu-my.sharepoint.com/:u:/g/personal/4301104136_student_hcmup_edu_vn/ERbPTJX8iOFGnQiag3Ew1v0BV2A3DfnskqKs4JvuqtVa0g?e=fL15ma) và giải nén vào thư mục gốc logo-recognizer.
### Run
Chạy 2 command sau để khởi động server

Windows:
```
set FLASK_APP=run.py
flask run
```
Linux:
```
export FLASK_APP=run.py
flask run
```
Sau đó truy cập vào [localhost:5000](http://localhost:5000/)
## Built With

* [Flask](https://palletsprojects.com/p/flask/) - Web framework
