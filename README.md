# 💰 Dynamic Pricing & Customer Segmentation Engine

### An End-to-End Machine Learning Pipeline for Retail Optimization
---

### 🔗 Quick Links
* **🚀 Live Demo:** [Click here to use the App](https://dynamic-pricing-optimizer.streamlit.app/)
* **✍️ Medium Article:** [My Journey Building a Production-Ready ML App](https://jacknayem.medium.com/my-journey-building-a-production-ready-machine-learning-app-with-unit-tests-c67d94ca8025?postPublishedType=initial)

---

## 📖 Project Overview
In the retail industry, "one-size-fits-all" pricing strategies waste margin and fail to prevent churn. This project is a full-stack Machine Learning solution designed to **automatically segment customers** and recommend targeted discount strategies based on purchasing behavior.

Instead of a static analysis, this project features a **live web application** that allows marketing teams to:
1.  Simulate single-user scenarios.
2.  Batch process thousands of transaction rows via Excel upload.
3.  Download actionable reports with discount recommendations.

## 🏗️ Technical Architecture
This project moves beyond simple notebooks by implementing a modular, production-oriented workflow:

1.  **ETL Pipeline:** Ingests raw Excel transaction data, cleans it, and loads it into a **SQLite** database for persistent storage.
2.  **Feature Engineering:** transform raw data into **RFM Metrics** (Recency, Frequency, Monetary).
3.  **Machine Learning:** Uses **K-Means Clustering** (Unsupervised Learning) to identify distinct customer personas.
4.  **Unit Testing:** Implements **Pytest** to ensure data cleaning logic handles edge cases (e.g., negative quantities/returns) correctly.
5.  **Deployment:** Hosted on **Streamlit Cloud** with a CI/CD pipeline via GitHub.

## 📊 Key Results: Customer Segments
The unsupervised model identified 3 distinct customer groups:

| Cluster | Profile | Behavior | Recommendation |
| :--- | :--- | :--- | :--- |
| **0** | **At-Risk** | High Recency (hasn't bought in a long time), Low Frequency. | **Targeted 15% Discount** to prevent churn. |
| **1** | **Regular** | Average spending and frequency patterns. | **Standard Marketing** engagement. |
| **2** | **VIP** | High Frequency and High Monetary spend. | **No Discount.** Upsell premium products. |

## 🛠️ Installation & Local Usage

To run this project on your local machine, follow these steps:

**1. Clone the Repository**
```bash
git clone [https://github.com/jacknayem/dynamic-pricing-optimizer.git](https://github.com/jacknayem/dynamic-pricing-optimizer.git)
cd dynamic-pricing-optimizer