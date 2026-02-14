import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from supabase import create_client, Client
from supabase import create_client, Client
import math
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_default_secret')
socketio = SocketIO(app, cors_allowed_origins="*")

# Supabase Setup
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    # MVP fallback if env not set for dev ease, though highly recommended to set .env
    print("WARNING: SUPABASE_URL or SUPABASE_KEY missing in .env")
    supabase = None
else:
    try:
        supabase: Client = create_client(url, key)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Failed to initialize Supabase client: {e}")
        supabase = None

# Initialize Admin Client (Service Role) if available - Bypasses RLS
service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase_admin = None
if url and service_role_key:
    try:
        supabase_admin = create_client(url, service_role_key)
    except Exception as e:
        print(f"Failed to initialize Admin Supabase client: {e}")

# --- LOCAL DATABASE FALLBACK SYSTEM ---
import json
LOCAL_DB_FILE = 'local_db.json'

def load_local_db():
    if os.path.exists(LOCAL_DB_FILE):
        try:
            with open(LOCAL_DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'riders': [], 'orders': []}

def save_local_db(data):
    try:
        with open(LOCAL_DB_FILE, 'w') as f:
            json.dump(data, f, indent=4, default=str)
    except Exception as e:
        print(f"Local DB Save Error: {e}")

local_db = load_local_db()

# Helper to sync/get order
def get_order_by_id(oid):
    # Try local first if recent
    for o in local_db['orders']:
        if str(o.get('id')) == str(oid): return o
    
    # Try Supabase
    if supabase_admin or supabase:
        try:
            client = supabase_admin if supabase_admin else supabase
            res = client.table('orders').select('*').eq('id', oid).execute()
            if res.data: return res.data[0]
        except:
            pass
    return None

def update_order_local(oid, updates):
    found = False
    for o in local_db['orders']:
        if str(o.get('id')) == str(oid):
            o.update(updates)
            found = True
            break
    if found: save_local_db(local_db)
    return found

def add_rider_local(rider_data):
    # Check dupes
    for r in local_db['riders']:
        if r['id'] == rider_data['id']: return
    local_db['riders'].append(rider_data)
    save_local_db(local_db)

def get_rider_local(rider_id):
    for r in local_db['riders']:
        if str(r.get('id')) == str(rider_id): return r
    return None
# ----------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        if not lat1 or not lon1 or not lat2 or not lon2: return 0.0
        R = 6371 # Radius of earth in km
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d
    except:
        return 0.0

# Helper functions to fetch data
def get_products():
    products = []
    if supabase:
        try:
            response = supabase.table('products').select("*").order('id').execute()
            products = response.data
        except Exception as e:
            print(f"Error fetching products: {e}")
    
    # Fallback if no products found or supabase not connected
    if not products:
        products = [
            # Starters
            {"id": 1, "title": "The Daily Green", "price": 15.00, "tag": "Best Seller", "type": "Starter", "description": "Spinach, Cucumber, Green Apple, Lemon, Ginger. The perfect alkalizing start."},
            {"id": 2, "title": "Morning Glow", "price": 18.00, "tag": "Vitamin C", "type": "Starter", "description": "Carrot, Orange, Turmeric, Black Pepper. Anti-inflammatory power."},
             # Signature
            {"id": 3, "title": "Beet It", "price": 20.00, "tag": "Stamina", "type": "Signature", "description": "Beetroot, Apple, Lemon. Increases blood flow and endurance."},
            {"id": 4, "title": "Charcoal Detox", "price": 22.00, "tag": "Cleanse", "type": "Signature", "description": "Activated Charcoal, Lemon, Agave, Alkaline Water. Deep system cleanse."},
            # Functional
            {"id": 5, "title": "Immunity Shot", "price": 10.00, "tag": "Booster", "type": "Functional", "description": "Concentrated Ginger, Lemon, Cayenne. 60ml shot."},
            {"id": 6, "title": "Nut Mylk", "price": 25.00, "tag": "Protein", "type": "Functional", "description": "Raw Almonds, Dates, Vanilla, Sea Salt. Creamy and satisfying."}
        ]
    return products

def get_product(prod_id):
    product = None
    if supabase:
        try:
            response = supabase.table('products').select("*").eq('id', prod_id).execute()
            if response.data: product = response.data[0]
        except Exception as e:
            print(f"Error fetching product {prod_id}: {e}")
    
    if not product:
        # Fallback search
        all_products = get_products()
        for p in all_products:
            if p.get('id') == prod_id:
                return p
    return product

