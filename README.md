TeenLief
========
### 가출 청소년들을 위한 믿을 수 있는 헬퍼 매칭 어플리케이션

Tech Stack
----------
* WSGI
    * Django v4.0.5 - Backend Framework
    * Django Rest Framework v3.13.1
* DATABASE
    * MySQL v8.0.29 - Oracle Cloud
* DevOps
    * Github Actions(for CI/CD)
    * Docker

## Prerequisites
* Python3(3.10 recommended)
* pip

## Installing
Create a **teenlief** directory on your local machine to store the project repositories

### Setting up the backend
1. Clone the teenlief-backend, teenlief-secrets repositories inside the **teenlief** folder
```
git clone https://github.com/GMG-group/teenlief-backend.git
git clone https://github.com/GMG-group/teenlief-secrets.git
```
2. Set up a Environment
* Create venv
```
cd teenlief-backend
python -m venv venv
```
* Activate venv
##### Windows
```
.\venv\Scripts\activate
```
##### Mac
```
source ./venv/bin/activate
```
4. Install requirements
```
pip install --upgrade pip
pip install -r requirements.txt
```
5. Get Secrets
##### Windows
```
Drag teenlief/teenlief-secrets/backend/secrets.json to teenlief/teenlief-backend
```
##### Mac
```
cp ../teenlief-secrets/backend/secrets.json .
```
6. Run server locally
```
python manage.py runserver
```