"""
BizTrack AI - Smart Inventory & Bookkeeping for Small Businesses
Main Application Entry Point
"""

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

# Import custom modules
import database
import auth
import inventory
import sales
import expenses
import reports
import forecasting
import insights
import utils
import sample_data

# Page config
st.set_page_config(
    page_title="BizTrack AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'sample_data_loaded' not in st.session_state:
    st.session_state.sample_data_loaded = False

# Apply theme
st.markdown(utils.apply_theme(st.session_state.dark_mode), unsafe_allow_html=True)

def show_login_page():
    """Display login/signup page"""
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1 style="font-size: 48px; margin-bottom: 10px;">BizTrack AI</h1>
        <p style="font-size: 18px; color: #666; margin-bottom: 40px;">
            Smart Inventory & Bookkeeping for Small Businesses
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")

                if st.form_submit_button("Login", use_container_width=True):
                    if email and password:
                        success, result = auth.login(email, password)
                        if success:
                            st.session_state.user = result
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.warning("Please fill in all fields")

        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name", placeholder="Enter your name")
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                role = st.selectbox("Role", ["staff", "owner"])

                if st.form_submit_button("Create Account", use_container_width=True):
                    if name and email and password:
                        success, message = auth.signup(name, email, password, role)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill in all fields")

def show_dashboard():
    """Display main dashboard"""
    st.title("📊 Dashboard")

    # Get quick stats
    stats = insights.get_quick_stats()

    # KPI Cards Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Total Products", stats['total_products'])

    with col2:
        st.metric("Inventory Value", utils.format_currency(stats['inventory_value']))

    with col3:
        st.metric("Today's Sales", utils.format_currency(stats['today_sales']))

    with col4:
        st.metric("Monthly Revenue", utils.format_currency(stats['monthly_revenue']))

    with col5:
        st.metric("Total Expenses", utils.format_currency(stats['total_expenses']))

    with col6:
        net_profit = stats['net_profit']
        st.metric("Net Profit", utils.format_currency(net_profit),
                 delta=f"{net_profit:.0f}" if net_profit > 0 else f"{net_profit:.0f}")

    st.markdown("---")

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Monthly Sales Trend")
        monthly_sales = sales.get_monthly_sales_trend()
        if not monthly_sales.empty:
            monthly_sales = monthly_sales.sort_values('month')
            fig = px.line(monthly_sales, x='month', y='revenue',
                         labels={'revenue': 'Revenue ($)', 'month': 'Month'},
                         line_shape='spline')
            fig.update_traces(line_color='#1e3a5f', line_width=3)
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data available yet")

    with col2:
        st.subheader("💰 Revenue vs Expenses")
        monthly_sales_data = sales.get_monthly_sales_trend()
        monthly_expenses = expenses.get_monthly_expenses_trend()

        if not monthly_sales_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_sales_data['month'],
                y=monthly_sales_data['revenue'],
                name='Revenue',
                marker_color='#2ecc71'
            ))
            if not monthly_expenses.empty:
                fig.add_trace(go.Bar(
                    x=monthly_expenses['month'],
                    y=monthly_expenses['expenses'],
                    name='Expenses',
                    marker_color='#e74c3c'
                ))
            fig.update_layout(barmode='group', height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add sales data to see trends")

    # Second row of charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top Selling Products")
        top_products = sales.get_top_selling_products(5)
        if not top_products.empty:
            fig = px.bar(top_products, x='Product', y='Revenue',
                        color='Revenue', color_continuous_scale='Blues')
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20),
                             coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data yet")

    with col2:
        st.subheader("📦 Inventory by Category")
        inv_dist = inventory.get_inventory_distribution()
        if not inv_dist.empty:
            fig = px.pie(inv_dist, values='quantity', names='category',
                        hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inventory data yet")

    # Low stock alerts and recent transactions
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠️ Low Stock Alerts")
        low_stock = inventory.get_low_stock_products()
        if not low_stock.empty:
            st.dataframe(low_stock, use_container_width=True, hide_index=True)
        else:
            st.success("All products are well stocked!")

    with col2:
        st.subheader("📋 Recent Transactions")
        recent = sales.get_recent_transactions(5)
        if not recent.empty:
            recent['Amount'] = recent['Amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(recent, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions yet")

def show_inventory_page():
    """Display inventory management page"""
    st.title("📦 Inventory Management")

    col1, col2 = st.tabs(["Add Product", "Manage Inventory"])

    with col1:
        st.subheader("Add New Product")
        with st.form("add_product_form"):
            name = st.text_input("Product Name *")
            category = st.text_input("Category *")
            supplier = st.text_input("Supplier")
            col_a, col_b = st.columns(2)
            with col_a:
                cost_price = st.number_input("Cost Price ($)", min_value=0.0, format="%.2f")
                quantity = st.number_input("Quantity", min_value=0)
            with col_b:
                selling_price = st.number_input("Selling Price ($)", min_value=0.0, format="%.2f")
                reorder_level = st.number_input("Reorder Level", min_value=0, value=10)

            if st.form_submit_button("Add Product", type="primary"):
                if name and category:
                    success, result = inventory.add_product(
                        name, category, supplier, cost_price, selling_price,
                        quantity, reorder_level, st.session_state.user['id']
                    )
                    if success:
                        st.success(f"Product added! ID: {result}")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please fill in required fields (*)")

    with col2:
        st.subheader("Current Inventory")

        # Search and filter
        col_a, col_b, col_c = st.columns([2, 1, 1])
        with col_a:
            search = st.text_input("Search products", placeholder="Type to search...")
        with col_b:
            categories = inventory.get_categories()
            all_cats = ["All"] + categories
            cat_filter = st.selectbox("Category", all_cats)

        # Get filtered products
        if search or cat_filter != "All":
            products_df = inventory.search_products(search, cat_filter)
        else:
            products_df = inventory.get_all_products()

        if not products_df.empty:
            # Format for display
            display_df = products_df.copy()
            for col in ['Cost Price', 'Selling Price']:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Edit/Delete section
            st.markdown("### Edit Product")
            product_id = st.number_input("Enter Product ID to Edit/Delete", min_value=1, step=1)

            if st.button("Load Product", key="load_product"):
                product = inventory.get_product_by_id(product_id)
                if product:
                    st.session_state.edit_product = product
                else:
                    st.error("Product not found!")

            if 'edit_product' in st.session_state and st.session_state.edit_product:
                p = st.session_state.edit_product
                with st.form("edit_product_form"):
                    new_name = st.text_input("Name", value=p[1])
                    new_cat = st.text_input("Category", value=p[2])
                    new_supplier = st.text_input("Supplier", value=p[3] or "")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        new_cost = st.number_input("Cost Price", value=float(p[4]), format="%.2f")
                        new_qty = st.number_input("Quantity", value=int(p[6]))
                    with col_b:
                        new_price = st.number_input("Selling Price", value=float(p[5]), format="%.2f")
                        new_reorder = st.number_input("Reorder Level", value=int(p[7]))

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.form_submit_button("Update Product", type="primary"):
                            success, msg = inventory.update_product(
                                p[0], new_name, new_cat, new_supplier,
                                new_cost, new_price, new_qty, new_reorder,
                                st.session_state.user['id']
                            )
                            if success:
                                st.success(msg)
                                del st.session_state.edit_product
                                st.rerun()
                            else:
                                st.error(msg)
                    with col_b:
                        if st.form_submit_button("Delete Product"):
                            inventory.delete_product(p[0], st.session_state.user['id'])
                            st.success("Product deleted!")
                            del st.session_state.edit_product
                            st.rerun()
        else:
            st.info("No products in inventory. Add some products to get started!")

def show_sales_page():
    """Display sales management page"""
    st.title("💳 Sales Management")

    col1, col2 = st.tabs(["Record Sale", "Sales History"])

    with col1:
        st.subheader("Record New Sale")

        # Get products for dropdown
        products_df = inventory.get_all_products()
        if not products_df.empty:
            products_list = [f"{row['ID']} - {row['Name']} (Stock: {row['Quantity']})"
                           for _, row in products_df.iterrows()]

            with st.form("record_sale_form"):
                selected = st.selectbox("Select Product", products_list)
                quantity = st.number_input("Quantity to Sell", min_value=1, value=1)

                if selected:
                    product_id = int(selected.split(" - ")[0])
                    product = inventory.get_product_by_id(product_id)
                    if product:
                        unit_price = product[5]  # Selling price
                        total = quantity * unit_price
                        st.info(f"Unit Price: ${unit_price:,.2f} | Total: ${total:,.2f}")

                        if st.form_submit_button("Complete Sale", type="primary"):
                            success, msg = sales.record_sale(
                                product_id, product[1], quantity, unit_price,
                                st.session_state.user['id']
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
        else:
            st.warning("No products available. Add inventory first!")

    with col2:
        st.subheader("Sales History")

        # Date filter
        col_a, col_b, col_c = st.columns([2, 2, 1])
        with col_a:
            start_date = st.date_input("From", value=datetime.now() - timedelta(days=30))
        with col_b:
            end_date = st.date_input("To", value=datetime.now())
        with col_c:
            if st.button("Filter", key="filter_sales"):
                pass

        # Get sales
        sales_df = sales.get_sales_by_date_range(str(start_date), str(end_date))

        if not sales_df.empty:
            # Format display
            display_df = sales_df.copy()
            display_df['Unit Price'] = display_df['Unit Price'].apply(lambda x: f"${x:,.2f}")
            display_df['Total'] = display_df['Total'].apply(lambda x: f"${x:,.2f}")

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Summary stats
            total_revenue = sales_df['Total'].sum()
            total_units = sales_df['Quantity'].sum()
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            with col_b:
                st.metric("Units Sold", total_units)
        else:
            st.info("No sales records found for selected period")

def show_expenses_page():
    """Display expenses tracking page"""
    st.title("💸 Expense Tracking")

    col1, col2 = st.tabs(["Add Expense", "View Expenses"])

    with col1:
        st.subheader("Add New Expense")
        with st.form("add_expense_form"):
            category = st.selectbox("Category", expenses.get_expense_categories())
            description = st.text_area("Description")
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")

            if st.form_submit_button("Add Expense", type="primary"):
                if amount > 0:
                    success, msg = expenses.add_expense(
                        category, description, amount,
                        st.session_state.user['id']
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter an amount greater than 0")

    with col2:
        st.subheader("Expense Records")

        # Filters
        col_a, col_b, col_c = st.columns([2, 2, 1])
        with col_a:
            start_date = st.date_input("From", value=datetime.now() - timedelta(days=30))
        with col_b:
            cat_filter = st.selectbox("Category Filter", ["All"] + expenses.get_expense_categories())
        with col_c:
            if st.button("Filter", key="filter_expenses"):
                pass

        # Get expenses
        if cat_filter != "All":
            expenses_df = expenses.get_expenses_by_category(cat_filter)
        else:
            expenses_df = expenses.get_expenses_by_date_range(str(start_date), str(datetime.now()))

        if not expenses_df.empty:
            # Format display
            display_df = expenses_df.copy()
            display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Summary by category
            st.markdown("### Expenses by Category")
            category_summary = expenses.get_expenses_by_category_summary()
            if not category_summary.empty:
                fig = px.pie(category_summary, values='Total Amount', names='Category',
                            hole=0.4, color_discrete_sequence=px.colors.sequential.Reds_r)
                st.plotly_chart(fig, use_container_width=True)

            # Delete expense
            expense_id = st.number_input("Enter Expense ID to Delete", min_value=0, step=1)
            if st.button("Delete Expense"):
                expenses.delete_expense(expense_id, st.session_state.user['id'])
                st.success("Expense deleted!")
                st.rerun()
        else:
            st.info("No expense records found")

def show_reports_page():
    """Display reports page"""
    st.title("📊 Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Profit & Loss Summary")
        profit_data = reports.get_profit_report()

        # Display in metric cards
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Revenue", utils.format_currency(profit_data['total_revenue']))
        with m2:
            st.metric("COGS", utils.format_currency(profit_data['cost_of_goods']))
        with m3:
            st.metric("Expenses", utils.format_currency(profit_data['total_expenses']))

        st.metric("Net Profit", utils.format_currency(profit_data['net_profit']),
                delta=f"{profit_data['net_profit']:.0f}")

        # Monthly breakdown
        st.subheader("Monthly Profit Trend")
        monthly_profit = reports.get_monthly_profit_report()
        if not monthly_profit.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Revenue', x=monthly_profit['Month'], y=monthly_profit['Revenue'],
                                marker_color='#2ecc71'))
            fig.add_trace(go.Bar(name='Expenses', x=monthly_profit['Month'], y=monthly_profit['Expenses'],
                                marker_color='#e74c3c'))
            fig.update_layout(barmode='group', height=300)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Download Reports")

        # Inventory Report
        inventory_df = reports.get_inventory_report()
        inv_csv = reports.export_to_csv(inventory_df)
        inv_excel = reports.export_to_excel(inventory_df, "Inventory")

        st.download_button(
            "📥 Download Inventory (CSV)",
            inv_csv,
            "inventory_report.csv",
            "text/csv",
            use_container_width=True
        )
        st.download_button(
            "📥 Download Inventory (Excel)",
            inv_excel,
            "inventory_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

        # Sales Report
        sales_df = reports.get_sales_report()
        sales_csv = reports.export_to_csv(sales_df)

        st.download_button(
            "📥 Download Sales (CSV)",
            sales_csv,
            "sales_report.csv",
            "text/csv",
            use_container_width=True
        )

        # Expense Report
        expense_df = reports.get_expense_report()
        exp_csv = reports.export_to_csv(expense_df)

        st.download_button(
            "📥 Download Expenses (CSV)",
            exp_csv,
            "expenses_report.csv",
            "text/csv",
            use_container_width=True
        )

        # Comprehensive Report
        comprehensive = reports.get_comprehensive_report()
        st.download_button(
            "📥 Download Full Report (Excel)",
            comprehensive,
            "biztrack_full_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

def show_forecasting_page():
    """Display forecasting page"""
    st.title("🔮 Demand Forecasting")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Restock Recommendations")
        recommendations = forecasting.get_restock_recommendations()

        if not recommendations.empty:
            urgent = recommendations[recommendations['restock_needed'] == True]

            if not urgent.empty:
                urgent = urgent[['name', 'category', 'current_stock',
                               'predicted_demand_14d', 'recommended_order', 'order_cost']]
                urgent.columns = ['Product', 'Category', 'Current Stock',
                                 'Pred. Demand (14d)', 'Order Qty', 'Est. Cost ($)']

                st.dataframe(urgent, use_container_width=True, hide_index=True)

                total_order_cost = recommendations[recommendations['restock_needed'] == True]['order_cost'].sum()
                st.metric("Total Reorder Cost", utils.format_currency(total_order_cost))
            else:
                st.success("No urgent restocking needed!")

        st.subheader("Daily Demand Forecast")
        forecast_data = forecasting.get_demand_forecast_chart_data()
        if not forecast_data.empty:
            fig = px.bar(forecast_data, x='product', y='predicted_weekly',
                        labels={'product': 'Product', 'predicted_weekly': 'Predicted Weekly Demand'},
                        color='predicted_weekly', color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Stockout Risk Analysis")
        stockout_risk = forecasting.predict_stockout_risk()

        if not stockout_risk.empty:
            stockout_risk.columns = ['ID', 'Product', 'Category', 'Stock', 'Velocity', 'Days Left']
            st.dataframe(stockout_risk, use_container_width=True, hide_index=True)

            # Visualization
            fig = px.bar(stockout_risk.head(10), x='Product', y='Days Left',
                        color='Days Left', color_continuous_scale='RdYlGn')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Weekly Sales Pattern")
        weekly_trends = forecasting.get_seasonal_trends()
        if not weekly_trends.empty:
            fig = px.bar(weekly_trends, x='day_name', y='transaction_count',
                        labels={'day_name': 'Day', 'transaction_count': 'Transactions'},
                        color='transaction_count', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)

def show_insights_page():
    """Display AI insights page"""
    st.title("🤖 AI Business Insights")

    # Performance Score
    score_data = insights.get_performance_score()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3a5f, #2ecc71);
                    border-radius: 20px; padding: 30px; text-align: center; color: white;">
            <h2 style="margin: 0;">{score_data['score']:.0f}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">{score_data['rating']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Performance Breakdown")
        for detail in score_data['details']:
            st.markdown(f"- {detail}")

    st.markdown("---")

    # Insights Grid
    st.subheader("Smart Insights")
    generated_insights = insights.generate_insights()

    cols = st.columns(3)
    for i, insight in enumerate(generated_insights):
        with cols[i % 3]:
            bg_color = {
                'success': '#d4edda',
                'warning': '#fff3cd',
                'info': '#d1ecf1',
                'danger': '#f8d7da'
            }.get(insight['type'], '#f0f4f8')
            border_color = {
                'success': '#28a745',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'danger': '#dc3545'
            }.get(insight['type'], '#1e3a5f')

            st.markdown(f"""
            <div style="background: {bg_color}; border-left: 4px solid {border_color};
                        border-radius: 8px; padding: 15px; margin: 10px 0;">
                <h4 style="margin: 0 0 10px 0;">{insight['icon']} {insight['title']}</h4>
                <p style="margin: 0; font-size: 14px;">{insight['insight']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Restock Recommendations
    st.subheader("Restock Recommendations")
    restock_df = insights.get_restock_recommendations_insight()
    if not restock_df.empty:
        st.dataframe(restock_df, use_container_width=True, hide_index=True)
    else:
        st.success("All products are well stocked!")

def show_settings_page():
    """Display settings page"""
    st.title("⚙️ Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Profile Settings")
        user = st.session_state.user

        st.markdown(f"""
        **Name:** {user['name']}

        **Email:** {user['email']}

        **Role:** {user['role'].title()}
        """)

        st.markdown("### Change Password")
        with st.form("change_password_form"):
            old_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.form_submit_button("Change Password"):
                if new_password == confirm_password:
                    success, msg = auth.change_password(user['id'], old_password, new_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.error("Passwords do not match!")

    with col2:
        st.subheader("Appearance")
        dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        st.subheader("Data Management")
        if st.button("Generate Sample Data", type="primary"):
            if not st.session_state.sample_data_loaded:
                success, msg = sample_data.generate_sample_data()
                if success:
                    st.session_state.sample_data_loaded = True
                    st.success(msg)
                    st.rerun()
                else:
                    st.info(msg)
            else:
                st.info("Sample data already loaded!")

        if st.session_state.user['role'] == 'owner':
            if st.button("Clear All Data"):
                sample_data.clear_all_data()
                st.session_state.sample_data_loaded = False
                st.success("All data cleared!")
                st.rerun()

        st.subheader("Activity Logs")
        logs = database.get_activity_logs(10)
        if logs:
            for log in logs:
                timestamp, name, action, details = log
                st.markdown(f"- **{utils.format_date(timestamp)}** - {name}: {action} ({details or 'N/A'})")
        else:
            st.info("No activity logs yet")

def show_logout():
    """Handle logout"""
    st.session_state.user = None
    st.rerun()

def main():
    """Main application"""
    # Check authentication
    if not st.session_state.user:
        show_login_page()
        return

    # Sidebar
    with st.sidebar:
        st.markdown(utils.get_sidebar_navigation(), unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Inventory", "Sales", "Expenses", "Reports", "Forecasting", "AI Insights", "Settings"],
            icons=["speedometer2", "box-seam", "credit-card", "cash-stack", "file-earmark-bar-graph", "graph-up-arrow", "robot", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#1e3a5f"},
                "icon": {"color": "#fff", "font-size": "18px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "5px", "--hover-color": "#2d4a6f"},
                "nav-link-selected": {"background-color": "#2ecc71", "color": "white"},
            }
        )

        st.markdown("---")

        # User info
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(255,255,255,0.1);
                    border-radius: 8px; margin-top: 20px;">
            <p style="color: white; margin: 0; font-weight: 600;">{st.session_state.user['name']}</p>
            <p style="color: #a0aec0; margin: 5px 0 0 0; font-size: 12px;">{st.session_state.user['role'].title()}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            show_logout()

    # Page routing
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Inventory":
        show_inventory_page()
    elif selected == "Sales":
        show_sales_page()
    elif selected == "Expenses":
        show_expenses_page()
    elif selected == "Reports":
        show_reports_page()
    elif selected == "Forecasting":
        show_forecasting_page()
    elif selected == "AI Insights":
        show_insights_page()
    elif selected == "Settings":
        show_settings_page()

if __name__ == "__main__":
    main()
