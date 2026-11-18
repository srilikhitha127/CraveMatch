🍽️ CraveMatch — AI-Powered Restaurant Recommendation System
✨ Discover delicious places. Find your perfect dining match.

CraveMatch is a restaurant discovery web application that helps users find restaurants based on their preferences. Users can choose a city, cuisine, price range, minimum rating, restaurant type, table-booking preference, and online-delivery preference. The application displays matching restaurants from the bundled dataset.

The project uses FastAPI for the backend, Uvicorn as the ASGI server, Jinja2 for dynamic HTML rendering, and an existing content-based recommendation engine built with TF-IDF and cosine similarity.

✨ Main Features
- 🏠 Responsive Homepage — Explore restaurants through a clean, mobile-friendly interface.
- 🔎 Smart Search & Filters — Find restaurants by city, cuisine, price range, minimum rating, and restaurant type.
- 🛵 Dining Preferences — Filter restaurants by table-booking and online-delivery availability.
- 🍴 Restaurant Recommendations — View restaurant name, cuisine, location, rating, price range, and match score.
- ↕️ Sort Results — Organize matching restaurants using the available sorting interaction.
- ❤️ Favourites — Mark restaurants as favourites in the frontend.
- 📊 Dataset Integration — Load restaurant records from the project's CSV dataset.
- 🩺 Health Check — Check application status and the restaurant count.
- 📚 API Documentation — Explore the available endpoints through FastAPI Swagger docs.
- 👩‍💻 Developer Credit — Footer attribution: Developed by Sri Likhitha.

🛠️ Technology Stack
Technology	Usage
Python 3.12	Application runtime (recommended)
FastAPI	Backend web framework and routes
Uvicorn	ASGI development server
Jinja2	Server-rendered HTML templates
HTML5	Page structure
CSS3	Responsive styling and layout
JavaScript	Browser interactions
Pandas	Dataset loading and data handling
Scikit-learn	TF-IDF and similarity-based recommendations
NumPy	Numerical operations


📋 Requirements
- Windows, macOS, or Linux
- Python 3.12 recommended
- pip
- Internet access for externally hosted fonts and food images
🚀 Installation & Run (Windows)
1. 📦 Extract the project ZIP file.
2. 💻 Open the extracted CraveMatch folder in Visual Studio Code.
3. 🖥️ Open Terminal → New Terminal.
4. 🧪 Create a virtual environment:
   py -3.12 -m venv venv
5. 🔓 Activate the virtual environment:
   venv\Scripts\activate
6. 📥 Upgrade pip and install dependencies:
   python -m pip install --upgrade pip
   pip install -r requirements.txt
7. ▶️ Start the application with Uvicorn:
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
8. 🌐 Open the website in your browser:
   http://127.0.0.1:8000
💡 Keep the terminal running while using the website. Press Ctrl + C in the terminal to stop the server.
⚡ Alternative Start Command
The application also includes a direct Python entry point:
python app.py

🔗 Useful URLs
URL	Purpose
http://127.0.0.1:8000/	CraveMatch homepage
http://127.0.0.1:8000/health	Application health and dataset count
http://127.0.0.1:8000/docs	Interactive FastAPI Swagger documentation
http://127.0.0.1:8000/api/cuisines	Available cities and cuisines in JSON format


📁 Project Structure
CraveMatch/
├── app.py                         # FastAPI application and routes
├── recommender.py                 # Content-based recommendation engine
├── preprocessing.py               # Dataset preprocessing utilities
├── recommendation_demo.py         # Recommendation demonstration script
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── QUICK_START.md                 # Short setup guide
├── data/
│   ├── Dataset.csv                # Source restaurant dataset
│   └── processed_restaurants.csv  # Dataset used by the application
├── templates/
│   └── index.html                 # Jinja2 homepage and results
└── static/
    ├── css/
    │   └── style.css              # Website styling
    ├── js/
    │   ├── app.js                 # Page interactions
    │   └── script.js              # Supporting frontend script
    └── images/                    # Local image assets

🧠 Recommendation Workflow
1. The FastAPI application loads data/processed_restaurants.csv when it starts.
2. The homepage displays restaurant information from the dataset.
3. The user submits preferences through the Jinja2-rendered form.
4. The /recommend route passes the selected filters to recommend_restaurants() in recommender.py.
5. The recommendation engine filters and ranks matching restaurant records using the project's content-based recommendation logic.
6. The results are rendered in the homepage template.
✅ The recommendation cards are populated from the bundled dataset and recommendation output, rather than being fixed sample records.
🔌 API Routes
Method	Route	Description
GET	/	Displays the homepage and popular restaurants
POST	/recommend	Accepts preferences and renders matching restaurants
GET	/health	Returns application status and restaurant count
GET	/api/cuisines	Returns available cuisines and cities


🧰 Troubleshooting
❌ ModuleNotFoundError
Confirm that the virtual environment is activated. The terminal prompt should begin with (venv). Then run:
pip install -r requirements.txt
⚠️ Address already in use
Another process may already be using port 8000. Stop the other server with Ctrl + C, or start this project on another port:
uvicorn app:app --reload --host 127.0.0.1 --port 8001
Then visit http://127.0.0.1:8001.
📂 Dataset File Not Found
Make sure the data folder and processed_restaurants.csv are present inside the project folder. Do not move app.py away from the project root.
🖼️ Food Images or Fonts Do Not Load
Some visual assets are hosted externally. Check your internet connection. The local application and recommendation data are served from your computer.
📬 Contact
Developed by Sri Likhitha
Email: srilikhitha127@gmail.com
❤️ © 2026 CraveMatch. Made for people who love good food.