def get_orders():
    # Use Admin client if available to list all orders
    client = supabase_admin if supabase_admin else supabase
    if not client: return []
    try:
        response = client.table('orders').select("*").order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return []

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.json.get('email') if request.is_json else request.form.get('username')
        password = request.json.get('password') if request.is_json else request.form.get('password')
        
        # Hardcoded Admin Check (or limit via env var)
        admin_email = os.getenv('ADMIN_EMAIL', 'seyramsparkdzakpasu100@gmail.com')
        
        if not supabase:
            error = "Database connection error. Please contact support."
        else:
            try:
                # Attempt to sign in with Supabase Auth
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                
                # Set Session Data
                session['user_id'] = user.user.id
                session['email'] = user.user.email
                
                # Admin Check Logic
                admin_emails_str = os.getenv('ADMIN_EMAILS', '')
                initial_admin = os.getenv('ADMIN_EMAIL', 'seyramsparkdzakpasu100@gmail.com')
                
                # Create set of admin emails for faster lookup
                admin_emails = {e.strip() for e in admin_emails_str.split(',') if e.strip()}
                if initial_admin:
                    admin_emails.add(initial_admin)

                # Role Determination
                if user.user.email in admin_emails:
                    session['role'] = 'admin'
                    session['admin_logged_in'] = True
                    return redirect(url_for('admin'))
                
                # Check if Rider
                is_rider = False
                try:
                    # Use Admin client to check if user is a rider (Bypasses RLS issues)
                    check_client = supabase_admin if supabase_admin else supabase
                    rider_check = check_client.table('riders').select('id').eq('id', user.user.id).execute()
                    if rider_check.data: is_rider = True
                except Exception as e:
                    print(f"Rider Check Error: {e}")
                    pass
                
                # Check Local DB for Rider if not found in Supabase
                # if not is_rider:
                #     if get_rider_local(user.user.id):
                #         is_rider = True

                if is_rider:
                    session['role'] = 'rider'
                    session['is_rider'] = True
                    return redirect(url_for('rider_dashboard'))
                else:
                    session['role'] = 'user'
                    session['is_rider'] = False
                    return redirect(url_for('user_dashboard'))
                    
            except Exception as e:
                # Handle Auth Failures
                error = 'Invalid Credentials.'
                print(f"Login Error: {e}")

    return render_template('login.html', title="Login", error=error)

@app.route('/switch_role/<role>')
def switch_role(role):
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    # Only allow switching if the user is actually a rider (has dual capability)
    # or if we implement a 'become a rider' flow later.
    # For now, we assume only riders can switch between rider/user views.
    if session.get('is_rider'):
        if role == 'user':
            session['role'] = 'user'
            return redirect(url_for('user_dashboard'))
        elif role == 'rider':
            session['role'] = 'rider'
            return redirect(url_for('rider_dashboard'))
            
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        
        if supabase:
            try:
                # Sign up with Supabase
                response = supabase.auth.sign_up({"email": email, "password": password})
                print(f"Supabase Signup Response: {response}")

                # Check if email confirmation is required or not (depends on Supabase settings)
                # If a user object is returned and no error, we can auto-login or ask to check email
                user = response.user if hasattr(response, 'user') else None
                session_data = response.session if hasattr(response, 'session') else None

                if user:
                    # Auto login? Or redirect to message?
                    # For simplicity, let's ask them to login, or auto-set session if Supabase returns session
                    if session_data:
                         session['user_id'] = user.id
                         session['email'] = user.email
                         session['role'] = 'user'
                         return redirect(url_for('user_dashboard'))
                    else:
                        error = "success: Please check your email to confirm your account." 
                else: 
                     # Fallback check if response signals success differently
                     if not error:
                         # Sometimes response structure varies
                         error = "Could not create account. Please try again."

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Signup Error: {e}")
                # Clean up error message for user
                msg = str(e)
                if "User already registered" in msg:
                    error = "Account already exists. Please log in."
                else:
                    error = f"Error: {str(e)}"
        else:
             error = "Signup disabled in dev mode without Supabase."

    return render_template('signup.html', title="Sign Up", error=error)

