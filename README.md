#finished 
Python Basics
NumPy Basics
Panda Basics
Panda Basics
Introduction of Project
Data Cleaning
Data Transmission
Sentiment Analysis NLP
Plotly - Part 1
Plotly - Part 2
Plotly - Part 3
Creating Web Dashboard
Tkinter vs HTML
<img width="1366" height="768" alt="Screenshot 2026-02-03 210251" src="https://github.com/user-attachments/assets/8fb7b148-5d2d-4461-9bad-eefbff4355d2" />
<img width="1366" height="768" alt="Screenshot 2026-02-03 210423" src="https://github.com/user-attachments/assets/575d90e9-0c89-4695-9653-757df2c575b9" />
<img width="1366" height="768" alt="Screenshot 2026-02-03 210546" src="https://github.com/user-attachments/assets/bbede2b5-cd09-4246-8734-d4ee69a2a533" />
<img width="1366" height="768" alt="Screenshot 2026-02-03 210652" src="https://github.com/user-attachments/assets/c96f1ef7-dfa8-4ab6-9703-665f359c2679" />
<img width="1366" height="768" alt="Screenshot 2026-02-03 210749" src="https://github.com/user-attachments/assets/dab71ce2-8685-47cf-aeff-855daa82a678" />
<img width="1366" height="768" alt="Screenshot 2026-02-03 210849" src="https://github.com/user-attachments/assets/fdd679c1-643a-493e-88e5-0ae5726caf49" />
Google Play Store Data Analysis

Null Class Data Analytics Internship Project

About This Project

I analyzed 10,841 Google Play Store apps using Python and built six interactive charts to dig into how apps perform, what users like, and where the market’s heading.

Projects Completed

Project 1: Top Categories - Rating vs Reviews
- Pulled out the top 10 app categories
- Compared their average ratings and total reviews
- What stood out: FAMILY apps came out on top with an average 4.4 rating and racked up 4.5 million reviews

Project 2: Free vs Paid Apps
- Compared installs and revenue across categories
- Focused on the top 3
- Main takeaway: PHOTOGRAPHY paid apps brought in the most money ($6 million)

Project 3: Category Popularity Map
- Highlighted the top 5 categories by total installs
- Biggest surprise: PRODUCTIVITY apps took the lead with 14 billion installs

Project 4: Growth Over Time
- Tracked installs month by month
- Translated categories into French, Spanish, and Japanese
- Saw a huge growth spike in August 2018

Project 5: Size vs Rating Analysis
- Used bubble size to show number of installs
- GAME category got a pop of pink for visibility
- Noticed that apps sized 10–20 MB scored the best ratings

Project 6: Install Trends Timeline
- Mapped out install trends and highlighted periods of big growth
- Red months mean growth jumped over 20%
- COMMUNICATION apps exploded in July 2018

Tools Used

- Python for coding
- Pandas for cleaning up and analyzing data
- Plotly for interactive charts

Files

nullproject/
├── data/
│   ├── googleplaystore.csv
│   └── googleplaystore_user_reviews.csv
├── visualizations/
│   ├── project1_grouped_bar_chart.py
│   ├── project2_dual_axis_chart.py
│   ├── project3_choropleth_map.py
│   ├── project4_stacked_area_chart.py
│   ├── project5_bubble_chart.py
│   └── project6_time_series_chart.py
└── screenshots/
    ├── project1_result.png
    ├── project2_result.png
    ├── project3_result.png
    ├── project4_result.png
    ├── project5_result.png
    └── project6_result.png

How to Run

Install packages:
pip install pandas plotly pytz

Run any project:
python project1_grouped_bar_chart.py
python project2_dual_axis_chart.py
python project3_choropleth_map.py
python project4_stacked_area_chart.py
python project5_bubble_chart.py
python project6_time_series_chart.py

Every script spits out an interactive HTML chart that pops up in your browser.

Key Insights

What I Learned:

1. FAMILY and GAME are the big hitters on the Play Store.
2. Free apps get downloaded more, but paid apps make more money.
3. App size matters—a sweet spot is 10–20 MB for top ratings.
4. There was a huge surge in app installs around mid-2018.
5. Communication apps went wild, picking up 826 million installs in a single month.

Business Takeaways:

- Keep your app size under 30 MB if you can.
- Target a rating above 4.0.
- Free apps need tons of users to compete.
- If you’re building a paid app, try Photography—it’s where the money is.

What Each Project Does

| Project | Chart Type | What It Shows                      |
|---------|------------|-------------------------------------|
| 1       | Grouped Bar Chart | Top 10 categories by rating and reviews |
| 2       | Dual-Axis Chart   | Free vs Paid app comparison           |
| 3       | Treemap           | Category market share by installs     |
| 4       | Stacked Area      | Cumulative growth over time          |
| 5       | Bubble Chart      | Size vs Rating relationship          |
| 6       | Time Series       | Monthly install trends               |

Project Requirements Met

- Six different visualizations
- Real data (10,841 apps)
- Multiple filters
- Time-based restrictions (IST)
- Multi-language support
- Interactive charts
- Clean, working code

About

Student: Jaya Akshaya J  
Program: Null Class Data Analytics Internship  
Date: February 2026  
GitHub: jayaakshayaj1111

Note

All projects have TESTING_MODE = True so you can run them anytime. Flip it to False when you want to use real production time windows.

Made for the Null Class Internship
