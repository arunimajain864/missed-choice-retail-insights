import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "missed_choice.db"

st.set_page_config(
    page_title="Missed Choice | Retail Insights",
    page_icon="🛍️",
    layout="wide",
)

REASONS = [
    "Price was too high",
    "Size unavailable",
    "Preferred colour unavailable",
    "Design/style not available",
    "Could not decide",
    "Product quality/fit concern",
    "Just browsing",
    "Other",
]
CATEGORIES = ["Kurtis", "Dresses", "Sarees", "Tops", "Bottomwear", "Ethnic sets", "Other"]
PRICE_BANDS = ["Under ₹500", "₹500–₹999", "₹1,000–₹1,999", "₹2,000–₹3,999", "₹4,000+"]
SIZES = ["XS", "S", "M", "L", "XL", "XXL", "Free size", "Not applicable"]
COLOURS = ["Black", "White", "Red", "Blue", "Green", "Pink", "Yellow", "Beige", "Other", "Not specified"]


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS missed_choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visit_date TEXT NOT NULL,
                reason TEXT NOT NULL,
                category TEXT NOT NULL,
                price_band TEXT NOT NULL,
                desired_size TEXT,
                desired_colour TEXT,
                desired_style TEXT,
                notes TEXT,
                staff_member TEXT,
                follow_up_allowed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def load_missed_choices():
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM missed_choices ORDER BY visit_date DESC, id DESC", conn)
    if not df.empty:
        df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    return df


def load_sales():
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM sales ORDER BY sale_date DESC, id DESC", conn)
    if not df.empty:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    return df


def add_missed_choice(data):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO missed_choices
            (visit_date, reason, category, price_band, desired_size, desired_colour,
             desired_style, notes, staff_member, follow_up_allowed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["visit_date"], data["reason"], data["category"], data["price_band"],
            data["desired_size"], data["desired_colour"], data["desired_style"],
            data["notes"], data["staff_member"], int(data["follow_up_allowed"]),
            datetime.now().isoformat(timespec="seconds")
        ))
        conn.commit()


