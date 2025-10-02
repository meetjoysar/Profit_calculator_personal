import streamlit as st
from streamlit.components.v1 import html as components_html

# Page configuration
st.set_page_config(page_title="Profit Calculator", page_icon="💰", layout="centered")

# Mobile-first readability CSS
st.markdown("""
<style>
  .stApp { max-width: 760px; margin: 0 auto; }
  html, body, [class*="css"] { line-height: 1.6; }
  @media (max-width: 480px) {
    html, body, [class*="css"] { font-size: 17px; }
    input, select, textarea { font-size: 16px !important; }
    button[kind="primary"], button[kind="secondary"] { min-height: 48px; font-size: 16px; }
  }
</style>
""", unsafe_allow_html=True)

# One-time state for jump behavior
if "jump_to" not in st.session_state:
  st.session_state["jump_to"] = None

# Title
st.title("💰 Profit Calculator with GST")
st.caption("Optimized for mobile and desktop • Batched input with a single Calculate action")

# Method selector OUTSIDE the form so dependent fields update immediately
st.subheader("Sale method")
sale_method = st.radio(
  "Sale price input method",
  ["Method 1: Sale Price WITHOUT GST", "Method 2: Sale Price WITH GST"],
  index=0,
  horizontal=False,
  key="sale_method",
)

# INPUTS (batched in a form)
with st.form("calc_form"):
  st.header("📥 Input")

  # Purchase details
  st.subheader("Purchase")
  colp1, colp2 = st.columns(2)
  with colp1:
    purchase_price = st.number_input(
      "Purchase Price (without GST)", min_value=0.0, value=6450.0, step=100.0, format="%.2f", key="purchase_price"
    )
  with colp2:
    gst_rate_purchase = st.number_input(
      "GST Rate on Purchase (%)", min_value=0.0, value=18.0, step=0.5, format="%.1f", key="gst_rate_purchase"
    )

  # Sale details (change instantly when sale_method toggles above)
  st.subheader("Sale")
  colS1, colS2 = st.columns(2)
  if sale_method.startswith("Method 1"):
    with colS1:
      sale_price_excl = st.number_input(
        "Sale Price (without GST)", min_value=0.0, value=7400.0, step=100.0, format="%.2f", key="sale_price_excl"
      )
    with colS2:
      gst_rate_sale = st.number_input(
        "GST Rate on Sale (%)", min_value=0.0, value=18.0, step=0.5, format="%.1f", key="gst_rate_sale"
      )
    base_for_other = sale_price_excl
  else:
    with colS1:
      gst_rate_sale = st.number_input(
        "GST Rate on Sale (%)", min_value=0.0, value=18.0, step=0.5, format="%.1f", key="gst_rate_sale"
      )
    with colS2:
      sale_price_incl = st.number_input(
        "Sale Price (WITH GST inclusive)", min_value=0.0, value=8500.0, step=100.0, format="%.2f", key="sale_price_incl"
      )
    base_for_other = sale_price_incl / (1.0 + gst_rate_sale / 100.0)

  # Expenses
  st.subheader("Expenses")
  colE1, colE2 = st.columns(2)
  with colE1:
    transport_cost = st.number_input("Transport Cost", min_value=0.0, value=0.0, step=10.0, format="%.2f", key="transport_cost")
  with colE2:
    goodwill_spent = st.number_input("Goodwill Spent", min_value=0.0, value=100.0, step=10.0, format="%.2f", key="goodwill_spent")

  other_expenses_percent = 0.5
  other_expenses_preview = base_for_other * (other_expenses_percent / 100.0)
  st.caption(f"Other Expenses auto-set: {other_expenses_percent}% of sale price (without GST) → ₹{other_expenses_preview:.2f}")

  submitted = st.form_submit_button("Calculate", type="primary", use_container_width=True)
  if submitted:
    st.session_state["jump_to"] = "results"

# Anchor to scroll to (always present in DOM)
st.markdown('<div id="results"></div>', unsafe_allow_html=True)

# CALCULATIONS (use values from current branch)
if sale_method.startswith("Method 1"):
  sale_price_without_gst = st.session_state.get("sale_price_excl", 7400.0)
  gst_rate_sale = st.session_state.get("gst_rate_sale", 18.0)
  gst_on_sale = sale_price_without_gst * (gst_rate_sale / 100.0)
  total_sale_amount = sale_price_without_gst + gst_on_sale
