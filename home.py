
# Home.py - Enhanced Interactive Banking Interface
import streamlit as st
import json
from pathlib import Path
import random
import string
from datetime import datetime
import time

# ====================== CONFIG ======================
st.set_page_config(
    page_title="Central Bank Pro",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: #000;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #d4edda;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 2px solid #17a2b8;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ====================== DATABASE ======================
DB_FILE = "database.json"
TRANSACTIONS_FILE = "transactions.json"

def load_data():
    if Path(DB_FILE).exists():
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_transactions():
    if Path(TRANSACTIONS_FILE).exists():
        with open(TRANSACTIONS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_transaction(acc_no, type_tx, amount, balance_after):
    transactions = load_transactions()
    tx = {
        "account_no": acc_no,
        "type": type_tx,
        "amount": amount,
        "balance_after": balance_after,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions.append(tx)
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

def get_user_transactions(acc_no, limit=5):
    transactions = load_transactions()
    user_txs = [tx for tx in transactions if tx["account_no"] == acc_no]
    return user_txs[-limit:][::-1]  # Last 5, most recent first

def generate_account_no():
    alpha = random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5)
    digits = random.choices(string.digits, k=4)
    code = alpha + digits
    random.shuffle(code)
    return "".join(code)

def find_user_index(acc, pin):
    for i, u in enumerate(Bank.data):
        if u.get("Account No.") == acc and str(u.get("pin")) == str(pin):
            return i
    return None

# Initialize Bank object and session_state keys
Bank = type("Bank", (), {})()
Bank.data = load_data()

if "user_index_update" not in st.session_state:
    st.session_state["user_index_update"] = None
if "user_index_delete" not in st.session_state:
    st.session_state["user_index_delete"] = None
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "show_confetti" not in st.session_state:
    st.session_state["show_confetti"] = False
if "navigate_to" not in st.session_state:
    st.session_state["navigate_to"] = None

# ====================== HEADER ======================
st.markdown("""
<div class="main-header">
    <h1>🏦 Central Bank Pro</h1>
    <p style="font-size: 1.2rem; margin: 0;">Secure • Simple • Smart Banking Experience</p>
</div>
""", unsafe_allow_html=True)

# ====================== DASHBOARD STATS ======================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <h3>👥 Total Accounts</h3>
        <h1>{len(Bank.data)}</h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    total_balance = sum(u.get("balance", 0) for u in Bank.data)
    st.markdown(f"""
    <div class="stat-card">
        <h3>💰 Total Deposits</h3>
        <h1>₹{total_balance:,}</h1>
    </div>
    """, unsafe_allow_html=True)
with col3:
    total_txs = len(load_transactions())
    st.markdown(f"""
    <div class="stat-card">
        <h3>📊 Transactions</h3>
        <h1>{total_txs}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ====================== SIDEBAR MENU ======================
st.sidebar.title("🗂️ Banking Menu")
st.sidebar.markdown("---")

if st.session_state["logged_in_user"]:
    user = Bank.data[st.session_state["logged_in_user"]]
    st.sidebar.success(f"👤 Welcome, **{user['name']}**!")
    st.sidebar.info(f"💳 Balance: ₹**{user['balance']:,}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in_user"] = None
        st.rerun()
    st.sidebar.markdown("---")

choice = st.sidebar.radio("Choose an Option", [
    "🏠 Dashboard",
    "➕ Create Account",
    "💵 Deposit Money",
    "💸 Withdraw Money",
    "🔍 View Details",
    "✏️ Update Details",
    "🗑️ Delete Account"
], label_visibility="collapsed")

# ====================== MAIN APP ======================

# Dashboard / Quick Login
if choice == "🏠 Dashboard":
    st.header("🏠 Quick Access Dashboard")
    
    if not st.session_state["logged_in_user"]:
        # Show welcome message for new users
        if len(Bank.data) == 0:
            st.info("👋 **Welcome to Central Bank Pro!** No accounts exist yet. Create your first account to get started!")
            if st.button("➕ Create Your First Account", use_container_width=True):
                st.session_state["navigate_to"] = "create"
                st.rerun()
        else:
            pass
            
        col1, col2 = st.columns([2, 1])
        with col1:
            with st.form("quick_login"):
                acc = st.text_input("Account Number", placeholder="Enter your account number")
                pin = st.text_input("PIN", type="password", placeholder="4-digit PIN")
                login_btn = st.form_submit_button("🔑 Login", use_container_width=True)
                
                if login_btn:
                    user_index = find_user_index(acc, pin)
                    if user_index is None:
                        st.error("❌ Invalid credentials")
                    else:
                        st.session_state["logged_in_user"] = user_index
                        st.success("✅ Login successful!")
                        time.sleep(0.5)
                        st.rerun()
        
        with col2:
            st.info("""
            ### 🚀 Getting Started
            
            **New User?**
            1. Click "Create Account" 
            2. Fill in your details
            3. Get your account number
            4. Start banking!
            
            **Existing User?**
            Login with your account number and PIN
            """)
        
        # Show all accounts preview (without sensitive info)
        if len(Bank.data) > 0:
            st.markdown("---")
            st.subheader("📋 Recent Accounts (Preview)")
            preview_data = []
            for user in Bank.data[-5:]:  # Show last 5 accounts
                preview_data.append({
                    "Name": user.get("name", "N/A"),
                    "Account No": user.get("Account No.", "N/A"),
                    "Status": "✅ Active"
                })
            import pandas as pd
            df = pd.DataFrame(preview_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    else:
        # Show user dashboard
        user = Bank.data[st.session_state["logged_in_user"]]
        st.subheader(f"Welcome back, {user['name']}! 👋")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h3>💳 Account Information</h3>
                <p><strong>Account No:</strong> {user['Account No.']}</p>
                <p><strong>Balance:</strong> ₹{user['balance']:,}</p>
                <p><strong>Email:</strong> {user['email']}</p>
                <p><strong>Phone:</strong> {user['phone no']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📜 Recent Transactions")
            recent_txs = get_user_transactions(user['Account No.'])
            if recent_txs:
                for tx in recent_txs:
                    emoji = "💵" if tx['type'] == "deposit" else "💸"
                    color = "green" if tx['type'] == "deposit" else "red"
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 0.5rem; margin: 0.5rem 0; border-radius: 5px; border-left: 4px solid {color};">
                        {emoji} <strong>{tx['type'].title()}</strong>: ₹{tx['amount']:,} <br>
                        <small>{tx['timestamp']} | Balance: ₹{tx['balance_after']:,}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No transactions yet")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💵 Deposit", use_container_width=True):
                st.session_state["quick_action"] = "deposit"
        with col2:
            if st.button("💸 Withdraw", use_container_width=True):
                st.session_state["quick_action"] = "withdraw"
        with col3:
            if st.button("✏️ Update Profile", use_container_width=True):
                st.session_state["quick_action"] = "update"

# Create Account
elif choice == "➕ Create Account":
    st.header("➕ Create New Account")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("create_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="10-digit mobile number", max_chars=10)
            pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4, placeholder="Create secure PIN")
            
            submitted = st.form_submit_button("🎉 Create Account", use_container_width=True)
            if submitted:
                if not all([name, email, phone, pin]):
                    st.error("❌ All fields are required!")
                elif len(phone) != 10 or not phone.isdigit():
                    st.error("❌ Enter valid 10-digit phone number")
                elif len(pin) != 4 or not pin.isdigit():
                    st.error("❌ PIN must be exactly 4 digits")
                elif "@" not in email:
                    st.error("❌ Enter valid email")
                else:
                    acc_no = generate_account_no()
                    new_user = {
                        "name": name,
                        "email": email,
                        "phone no": phone,
                        "pin": int(pin),
                        "Account No.": acc_no,
                        "balance": 0
                    }
                    Bank.data.append(new_user)
                    save_data(Bank.data)
                    st.balloons()
                    st.success("✅ Account Created Successfully!")
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>🎊 Welcome to Central Bank!</h3>
                        <p><strong>Your Account Number:</strong> <code style="font-size: 1.3rem; background: #fff; padding: 5px 10px; border-radius: 5px;">{acc_no}</code></p>
                        <p>⚠️ Save this account number securely!</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.info("""
        ### 📋 Requirements
        - ✅ Valid email
        - ✅ 10-digit phone
        - ✅ 4-digit secure PIN
        
        ### 🔒 Security
        Your data is encrypted and secure.
        """)

# Deposit Money
elif choice == "💵 Deposit Money":
    st.header("💵 Deposit Money")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("deposit_form"):
            acc = st.text_input("Account Number", placeholder="Your account number")
            pin = st.text_input("PIN", type="password", max_chars=4, placeholder="4-digit PIN")
            amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=100000, step=100, value=500)
            submitted = st.form_submit_button("💰 Deposit Now", use_container_width=True)

            if submitted:
                user_index = find_user_index(acc, pin)
                if user_index is None:
                    st.error("❌ Invalid Account Number or PIN")
                else:
                    amt = int(amount)
                    if amt <= 0:
                        st.error("❌ Enter a valid amount greater than 0")
                    else:
                        Bank.data[user_index]["balance"] = int(Bank.data[user_index].get("balance", 0)) + amt
                        new_balance = Bank.data[user_index]["balance"]
                        save_data(Bank.data)
                        save_transaction(acc, "deposit", amt, new_balance)
                        st.success(f"✅ ₹{amt:,} deposited successfully!")
                        st.balloons()
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>💵 Transaction Successful</h3>
                            <p><strong>Deposited:</strong> ₹{amt:,}</p>
                            <p><strong>New Balance:</strong> ₹{new_balance:,}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.info("""
        ### 💡 Quick Tips
        - Min: ₹1
        - Max: ₹1,00,000 per transaction
        - Instant credit
        - Secure & encrypted
        """)

# Withdraw Money
elif choice == "💸 Withdraw Money":
    st.header("💸 Withdraw Money")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("withdraw_form"):
            acc = st.text_input("Account Number", placeholder="Your account number")
            pin = st.text_input("PIN", type="password", max_chars=4, placeholder="4-digit PIN")
            amount = st.number_input("Amount to Withdraw (₹)", min_value=1, step=100, value=500)
            submitted = st.form_submit_button("💸 Withdraw Now", use_container_width=True)

            if submitted:
                user_index = find_user_index(acc, pin)
                if user_index is None:
                    st.error("❌ Invalid Account Number or PIN")
                else:
                    balance = int(Bank.data[user_index].get("balance", 0))
                    amt = int(amount)
                    if balance <= 0:
                        st.error("❌ Insufficient balance (₹0). Deposit first.")
                    elif amt <= 0:
                        st.error("❌ Enter a valid amount greater than 0")
                    elif amt > balance:
                        st.error(f"❌ Insufficient balance. Available: ₹{balance:,}")
                    else:
                        Bank.data[user_index]["balance"] = balance - amt
                        new_balance = Bank.data[user_index]["balance"]
                        save_data(Bank.data)
                        save_transaction(acc, "withdraw", amt, new_balance)
                        st.success(f"✅ ₹{amt:,} withdrawn successfully!")
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>💸 Transaction Successful</h3>
                            <p><strong>Withdrawn:</strong> ₹{amt:,}</p>
                            <p><strong>Remaining Balance:</strong> ₹{new_balance:,}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.warning("""
        ### ⚠️ Important
        - Check available balance
        - Withdrawal limits apply
        - Instant debit
        - Transaction is irreversible
        """)

# View Details
elif choice == "🔍 View Details":
    st.header("🔍 Account Details")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        acc = st.text_input("Account Number", placeholder="Enter account number")
        pin = st.text_input("PIN", type="password", placeholder="4-digit PIN")

        if st.button("🔍 View Details", use_container_width=True):
            user_index = find_user_index(acc, pin)
            if user_index is None:
                st.error("❌ Account not found or invalid PIN")
            else:
                user = Bank.data[user_index]
                st.success("✅ Account Found!")
                st.markdown(f"""
                <div class="info-box">
                    <h3>👤 Account Information</h3>
                    <p><strong>Name:</strong> {user['name']}</p>
                    <p><strong>Email:</strong> {user['email']}</p>
                    <p><strong>Phone:</strong> {user['phone no']}</p>
                    <p><strong>Account No:</strong> <code>{user['Account No.']}</code></p>
                    <p><strong>Balance:</strong> ₹{user['balance']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show recent transactions
                st.markdown("### 📜 Recent Transactions")
                recent_txs = get_user_transactions(user['Account No.'])
                if recent_txs:
                    for tx in recent_txs:
                        emoji = "💵" if tx['type'] == "deposit" else "💸"
                        st.markdown(f"{emoji} **{tx['type'].title()}**: ₹{tx['amount']:,} | {tx['timestamp']}")
                else:
                    st.info("No transactions found")
    
    with col2:
        st.info("""
        ### 🔐 Privacy
        Your account details are secure and private.
        
        Only you can access your information with correct credentials.
        """)

# Update Details
elif choice == "✏️ Update Details":
    st.header("✏️ Update Account Details")
    
    with st.form("update_login_form"):
        col1, col2 = st.columns(2)
        with col1:
            acc_login = st.text_input("Account Number", placeholder="Your account number")
        with col2:
            pin_login = st.text_input("PIN", type="password", max_chars=4, placeholder="4-digit PIN")
        login = st.form_submit_button("🔑 Login to Update", use_container_width=True)

        if login:
            idx = find_user_index(acc_login, pin_login)
            if idx is None:
                st.error("❌ Invalid credentials")
                st.session_state["user_index_update"] = None
            else:
                st.success("✅ Logged in! You can now update details below.")
                st.session_state["user_index_update"] = idx

    if st.session_state["user_index_update"] is not None:
        idx = st.session_state["user_index_update"]
        user = Bank.data[idx]
        
        st.markdown("---")
        with st.form("update_form"):
            st.subheader("Update Your Information")
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Name", value=user.get("name", ""))
                new_email = st.text_input("Email", value=user.get("email", ""))
            with col2:
                new_phone = st.text_input("Phone", value=user.get("phone no", ""))
                new_pin = st.text_input("New PIN (4 digits)", type="password", max_chars=4, placeholder="Leave blank to keep current")
            
            submit_update = st.form_submit_button("💾 Update Details", use_container_width=True)

            if submit_update:
                if new_phone and (len(new_phone) != 10 or not new_phone.isdigit()):
                    st.error("❌ Enter valid 10-digit phone number")
                elif new_pin and (len(new_pin) != 4 or not new_pin.isdigit()):
                    st.error("❌ New PIN must be exactly 4 digits")
                elif new_email and ("@" not in new_email):
                    st.error("❌ Enter valid email")
                else:
                    user["name"] = new_name if new_name else user.get("name")
                    user["email"] = new_email if new_email else user.get("email")
                    user["phone no"] = new_phone if new_phone else user.get("phone no")
                    if new_pin:
                        user["pin"] = int(new_pin)
                    Bank.data[idx] = user
                    save_data(Bank.data)
                    st.success("✅ Details updated successfully!")
                    st.balloons()
                    st.session_state["user_index_update"] = None

# Delete Account
elif choice == "🗑️ Delete Account":
    st.header("🗑️ Delete Account")
    st.warning("⚠️ **Warning:** This action is permanent and cannot be undone!")

    with st.form("delete_login_form"):
        col1, col2 = st.columns(2)
        with col1:
            acc_login = st.text_input("Account Number", placeholder="Your account number")
        with col2:
            pin_login = st.text_input("PIN", type="password", max_chars=4, placeholder="4-digit PIN")
        login_del = st.form_submit_button("🔑 Login to Delete", use_container_width=True)

        if login_del:
            idx = find_user_index(acc_login, pin_login)
            if idx is None:
                st.error("❌ Invalid credentials")
                st.session_state["user_index_delete"] = None
            else:
                st.session_state["user_index_delete"] = idx
                st.error(f"⚠️ Are you sure you want to delete account of **{Bank.data[idx]['name']}**?")

    if st.session_state["user_index_delete"] is not None:
        idx = st.session_state["user_index_delete"]
        user = Bank.data[idx]
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Yes, Delete Forever", use_container_width=True):
                Bank.data.pop(idx)
                save_data(Bank.data)
                st.success(f"✅ Account of {user['name']} deleted permanently.")
                st.session_state["user_index_delete"] = None
                time.sleep(1)
                st.rerun()
        with col2:
            if st.button("❌ No, Cancel", use_container_width=True):
                st.info("✅ Deletion cancelled")
                st.session_state["user_index_delete"] = None

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p style="font-size: 0.9rem;">🏦 <strong>Central Bank Pro</strong> • Built with ❤️ using Streamlit</p>
    <p style="font-size: 0.8rem;">© 2024 Central Bank. All rights reserved. | Secure Banking Solution</p>
</div>
""", unsafe_allow_html=True)

# python -m streamlit run Home.py