@app.route('/dashboard')
def user_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    # If admin, redirect to admin dashboard
    if session.get('role') == 'admin':
        return redirect(url_for('admin'))
    
    # If rider, redirect to rider dashboard
    if session.get('role') == 'rider':
        return redirect(url_for('rider_dashboard'))
    
    # Fetch User's Orders
    orders = []
    if supabase:
        try:
            # Search by email or user ID if stored in orders table
            # Assuming orders table has 'customer' (name) or 'phone'.Ideally should have 'user_id' or 'email'
            # For now, let's filter by the session email if we add that column, or just return empty
            # NOTE: You need to ensure 'email' column exists in your orders table for this to work perfectly.
            # Using 'customer' as a fallback search isn't secure but works for MVP if names match.
            # Use Admin client if available to bypass RLS issues
             client = supabase_admin if supabase_admin else supabase
             response = client.table('orders').select("*").eq('email', session.get('email')).order('created_at', desc=True).execute()
             orders = response.data
        except Exception as e:
            print(f"Error fetching user orders: {e}")
            
    return render_template('dashboard.html', title="My Dashboard", orders=orders)

@app.route('/logout')
def logout():
    session.clear() # Clear all session data (role, user_id, etc)
    if supabase:
        supabase.auth.sign_out()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/menu')
def menu():
    if session.get('role') == 'rider':
        return redirect(url_for('rider_dashboard'))
    products = get_products()
    return render_template('menu.html', title="Menu", products=products)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        # Prepare Order Data
        cart_json = request.form.get('cart_json')
        plan = request.form.get('plan_name')
        price = float(request.form.get('price', 0))
        customer = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        paystack_ref = request.form.get('paystack_reference') # New field
        
        # Location logic
        lat = request.form.get('latitude')
        lng = request.form.get('longitude')
        loc_text = request.form.get('location')
        
        location_data = {
            "address": loc_text,
            "lat": lat,
            "lng": lng
        }

        new_order = {
            'customer': customer,
            'email': email,
            'plan_name': plan, # Mapped column name
            'type': request.form.get('type', 'Subscription'),
            'status': 'Paid' if paystack_ref else 'Pending', # Update status based on payment
            'phone': phone,
            'total_price': price,
            'location': location_data,
            'cart_json': cart_json if cart_json else None,
            'payment_ref': paystack_ref # Store reference if needed (add column to DB later if desired)
        }

        if supabase:
            try:
                # Use Admin client if available to bypass RLS issues for public orders
                client = supabase_admin if supabase_admin else supabase
                data = client.table('orders').insert(new_order).execute()
                
                # Use returned data for confirmation page
                confirm_order = data.data[0] if data.data else new_order
                
                # Realtime: Notify Riders (Send the full object with ID)
                socketio.emit('new_order', confirm_order)
                # Ensure 'id' is present for UI
                if 'id' not in confirm_order: confirm_order['id'] = 'New'
            except Exception as e:
                import traceback
                print(f"Order Insert Error: {e}")
                # FALLBACK to local DB
                new_order['id'] = int(time.time()) # Mock ID
                local_db['orders'].append(new_order)
                save_local_db(local_db)
                confirm_order = new_order
                
                # Still emit socket event
                socketio.emit('new_order', new_order)
        else:
             # Dev Fallback
             new_order['id'] = int(time.time())
             local_db['orders'].append(new_order)
             save_local_db(local_db)
             confirm_order = new_order

        # Map back to template expectations if needed (e.g. 'plan' vs 'plan_name')
        confirm_order['plan'] = confirm_order.get('plan_name')
        
        # Redirect to tracking page so user has a persistent URL
        return redirect(url_for('track', order_id=confirm_order.get('id'), show_success=1))

    if session.get('role') == 'rider':
        return redirect(url_for('rider_dashboard'))
    return render_template('subscribe.html', title="Subscribe & Save", paystack_key=os.getenv('PAYSTACK_PUBLIC_KEY'))

@app.route('/checkout')
def checkout():
    if session.get('role') == 'rider':
        return redirect(url_for('rider_dashboard'))
    product_id = request.args.get('product_id')
    product = get_product(int(product_id)) if product_id else None
    return render_template('checkout.html', title="Checkout", product=product, paystack_key=os.getenv('PAYSTACK_PUBLIC_KEY'))

