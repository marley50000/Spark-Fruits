# How to Verify the Rider System

The Rider System has been fully implemented with a robust local fallback mechanism, allowing you to test all features immediately without configuring the external database.

## 1. Create a Rider Account
1. Navigate to `/rider/signup`.
2. Enter your details (Name, Email, Password, Phone, Vehicle).
3. Click **Register**.
4. You will be redirected to the **Rider Dashboard**.

## 2. Place an Order (as Customer)
1. Open a new incognito window or browser session.
2. Go to `/subscribe` or `/checkout?product_id=1`.
3. Complete the form. Make sure to allow location access if prompted, or enter a manual location.
4. Click **Subscribe** or **Place Order**.
5. You will see the **Order Tracking Page**.

## 3. Accept Order (as Rider)
1. Go back to your Rider Dashboard.
2. You should see the new order under "Available Orders".
3. Click **Accept Order**.
4. The order will move to "My Active Orders".

## 4. Track Live Updates
1. On the Customer's Tracking Page, the status will update to **Rider Assigned**.
2. The map will show the rider's location (simulated).

## 5. Verify Arrival (Geolocation)
1. On the Rider Dashboard, click **Arrived at Pickup**.
   - **Note:** The system checks if you are within 500m of the pickup location (Default Vendor: 5.6037, -0.1870).
   - If testing locally, you may need to use browser developer tools to mock your location or be physically close.
2. Proceed through **Picked Up** -> **Arrived at Dropoff** -> **Delivered**.

## Database Setup (Production)
For production deployment, run the valid SQL commands from `master_db_setup.sql` in your Supabase SQL Editor to create the necessary tables.
