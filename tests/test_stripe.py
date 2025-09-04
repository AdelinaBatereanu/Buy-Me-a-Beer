from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, ANY
from src.app import app

client = TestClient(app)

@patch("src.payments.stripe.checkout.Session.create")
def test_create_checkout_session(mock_create):
    # Mock Stripe session
    mock_session = MagicMock()
    mock_session.id = "sess_123"
    mock_session.url = "https://stripe.com/checkout/session/123"
    mock_create.return_value = mock_session

    payload = {
        "donor_name": "Test",
        "amount": 2.5,
        "message": "Test donation"
    }
    resp = client.post("/payments/create-checkout-session/", json=payload)
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://stripe.com/checkout/session/123"
    mock_create.assert_called_once()

@patch("src.payments.stripe.Webhook.construct_event")
@patch("src.payments.complete_donation")
def test_stripe_webhook(mock_complete, mock_construct_event):
    # Mock event
    mock_event = {
        "type": "checkout.session.completed",
        "data": {"object": {"metadata": {"donation_id": "abc123"}}}
    }
    mock_construct_event.return_value = mock_event
    mock_complete.return_value = None

    resp = client.post(
        "/payments/webhook/",
        content=b"{}",
        headers={"Stripe-Signature": "test"}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"
    mock_complete.assert_called_once_with(ANY, "abc123")