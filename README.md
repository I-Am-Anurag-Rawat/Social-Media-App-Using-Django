# 🌐 SocialBuzz  

A modern, responsive social media web application built with **Django** and **Tailwind CSS**, inspired by platforms like **Twitter** and **Instagram**.  
With SocialBuzz, users can connect, share, and engage through posts, likes, comments, and profiles — all in a sleek, mobile-first UI.  

---

## 🚀 Features  

- 🔐 **User Authentication**  
  Register (with OTP verification), login, logout, and manage profile details.  

- 📝 **Post Creation**  
  Share thoughts, images, and videos in your feed.  

- ❤️ **Engagement Tools**  
  - Like/Unlike posts in real-time  
  - Comment on posts with instant updates  

- 👥 **Social Graph**  
  - Follow/Unfollow other users  
  - View follower & following counts  

- 🔎 **Search**  
  Find users easily and explore their profiles.  

- 🗑️ **Manage Content**  
  Delete your own posts anytime.  

- 📱 **Responsive Design**  
  Beautifully optimized for desktop, tablet, and mobile.  
  Bottom navigation on mobile for a native-app feel.  

---

## 📸 Screenshots  

### Desktop View  
![Desktop Screenshot]("C:\Users\Anurag Rawat\Pictures\Screenshots\Screenshot 2025-08-17 235058.png")  

### Mobile View  
![Mobile Screenshot]("C:\Users\Anurag Rawat\Pictures\Screenshots\Screenshot 2025-08-17 235230.png")  

---

## 🛠️ Tech Stack  

- **Backend:** Django
- **Frontend:** HTML, CSS (Media Query for responsiveness), Tailwind CSS, JavaScript (AJAX for interactivity)  
- **Database:** SQLite (dev), PostgreSQL (ready for production)  
- **Deployment Ready:** Render / Any cloud platform  

---

## ⚡ Project Highlights  

- OTP-based registration system for secure signups  
- Single-page-like interactions with AJAX for delete/like/comment  
- Instagram/Twitter-style responsive layout  
- Built fully **without external UI templates** — handcrafted using CSS and Tailwind CSS  

---

## 🏗️ Installation  

Clone the repository:  

```bash
git clone https://github.com/I-Am-Anurag-Rawat/Social-Media-App-Using-Django.git
cd Social-Media-App-Using-Django
python -m venv .venv
venv\Scripts\activate # or source venv/bin/activate on mac
pip install -r requirements.txt
python manage.py runserver

--> Very important Note : Go to .myenv file and rename it into .env and follow the instructions given there. <--
