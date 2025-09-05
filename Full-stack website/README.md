# 🌐 Full-Stack Web Control Interfaces

This directory contains projects focused on real-time device control via full-stack web technologies — combining frontend UI design with backend device logic for embedded or simulated hardware.

## 📁 Projects

### 🚀 [IoT Web Controller on Raspberry Pi 4B](./iot_nuc140_web_control/)

- Built a responsive HTML/CSS/JS frontend
- Backend: Python FastAPI with WebSocket real-time control
- Exposed via Cloudflare Tunnel for public access

### 💻 [SCADA System with Siemens Ecosystem](./scada_siemens_project/)

- HMI design in WinCC + Ladder Logic in TIA Portal (IEC 61131-3)
- Real-time monitoring of conveyor belt operations and sensors
- Ethernet-based Profinet communication with fault tolerance

## 🛠 Technologies Used

- HTML, CSS, JavaScript, WebSockets
- Python (FastAPI, Uvicorn)
- Siemens TIA Portal, S7-1200 PLC, WinCC HMI
- Cloudflared tunneling for public access

## 🔍 Key Concepts

- Bi-directional communication between browser and hardware
- Real-time HMI feedback and error handling
- Industrial protocols and embedded interface logic

## 🧠 Outcomes

- Developed understanding of both **industrial SCADA** systems and **modern web-based controls**
- Integrated embedded C/C++ logic with cloud-based frontend
