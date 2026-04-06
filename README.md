# RiraXOne

RiraXOne is a simple flight booking web application built using Python (Flask), HTML/CSS,Javascript and Bootstrap. The app allows users to search for flights, book them, and proceed to a mock payment page. This is a demo application, with mock flight data.

Features-
* Search flights between major Indian cities (mock data).
* Select travel date, passenger count, and class.
* View flight details with airline, departure time, duration, stops, and price.
* Create a booking and view a ticket summary.
* Redirect to a mock payment page after booking.
* Responsive design with Bootstrap.
* Interactive ticket card with barcode-style booking reference.

Folder Structure-
RiraXOne/

│

├─ app.py                  # Flask backend application

├─ RiraXOne.html           # Main landing page

├─ style.css               # Global CSS

├─ env/                    # Python virtual environment

├─ static/                 # Static HTML pages

│   ├─ flight.html         # Flight search results page

│   ├─ book.html           # Booking page

│   ├─ boarding.html       # Boarding pass page (optional)

│   └─ payment.html        # Payment confirmation page

Requirements-
Python 3.8+
Flask (pip install flask)
A modern web browser (Chrome, Firefox, Edge, etc.)

Installation-
Clone this repository:
git clone https://github.com/rishikapandagre/RiraXOne.git
cd RiraXOne
(Optional) Create a virtual environment:
python -m venv env
Activate the virtual environment:
Windows (PowerShell):
.\env\Scripts\Activate.ps1
Linux/Mac
source env/bin/activate
Install Flask (if not already installed):
pip install flask
Running the App
Start the Flask server:
python app.py
Open your browser and go to:
http://127.0.0.1:5000/
This will open the main landing page (RiraXOne.html).

How to Test-
Step 1: Search Flights
On the homepage, scroll: to Book Flight section.
Enter:
Departure Airport (IATA code, e.g., DEL, BOM, BLR)
Arrival Airport (IATA code, e.g., MAA, HYD)
Date
Select number of passengers and class
Click Search Flight.
You will be redirected to the flight.html page showing available flights.
Step 2: Book a Flight
On the flight.html page, click Book Now for a flight.
You will be redirected to book.html with booking details pre-filled.
Enter lead passenger name and email, then click Proceed to Payment.
Step 3: Mock Payment
After booking, you will be redirected to payment.html.
This page will show booking confirmation with a ticket/card.
Step 4: Optional Boarding Pass
If you implement boarding.html, you can test generating a boarding pass from the booking ID.

Notes-
This is a demo app, flight and booking data are mocked.
The backend is fully in Flask, serving static pages and JSON responses for flight search and booking.
All redirects between pages are handled via query parameters (?flight_id=...&source=...&destination=...).

Screenshots-
<img width="1891" height="839" alt="Screenshot 2025-11-29 201449" src="https://github.com/user-attachments/assets/4ada7ad1-20c3-431f-9290-91ec95f6f2e4" />
<img width="1737" height="670" alt="Screenshot 2025-11-29 201535" src="https://github.com/user-attachments/assets/cc551bfb-44aa-406a-af9e-4d9aec6e4f58" />
<img width="1087" height="584" alt="Screenshot 2025-11-29 201639" src="https://github.com/user-attachments/assets/844d39c6-e991-4333-8ee3-f3f71425fe7d" />
<img width="1085" height="426" alt="Screenshot 2025-11-29 201743" src="https://github.com/user-attachments/assets/b8984747-04e2-4e82-86dd-9b20eb90b0ac" />
<img width="1545" height="830" alt="Screenshot 2025-11-29 202030" src="https://github.com/user-attachments/assets/3ed33db1-6f3e-451b-a587-6959c9405391" />
<img width="1548" height="862" alt="Screenshot 2025-11-29 202114" src="https://github.com/user-attachments/assets/b1de7db4-a678-458f-8cd0-2227f104cd56" />
<img width="1514" height="861" alt="Screenshot 2025-11-29 202202" src="https://github.com/user-attachments/assets/23f30900-7bf7-4074-9662-0c1f5fef2c53" />
<img width="1523" height="848" alt="Screenshot 2025-11-29 202300" src="https://github.com/user-attachments/assets/532d1871-ca6d-43c7-9a34-1d333d7cb632" />
<img width="1063" height="650" alt="Screenshot 2025-11-29 201803" src="https://github.com/user-attachments/assets/e89672fa-d8f5-4f2d-84e9-132a9050ed5e" />
<img width="1076" height="449" alt="Screenshot 2025-11-29 201824" src="https://github.com/user-attachments/assets/0b232e7e-806c-43bb-97e7-a1c636f8f86c" />
<img width="1228" height="656" alt="Screenshot 2025-11-29 201853" src="https://github.com/user-attachments/assets/cbd6a53d-8695-4fc1-a569-4446ccd0fb73" />
<img width="1871" height="381" alt="Screenshot 2025-11-29 204300" src="https://github.com/user-attachments/assets/60b2838e-7b78-4ade-aaf7-d75eef4a7dc7" />

