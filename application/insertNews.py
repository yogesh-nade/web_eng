from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://yogeshnade34:IiitsuratCS51@cluster0.rfz6m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")  # Change URI if needed
db = client["myFirstDatabase"]  # Replace with your database name
news_collection = db["news"]

# Sample News Data
news_data = [
    {
        "title": "Supreme Court Upholds New Land Acquisition Act",
        "description": "The Supreme Court ruled in favor of the new land acquisition act, ensuring fair compensation for landowners.",
        "category": "Judgment",
        "link": "https://example.com/news1",
        "date_published": "2025-02-07"
    },
    {
        "title": "New Consumer Protection Rules Announced",
        "description": "The government has introduced new rules to protect consumers from fraudulent online transactions.",
        "category": "Law & Policy",
        "link": "https://example.com/news2",
        "date_published": "2025-02-06"
    },
    {
        "title": "High Court Bans Single-Use Plastics in State",
        "description": "A landmark decision by the High Court bans single-use plastics, enforcing stricter environmental laws.",
        "category": "Environment",
        "link": "https://example.com/news3",
        "date_published": "2025-02-05"
    },
    {
        "title": "Parliament Passes New Cybersecurity Law",
        "description": "The cybersecurity bill aims to strengthen data privacy and cybercrime laws across the country.",
        "category": "Technology & Law",
        "link": "https://example.com/news4",
        "date_published": "2025-02-04"
    },
    {
        "title": "Supreme Court Rules on Workplace Harassment Cases",
        "description": "New guidelines have been set for handling workplace harassment complaints in corporate sectors.",
        "category": "Employment Law",
        "link": "https://example.com/news5",
        "date_published": "2025-02-03"
    }
]

# Insert Data into MongoDB
news_collection.insert_many(news_data)

print("News data inserted successfully!")

