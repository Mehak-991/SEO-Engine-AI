# ✨ SEO Engine AI: From Market Trends to Published Content in 60 Seconds

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)

> **"Traditional e-commerce research takes hours. I built this to make it take seconds."**

---

## 📖 The Story Behind the Project
In the fast-paced world of e-commerce, **timing is everything**. By the time a content writer researches a trending product and writes a blog post, the trend might already be fading. 

I built **SEO Engine AI** to solve this bottleneck. It's not just a tool; it's a bridge between **Live Market Data** and **SEO-Optimized Content**. It automates the "boring" parts of research, letting users focus on what matters: growing their business.

---

## 🌟 What Makes This Special?

### 🕵️ Human-Centric Scraping
Instead of just grabbing data, the tool uses **Playwright with Stealth mode** to mimic human behavior while navigating eBay's daily deals. This ensures we always get the most accurate, real-world trending items.

### 🧠 Intent-Aware AI Analysis
Most AI tools just spam keywords. My implementation uses **Gemini 2.0 Flash** to actually *understand* the user intent:
- **Commercial Intent?** AI focuses on conversion copy.
- **Informational Intent?** AI focuses on value-driven content.
- **Detailed Reports:** Every keyword is accompanied by a strategy—because a keyword without a plan is just a word.

### 🚀 Zero-Friction Publishing
I integrated the **WordPress REST API** and **Medium API** directly. This means you can discover, analyze, write, and publish an entire article without ever leaving the dashboard. 

---

## 🛠️ My Engineering Stack

- **Frontend:** React + Framer Motion (for that butter-smooth executive feel).
- **Backend:** FastAPI (chosen for its high performance and native async support).
- **Automation:** Playwright (industry standard for robust web automation).
- **Design System:** Custom CSS Architecture (Glassmorphism design for a premium UI/UX).

---

## 💡 Engineering Challenges I Overcame
- **The "Blank Page" Problem:** Handled complex AI response parsing with robust data-validation to ensure the UI never crashes, even if the AI returns unexpected formats.
- **Async Synchronization:** Managed multiple concurrent processes (scraping + keywords + content) to ensure the UI remains responsive and fast.
- **Port Conflicts:** Implemented automated cleanup scripts to ensure the development environment remains stable.

---

## 📂 Quick Start
1. **Clone & Setup:**
   ```bash
   cd backend && pip install -r requirements.txt && playwright install
   cd ../web-app && npm install
   ```
2. **Configure:** Add your keys to the `.env` file.
3. **Launch:** Run `npm run dev` and `python main.py`.

---

## 📈 Future Roadmap
- [ ] **AI-Powered Image Synthesis**: Generate custom hero images for each blog post.
- [ ] **Multi-Store Support**: Scraping from Amazon, Etsy, and AliExpress.
- [ ] **Real-Time SEO Scoring**: Integrated content auditing before publishing.

---

