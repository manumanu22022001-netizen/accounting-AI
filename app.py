import streamlit as st
import time
import random

# Set up the page
st.title("Welcome Kudo's")
st.write("Ask me questions about accounting, bookkeeping, financial statements, and more!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize with a welcome message
if not st.session_state.messages:
    welcome_msg = {
        "role": "assistant", 
        "content": "Hello! I'm your accounting assistant. I can help you with:\n\n• **Bookkeeping** questions\n• **Financial statements** explanations\n• **Tax** guidance\n• **Accounting principles** (GAAP, IFRS)\n• **Business finance** advice\n\nWhat would you like to know about?"
    }
    st.session_state.messages.append(welcome_msg)

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accounting knowledge base (you can expand this)
accounting_responses = {
    "balance sheet": "A **Balance Sheet** shows your company's financial position at a specific point in time. It follows the equation: **Assets = Liabilities + Equity**. Assets include cash, inventory, and equipment. Liabilities are debts like loans and accounts payable. Equity represents owner's investment and retained earnings.",

    "income statement": "An **Income Statement** (P&L) shows revenues and expenses over a period. It follows: **Revenue - Expenses = Net Income**. It helps you understand profitability and operational efficiency.",

    "cash flow": "**Cash Flow Statement** tracks cash in and out of your business in three categories: Operating (day-to-day operations), Investing (equipment, investments), and Financing (loans, equity). Positive cash flow means more money coming in than going out.",

    "depreciation": "**Depreciation** spreads the cost of an asset over its useful life. Common methods include straight-line (equal amounts each year) and accelerated methods. It's a non-cash expense that reduces taxable income.",

    "accounts receivable": "**Accounts Receivable (AR)** represents money customers owe you for goods/services delivered on credit. Manage AR by setting clear payment terms, sending timely invoices, and following up on overdue accounts.",

    "accounts payable": "**Accounts Payable (AP)** is money you owe suppliers for goods/services received. Good AP management involves taking advantage of early payment discounts while maintaining healthy cash flow.",

    "double entry": "**Double-Entry Bookkeeping** means every transaction affects at least two accounts, and debits must equal credits. For example, when you sell a product: Debit Cash (asset increases) and Credit Sales Revenue (revenue increases).",

    "gaap": "**GAAP (Generally Accepted Accounting Principles)** are standard accounting rules in the US. Key principles include revenue recognition, matching principle, and conservatism. They ensure consistency and comparability in financial reporting."
}

def get_accounting_response(user_input):
    """Generate response based on user input"""
    user_lower = user_input.lower()

    # Check for keywords in the knowledge base
    for keyword, response in accounting_responses.items():
        if keyword in user_lower:
            return response

    # General accounting topics
    if any(word in user_lower for word in ["tax", "taxes", "deduction"]):
        return "For **tax questions**, I recommend consulting with a qualified tax professional. However, some general tips: keep detailed records, understand business deductions (office supplies, business meals, travel), and consider quarterly estimated payments if you're self-employed."

    elif any(word in user_lower for word in ["budget", "budgeting"]):
        return "**Budgeting** is crucial for financial planning. Start with: 1) Track historical income/expenses, 2) Set realistic revenue goals, 3) Plan for fixed and variable costs, 4) Include a contingency fund, 5) Review and adjust monthly."

    elif any(word in user_lower for word in ["invoice", "invoicing"]):
        return "**Best invoicing practices**: Include clear payment terms, detailed descriptions, due dates, and your business information. Send promptly after delivery, follow up on overdue payments, and consider offering early payment discounts."

    elif any(word in user_lower for word in ["ratio", "ratios", "analysis"]):
        return "Key **financial ratios** include:\n• **Liquidity**: Current Ratio (Current Assets/Current Liabilities)\n• **Profitability**: Gross Margin, Net Margin\n• **Efficiency**: Inventory Turnover, AR Turnover\n• **Leverage**: Debt-to-Equity Ratio"

    else:
        return "I'd be happy to help with that accounting question! Could you be more specific? I can assist with topics like financial statements, bookkeeping, taxes, budgeting, or accounting principles."

def stream_response(response_text):
    """Simulate streaming response"""
    words = response_text.split()
    for i, word in enumerate(words):
        yield word + " "
        time.sleep(0.05)  # Adjust speed as needed

# Chat input
if prompt := st.chat_input("Ask me an accounting question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = get_accounting_response(prompt)
        # Stream the response for better UX
        response_placeholder = st.empty()
        full_response = ""

        for chunk in stream_response(response):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with helpful information
with st.sidebar:
    st.header("📚 Quick Reference")

    st.subheader("Common Topics")
    topics = [
        "Balance Sheet",
        "Income Statement", 
        "Cash Flow",
        "Accounts Receivable",
        "Accounts Payable",
        "Depreciation",
        "Financial Ratios",
        "Budgeting",
        "Tax Planning"
    ]

    for topic in topics:
        if st.button(topic, key=f"topic_{topic}"):
            # Add the topic as a user message
            st.session_state.messages.append({"role": "user", "content": f"Tell me about {topic.lower()}"})
            st.rerun()

    st.markdown("---")
    st.markdown("💡 **Tip**: Ask specific questions for better answers!")

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
