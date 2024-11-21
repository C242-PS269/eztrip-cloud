<div align=center>
    <h1>EzTrip: AI Travel Companion App in Your Hand!</h1>
    <img src="https://github.com/user-attachments/assets/2f45acea-59d4-4d0c-a3c8-e73d17c3ed53"/>
</div>
<br>
<div>
    <img src="https://img.shields.io/badge/Python-3670A0?&logo=python&logoColor=ffdd54"/>
    <img src="https://img.shields.io/badge/Flask-%23000.svg?&logo=flask&logoColor=white"/>
    <img src="https://img.shields.io/badge/Docker-%230db7ed.svg?&logo=docker&logoColor=white"/>
    <img src="https://img.shields.io/badge/Google_Cloud-%234285F4.svg?&logo=google-cloud&logoColor=white"/>
    <img src="https://img.shields.io/badge/FastAPI-005571?&logo=fastapi"/>
    <img src="https://img.shields.io/badge/MySQL-4479A1.svg?&logo=mysql&logoColor=white"/>
    <h3 align=center>Back-End Servers and API Services Documentation</h3>
<div>

#### Repository Overview

<p align=justify>
This repository contains a collection of backend servers designed for various specific functions in a single ecosystem for the EzTrip application. 
Each server has a specific role and is documented separately in this repository. The purpose of this repository is to provide an organized 
structure for the development, maintenance, and documentation of all EzTrip servers.
</p>

#### Tech Stacks

- **Programming Language**: Python
- **Framework**: FastAPI or Flask for Server & API development
- **Relational Database**: MySQL

#### Project Structures

1. Prototype Server:
    - Server using FastAPI:
      ```
        .
        ├── README.md
        ├── __pycache__
        │   └── main.cpython-312.pyc
        ├── app.log
        ├── config
        │   ├── __pycache__
        │   │   ├── database.cpython-312.pyc
        │   │   ├── logging.cpython-312.pyc
        │   │   └── models.cpython-312.pyc
        │   ├── database.py
        │   ├── logging.py
        │   └── models.py
        ├── main.py
        └── requirements.txt
      ```
    - Server using Flask
      ```
        .
        ├── app
        │   ├── __init__.py
        │   ├── db.py
        │   ├── logging.py
        │   ├── models.py
        │   ├── routes.py
        │   ├── schemas.py
        │   └── services.py
        ├── requirements.txt
        └── run.py
      ```
2. Machine Learning Services
```
N/A
```
4. User Data Services
```
N/A
```
6. Gateway Services
```
N/A
```

#### Servers & API Services Documentation

<center>

|No. | Services | Description | Links |
|---|---|---|---|
| 1 | Machine Learning Model Server & API Services | This server contains APIs for using machine learning models. | [Click here!]() |
| 2 | Data Server & API Services | This server is used to manage user data and provide APIs for data-related operations. | [Click here!]() |
| 3 | Gateway Server & API Services | This server acts as the main gateway to connect and manage all APIs from other servers. | [Click here!]() |

</center>

#### Deployment

- **Environment**: [Google Cloud Platform](https://cloud.google.com)
- **Server Deployments**: Cloud Run & App Engine
- **Database Services**: Cloud SQL & Firebase(Optional)
- **Storage**: Cloud Storage

#### Contributing

<div align=center>

| Name  | Bangkit ID | Roles | University |
|---|---|---|---|
| Naufal Rahfi Anugerah | C254B4KY3294 | Project Lead, Cloud Architect & BackEnd Engineer | Universitas Mercu Buana |
| Royan Sabila Rosyad Wahyudi | C550B4NY3971 | Project Manager, DevOps Engineer & BackEnd Engineer | Universitas Islam Negeri Syarif Hidayatullah Jakarta |

</div>

#### License

<p align=justify>
There is <b>NO LICENSE</b> available yet as this project is still being used for purposes that cannot be published as open source, therefore please read the disclaimer section.
</p>

#### Disclaimer

- This project is currently part of the <a href="https://www.dicoding.com/programs/bangkit">Bangkit Academy led by Google, Tokopedia, Gojek, and Traveloka</a> program and is being developed by our team as part of the Capstone Project.
- The primary purpose of this project is to fulfill the requirements of the <b>Bangkit Academy 2024 Batch 2</b> program and to demonstrate the technical and collaborative skills we have acquired during the program.
- The project is not yet intended for open-source release or commercial use. All rights and restrictions related to the project remain under the team's discretion until further notice.

#### Author

Github Organization: [EzTrip - C242-PS269 Capstone Team](https://github.com/C242-PS269)
