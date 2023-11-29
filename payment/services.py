import stripe
from config.settings import STRIPE_API_KEY, DOMAIN_NAME


def get_stripe_session(course, user, amount):
    stripe.api_key = STRIPE_API_KEY

    product_for_stripe = stripe.Product.create(name=course.title)
    price_for_stripe = stripe.Price.create(
        unit_amount=int(amount*100),  # todo - change model for price
        currency="usd",
        product=f"{product_for_stripe.id}",
    )
    session_for_stripe = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': f'{price_for_stripe.id}',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=f'{DOMAIN_NAME}',
        cancel_url=f'{DOMAIN_NAME}',
        customer_email=f'{user.email}'
    )
    return session_for_stripe


def get_session_by_stripe_id(stripe_id) -> dict:
    """ return session from stripe API"""
    stripe.api_key = STRIPE_API_KEY
    return stripe.checkout.Session.retrieve(stripe_id)