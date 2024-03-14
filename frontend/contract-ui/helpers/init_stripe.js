// ?getStripePublishableKey
const getStripePublishableKey = () => {
    // Initialize Stripe.js
    return Stripe(import.meta.env.VITE_VUE_PUBLISHABLE_KEY)
}
export default getStripePublishableKey