def add_sale(sale_date, category, amount):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO sales (sale_date, category, amount, created_at) VALUES (?, ?, ?, ?)",
            (sale_date.isoformat(), category, float(amount), datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()


def seed_demo_data():
    """Add a small, clearly labelled synthetic dataset for exploring the dashboard."""
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM missed_choices").fetchone()[0]
        if count:
            return False
        today = date.today()
        demo = [
            (today - timedelta(days=1), "Size unavailable", "Kurtis", "₹500–₹999", "M", "Blue", "Straight kurti", "Wanted a medium in blue", "Demo", 0),
            (today - timedelta(days=2), "Price was too high", "Dresses", "₹2,000–₹3,999", "L", "Black", "Party dress", "Budget was around ₹1,500", "Demo", 0),
            (today - timedelta(days=3), "Design/style not available", "Sarees", "₹1,000–₹1,999", "Not applicable", "Green", "Lightweight festive saree", "", "Demo", 0),
            (today - timedelta(days=4), "Size unavailable", "Kurtis", "₹500–₹999", "L", "Pink", "A-line kurti", "", "Demo", 0),
            (today - timedelta(days=5), "Could not decide", "Ethnic sets", "₹2,000–₹3,999", "M", "Not specified", "Office/festive use", "", "Demo", 0),
            (today - timedelta(days=6), "Preferred colour unavailable", "Tops", "Under ₹500", "S", "White", "Casual top", "", "Demo", 0),
            (today - timedelta(days=8), "Price was too high", "Kurtis", "₹1,000–₹1,999", "XL", "Red", "Cotton kurti", "", "Demo", 0),
            (today - timedelta(days=9), "Size unavailable", "Kurtis", "₹500–₹999", "M", "Black", "Printed kurti", "", "Demo", 0),
            (today - timedelta(days=10), "Product quality/fit concern", "Dresses", "₹1,000–₹1,999", "L", "Blue", "Casual dress", "", "Demo", 0),
            (today - timedelta(days=12), "Price was too high", "Sarees", "₹4,000+", "Not applicable", "Red", "Silk saree", "", "Demo", 0),
            (today - timedelta(days=14), "Size unavailable", "Kurtis", "₹500–₹999", "S", "Green", "Daily wear kurti", "", "Demo", 0),
            (today - timedelta(days=16), "Just browsing", "Bottomwear", "₹500–₹999", "M", "Black", "Straight pants", "", "Demo", 0),
        ]
        for row in demo:
            conn.execute("""
                INSERT INTO missed_choices
                (visit_date, reason, category, price_band, desired_size, desired_colour,
                 desired_style, notes, staff_member, follow_up_allowed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (row[0].isoformat(), *row[1:], datetime.now().isoformat(timespec="seconds")))
        for i, (cat, amount) in enumerate([
            ("Kurtis", 1800), ("Dresses", 3200), ("Sarees", 4500), ("Tops", 900),
            ("Kurtis", 2400), ("Ethnic sets", 5100), ("Bottomwear", 1200)
        ]):
            conn.execute(
                "INSERT INTO sales (sale_date, category, amount, created_at) VALUES (?, ?, ?, ?)",
                ((today - timedelta(days=i * 2)).isoformat(), cat, amount, datetime.now().isoformat(timespec="seconds"))
            )
        conn.commit()
        return True


def money(value):
    return f"₹{value:,.0f}"


init_db()

st.title("🛍️ Missed Choice")
st.caption("Understand why customers leave without buying — and turn those observations into better stock and service decisions.")

with st.sidebar:
    st.header("Shop workspace")
    shop_name = st.text_input("Shop name", value="My Clothing Shop")
    st.caption("This demo stores data locally in a SQLite database.")
    page = st.radio(
        "Navigate",
        ["Overview", "Record a missed sale", "Sales log", "Insights & actions", "View records"],
    )
    st.divider()
    st.subheader("Demo data")
    if st.button("Load sample data", use_container_width=True):
        added = seed_demo_data()
        if added:
            st.success("Sample data loaded.")
        else:
            st.info("Records already exist. Sample data was not duplicated.")
    if st.button("Delete all data", use_container_width=True):
        st.session_state["confirm_delete"] = True
    if st.session_state.get("confirm_delete"):
        st.warning("This permanently deletes all records in this local demo database.")
        c1, c2 = st.columns(2)
        if c1.button("Confirm delete", type="primary"):
            with get_connection() as conn:
                conn.execute("DELETE FROM missed_choices")
                conn.execute("DELETE FROM sales")
                conn.commit()
            st.session_state["confirm_delete"] = False
            st.rerun()
        if c2.button("Cancel"):
            st.session_state["confirm_delete"] = False
            st.rerun()

missed = load_missed_choices()
sales = load_sales()

if page == "Overview":
    st.header(f"{shop_name} | Overview")
    st.write("A simple view of customer demand that did not convert into a purchase.")
    total = len(missed)
    recent = missed[missed["visit_date"] >= pd.Timestamp(date.today() - timedelta(days=7))] if total else missed
    top_reason = missed["reason"].mode().iloc[0] if total else "No data yet"
    top_category = missed["category"].mode().iloc[0] if total else "No data yet"
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Recorded missed choices", total)
    col2.metric("Last 7 days", len(recent))
    col3.metric("Most common reason", top_reason)
    col4.metric("Most requested category", top_category)

    if total:
        left, right = st.columns(2)
        with left:
            reason_counts = missed["reason"].value_counts().rename_axis("Reason").reset_index(name="Count")
            fig = px.bar(reason_counts, x="Count", y="Reason", orientation="h", title="Why customers left without buying")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            category_counts = missed["category"].value_counts().rename_axis("Category").reset_index(name="Count")
            fig = px.pie(category_counts, names="Category", values="Count", title="Products customers were looking for")
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("Recent observations")
        show_cols = ["visit_date", "reason", "category", "price_band", "desired_size", "desired_colour"]
        st.dataframe(missed[show_cols].head(8), use_container_width=True, hide_index=True)
    else:
        st.info("No observations recorded yet. Start by recording a missed sale or load sample data to explore the dashboard.")

elif page == "Record a missed sale":
    st.header("Record a missed sale")
    st.write("Ask politely and keep it optional. Do not collect names, phone numbers or other personal information for this exercise.")
    with st.form("missed_sale_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            visit_date = st.date_input("Visit date", value=date.today(), max_value=date.today())
            reason = st.selectbox("Why did the customer leave without buying?", REASONS)
            category = st.selectbox("What type of product were they looking for?", CATEGORIES)
            price_band = st.selectbox("Approximate budget / price range", PRICE_BANDS)
            desired_size = st.selectbox("Size (if relevant)", SIZES)
        with c2:
            desired_colour = st.selectbox("Preferred colour (optional)", COLOURS)
            desired_style = st.text_input("Design or style requested (optional)", placeholder="e.g. cotton A-line kurti")
            staff_member = st.text_input("Recorded by (optional)", placeholder="e.g. Staff 1")
            follow_up_allowed = st.checkbox("Customer voluntarily agreed to be contacted (only if contact details are collected separately and securely)")
            notes = st.text_area("Additional note (optional)", placeholder="Keep notes short and non-identifying.")
        submitted = st.form_submit_button("Save observation", type="primary", use_container_width=True)
        if submitted:
            add_missed_choice({
                "visit_date": visit_date.isoformat(),
                "reason": reason,
                "category": category,
                "price_band": price_band,
                "desired_size": desired_size,
                "desired_colour": desired_colour,
                "desired_style": desired_style.strip(),
                "notes": notes.strip(),
                "staff_member": staff_member.strip(),
                "follow_up_allowed": follow_up_allowed,
            })
            st.success("Observation saved. Thank you for recording customer feedback.")

elif page == "Sales log":
    st.header("Sales log")
    st.write("Add daily or individual sales totals so you can compare sales trends with missed-choice observations.")
    with st.form("sale_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        sale_date = c1.date_input("Sale date", value=date.today(), max_value=date.today())
        sale_category = c2.selectbox("Product category", CATEGORIES)
        amount = c3.number_input("Sale amount (₹)", min_value=1.0, value=1000.0, step=100.0)
        submitted = st.form_submit_button("Add sale", type="primary")
        if submitted:
            add_sale(sale_date, sale_category, amount)
            st.success("Sale added.")
            st.rerun()
    if not sales.empty:
        st.subheader("Recorded sales")
        st.dataframe(sales[["sale_date", "category", "amount"]], use_container_width=True, hide_index=True)
        st.metric("Total recorded sales", money(sales["amount"].sum()))
    else:
        st.info("No sales entered yet. You can still use the missed-choice insights without sales data.")

elif page == "Insights & actions":
    st.header("Insights & actions")
    st.write("Look for repeated patterns before changing inventory or pricing. A few observations are signals, not proof.")
    if missed.empty:
        st.info("Record observations or load sample data to see insights.")
    else:
        min_date = missed["visit_date"].min().date()
        max_date = missed["visit_date"].max().date()
        c1, c2 = st.columns(2)
        start_date = c1.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
        end_date = c2.date_input("To", value=max_date, min_value=min_date, max_value=max_date)
        filtered = missed[(missed["visit_date"].dt.date >= start_date) & (missed["visit_date"].dt.date <= end_date)]
        if start_date > end_date:
            st.error("The start date must be on or before the end date.")
        elif filtered.empty:
            st.warning("No observations in this date range.")
        else:
            reason_counts = filtered["reason"].value_counts().rename_axis("Reason").reset_index(name="Count")
            category_counts = filtered["category"].value_counts().rename_axis("Category").reset_index(name="Count")
            st.subheader("Patterns in the selected period")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(px.bar(reason_counts, x="Reason", y="Count", title="Reasons customers did not buy"), use_container_width=True)
            with col2:
                st.plotly_chart(px.bar(category_counts, x="Category", y="Count", title="Categories customers requested"), use_container_width=True)

            st.subheader("Potential actions to investigate")
            top = filtered.groupby(["category", "reason"]).size().reset_index(name="observations")
            top = top.sort_values("observations", ascending=False)
            suggestions = []
            for _, row in top.head(5).iterrows():
                cat, why, count = row["category"], row["reason"], int(row["observations"])
                if why == "Size unavailable":
                    action = f"Check size availability and recent demand for {cat} before the next stock order."
                elif why == "Price was too high":
                    action = f"Review the price range and nearby alternatives for {cat}; do not discount without checking margins."
                elif why in ["Preferred colour unavailable", "Design/style not available"]:
                    action = f"Ask suppliers about a small test quantity of the requested colours/styles in {cat}."
                elif why == "Could not decide":
                    action = f"Test clearer product information or simple outfit suggestions for {cat}."
                elif why == "Product quality/fit concern":
                    action = f"Review product descriptions, fabric/fit information and quality feedback for {cat}."
                else:
                    action = f"Review customer conversations for {cat} to understand whether there is a specific unmet need."
                suggestions.append({"Pattern": f"{cat} — {why}", "Observations": count, "Possible next step": action})
            st.dataframe(pd.DataFrame(suggestions), use_container_width=True, hide_index=True)

            if len(filtered) < 10:
                st.caption("You have fewer than 10 observations in this period. Treat these patterns as early signals and collect more feedback before making stock decisions.")
            else:
                st.caption("These are descriptive patterns from recorded observations, not a statistically proven explanation of all lost sales.")

            if not sales.empty:
                st.subheader("Sales recorded by category")
                sales_period = sales[(sales["sale_date"].dt.date >= start_date) & (sales["sale_date"].dt.date <= end_date)]
                if not sales_period.empty:
                    sales_cat = sales_period.groupby("category", as_index=False)["amount"].sum()
                    st.plotly_chart(px.bar(sales_cat, x="category", y="amount", title="Recorded sales by category (₹)"), use_container_width=True)
                else:
                    st.caption("No sales were recorded in this date range.")

elif page == "View records":
    st.header("View and export records")
    st.subheader("Missed-choice observations")
    if missed.empty:
        st.info("No observations recorded yet.")
    else:
        export_df = missed.drop(columns=["created_at"], errors="ignore").copy()
        st.dataframe(export_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download missed-choice data (CSV)",
            export_df.to_csv(index=False).encode("utf-8"),
            file_name="missed_choice_observations.csv",
            mime="text/csv",
        )
    st.subheader("Sales records")
    if sales.empty:
        st.info("No sales recorded yet.")
    else:
        sales_export = sales.drop(columns=["created_at"], errors="ignore").copy()
        st.dataframe(sales_export, use_container_width=True, hide_index=True)
        st.download_button(
            "Download sales data (CSV)",
            sales_export.to_csv(index=False).encode("utf-8"),
            file_name="shop_sales.csv",
            mime="text/csv",
        )

st.divider()
st.caption("Missed Choice is a portfolio/demo tool. Record only voluntary, non-identifying feedback. Sample records are synthetic.")
