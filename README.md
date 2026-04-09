# Gesturify

**Gesturify** is an interactive learning platform designed to bridge the gap between spoken language and **Indian Sign Language (ISL)**. By leveraging Computer Vision and Deep Learning, the app allows users to learn, practice, and test their knowledge of signs (A-Z and 1-9) in real-time using their webcam.

[![Deployment Link](https://img.shields.io/badge/Live-Demo-blue)](https://yuki-sf-gesturify.hf.space)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

* **Learn & Practice:** Browse through signs A-Z and 1-9. Use your camera to practice signs with real-time feedback.
* **Progressive Quiz System:**
    * **Beginner:** Multiple-choice questions based on sign images.
    * **Intermediate:** Identification mode—view a sign and type the answer.
    * **Advanced:** Performance mode—receive a character and perform the sign via webcam (no hints).
* **History Tracking:** Log of all previous practice sessions and quiz results.
* **Personal Statistics:** Detailed analytics showing signs practiced, accuracy per sign, and overall quiz performance.

---

## Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla).
* **Backend:** FastAPI (Python).
* **AI/ML:** MediaPipe, OpenCV, Keras (Neural Network model).
* **Environment Management:** `uv` for lightning-fast dependency resolution and `pyproject.toml`.

---

## Installation & Setup

This project uses **uv** to manage dependencies and a custom setup script to ensure compatibility across different Operating Systems.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yuki-sf/gesturify.git](https://github.com/yuki-sf/gesturify.git)
    cd gesturify
    ```

2.  **Configure Environment:**
    Run the setup script to modify `pyproject.toml` based on your OS:
    ```bash
    python setup_env.py
    ```

3.  **Sync Dependencies:**
    ```bash
    uv sync
    ```

4.  **Run the App:**
    ```bash
    uv run uvicorn main:app --reload
    ```
    Access the app at `http://127.0.0.1:8000`.

---

## Architecture

1.  **Client-Side:** JavaScript handles the camera feed and UI logic.
2.  **Server-Side:** FastAPI receives frames, processes them using **MediaPipe** for hand landmark extraction, and passes coordinates to a **Keras NN model**.
3.  **Prediction:** The model returns the predicted character/digit to the frontend in real-time.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