else:
  sale_price_with_gst = st.session_state.get("sale_price_incl", 8500.0)
  gst_rate_sale = st.session_state.get("gst_rate_sale", 18.0)
  sale_price_without_gst = sale_price_with_gst / (1.0 + gst_rate_sale / 100.0)
  gst_on_sale = sale_price_with_gst - sale_price_without_gst
  total_sale_amount = sale_price_with_gst

purchase_price = st.session_state.get("purchase_price", 6450.0)
gst_rate_purchase = st.session_state.get("gst_rate_purchase", 18.0)
gst_on_purchase = purchase_price * (gst_rate_purchase / 100.0)
total_purchase_cost = purchase_price + gst_on_purchase

gst_difference = gst_on_sale - gst_on_purchase
gross_profit = sale_price_without_gst - purchase_price

transport_cost = st.session_state.get("transport_cost", 0.0)
goodwill_spent = st.session_state.get("goodwill_spent", 100.0)
other_expenses = sale_price_without_gst * (other_expenses_percent / 100.0)
total_expenses = transport_cost + other_expenses + goodwill_spent
profit_before_tax = gross_profit - total_expenses

# Tax: apply only if profit positive; Excel-derived formula (2% of Sale × 30.4%)
if profit_before_tax > 0:
  tax_amount = (sale_price_without_gst * 0.02) * 0.304
  tax_caption = "✓ Tax is applicable as profit before tax is positive"
else:
  tax_amount = 0.0
  tax_caption = "⚠️ No tax as profit before tax is zero or negative (business loss)"

net_profit_after_tax = profit_before_tax - tax_amount

# RESULTS
st.header("📊 Results")

# Top KPI
if net_profit_after_tax > 0:
  st.success(f"### ✅ NET PROFIT AFTER TAX: ₹{net_profit_after_tax:.2f}")
elif net_profit_after_tax == 0:
  st.info(f"### ⚖️ BREAK-EVEN: ₹{net_profit_after_tax:.2f}")
else:
  st.error(f"### ❌ NET LOSS: ₹{abs(net_profit_after_tax):.2f}")

# Row 1: Profit Before Tax (left), GST Difference (right)
r1c1, r1c2 = st.columns(2)
r1c1.metric("Profit Before Tax", f"₹{profit_before_tax:.2f}")
r1c2.metric("GST Difference", f"₹{gst_difference:.2f}")

# Row 2: Total Expenses (left), Taxation (right)
r2c1, r2c2 = st.columns(2)
r2c1.metric("Total Expenses", f"₹{total_expenses:.2f}")
r2c2.metric("Taxation", f"₹{tax_amount:.2f}")
st.caption(tax_caption)

# Details below the two rows
with st.expander("See expense breakdown"):
  e1, e2, e3 = st.columns(3)
  e1.metric("Transport", f"₹{transport_cost:.2f}")
  e2.metric("Other (0.5%)", f"₹{other_expenses:.2f}")
  e3.metric("Goodwill", f"₹{goodwill_spent:.2f}")

# Sale details
st.subheader("Sale Details")
s1, s2, s3 = st.columns(3)
s1.metric("Sale (without GST)", f"₹{sale_price_without_gst:.2f}")
s2.metric("GST on Sale", f"₹{gst_on_sale:.2f}")
s3.metric("Total Sale Amount", f"₹{total_sale_amount:.2f}")

# Purchase details
st.subheader("Purchase Details")
p1, p2, p3 = st.columns(3)
p1.metric("Purchase (without GST)", f"₹{purchase_price:.2f}")
p2.metric("GST on Purchase", f"₹{gst_on_purchase:.2f}")
p3.metric("Total Purchase Cost", f"₹{total_purchase_cost:.2f}")

# Smooth auto-scroll to the results after submit
if st.session_state.get("jump_to") == "results":
  components_html("""
  <script>
    (function(){
      const targetId = "results";
      function scroll(){
        const el = window.parent.document.getElementById(targetId);
        if (el) { el.scrollIntoView({behavior:'smooth', block:'start'}); }
        else { setTimeout(scroll, 100); }
      }
      scroll();
    })();
  </script>
  """, height=0)
  st.session_state["jump_to"] = None

# Footer
st.markdown("---")
st.caption("Profit Calculator • Made with Streamlit • Compliant with Indian Tax Logic")