@app.route('/track', methods=['GET', 'POST'])
def track():
    if session.get('role') == 'rider':
        return redirect(url_for('rider_dashboard'))
    
    order = None
    order_id = request.args.get('order_id') # GET param
    
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        
    show_success = request.args.get('show_success')
        
    if order_id:
        if supabase:
            try:
                # Try to parse ID 
                oid = int(order_id)
                # Use Admin client if available to ensure we can see the order even if not logged in (Public Tracking)
                client = supabase_admin if supabase_admin else supabase
                response = client.table('orders').select("*").eq('id', oid).execute()
                if response.data:
                    order = response.data[0]
            except:
                pass
        
        # Fallback Local Check (if Supabase failed or empty)
        if not order:
             for o in local_db['orders']:
                 if str(o.get('id')) == str(order_id):
                     order = o
                     break
        
        # Map fields if order found
        if order:
            order['plan'] = order.get('plan_name')
            order['pressed'] = order.get('pressed_time', 'Pending')
            
            # Fetch Rider Info if assigned
            if order.get('rider_id'):
                try:
                    client = supabase_admin if supabase_admin else supabase
                    r_res = client.table('riders').select('name, vehicle_type, current_lat, current_lng, plate_number, vehicle_color, phone').eq('id', order['rider_id']).execute()
                    if r_res.data:
                        rider_data = r_res.data[0]
                        order['rider_name'] = rider_data['name']
                        order['rider_vehicle'] = rider_data.get('vehicle_type', 'Motorbike')
                        order['rider_plate'] = rider_data.get('plate_number', 'Not Listed')
                        order['rider_color'] = rider_data.get('vehicle_color', 'Green')
                        order['rider_phone'] = rider_data.get('phone') # Added
                        order['rider_lat'] = rider_data.get('current_lat')
                        order['rider_lng'] = rider_data.get('current_lng')
                except: pass

    return render_template('track.html', title="Track Order", order=order, show_success=show_success)

@app.route('/api/order/<order_id>/track')
def api_track_order(order_id):
    # Public API for frontend map to poll status
    order = None
    rider = None
    
    if supabase:
        try:
            client = supabase_admin if supabase_admin else supabase
            res = client.table('orders').select("*").eq('id', order_id).execute()
            if res.data: order = res.data[0]
        except: pass
        
    if order and order.get('rider_id'):
        try:
             client = supabase_admin if supabase_admin else supabase
             # In a real app, we would fetch rider's real-time coords from a 'rider_locations' table
             # Here we just fetch static rider profile
             r_res = client.table('riders').select('*').eq('id', order['rider_id']).execute()
             if r_res.data: rider = r_res.data[0]
        except: pass
        
    if not order:
        return jsonify({'error': 'Not found'}), 404
        
    return jsonify({
        'status': order.get('status'),
        'rider': {
            'name': rider.get('name') if rider else 'Assigning...',
            'lat': rider.get('lat', order.get('location', {}).get('lat')) if rider else None, # Mock: use order loc if no real rider loc
            'lng': rider.get('lng', order.get('location', {}).get('lng')) if rider else None
        } if order.get('rider_id') else None
    })

@socketio.on('join_order')
def on_join(data):
    order_id = data.get('order_id')
    if order_id:
        join_room(str(order_id))
        print(f"Client joined room: {order_id}")

@socketio.on('update_location')
def on_location_update(data):
    # Data: { rider_id, lat, lng, order_ids: [] }
    print(f"DEBUG: Received location update: {data}")
    rider_id = data.get('rider_id')
    lat = data.get('lat')
    lng = data.get('lng')
    order_ids = data.get('order_ids', [])
    
    if not rider_id or not lat or not lng:
        print("DEBUG: Missing data in location update")
        return

    # Update Rider Location in DB
    if supabase:
        try:
            client = supabase_admin if supabase_admin else supabase
            client.table('riders').update({
                'current_lat': lat, 
                'current_lng': lng
            }).eq('id', rider_id).execute()
        except Exception as e:
            print(f"Loc Update Error: {e}")
            pass
            
    # Also update local DB for fallback
    updated_local = False
    for r in local_db['riders']:
        if str(r.get('id')) == str(rider_id):
            r['current_lat'] = lat
            r['current_lng'] = lng
            updated_local = True
            break
    if updated_local: save_local_db(local_db)
    
    # Emit to all active order rooms
    for oid in order_ids:
        print(f"DEBUG: Emitting location to room {oid}")
        socketio.emit('location_update', {
            'rider_id': rider_id,
            'lat': lat,
            'lng': lng
        }, room=str(oid))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    orders = get_orders()
    products = get_products()
    
    # Calculate Stats
    total_orders = len(orders)
    total_revenue = sum(float(o.get('total_price', 0)) for o in orders)
    pending_orders = sum(1 for o in orders if o.get('status') == 'Pending')
    
    # Map fields for template display compatibility
    for o in orders:
         o['plan'] = o.get('plan_name')
         o['pressed'] = o.get('created_at', 'Pending')[:10] if o.get('created_at') else 'Pending' # Format date

    return render_template('admin.html', 
                           title="Admin Dashboard", 
                           orders=orders, 
                           products=products,
                           stats={
                               'total_orders': total_orders,
                               'revenue': total_revenue,
                               'pending': pending_orders
                           })

