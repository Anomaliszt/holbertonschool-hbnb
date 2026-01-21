# HBnB - Holberton School AirBnB Clone

![HBnB Logo](https://user-images.githubusercontent.com/70502261/151993984-204d5d84-c703-434d-a23f-8855a7c6fdb2.png)

## Project Overview

HBnB is a comprehensive web application project developed as part of the Holberton School curriculum. This project implements a simplified version of AirBnB, demonstrating full-stack development skills including backend API development, database management, and frontend implementation.

The project is structured in multiple parts, each building upon the previous implementation to create a complete, production-ready application.

## Project Structure

This repository contains multiple phases of the HBnB project development:

```
holbertonschool-hbnb/
├── part2/          # Initial implementation of business logic and API endpoints
├── part3/          # Enhanced implementation with additional features
└── part4/          # Complete implementation with frontend and backend
    ├── back_end/   # Flask-based REST API
    └── front_end/  # HTML/CSS/JavaScript web interface
```

## Parts Overview

### Part 2: Implementation of Business Logic and API Endpoints

In this phase, we implement the core functionality of the application using Python and Flask. This involves creating the presentation and business logic layers, as well as defining essential classes, methods, and API endpoints.

**Key Features:**
- RESTful API endpoints for managing resources
- Business logic layer with models (User, Place, Review, Amenity)
- Facade pattern for managing layer interactions
- In-memory repository for data persistence

[View Part 2 README](./part2/hbnb/README.md)

### Part 3: Enhanced Implementation

This part builds upon Part 2 with additional features and improvements to the application architecture.

[View Part 3 README](./part3/hbnb/README.md)

### Part 4: Full-Stack Application

The final implementation includes both a complete backend API and a frontend web interface, creating a fully functional web application.

**Components:**
- **Backend**: Flask-based REST API with comprehensive endpoints
- **Frontend**: Responsive web interface with HTML, CSS, and JavaScript
- **Features**: User authentication, place management, reviews, and amenities

[View Part 4 Backend README](./part4/hbnb/back_end/README.md)

## Technology Stack

### Backend
- **Python 3.x**: Core programming language
- **Flask**: Web framework for REST API
- **SQLAlchemy**: ORM for database management (later phases)

### Frontend
- **HTML5**: Markup structure
- **CSS3**: Styling and layout
- **JavaScript**: Client-side interactivity

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- pip (Python package installer)
- A web browser for testing the frontend

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Anomaliszt/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. Navigate to the desired part (e.g., part4 for the complete implementation):
```bash
cd part4/hbnb/back_end
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python3 run.py
```

The API server will start running (typically on `http://localhost:5000`).

### Running the Frontend

1. Navigate to the frontend directory:
```bash
cd part4/hbnb/front_end
```

2. Open `index.html` in your web browser or use a local server:
```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## Project Architecture

The HBnB project follows a layered architecture pattern:

- **Presentation Layer**: API endpoints and frontend interface
- **Business Logic Layer**: Core application logic and models
- **Persistence Layer**: Data storage and retrieval (repository pattern)

Key design patterns implemented:
- **Facade Pattern**: Simplifies interactions between layers
- **Repository Pattern**: Abstracts data access logic
- **MVC Pattern**: Separates concerns in the frontend

## API Documentation

The API provides endpoints for managing:
- **Users**: Registration, authentication, profile management
- **Places**: Listing properties, creating new places
- **Reviews**: Adding and viewing reviews for places
- **Amenities**: Managing available amenities

Refer to individual part READMEs for detailed API endpoint documentation.

## Authors

This project was developed by Holberton School students:

- **Yanis MEFTOUH** - [GitHub](https://github.com/yanis59100) - <8845@holbertonstudents.com>
- **Binbin HE** - <8755@holbertonstudents.com>
- **Xavier Sanchez** - [GitHub](https://github.com/binbinher) - <9552@holbertonstudents.com>

## License

This project is part of the Holberton School curriculum.

## Acknowledgments

- Holberton School for project guidance and requirements
- AirBnB for the inspiration behind this clone project
