import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# Set page configuration and styling
st.set_page_config(
    page_title="Medical Lab Analytics",
    page_icon="med.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #18191a !important;
        color: #f8f9fa !important;
        font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
    }
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #22232a;
        color: #f8f9fa;
        font-weight: 500;
        border-radius: 12px 12px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #18191a !important;
        color: #fff !important;
        font-weight: 600;
    }
    h1, h2, h3, h4 {
        color: #f8f9fa;
        font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
    }
    h1 {
        font-size: 2.2rem;
        font-weight: 700;
        padding-bottom: 20px;
    }
    h2 {
        font-size: 1.5rem;
        font-weight: 600;
        padding: 10px 0;
    }
    h3 {
        color: #a0a0a0;
        font-size: 1.2rem;
    }
    .metric-card {
        background-color: #23242a;
        padding: 20px;
        border-radius: 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        margin: 18px 10px 18px 10px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        word-break: break-word;
        overflow: hidden;
        text-align: center;
        border: 1.5px solid #23242a;
        transition: border 0.2s;
    }
    .metric-card:hover {
        border: 1.5px solid #4c78a8;
    }
    .metric-card h2 {
        font-size: 1.5rem;
        margin: 0.5rem 0 0 0;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .metric-card h4 {
        font-size: 0.95rem;
        margin: 0 0 0.5rem 0;
        color: #b0b0b0;
        font-weight: 500;
    }
    .metric-card .accent {
        color: #ff2d55;
    }
    .metric-card .blue {
        color: #32aaff;
    }
    .metric-card .green {
        color: #30d158;
    }
    .metric-card .yellow {
        color: #ffd60a;
    }
    .metric-card .red {
        color: #ff453a;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_statistics(data):
    stats = {
        'Total Patients': len(data),
        'Average Haemoglobin': round(data['HAEMOGLOBIN'].mean(), 2),
        'Average Platelet Count': round(data['PLATELET COUNT'].mean(), 2),
        'Average INR': round(data['INR'].mean(), 2) if 'INR' in data.columns else 'N/A',
        'Average TLC': round(data['TLC'].mean(), 2) if 'TLC' in data.columns else 'N/A',
        'Critical Cases (Hb ≤ 8 & PLT ≤ 50 & INR ≥ 1.5 & TLC ≥ 11000)': len(
            data[
                (data['HAEMOGLOBIN'] <= 8) &
                (data['PLATELET COUNT'] <= 50) &
                (data['INR'] >= 1.5 if 'INR' in data.columns else False) &
                (data['TLC'] >= 11000 if 'TLC' in data.columns else False)
            ]
        ) if ('INR' in data.columns and 'TLC' in data.columns) else 'N/A'
    }
    return stats

def segregate_data(data):
    conditions = {
        'Low Haemoglobin (≤8)': data['HAEMOGLOBIN'] <= 8,
        'High Haemoglobin (>8)': data['HAEMOGLOBIN'] > 8,
        'Low Platelet Count (≤50)': data['PLATELET COUNT'] <= 50,
        'High Platelet Count (>50)': data['PLATELET COUNT'] > 50
    }
    if 'INR' in data.columns:
        conditions['Low INR (≤1.5)'] = data['INR'] <= 1.5
        conditions['High INR (>1.5)'] = data['INR'] > 1.5
    if 'TLC' in data.columns:
        conditions['Low TLC (≤11000)'] = data['TLC'] <= 11000
        conditions['High TLC (>11000)'] = data['TLC'] > 11000
    return {condition: data[mask] for condition, mask in conditions.items()}

def plot_patient_groups(segregated_data):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    # Medical-appropriate color palette
    colors = ['#4c78a8', '#73c2fb', '#e15759', '#76b7b2']
    
    conditions = [
        ('Low Haemoglobin (≤8)', 'Haemoglobin ≤ 8'),
        ('High Haemoglobin (>8)', 'Haemoglobin > 8'),
        ('Low Platelet Count (≤50)', 'Platelet Count ≤ 50'),
        ('High Platelet Count (>50)', 'Platelet Count > 50')
    ]

    for ax, (condition, title), color in zip(axes, conditions, colors):
        group_data = segregated_data[condition]
        sns.scatterplot(
            x='HAEMOGLOBIN', y='PLATELET COUNT', data=group_data,
            ax=ax, color=color, alpha=0.6, s=100
        )
        ax.set_title(title, fontsize=12, pad=15)
        ax.set_xlabel('Haemoglobin (g/dL)', fontsize=10)
        ax.set_ylabel('Platelet Count (×10³/µL)', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig

def display_metrics(stats):
    st.markdown("""<div style='padding-top: 1.5rem;'></div>""", unsafe_allow_html=True)
    st.markdown("""<h2 style='margin-bottom: 0.5rem;'>Summary</h2>""", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Activity Ring (Move) - use Haemoglobin as example
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Total Patients</h4>
            <h2 class="accent">{stats['Total Patients']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. Haemoglobin</h4>
            <h2 class="blue">{stats['Average Haemoglobin']} g/dL</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. Platelet Count</h4>
            <h2 class="yellow">{stats['Average Platelet Count']} ×10³/µL</h2>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. INR</h4>
            <h2 class="green">{stats['Average INR']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. TLC</h4>
            <h2 class="blue">{stats['Average TLC']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Critical Cases</h4>
            <h2 class="red">{stats['Critical Cases (Hb ≤ 8 & PLT ≤ 50 & INR ≥ 1.5 & TLC ≥ 11000)']}</h2>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""<div style='padding-bottom: 1.5rem;'></div>""", unsafe_allow_html=True)

def main():
    # Header with logo and title
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image("med.png", width=80)
    with col_title:
        st.markdown("<h1 style='padding-top: 0.2em; padding-bottom: 0.2em;'>Medical Laboratory Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Patient Data (Excel or CSV Format)", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file, sheet_name='ag-grid')
        elif uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload an Excel (.xlsx) or CSV (.csv) file.")
            return

        # Normalize column names
        data.columns = [col.strip().upper().replace('_', ' ').replace('  ', ' ') for col in data.columns]

        # Map common variants to standard names
        col_map = {}
        for col in data.columns:
            if col in ['PLATELET COUNT', 'PLATELETS COUNT', 'PLATELETCOUNT', 'PLATELETS']:
                col_map[col] = 'PLATELET COUNT'
            if col in ['HAEMOGLOBIN', 'HEMOGLOBIN']:
                col_map[col] = 'HAEMOGLOBIN'
            if col in ['INR']:
                col_map[col] = 'INR'
            if col in ['TLC', 'TOTAL LEUCOCYTE COUNT', 'TOTAL LEUKOCYTE COUNT']:
                col_map[col] = 'TLC'
            if col in ['REGNO', 'REG NO', 'REGISTRATION NO', 'REGISTRATION NUMBER']:
                col_map[col] = 'REGNO'
            if col in ['PATIENTNAME', 'PATIENT NAME', 'NAME']:
                col_map[col] = 'PATIENTNAME'
        data = data.rename(columns=col_map)

        # Check for required columns
        required = ['HAEMOGLOBIN', 'PLATELET COUNT']
        missing = [col for col in required if col not in data.columns]
        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}. Please check your file.")
            return

        segregated_data = segregate_data(data)
        stats = calculate_statistics(data)

        # Display key metrics
        display_metrics(stats)
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Visualization", "📋 Patient Groups", "📥 Export Data"])
        
        with tab1:
            st.subheader("Patient Distribution Analysis")
            fig = plot_patient_groups(segregated_data)
            st.pyplot(fig)

            # Additional Visualizations
            st.subheader("Distributions & Relationships")
            metrics = ['HAEMOGLOBIN', 'PLATELET COUNT']
            if 'INR' in data.columns:
                metrics.append('INR')
            if 'TLC' in data.columns:
                metrics.append('TLC')

            # Histograms
            st.markdown("**Histograms**")
            fig_hist, axes_hist = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 4))
            if len(metrics) == 1:
                axes_hist = [axes_hist]
            for i, col in enumerate(metrics):
                axes_hist[i].hist(data[col].dropna(), bins=30, color='#4c78a8', alpha=0.7)
                axes_hist[i].set_title(f"{col} Distribution")
                axes_hist[i].set_xlabel(col)
                axes_hist[i].set_ylabel('Count')
            plt.tight_layout()
            st.pyplot(fig_hist)

            # Boxplots
            st.markdown("**Boxplots**")
            fig_box, axes_box = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 4))
            if len(metrics) == 1:
                axes_box = [axes_box]
            for i, col in enumerate(metrics):
                axes_box[i].boxplot(data[col].dropna(), vert=True, patch_artist=True, boxprops=dict(facecolor='#73c2fb'))
                axes_box[i].set_title(f"{col} Boxplot")
                axes_box[i].set_ylabel(col)
            plt.tight_layout()
            st.pyplot(fig_box)

            # Pie Chart for Patient Groups
            st.markdown("**Patient Group Proportions**")
            group_labels = list(segregated_data.keys())
            group_sizes = [len(group) for group in segregated_data.values()]
            pastel_colors = [
                '#a3c9f9', '#f9a3a3', '#f9e6a3', '#a3f9c9', '#d1a3f9', '#f9c9a3', '#a3f9f3', '#f3a3f9', '#c9f9a3', '#f9a3e6'
            ]
            fig_pie, ax_pie = plt.subplots(figsize=(7, 7))
            wedges, texts, autotexts = ax_pie.pie(
                group_sizes,
                labels=None,
                autopct='%1.1f%%',
                startangle=140,
                colors=pastel_colors[:len(group_labels)],
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
            )
            # Style percentage labels
            plt.setp(autotexts, size=16, weight='bold', color='black')
            # Draw legend outside
            ax_pie.legend(wedges, group_labels, title="Groups", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12)
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
            
        with tab2:
            st.subheader("Detailed Patient Groups")
            for condition, group in segregated_data.items():
                with st.expander(f"{condition} - {len(group)} patients"):
                    display_cols = ['REGNO', 'PATIENTNAME', 'HAEMOGLOBIN', 'PLATELET COUNT']
                    if 'INR' in group.columns:
                        display_cols.append('INR')
                    if 'TLC' in group.columns:
                        display_cols.append('TLC')
                    st.dataframe(
                        group[display_cols]
                        .style.background_gradient(cmap='Blues', subset=[col for col in ['HAEMOGLOBIN', 'PLATELET COUNT', 'INR', 'TLC'] if col in group.columns])
                        .format({k: '{:.1f}' if k != 'PLATELET COUNT' and k != 'TLC' else '{:.0f}' for k in display_cols if k in ['HAEMOGLOBIN', 'INR', 'TLC']} | {'PLATELET COUNT': '{:.0f}'})
                    )
        
        with tab3:
            st.subheader("Export Results")
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for condition, group in segregated_data.items():
                    group.to_excel(writer, sheet_name=condition[:31], index=False)
            output.seek(0)
            
            st.download_button(
                label="📥 Download Complete Analysis (Excel)",
                data=output,
                file_name="patient_analysis_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Developed by <a href="https://github.com/Rktim" target="_blank">Raktim Kalita</a> | Version 2.0</p>
</div>
""", unsafe_allow_html=True)