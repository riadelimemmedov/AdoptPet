import Stripe from "stripe"
import 'dotenv/config'

// ?getStripePublishableKey
const getStripePublishableKey = () => {
    // Initialize Stripe.js
    return Stripe(process.env.VITE_VUE_PUBLISHABLE_KEY)
}
getStripePublishableKey()
