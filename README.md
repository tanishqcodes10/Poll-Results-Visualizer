# 📊 Poll Results Visualizer

> A complete data analysis and visualization pipeline that transforms raw poll/survey data
> into actionable insights through professional charts and an interactive Streamlit dashboard.

---

## 🧩 Problem Statement
Organizations collect thousands of poll responses but lack a structured, visual way to analyze
them. This project bridges that gap with a reusable pipeline that ingests poll data, cleans it,
runs multi-dimensional analysis, and produces publication-quality visualizations.

---

## 💡 Solution
A Python pipeline with:
- Automated **synthetic data generation** (no enterprise access needed)
- 5-stage pipeline: Generate → Clean → Analyze → Visualize → Export
- Multiple chart types: bar, pie/donut, stacked bar, demographic heatmap, trend line
- Optional **Streamlit interactive dashboard** with region + age filters

---

## 🎯 Features
| Feature | Description |
|---|---|
| 🏭 Synthetic Generator | Realistic 500-row dataset with demographic metadata |
| 🧹 Cleaning Pipeline | Type conversion, outlier handling, missing value treatment |
| 📈 Vote Share Analysis | Per-question % breakdown with leading option detection |
| 🌍 Region-wise Charts | Stacked bar charts showing regional voting patterns |
| 👥 Demographic Heatmaps | Age-group comparison matrices |
| 📅 Monthly Trends | Line charts tracking response patterns over 12 months |
| 🎛️ Streamlit Dashboard | Interactive filters; CSV export |

---

## 🛠️ Tech Stack
`Python 3.10+` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit`

---

## ⚡ How to Run
```bash
Install dependencies
pip install -r requirements.txt

Run full pipeline (dataset + all charts)
python main.py

Launch interactive dashboard
streamlit run app_dashboard.py

---

## 📊 Sample Insights
| Question | Leading Option | Share |
|---|---|---|
| Which product do you prefer? | Product A | 40.7% |
| How satisfied are you? | Satisfied | 44.3% |
| Which feature matters most? | Price | 46.4% |
| How often do you use it? | Weekly | 38.5% |
| Would you recommend us? | Definitely Yes | 34.0% |

---

## 🔭 Future Improvements
- [ ] Live Google Form webhook integration
- [ ] Sentiment analysis on open-ended responses
- [ ] PDF report auto-generation
- [ ] Power BI `.pbix` export template

---
