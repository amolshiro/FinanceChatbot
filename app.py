from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import openai
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

# Keywords related to finance
finance_keywords = [
    'finance', 'account', 'bank', 'money', 'banking', 'investment', 'savings', 'loan', 'credit',
    'budget', 'mortgage', 'tax', 'stock', 'shares', 'market', 'trading',
    'insurance', 'retirement', '401k', 'ira', 'economy', 'capital', 'interest',
    'rate', 'fund', 'security', 'bond', 'equity', 'income', 'expense', 'debit',
    'credit score', 'portfolio', 'dividend', 'yield', 'bankrupt', 'forex',
    'fiscal', 'monetary', 'wealth', 'asset', 'liability', 'debt', 'audit',
    'ledger', 'accounting', 'inflation', 'deflation', 'stagnation', 'recession',
    'growth', 'financial crisis', 'dow jones', 'nasdaq', 's&p 500', 'bear market',
    'bull market', 'trader', 'broker', 'analyst', 'advisor', 'consultant',
    'hedge', 'arbitrage', 'leverage', 'liquid', 'liquidity', 'option', 'pension',
    'annuity', 'capital gain', 'interest rate', 'credit report', 'bank statement',
    'wealth management', 'risk management', 'estate', 'trust fund', 'commodities',
    'gold', 'silver', 'oil', 'gas', 'energy', 'real estate', 'property', 'rental',
    'lease', 'valuation', 'trade', 'exchange', 'currency', 'cryptocurrency',
    'bitcoin', 'ethereum', 'blockchain', 'fintech', 'financial technology',
    'payment', 'transaction', 'wire transfer', 'mobile banking', 'online banking',
    'financial planning', 'tax planning', 'estate planning', 'credit card',
    'debit card', 'balance', 'financial statement', 'profit', 'loss', 'revenue',
    'diversification', 'portfolio diversification', 'financial market',
    'capital market', 'derivative', 'futures', 'financial regulation',
    'compliance', 'sarbanes-oxley', 'dodd-frank', 'sec', 'securities exchange',
    'ipo', 'initial public offering', 'merger', 'acquisition', 'equity financing',
    'debt financing', 'public sector financing', 'private sector financing',
    'non-profit financing', 'microfinance', 'startup financing', 'venture capital',
    'private equity', 'credit union', 'savings account', 'checking account',
    'remittance', 'payment gateway', 'payment processing', 'financial counseling',
    'bankruptcy', 'foreclosure', 'loan refinancing', 'loan consolidation',
    'financial aid', 'scholarship', 'grant', 'student loan', 'auto loan',
    'payday loan', 'business loan', 'personal loan', 'home equity loan',
    'financial fraud', 'scam', 'phishing', 'money laundering', 'financial crime',
    'insurance claim', 'insurance policy', 'insurance premium', 'insurance broker',
    'underwriting', 'actuarial science', 'financial modeling', 'economic model',
    'economic development', 'economic indicator', 'financial indicator', 'market indicator',
    'credit risk', 'market risk', 'operational risk', 'systematic risk'
]

def is_finance_related(text):
    """Check if the text is related to finance based on predefined keywords."""
    return any(keyword in text.lower() for keyword in finance_keywords)

def get_context_by_age(age):
    """Return a contextual message based on the user's age."""
    if age <= 8:
        return "You are a friendly Bank of America personal finance assistant, and you use simple vocabulary and analogies to help teach finance concepts to children."
    elif age <= 12:
        return "You are a funny and engaging personal finance assistant for kids."
    elif age <= 18:
        return "You are a humorous and informative personal finance assistant for teenagers."
    else:
        return "You are a knowledgeable personal finance assistant for young adults."

@app.route('/')
def home():
    session.clear()  # Start a new conversation session
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    if not is_finance_related(user_input):
        return jsonify("I am only able to answer questions related to finance. Please ask a finance-related question.")

    if 'age' not in session:
        session['age'] = int(data.get('age'))

    if 'conversation' not in session:
        session['conversation'] = []
        context = get_context_by_age(session['age'])
        session['conversation'].append({"role": "system", "content": context})

    session['conversation'].append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=session['conversation']
    )

    chat_response = response.choices[0].message['content']
    session['conversation'].append({"role": "assistant", "content": chat_response})

    return jsonify(chat_response)

if __name__ == '__main__':
    app.run(debug=True)
