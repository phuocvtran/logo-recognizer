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
Sau đó truy cập vào [http://localhost:5000/](http://localhost:5000/) để sử dụng model NBNN nhận dạng.
Hoặc [http://localhost:5000/detect](http://localhost:5000/detect) để detect sau đó nhận dạng. (Chưa hoàn thiện)
## Built With

* [Flask](https://palletsprojects.com/p/flask/) - Web framework
