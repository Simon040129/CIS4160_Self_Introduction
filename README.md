# CIS4160_Self_Introduction

This is a simple self-introduction web application built with **Python** and **Streamlit**.  
It is designed as part of a Web Engineering course project, and demonstrates how to combine personal information with interactive data visualization.

---

## ✨ Features

- **Profile Section**
  - Displays a personal photo (auto-orient based on EXIF).
  - Includes name, academic background, and a short introduction.
  - Supports uploading a photo if the default one (`my_photo.jpg`) is not found.

- **Interactive Random Walk Simulation**
  - Simulates a 1D random walk with adjustable step count.
  - Options:
    - Fix random seed (reproducibility).
    - Regenerate random walk at the same number of steps.
  - Provides basic statistics:
    - **Endpoint**: final value of the random walk.
    - **Max Drawdown**: maximum decline from peak.
    - **Step Volatility**: standard deviation of increments.
  - Includes a dynamic chart rendered with Matplotlib.

---

## 📦 Requirements

Make sure you have Python 3.9+ installed.  
Install the required packages using:

```bash
pip install streamlit numpy matplotlib pillow
```

## 🚀 Usage

1. Place a photo named `my_photo.jpg` in the same folder as `homepage.py`.
(Alternatively, you can upload a photo via the UI.)

2. Run the app with Streamlit:

```bash
streamlit run homepage.py
```

3. Open the link shown in the terminal (usually http://localhost:8501).
