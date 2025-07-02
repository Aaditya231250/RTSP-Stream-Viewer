<div align="left" style="position: relative;">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="right" width="30%" style="margin: -20px 0 0 20px;">
<h1>RTSP-STREAM-VIEWER</h1>
<p align="left">
<em><code>❯ A web-based platform for viewing real-time RTSP streams, built with Django and React.</code></em>
</p>
<p align="left">
<img src="https://img.shields.io/github/license/Aaditya231250/RTSP-Stream-Viewer?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/Aaditya231250/RTSP-Stream-Viewer?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Aaditya231250/RTSP-Stream-Viewer?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Aaditya231250/RTSP-Stream-Viewer?style=default&color=0080ff" alt="repo-language-count">
</p>
</div>
<br clear="right">

## 🔗 Table of Contents

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
  - [📂 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#-prerequisites)
  - [⚙️ Installation](#-installation)
  - [🤖 Usage](#-usage)
  - [🧪 Testing](#-testing)
- [📌 Project Roadmap](#-project-roadmap)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
- [🙌 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

<code>❯ This project is a comprehensive RTSP streaming platform that allows users to view camera feeds in real-time through a web browser. It features a Django backend that ingests RTSP streams, processes them with FFmpeg into a web-friendly HLS format, and serves them to a dynamic React frontend via WebSockets. The entire application is containerized with Docker for easy setup and deployment.</code>

---

## 👾 Features

<code>❯ ▶️ **Real-time Streaming**: Ingests any RTSP stream and displays it with low latency on the web.</code><br>
<code>❯ 🚀 **HLS Transcoding**: Uses FFmpeg to transcode RTSP streams into HTTP Live Streaming (HLS) format for broad browser compatibility.</code><br>
<code>❯ 💬 **WebSocket Communication**: Leverages Django Channels for real-time, bidirectional communication between the frontend and backend.</code><br>
<code>❯ 🖥️ **Dynamic UI**: A responsive React frontend allows users to easily start, stop, and view streams.</code><br>
<code>❯ 📦 **Containerized**: Fully containerized with Docker and Docker Compose for consistent environments and simplified deployment.</code><br>
<code>❯ ❤️ **Stream Health Monitoring**: Includes a basic health check service to monitor the status of active streams.</code><br>
<code>❯ 💾 **State Management**: Utilizes Redis for managing stream state and as a message broker for Django Channels.</code>

---

## 📁 Project Structure

```sh
└── RTSP-Stream-Viewer/
    ├── .github
    │   └── workflows
    ├── README.md
    ├── backend
    │   ├── Dockerfile
    │   ├── entrypoint.sh
    │   ├── manage.py
    │   ├── requirements.txt
    │   ├── streams
    │   └── streamviewer
    ├── docker-compose.yml
    └── frontend
        ├── .env.production
        ├── Dockerfile
        ├── frontend-entrypoint.sh
        ├── index.html
        ├── package-lock.json
        ├── package.json
        ├── postcss.config.js
        ├── src
        ├── tailwind.config.js
        ├── tsconfig.json
        ├── tsconfig.node.json
        ├── vite.config.ts
        └── yarn.lock
```



### 📂 Project Index
<details open>
<summary><b><code>RTSP-STREAM-VIEWER/</code></b></summary>
<details> 
<summary><b>__root__</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/docker-compose.yml'>docker-compose.yml</a></b></td>
<td><code>❯ Defines and orchestrates the multi-container setup (backend, frontend, redis).</code></td>
</tr>
</table>
</blockquote>
</details>
<details> 
<summary><b>.github</b></summary>
<blockquote>
<details>
<summary><b>workflows</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/.github/workflows/deploy.yml'>deploy.yml</a></b></td>
<td><code>❯ CI/CD workflow for automated deployment (placeholder).</code></td>
</tr>
</table>
</blockquote>
</details>
</blockquote>
</details>
<details> 
<summary><b>backend</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/Dockerfile'>Dockerfile</a></b></td>
<td><code>❯ Instructions to build the Django backend Docker image, including FFmpeg installation.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/entrypoint.sh'>entrypoint.sh</a></b></td>
<td><code>❯ Entrypoint script that runs Django migrations and starts the Daphne server.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/manage.py'>manage.py</a></b></td>
<td><code>❯ Django's command-line utility for administrative tasks.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/requirements.txt'>requirements.txt</a></b></td>
<td><code>❯ Lists all Python dependencies for the backend service.</code></td>
</tr>
</table>
<details>
<summary><b>streams</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/apps.py'>apps.py</a></b></td>
<td><code>❯ Configuration for the 'streams' Django app.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/consumers.py'>consumers.py</a></b></td>
<td><code>❯ Handles WebSocket connections for starting/stopping streams and sending status updates.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/ffmpeg_processor.py'>ffmpeg_processor.py</a></b></td>
<td><code>❯ Manages FFmpeg subprocesses for transcoding RTSP to HLS.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/health_service.py'>health_service.py</a></b></td>
<td><code>❯ Service to periodically check the health of active FFmpeg processes.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/models.py'>models.py</a></b></td>
<td><code>❯ Defines the data models for the application (e.g., Stream).</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/redis_service.py'>redis_service.py</a></b></td>
<td><code>❯ Provides an interface for interacting with Redis to manage stream state.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/routing.py'>routing.py</a></b></td>
<td><code>❯ Defines WebSocket URL routing for Django Channels.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/stream_manager.py'>stream_manager.py</a></b></td>
<td><code>❯ Core logic for managing the lifecycle of streams (start, stop, check status).</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/urls.py'>urls.py</a></b></td>
<td><code>❯ Defines HTTP URL patterns for the 'streams' app.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/views.py'>views.py</a></b></td>
<td><code>❯ Handles HTTP requests, including serving HLS manifest files (.m3u8).</code></td>
</tr>
</table>
<details>
<summary><b>management/commands</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streams/management/commands/test_system.py'>test_system.py</a></b></td>
<td><code>❯ A custom Django command to test system components like Redis and FFmpeg availability.</code></td>
</tr>
</table>
</blockquote>
</details>
</blockquote>
</details>
<details>
<summary><b>streamviewer</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streamviewer/asgi.py'>asgi.py</a></b></td>
<td><code>❯ ASGI entrypoint for the Django application to handle async requests (WebSockets).</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streamviewer/settings.py'>settings.py</a></b></td>
<td><code>❯ Main Django project settings, including app, database, and channels configuration.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/backend/streamviewer/urls.py'>urls.py</a></b></td>
<td><code>❯ Root URL configuration for the Django project.</code></td>
</tr>
</table>
</blockquote>
</details>
</blockquote>
</details>
<details> 
<summary><b>frontend</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/Dockerfile'>Dockerfile</a></b></td>
<td><code>❯ Instructions to build the React frontend and serve it with Nginx.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/package.json'>package.json</a></b></td>
<td><code>❯ Lists frontend dependencies and scripts.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/vite.config.ts'>vite.config.ts</a></b></td>
<td><code>❯ Configuration file for Vite, the frontend build tool.</code></td>
</tr>
</table>
<details>
<summary><b>src</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/src/App.tsx'>App.tsx</a></b></td>
<td><code>❯ The main React component that renders the application layout and stream player.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/src/main.tsx'>main.tsx</a></b></td>
<td><code>❯ The entrypoint of the React application.</code></td>
</tr>
</table>
<details>
<summary><b>components</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/src/components/StreamPlayer.tsx'>StreamPlayer.tsx</a></b></td>
<td><code>❯ React component responsible for playing the HLS stream using HLS.js.</code></td>
</tr>
</table>
</blockquote>
</details>
<details>
<summary><b>hooks</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/src/hooks/useWebSocket.ts'>useWebSocket.ts</a></b></td>
<td><code>❯ Custom React hook to abstract and manage the WebSocket connection logic.</code></td>
</tr>
</table>
</blockquote>
</details>
<details>
<summary><b>store</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/frontend/src/store/streamStore.ts'>streamStore.ts</a></b></td>
<td><code>❯ State management using Zustand to handle global stream state.</code></td>
</tr>
</table>
</blockquote>
</details>
</blockquote>
</details>
</blockquote>
</details>
</details>

---
## 🚀 Getting Started

The recommended way to get started is by using Docker, which simplifies the setup of the application and its dependencies.

### ☑️ Prerequisites

Ensure you have the following installed on your system:

- **[Docker](https://www.docker.com/get-started)**
- **[Docker Compose](https://docs.docker.com/compose/install/)** (usually included with Docker Desktop)

### ⚙️ Installation

1.  **Clone the Repository**
    Clone the `RTSP-Stream-Viewer` repository to your local machine:
    ```
    ❯ git clone https://github.com/Aaditya231250/RTSP-Stream-Viewer.git
    ```

2.  **Navigate to the Project Directory**
    ```
    ❯ cd RTSP-Stream-Viewer
    ```

3.  **Build and Run with Docker Compose**
    Use Docker Compose to build the images and start all the services (backend, frontend, Redis) in detached mode.
    ```
    ❯ docker-compose up --build -d
    ```

### 🤖 Usage

1.  **Access the Application**
    Once the containers are running, open your web browser and navigate to:
    **`http://localhost:5173`**

2.  **Start a Stream**
    -   Enter a valid RTSP stream URL into the input field.
    -   Click the "Start Stream" button.
    -   The backend will start processing the stream, and the video player will appear and begin playing the live feed.

3.  **Stop a Stream**
    -   Click the "Stop Stream" button to terminate the FFmpeg process on the backend and stop the video feed.

4.  **Check Logs**
    To view the logs for the running services, use the following command:
    ```
    ❯ docker-compose logs -f
    ```

### 🧪 Testing

This project includes a custom Django management command to verify that essential services are running and configured correctly.

1.  **Access the Backend Container**
    Open a shell inside the running `backend` container:
    ```
    ❯ docker-compose exec backend /bin/bash
    ```

2.  **Run the System Test Command**
    Inside the container's shell, execute the `test_system` command. This will check the connection to Redis and the availability of FFmpeg.
    ```
    ❯ python manage.py test_system
    ```

---
## 📌 Project Roadmap

- [X] **`Core Functionality`**: <strike>Implement RTSP to HLS transcoding and web playback.
- [X] **`Containerization`**: <strike>Set up Docker and Docker Compose for all services.
- [X] **`Multi-Stream Support`**: Enhance the UI and backend to manage multiple concurrent streams.
- [X] **`Authentication`**: Add user authentication to secure access to the streaming platform.
- [X] **`Improved Error Handling`**: Implement more robust error handling and feedback on the frontend.

---

## 🔰 Contributing

Contributions are welcome! Whether it's reporting a bug, discussing improvements, or submitting a pull request, your help is appreciated.

- **💬 [Join the Discussions](https://github.com/Aaditya231250/RTSP-Stream-Viewer/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/Aaditya231250/RTSP-Stream-Viewer/issues)**: Submit bugs found or log feature requests for the `RTSP-Stream-Viewer` project.
- **💡 [Submit Pull Requests](https://github.com/Aaditya231250/RTSP-Stream-Viewer/pulls)**: Review open PRs, and submit your own.

<details closed>
<summary>Contributing Guidelines</summary>

1.  **Fork the Repository**: Start by forking the project repository to your GitHub account.
2.  **Clone Locally**: Clone the forked repository to your local machine.
    ```
    git clone https://github.com/<YOUR-USERNAME>/RTSP-Stream-Viewer.git
    ```
3.  **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
    ```
    git checkout -b feature/my-awesome-feature
    ```
4.  **Make Your Changes**: Develop and test your changes locally.
5.  **Commit Your Changes**: Commit with a clear and concise message.
    ```
    git commit -m 'feat: Implement my awesome feature'
    ```
6.  **Push to GitHub**: Push the changes to your forked repository.
    ```
    git push origin feature/my-awesome-feature
    ```
7.  **Submit a Pull Request**: Create a PR against the `main` branch of the original project repository. Clearly describe the changes and their motivation.
8.  **Review**: Once your PR is reviewed and approved, it will be merged. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com/Aaditya231250/RTSP-Stream-Viewer/graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Aaditya231250/RTSP-Stream-Viewer">
   </a>
</p>
</details>

---

## 🎗 License

This project is licensed under the **MIT License**. For more details, refer to the [LICENSE](https://github.com/Aaditya231250/RTSP-Stream-Viewer/blob/main/LICENSE) file (if available) or see the license text at [choosealicense.com](https://choosealicense.com/licenses/mit/).

---

## 🙌 Acknowledgments

-   **[Django](https://www.djangoproject.com/)**: The web framework that powers the backend.
-   **[React](https://react.dev/)**: The JavaScript library for building the user interface.
-   **[FFmpeg](https://ffmpeg.org/)**: The ultimate multimedia framework for video and audio processing.
-   **[HLS.js](https://github.com/video-dev/hls.js/)**: A JavaScript library that implements an HTTP Live Streaming client.
-   **[Docker](https://www.docker.com/)**: For making containerization a breeze.