@app.route('/admin/order/<order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    new_status = request.form.get('status')
    if supabase:
        try:
            # Handle both int and uuid/string IDs
            try:
                oid = int(order_id)
            except:
                oid = order_id
                
            # Use Admin client if available to bypass RLS, else fallback
            client = supabase_admin if supabase_admin else supabase
            client.table('orders').update({'status': new_status}).eq('id', oid).execute()
            
            # Notify Tracker
            socketio.emit('status_update', {'status': new_status}, room=str(oid))
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error updating order {order_id}: {e}")
            return jsonify({'error': str(e)}), 500
            
    return redirect(url_for('admin'))

@app.route('/admin/product/new', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        new_product = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'tag': request.form['tag'],
            'type': request.form['type']
            # image_url, etc can be added later
        }
        
        if supabase:
            try:
                # Use Admin client if available to bypass RLS
                client = supabase_admin if supabase_admin else supabase
                client.table('products').insert(new_product).execute()
                return redirect(url_for('admin'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Insert Error: {e}")
                return "Error adding product", 500
        
        return redirect(url_for('admin'))

    # Reuse edit template but pass empty product or flag
    return render_template('edit_product.html', title="Add New Product", product=None)

@app.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        update_data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'tag': request.form['tag'],
            'type': request.form['type']
        }
        
        if supabase:
            try:
                # Use Admin client if available to bypass RLS
                client = supabase_admin if supabase_admin else supabase
                client.table('products').update(update_data).eq('id', product_id).execute()
                return redirect(url_for('admin'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Update Error: {e}")
                return "Error updating product", 500
        
        return redirect(url_for('admin'))

    product = get_product(product_id)
    if not product:
        return "Product not found", 404

    return render_template('edit_product.html', title=f"Edit {product.get('title')}", product=product)

@app.route('/admin/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    if supabase:
        try:
             # Use Admin client if available to bypass RLS
            client = supabase_admin if supabase_admin else supabase
            client.table('products').delete().eq('id', product_id).execute()
        except Exception as e:
             import traceback
             traceback.print_exc()
             print(f"Delete Error: {e}")
            
    return redirect(url_for('admin'))

# --- RIDER ROUTES ---

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    try:
        R = 6371  # Radius of earth in km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c # Distance in km
        return d
    except:
        return 9999 # Return large distance if calculation fails

@app.route('/rider/signup', methods=['GET', 'POST'])
@app.route('/rider/signup', methods=['GET', 'POST'])
def rider_signup():
    error = None
    
    # Pre-fill email if logged in
    prefill_email = session.get('email', '')
    
    if request.method == 'POST':
        # Form Data
        email = request.form.get('email', prefill_email)
        password = request.form.get('password')
        name = request.form['name']
        phone = request.form['phone']
        vehicle = request.form['vehicle']
        plate_number = request.form.get('plate_number', 'Not Provided')
        vehicle_color = request.form.get('vehicle_color', 'Green')
        
        user_obj = None
        
        # 1. User Determination Strategy
        if supabase:
            # STRATEGY A: Check if already logged in (Session Upgrade)
            if session.get('user_id'):
                print("DEBUG: Upgrading existing user session to Rider")
                # Create a simple wrapper to mimic the Auth response object
                class UserWrapper:
                     def __init__(self, uid, uemail):
                         self.id = uid
                         self.email = uemail
                user_obj = UserWrapper(session['user_id'], session.get('email', email))
            
            # STRATEGY B: Create New User (if not logged in)
            else:
                # FORCE RELOAD ADMIN CLIENT TO DEBUG/ENSURE IT EXISTS
                c_url = os.getenv("SUPABASE_URL")
                c_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
                local_admin = None
                if c_url and c_key:
                    try:
                        local_admin = create_client(c_url, c_key)
                    except Exception as e:
                        print(f"DEBUG: Local Admin Client Init Failed: {e}")

                active_admin = local_admin if local_admin else supabase_admin
                
                # Try creating user with Admin (bypasses confirmation requirements sometimes)
                if active_admin:
                    try:
                        res = active_admin.auth.admin.create_user({
                            "email": email, 
                            "password": password, 
                            "email_confirm": True
                        })
                        user_obj = res.user
                    except Exception as e:
                        print(f"DEBUG: Admin Create User Failed: {e}")
                        # Fallback to public signup
                        try:
                            res = supabase.auth.sign_up({"email": email, "password": password})
                            user_obj = res.user if hasattr(res, 'user') else (res.session.user if hasattr(res, 'session') else None)
                        except Exception as e2:
                            error = str(e2)
                else:
                    # Public signup only
                    try:
                        res = supabase.auth.sign_up({"email": email, "password": password})
                        user_obj = res.user if hasattr(res, 'user') else (res.session.user if hasattr(res, 'session') else None)
                    except Exception as e3:
                        error = str(e3)

            # 2. Insert Rider Data (If we have a user)
            if user_obj:
                # Again, use Admin client for the INSERT to bypass RLS
                c_url = os.getenv("SUPABASE_URL")
                c_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
                insert_client = None
                try: 
                    if c_url and c_key: insert_client = create_client(c_url, c_key)
                except: pass
                
                final_client = insert_client if insert_client else (supabase_admin if supabase_admin else supabase)
                
                rider_data = {
                    'id': user_obj.id,
                    'name': name,
                    'phone': phone,
                    'vehicle_type': vehicle,
                    'plate_number': plate_number, # Added field
                    'vehicle_color': vehicle_color,
                    'status': 'available'
                }
                
                print(f"DEBUG: Inserting Rider Data for {user_obj.id} using {'ADMIN' if final_client != supabase else 'PUBLIC'}")
                
                try:
                    final_client.table('riders').insert(rider_data).execute()
                    
                    # Update Session
                    session['user_id'] = user_obj.id
                    session['email'] = user_obj.email
                    session['role'] = 'rider'
                    session['is_rider'] = True
                    return redirect(url_for('rider_dashboard'))
                    
                except Exception as e:
                    print(f"Rider Insert Error: {e}")
                    msg = str(e)
                    
                    # Handle Duplicate Key (Already a rider)
                    if '23505' in msg: 
                         session['user_id'] = user_obj.id
                         session['role'] = 'rider'
                         session['is_rider'] = True
                         return redirect(url_for('rider_dashboard'))
                    
                    # Handle Foreign Key Violation (User not in public.users)
                    # This happens if the trigger to sync auth.users -> public.users is missing/failed
                    elif '23503' in msg:
                        error = "Please create a standard account and Log In first, then apply to be a rider."
                    
                    else:
                        error = f"Database Error: {msg}"

    return render_template('rider_signup.html', error=error, prefill_email=prefill_email)

@app.route('/rider/dashboard')
def rider_dashboard():
    if session.get('role') != 'rider':
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    available_orders = []
    my_orders = []
    
    # Get ignored orders from session (Decline logic)
    ignored_orders = session.get('ignored_orders', [])
    
    client = supabase_admin if supabase_admin else supabase
    if client:
        try:
            res = client.table('orders').select("*").order('created_at', desc=True).execute()
            all_orders = res.data
            
            for o in all_orders:
                # Available: No rider assigned yet
                # Check explicitly for None or empty string
                rid = o.get('rider_id')
                status = o.get('status')
                
                # Check against ignored list
                if o.get('id') in ignored_orders:
                    continue
                
                if not rid and status in ['Paid', 'Pending', 'Pending Rider']:
                    # Add location summary
                    loc = o.get('location', {})
                    o['address_short'] = loc.get('address', 'Unknown') if loc else 'Unknown'
                    available_orders.append(o)
                # My Orders: Assigned to me
                elif str(rid) == str(user_id):
                    my_orders.append(o)
                    
        except Exception as e:
             print(f"Rider Dash Supabase Error: {e}")
    
    # Merge Local Orders (Fallback)
    for o in local_db['orders']:
        rid = o.get('rider_id')
        status = o.get('status')
        if o.get('id') in ignored_orders: continue
        
        if not rid and status in ['Paid', 'Pending', 'Pending Rider']:
             loc = o.get('location', {})
             o['address_short'] = loc.get('address', 'Unknown') if loc else 'Unknown'
             # Avoid dupes
             if not any(str(x.get('id')) == str(o.get('id')) for x in available_orders):
                 available_orders.append(o)
        elif str(rid) == str(user_id):
             if not any(str(x.get('id')) == str(o.get('id')) for x in my_orders):
                my_orders.append(o)
            
    return render_template('rider_dashboard.html', available=available_orders, my_orders=my_orders)

@app.route('/api/rider/orders')
def rider_orders_api():
    if session.get('role') != 'rider': return jsonify({'error': 'Unauthorized'}), 401
    
    ignored_orders = session.get('ignored_orders', [])
    available_orders = []
    
    client = supabase_admin if supabase_admin else supabase
    if client:
        try:
            res = client.table('orders').select("*").order('created_at', desc=True).execute()
            all_orders = res.data
            
            for o in all_orders:
                rid = o.get('rider_id')
                status = o.get('status')
                
                if o.get('id') in ignored_orders: continue
                
                if not rid and status in ['Paid', 'Pending', 'Pending Rider']:
                    loc = o.get('location', {})
                    o['address_short'] = loc.get('address', 'Unknown') if loc else 'Unknown'
                    available_orders.append(o)
        except:
             pass

    # Merge Local Orders (Fallback)
    for o in local_db['orders']:
        rid = o.get('rider_id')
        status = o.get('status')
        if o.get('id') in ignored_orders: continue
        
        if not rid and status in ['Paid', 'Pending', 'Pending Rider']:
             loc = o.get('location', {})
             o['address_short'] = loc.get('address', 'Unknown') if loc else 'Unknown'
             if not any(str(x.get('id')) == str(o.get('id')) for x in available_orders):
                 available_orders.append(o)

    return jsonify(available_orders)

@app.route('/rider/order/<order_id>/decline', methods=['POST'])
def rider_decline_order(order_id):
    if session.get('role') != 'rider': return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Handle int/str ID conversion for consistency
        try: oid = int(order_id)
        except: oid = order_id
            
        print(f"Declining Order: {oid}")
        if 'ignored_orders' not in session:
            session['ignored_orders'] = []
            
        # Append without duplicating
        if oid not in session['ignored_orders']:
            session['ignored_orders'].append(oid)
            session.modified = True
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rider/order/<order_id>/accept', methods=['POST'])
def rider_accept_order(order_id):
    if session.get('role') != 'rider': return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session.get('user_id')
    client = supabase_admin if supabase_admin else supabase
    
    try:
        # Handle int/str ID
        try: oid = int(order_id)
        except: oid = order_id
        
        # Get rider details
        rider_name = 'Rider'
        rider_vehicle = 'Motorbike'
        rider_plate = 'Not Listed'
        rider_color = 'Green'
        
        rider_phone = None # Added initialization
        
        if client:
             try:
                rider_res = client.table('riders').select('name, vehicle_type, plate_number, vehicle_color, phone').eq('id', user_id).execute()
                if rider_res.data:
                    rd = rider_res.data[0]
                    rider_name = rd.get('name', 'Rider')
                    rider_vehicle = rd.get('vehicle_type', 'Motorbike')
                    rider_plate = rd.get('plate_number', 'Not Listed')
                    rider_color = rd.get('vehicle_color', 'Green')
                    rider_phone = rd.get('phone')
             except:
                 # Local Rider Check
                 r = get_rider_local(user_id)
                 if r: 
                     rider_name = r.get('name', 'Rider')
                     rider_vehicle = r.get('vehicle_type', 'Motorbike')
                     rider_plate = r.get('plate_number', 'Not Listed')
                     rider_color = r.get('vehicle_color', 'Green')
                     rider_phone = r.get('phone')

        update_payload = {
            'rider_id': user_id,
            'rider': rider_name,
            'status': 'Rider Assigned'
        }
        
        success = False
        if client:
            try:
                client.table('orders').update(update_payload).eq('id', oid).execute()
                success = True
            except: pass
            
        if not success:
            # Update Local
            update_order_local(oid, update_payload)
            success = True

        socketio.emit('order_taken', {'id': oid, 'rider_id': user_id})
        socketio.emit('status_update', {
            'status': 'Rider Assigned', 
            'rider': rider_name,
            'vehicle': rider_vehicle,
            'plate': rider_plate,
            'color': rider_color,
            'phone': rider_phone
        }, room=str(oid))
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Accept Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/rider/order/<order_id>/navigate')
def rider_navigate(order_id):
    if session.get('role') != 'rider':
        return redirect(url_for('login'))
        
    try:
        # Handle int/str ID
        try: oid = int(order_id)
        except: oid = order_id
        
        client = supabase_admin if supabase_admin else supabase
        
        # Get Order Details
        res = client.table('orders').select('*').eq('id', oid).execute()
        if not res.data:
            return "Order not found", 404
            
        order = res.data[0]
        
        # Ensure location data exists
        if not order.get('location'):
            # Fallback for dev
            order['location'] = {'lat': 5.6037, 'lng': -0.1870, 'address': 'Unknown'}
            
        return render_template('rider_navigation.html', order=order)
        
    except Exception as e:
        print(f"Nav Error: {e}")
        return redirect(url_for('rider_dashboard'))

@app.route('/rider/order/<order_id>/arrive', methods=['POST'])
def rider_arrive(order_id):
    if session.get('role') != 'rider': return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        lat = float(data.get('lat', 0))
        lng = float(data.get('lng', 0))
        # action can be 'pickup' (arrived at vendor) or 'delivery' (arrived at customer)
        # For MVP, let's assume 'delivery' arrival or toggle based on current status
        
        client = supabase_admin if supabase_admin else supabase
        try: oid = int(order_id)
        except: oid = order_id
        
        # Get Order Details
        res = client.table('orders').select('*').eq('id', oid).execute()
        if not res.data: return jsonify({'error': 'Order not found'}), 404
        order = res.data[0]
        
        current_status = order.get('status')
        
        # Logic: 
        # Rider Assigned -> Arrived at Pickup (checking vendor loc) -> Picked Up -> Arrived at Dropoff (checking customer loc) -> Delivered
        
        # Vendor Location (Fixed for MVP)
        vendor_lat = 5.6037
        vendor_lng = -0.1870
        
        # Customer Location
        loc = order.get('location', {})
        cust_lat = float(loc.get('lat', 0) or 0)
        cust_lng = float(loc.get('lng', 0) or 0)
        
        new_status = current_status
        msg = "Status Updated"
        
        dist_to_vendor = calculate_distance(lat, lng, vendor_lat, vendor_lng)
        dist_to_cust = calculate_distance(lat, lng, cust_lat, cust_lng)
        
        if current_status == 'Rider Assigned':
            # Check Vendor Proximity
            if dist_to_vendor < 0.5: # 500m
                new_status = 'Arrived at Pickup'
                msg = "You have arrived at the restaurant!"
            else:
                 return jsonify({'success': False, 'message': f"Too far from restaurant ({dist_to_vendor:.2f}km)"}), 400
                 
        elif current_status == 'Arrived at Pickup':
            # Manual action usually to switch to 'Picked Up', but let's say this button confirms pickup
            new_status = 'Picked Up' 
            msg = "Order picked up! Navigate to customer."
            
        elif current_status == 'Picked Up':
             # Check Customer Proximity
             if dist_to_cust < 0.5:
                 new_status = 'Arrived at Dropoff'
                 msg = "You have arrived at the customer!"
             else:
                  return jsonify({'success': False, 'message': f"Too far from customer ({dist_to_cust:.2f}km)"}), 400

        elif current_status == 'Arrived at Dropoff':
            new_status = 'Delivered'
            msg = "Order Delivered! Great job."
            
        # Update DB
        success = False
        if client:
            try:
                client.table('orders').update({'status': new_status}).eq('id', oid).execute()
                client.table('riders').update({'current_lat': lat, 'current_lng': lng}).eq('id', session['user_id']).execute()
                success = True
            except: pass
            
        if not success:
            update_order_local(oid, {'status': new_status})
            # Update local rider loc
            for r in local_db['riders']:
                if str(r.get('id')) == str(session['user_id']):
                    r['current_lat'] = lat
                    r['current_lng'] = lng
            save_local_db(local_db)
        
        # Notify Tracking Page
        socketio.emit('status_update', {'status': new_status}, room=str(oid))
        
        return jsonify({'success': True, 'message': msg, 'new_status': new_status})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/order/<order_id>/track')
def track_order_api(order_id):
    try:
        # Handle int/str ID
        try: oid = int(order_id)
        except: oid = order_id
        
        client = supabase_admin if supabase_admin else supabase
        
        # Get Order
        res = client.table('orders').select('*, riders(name, phone, current_lat, current_lng, vehicle_type)').eq('id', oid).execute()
        
        if not res.data: return jsonify({'error': 'Not found'}), 404
        
        order = res.data[0]
        rider = order.get('riders') # Joined data if setup, otherwise need separate query
        
        # If relation not set up or using fallback
        rid = order.get('rider_id')
        if not rider and rid:
            # Try DB
            if client:
                 try:
                    r_res = client.table('riders').select('*').eq('id', rid).execute()
                    if r_res.data: rider = r_res.data[0]
                 except: pass
            
            # Try Local
            if not rider:
                rider = get_rider_local(rid)
            
        return jsonify({
            'status': order.get('status'),
            'eta': order.get('eta', 'Calculating...'),
            'rider': {
                'name': rider.get('name') if rider else 'Assigning...',
                'vehicle_type': rider.get('vehicle_type', 'Motorbike'), # Ensure consistent key if needed, or stick to 'vehicle'
                'vehicle': rider.get('vehicle_type', 'Motorbike'),
                'plate': rider.get('plate_number', 'Not Listed'),
                'color': rider.get('vehicle_color', 'Green'),
                'lat': rider.get('current_lat'),
                'lng': rider.get('current_lng'),
                'phone': rider.get('phone')
            } if rider else None
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    socketio.run(app, debug=True, port=port)
