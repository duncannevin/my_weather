# My Weather

My Weather Application is a comprehensive weather forecasting service built using FastAPI. It is designed to provide users with detailed weather forecasts based on their queries. The application leverages the capabilities of FastAPI to manage asynchronous endpoints efficiently, ensuring that users receive fast and accurate weather information. Additionally, it includes a frontend component enabling users to visually interact with the weather data.

## Features

- Weather Forecast Retrieval: Users can obtain weather forecasts by querying the service with specific parameters such as location and date.
- Caching Mechanism: The application employs a caching layer powered by Redis to store frequently accessed data, reducing load times and enhancing performance.
- Static and HTML Serving: The application serves static files, including HTML, CSS, and JavaScript, from designated directories, providing a rich and interactive user interface.
- RESTful API Endpoints: The weather information is accessible through well-defined RESTful API endpoints, facilitating easy integration with other services and applications.

## Project Structure

- Backend (FastAPI): The core of the application is built with FastAPI, offering a robust RESTful API and handling all backend logic and data processing.
- Frontend (Static Files): The application serves static files including HTML views, which allow users to interact with the backend services through a web interface.

## Installation

Step-by-step instructions on how to install and set up the project.

```bash
# Clone the repository
git clone https://github.com/duncannevin/my_weather.git

# Navigate to the project directory
cd my_weather 

# (Optional) Create a virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Setup

### Step 1: Install dependencies
Make sure you have Python 3.9.20 installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Add environment variables
Replace example.env with .env and add the relevant values.

### Step 3: Start the application
Run the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

### Step 4: View the frontend
Open your web browser and navigate to the following URL:
http://127.0.0.1:8000/

## API Endpoints

### `GET /weather/forecast`
Retrieve the weather forecast based on query parameters.

#### Query Parameters:
- **location (str)**: The location for the forecast.
- **date (str)**: The date for the forecast.

#### Example Request:
```sh
curl -X 'GET' \
  'http://localhost:8000/weather/forecast?lat=38.58252615935333&lon=-121.53088855581495&units=imperial&cnt=10'
```

### `POST /weather`
Submit weather data for processing.

#### Request Body:
- **data (WeatherQuery)**: The weather data to be processed.

#### Example Request:
```sh
curl -X 'POST' \
  'http://localhost:8000/weather' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
      "lat": 38.58252615935333,
      "lon": -121.53088855581495,
      "units": "imperial"
  }'
```

## Contributing

Guidelines for contributing to the project.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

Information about the project’s license.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to reach out.

- **Your Name**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)