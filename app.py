from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Sample user data for personalization and authentication
users = {
    'alice': {'password': 'password123', 'name': 'Alice', 'preferences': ['sports', 'technology'], 'purchases': {}, 'feedback': {}},
    'bob': {'password': 'password456', 'name': 'Bob', 'preferences': ['fashion', 'travel'], 'purchases': {}, 'feedback': {}}
}

# Simple chatbot responses with expanded knowledge and conversational improvements
chatbot_responses = {
    'hello': 'Hello! How can I assist you with our products today? Feel free to ask about skincare, purchases, or feedback.',
    'hi': 'Hi there! How can I help you today?',
    'hey': 'Hey! What can I do for you?',
    'good morning': 'Good morning! How can I assist you today?',
    'good afternoon': 'Good afternoon! How can I help you?',
    'good evening': 'Good evening! How can I assist you?',
    'thank you': 'You\'re welcome! If you have any more questions, feel free to ask.',
    'thanks': 'No problem! Happy to help.',
    'sorry': 'No worries! How can I assist you further?',
    'no problem': 'Glad to hear that! Let me know if you need anything else.',
    'yes': 'Great! How can I assist you further?',
    'no': 'Okay, let me know if you have any other questions.',
    'maybe': 'No worries, take your time. I\'m here if you need any help.',
    'okay': 'Alright! What would you like to know next?',
    'sure': 'Sure thing! How can I help?',
    'etc': 'If you have any other questions, feel free to ask!',
    'sports': 'We have great sports gear available. Would you like to see some?',
    'technology': 'Check out our latest tech gadgets!',
    'fashion': 'Our fashion collection is trending this season.',
    'travel': 'Explore our travel accessories for your next trip!',
    'skincare': 'Our skincare line includes creams, gels, moisturizers, and lotions tailored for different skin types.',
    'ingredients': 'Our products use natural ingredients like aloe vera, chamomile, and green tea extract to soothe and nourish your skin.',
    'usage': 'For best results, apply our skincare products twice daily after cleansing your face.',
    'allergy': 'If you have sensitive skin or allergies, please check the product ingredients or consult with a dermatologist before use.',
    'shipping': 'We offer free shipping on orders over $50 and provide tracking information for all shipments.',
    'return': 'You can return products within 30 days of purchase if you are not satisfied. Please see our return policy for details.',
    'discount': 'Sign up for our newsletter to receive exclusive discounts and offers on skincare products.',
    'support': 'If you need assistance, you can contact our support team via email or phone, available 9am-5pm weekdays.',
    'bye': 'Goodbye! Have a great day and take care of your skin!',
    'dry skin': 'Dry skin can benefit from our Revitalizing Skincare Cream and Hydrating Aloe Gel.',
    'oily skin': 'For oily skin, try our Mattifying Face Gel to control shine and balance moisture.',
    'combination skin': 'Our Balancing Moisturizer is perfect for combination skin, providing hydration without greasiness.',
    'sensitive skin': 'Sensitive skin is best cared for with our Soothing Aloe Lotion and Chamomile Calming Serum.',
    'anti-aging': 'Our Green Tea Antioxidant Cream helps reduce signs of aging and protects your skin.',
    'sun protection': 'We recommend using sunscreen daily along with our skincare products for optimal protection.',
    'exfoliation': 'Regular exfoliation helps remove dead skin cells. We offer gentle exfoliating products suitable for all skin types.',
    'hydration': 'Keeping your skin hydrated is key. Our Hydrating Aloe Gel provides deep moisture without clogging pores.',
    'acne': 'For acne-prone skin, our Mattifying Face Gel and Chamomile Calming Serum can help soothe and reduce breakouts.',
    'eczema': 'If you have eczema, our Soothing Aloe Lotion is formulated to calm irritation and redness.',
    'ingredients safety': 'All our products are dermatologically tested and free from harmful chemicals like parabens and sulfates.',
    'customer service': 'Our customer service team is here to help you with any questions or concerns you may have.',
    'order status': 'You can check your order status by logging into your account and visiting the orders section.',
    'payment methods': 'We accept all major credit cards, PayPal, and other secure payment options.',
    'gift cards': 'Gift cards are available for purchase and can be used on any of our products.',
    'store hours': 'Our customer support is available Monday to Friday, 9am to 5pm.',
    'newsletter': 'Subscribe to our newsletter to get the latest updates and exclusive offers.',
    'returns policy': 'Products can be returned within 30 days of purchase if unopened and in original condition.',
    'shipping options': 'We offer standard and expedited shipping options to meet your needs.',
    'privacy policy': 'Your privacy is important to us. We do not share your information with third parties.',
    'terms of service': 'Please review our terms of service on our website for detailed information.',
}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users.get(username, {})
    return render_template('index.html', user=user)

@app.route('/chatbot_page')
def chatbot_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

