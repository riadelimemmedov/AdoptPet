import httpx

from abstract.constants import stripe


# ? save_transaction
def save_transaction(
    session_id: str, pet_data: list, from_user: str, payment_options: str
):
    url = "http://127.0.0.1:8000/transactions/"
    try:
        for pet_data in pet_data:
            response = httpx.post(
                url,
                json={
                    "from_user": from_user,
                    "confirmations": 1 if session_id is not None else 0,
                    "value": str(pet_data["value"] / 100),
                    "adopted_pet_slug": pet_data["adopted_pet_slug"],
                    "payment_options": payment_options,
                    "session_id": session_id,
                },
            )
            response.raise_for_status()
            if response.status_code == 201:
                print("Request successful!")
                print("Response:", response.json())
            else:
                print("Request failed with status code:", response.status_code)
    except httpx.HTTPError as e:
        print("HTTPError occurred:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))


# ? get_transaction_detail
def get_transaction_detail(session_id: str):
    session = stripe.checkout.Session.retrieve(session_id)
    payment_intent = stripe.PaymentIntent.retrieve(session["payment_intent"])
    return payment_intent["amount"] / 100
