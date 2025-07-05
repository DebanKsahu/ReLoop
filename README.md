# ReLoop

## Problem Statement

The global proliferation of single-use plastic bags continues to be a major environmental concern, contributing to landfill overflow, marine pollution, and greenhouse gas emissions. Despite various recycling initiatives, most systems lack transparency, traceability, and meaningful incentives for both consumers and stakeholders. As highlighted by Walmart Canada's 2024 sustainability challenge, there is a critical need for an innovative, tech-driven solution that not only eliminates single-use plastics but also actively engages users and partners in a circular economy.

ReLoop addresses this challenge by providing a robust backend system for a reusable bag return ecosystem. The platform leverages unique QR-coded bags, digital transaction tracking, and an incentive-based model to encourage sustainable behavior. By enabling real-time lifecycle monitoring, role-based access for users and workers, and seamless partner/vendor integration, ReLoop ensures that every bag's journey—from issuance to reuse or recycling—is transparent, auditable, and rewarding. This approach empowers retailers, staff, and customers to collaboratively reduce plastic waste and build a more sustainable future.

## About the Project

ReLoop is a backend system designed to power a reusable bag return ecosystem, inspired by Walmart Canada’s 2024 initiative and enhanced with modern technology and incentives. The system eliminates single-use plastic bags by providing customers with uniquely identifiable, QR-coded reusable bags at checkout. Each bag’s journey—from issuance to return or recycling—is tracked in detail.

**How It Works:**
- **Receive Bag:** Customers receive a reusable bag with a unique QR code at the point of sale.
- **Return Bag:** Bags can be returned during the next visit or at any partner/vendor location.
- **Earn Incentives:** Users earn credits based on the bag’s condition and whether it is reused or recycled. Reuse yields higher rewards; recycling still provides value.
- **Lifecycle Tracking:** Every bag’s usage count, transaction history, and approval logs (including which worker processed the bag) are recorded.
- **Worker & Partner Integration:** Store staff and partner vendors can scan, approve, and process bags, with all actions logged for transparency.

**Key Features:**
- **Smart Bag Tracker:** Monitors each bag’s lifecycle, ownership, and usage.
- **Credit Engine:** Dynamically calculates rewards based on action and bag condition.
- **Role-Based Access:** Separate dashboards and permissions for users and workers.
- **Admin & Vendor Tools:** Enables third-party participation and digital approval/rejection of bag status.
- **Secure & Scalable:** Built with FastAPI, JWT authentication, and PostgreSQL for robust, secure operations.

By combining sustainability, technology, and incentives, ReLoop aims to drive real behavior change and make circular economy models practical for retailers and customers alike.

## Demo Video

Watch a quick demo of ReLoop in action:  
[![ReLoop Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

## API Endpoints

### Authentication

- `POST /auth/user/signup` - User registration
- `POST /auth/user/login` - User login
- `POST /auth/worker/signup` - Worker registration
- `POST /auth/worker/login` - Worker login

### User Dashboard

- `GET /dashboard/user/purchase_transactions`
- `GET /dashboard/user/coin_transactions`
- `GET /dashboard/user/total_coin`
- `GET /dashboard/user/profile`
- `POST /dashboard/user/redeem/{coin_amount}`

### Worker Dashboard

- `GET /dashboard/worker/scan_transactions`
- `GET /dashboard/worker/profile`
- `POST /dashboard/worker/scan_qr`
- `POST /dashboard/worker/about_bag`

## Project Structure

```
ReLoop/
│
├── Auth/
│   └── auth.py
├── Dashboard/
│   ├── dashboard.py
│   ├── user_dashboard.py
│   └── worker_dashboard.py
├── Database/
│   ├── Engine/
│   │   └── __init__.py
│   └── ORM_Models/
│       ├── auth_models.py
│       ├── bag_models.py
│       ├── info_models.py
│       ├── response_models.py
│       ├── token_models.py
│       └── transaction_models.py
├── Utils/
│   ├── dependency.py
│   ├── enums.py
│   ├── exceptions.py
│   ├── router_classes.py
│   └── utility_functions.py
├── config.py
├── main.py
├── pyproject.toml
└── README.md
```

## Setup

1. **Clone the repository**  
   ```sh
   git clone <your-repo-url>
   cd ReLoop
   ```

2. **Create and activate a virtual environment**  
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies with uv**  
   ```sh
   uv sync
   ```

4. **Set up environment variables**  
   Create a `.env` file in the root directory with:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ```

5. **Run the application**  
   ```sh
   uvicorn main:app --reload
   ```

## Dependencies

See [`pyproject.toml`](pyproject.toml) for the full list, including:
- FastAPI
- SQLModel
- PostgreSQL (via psycopg2)
- bcrypt, passlib
- pyjwt
- python-dotenv
- opencv-python, pyzbar
- numpy

