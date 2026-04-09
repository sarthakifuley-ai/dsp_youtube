# 📊 YouTube Training Video Analysis

An end-to-end data analysis project focused on extracting insights from YouTube training videos. This project explores video performance, engagement patterns, and category trends using data visualization and statistical analysis.

---

## 🚀 Project Overview

This project analyzes a dataset of YouTube training videos to uncover meaningful insights such as:

- Most popular video categories  
- Relationship between views and likes  
- Channel performance metrics  
- Audience engagement patterns  

The analysis is performed using Python-based data analysis and visualization tools.

---

## 🎯 Objectives

- Identify the **most popular training video categories**
- Analyze **views vs likes correlation**
- Evaluate **channel-wise performance**
- Generate **interactive and static visualizations**
- Extract actionable insights from the dataset

---

## 📂 Dataset

The dataset contains metadata of YouTube training videos, including:

- Video Title  
- Channel Name  
- Category  
- Views  
- Likes  
- Comments  
- Upload Date  

---

## 🛠️ Tech Stack

- **Python**
- **Pandas & NumPy** → Data cleaning & analysis  
- **Matplotlib** → Static visualizations  
- **Plotly** → Interactive dashboards  

---

## 📊 Analysis Performed

### 1. 📌 Category Analysis
- Identified top-performing categories based on views
- Compared engagement across categories

### 2. ❤️ Views vs Likes Correlation
- Studied relationship between video popularity and engagement
- Used scatter plots and correlation coefficients

### 3. 📈 Channel Performance
- Compared channels based on:
  - Total views
  - Average likes
  - Upload frequency

### 4. 📉 Data Visualization
- Static plots using Matplotlib  
- Interactive charts using Plotly  
- Trend analysis through graphs  

---

## 📷 Sample Visualizations

- Bar Charts (Category Popularity)  
- Scatter Plots (Views vs Likes)  
- Line Graphs (Trends over Time)  
- Interactive Dashboards  

---

## 🔍 Key Insights

- Certain categories consistently outperform others in engagement  
- High views do not always guarantee high likes (non-linear correlation)  
- Consistency in uploads improves channel performance  
- Audience engagement varies significantly across categories  

---

## ⚠️ Limitations

- Dataset size may limit generalization  
- Correlation does not imply causation  
- External factors (algorithm, thumbnails, trends) not included  

---

## 🔮 Future Work

- Integrate YouTube API for real-time data  
- Build a recommendation system for content creators  
- Add machine learning models for prediction  
- Deploy interactive dashboard (Streamlit / Web App)

---

## 📌 How to Run

```bash
# Clone the repository
git clone https://github.com/sarthakifuley-ai/dsp_youtube.git

# Navigate to project directory
cd dsp_youtube

# Install dependencies
pip install -r requirements.txt

# Run the notebook/script
```
2. Create Virtual Environment
```bash
python -m venv venv
```
3. Activate Environment
Windows:
```bash
venv\Scripts\activate
```
Mac/Linux:
```bash
source venv/bin/activate
```
4. Install Dependencies
```
pip install -r requirements.txt
```
5. Run the Dashboard
```
python app.py
```
6. Open in Browser

Go to:
```
http://127.0.0.1:8050/
```
🧩 Alternative Run

You can also run:
```
python second.py
📁 Project Structure
dsp_youtube/
├── app.py
├── second.py
├── youtube.csv
├── requirements.txt
└── README.md