# Product catalog with skincare products
products = {
    'skincare001': {
        'name': 'Revitalizing Skincare Cream',
        'description': 'A cream that rejuvenates your skin and keeps it healthy.',
        'price': 29.99,
        'suitability_percentage': 85
    },
    'skincare002': {
        'name': 'Mattifying Face Gel',
        'description': 'A lightweight gel that controls oil and shine for oily skin.',
        'price': 24.99,
        'suitability_percentage': 78
    },
    'skincare003': {
        'name': 'Balancing Moisturizer',
        'description': 'A moisturizer designed for combination skin to balance hydration.',
        'price': 27.99,
        'suitability_percentage': 82
    },
    'skincare004': {
        'name': 'Soothing Aloe Lotion',
        'description': 'A gentle lotion for sensitive skin with aloe vera extract.',
        'price': 22.99,
        'suitability_percentage': 90
    },
    'skincare005': {
        'name': 'Chamomile Calming Serum',
        'description': 'A serum infused with chamomile extract to calm irritated skin.',
        'price': 34.99,
        'suitability_percentage': 88
    },
    'skincare006': {
        'name': 'Green Tea Antioxidant Cream',
        'description': 'A cream rich in green tea extract to protect skin from free radicals.',
        'price': 31.99,
        'suitability_percentage': 80
    },
    'skincare007': {
        'name': 'Hydrating Aloe Gel',
        'description': 'A refreshing gel with aloe vera for deep hydration and soothing.',
        'price': 26.99,
        'suitability_percentage': 84
    }
}

@app.route('/products')
def product_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('products.html', products=products)

@app.route('/buy/<product_id>', methods=['POST'])
def buy_product(product_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    username = session['username']
    user = users.get(username)
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    user['purchases'][product_id] = products[product_id]
    return jsonify({'message': f"Product {products[product_id]['name']} purchased successfully."})

@app.route('/feedback/<product_id>', methods=['GET', 'POST'])
def feedback(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users.get(username)
    if request.method == 'POST':
        usefulness = request.form.get('usefulness')
        user['feedback'][product_id] = usefulness
        return redirect(url_for('product_list'))
    product = products.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template('feedback.html', product=product)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message', '').lower()
    if 'chat_history' not in session:
        session['chat_history'] = []
    chat_history = session['chat_history']

    # Add user input to chat history
    chat_history.append({'role': 'user', 'content': user_input})

    # Simple rule-based context-aware chatbot logic with skin type inquiry
    response = "Sorry, I did not understand that. Can you please rephrase?"

    # Check if we are in the middle of skin type inquiry
    if 'awaiting_skin_type' in session and session['awaiting_skin_type']:
        skin_type = None
        if 'dry' in user_input:
            skin_type = 'dry'
        elif 'oily' in user_input:
            skin_type = 'oily'
        elif 'combination' in user_input:
            skin_type = 'combination'
        elif 'sensitive' in user_input:
            skin_type = 'sensitive'
        if skin_type:
            session['awaiting_skin_type'] = False
            # Recommend product based on skin type
            if skin_type == 'dry':
                response = "For dry skin, I recommend our Revitalizing Skincare Cream. You can find it on the products page."
            elif skin_type == 'oily':
                response = "For oily skin, our Mattifying Face Gel is a great choice. Check it out on the products page."
            elif skin_type == 'combination':
                response = "For combination skin, try our Balancing Moisturizer. Available on the products page."
            elif skin_type == 'sensitive':
                response = "For sensitive skin, our Soothing Aloe Lotion is perfect. See it on the products page."
        else:
            response = "Please specify if your skin type is dry, oily, combination, or sensitive."
    else:
        if any(word in user_input for word in ['recommend', 'suggest', 'product', 'best', 'good']):
            response = "Can you please tell me your skin type? (dry, oily, combination, sensitive)"
            session['awaiting_skin_type'] = True
        elif any(word in user_input for word in ['buy', 'purchase', 'order']):
            response = "You can browse our products here: /products. Would you like to see skincare products?"
        elif any(word in user_input for word in ['ingredients', 'components', 'contents']):
            response = chatbot_responses.get('ingredients')
        elif any(word in user_input for word in ['usage', 'how to use', 'application']):
            response = chatbot_responses.get('usage')
        elif any(word in user_input for word in ['allergy', 'sensitive skin', 'reaction']):
            response = chatbot_responses.get('allergy')
        elif any(word in user_input for word in ['shipping', 'delivery']):
            response = chatbot_responses.get('shipping')
        elif any(word in user_input for word in ['return', 'refund']):
            response = chatbot_responses.get('return')
        elif any(word in user_input for word in ['discount', 'offer', 'coupon']):
            response = chatbot_responses.get('discount')
        elif any(word in user_input for word in ['support', 'help', 'assist']):
            response = chatbot_responses.get('support')
        elif any(word in user_input for word in ['thank', 'thanks']):
            response = chatbot_responses.get('thank you')
        elif any(word in user_input for word in ['bye', 'goodbye', 'see you']):
            response = chatbot_responses.get('bye')
        elif any(word in user_input for word in ['hello', 'hi', 'hey']):
            response = chatbot_responses.get('hello')
        else:
            # Check for keywords in chatbot_responses
            for key in chatbot_responses:
                if key in user_input:
                    response = chatbot_responses[key]
                    break
            else:
                # Fallback response
                response = "I'm here to help! Could you please specify what you need assistance with? For example, you can ask for product recommendations or support."

    # Add bot response to chat history
    chat_history.append({'role': 'bot', 'content': response})
    session['chat_history'] = chat_history

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
