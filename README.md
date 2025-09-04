# 🍺 Buy Me a Beer

A donation platform built with FastAPI and Stripe that allows user to support the developer by buying them a beer (the beer, of course, isn't real)

## ✨ Features

- **Multiple Donation Tiers**: Pre-set amounts from €0.50 to €5.00 with themed beer graphics
- **Custom Messages**: Donors can leave personalized messages
- **Secure Payments**: Stripe integration with support for cards, PayPal, Revolut Pay, Google Pay and Apple Pay
- **Email Notifications**: Automatic email alerts to the developer about a received donation
- **Responsive Design**: Works on desktop and mobile devices
- **Admin Dashboard**: API-protected endpoint to view all donations
- **Real-time Status**: Live donation status tracking (pending/completed/canceled)

## 🚀 Quick Start

### Prerequisites

- A Stripe account
- Gmail account for email notifications (or any SMTP provider)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/adelinabatereanu/Buy-Me-a-Beer.git
   cd Buy-Me-a-Beer
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your actual values (see .env.example)
   ```

5. **Run the application**

   ```bash
   uvicorn src.app:app --reload
   ```

6. **Visit your site**

   ```
   http://localhost:8000
   ```

## 🧪 Testing Webhooks Locally

For local development, use the Stripe CLI to forward webhooks:

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login to your Stripe account
stripe login

# Forward webhooks to your local server
stripe listen --forward-to localhost:8000/payments/webhook/
```

This will give you a webhook secret starting with `whsec_` - update your `.env` file with this secret.

## 📱 Usage

### For Donors

1. Visit the page
2. Choose a donation amount
3. Fill in their name and message (both optional)
4. Complete payment through Stripe
5. Get redirected to a personalized thank you page

### For Recipients

1. Receive email notifications for new donations
2. View donation details through the admin API
3. Monitor donation statuses in real-time

### Admin API

Access donation data with your API key:

```bash
# List all donations
curl -H "X-API-Key: your_admin_api_key" http://localhost:8000/donations/

# Get specific donation
curl http://localhost:8000/donations/{donation_id}
```

## 🏗️ Architecture

```
├── src/
│   ├── app.py          # Main FastAPI application
│   ├── payments.py     # Stripe payment handling
│   ├── models.py       # SQLAlchemy database models
│   ├── schemas.py      # Pydantic data validation
│   ├── crud.py         # Database operations
│   ├── config.py       # Configuration management
│   ├── db.py           # Database connection
│   └── utils.py        # Email notifications
├── templates/         # Jinja2 HTML templates
├── static/            # CSS, JavaScript, and images
└── tests/             # Test suite
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_stripe.py
```

## 🚀 Deployment

The application is ready for deployment on vercel

### Environment Variables for Production

Make sure to set these in your production environment:

- Set `DEBUG=false`
- Use production Stripe keys (`sk_live_...` and `pk_live_...`)
- Set `BASE_URL` to your actual domain
- Use a secure `ADMIN_API_KEY`
- Configure production database URL

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Author

**Adelina Batereanu**
- GitHub: [@adelinabatereanu](https://github.com/adelinabatereanu)
- Email: adelinabatereanu@gmail.com
