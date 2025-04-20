import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# Set page configuration and styling
st.set_page_config(
    page_title="Medical Lab Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #000080;
        color: white;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #000066 !important;
        color: white !important;
        font-weight: 600;
    }
    h1 {
        color: #2c3e50;
        padding-bottom: 20px;
    }
    h2 {
        color: #34495e;
        padding: 10px 0;
    }
    h3 {
        color: #2980b9;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_statistics(data):
    stats = {
        'Total Patients': len(data),
        'Average Haemoglobin': round(data['HAEMOGLOBIN'].mean(), 2),
        'Average Platelet Count': round(data['PLATELET COUNT'].mean(), 2),
        'Critical Cases (Hb ≤ 8 & PLT ≤ 50)': len(data[(data['HAEMOGLOBIN'] <= 8) & (data['PLATELET COUNT'] <= 50)])
    }
    return stats

def segregate_data(data):
    conditions = {
        'Low Haemoglobin (≤8)': data['HAEMOGLOBIN'] <= 8,
        'High Haemoglobin (>8)': data['HAEMOGLOBIN'] > 8,
        'Low Platelet Count (≤50)': data['PLATELET COUNT'] <= 50,
        'High Platelet Count (>50)': data['PLATELET COUNT'] > 50
    }
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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2c3e50;">Total Patients</h4>
            <h2 style="color: #4c78a8;">{stats['Total Patients']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2c3e50;">Avg. Haemoglobin</h4>
            <h2 style="color: #4c78a8;">{stats['Average Haemoglobin']} g/dL</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2c3e50;">Avg. Platelet Count</h4>
            <h2 style="color: #4c78a8;">{stats['Average Platelet Count']} ×10³/µL</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2c3e50;">Critical Cases</h4>
            <h2 style="color: #e15759;">{stats['Critical Cases (Hb ≤ 8 & PLT ≤ 50)']}</h2>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.title("🏥 Medical Laboratory Analytics Dashboard")
    
    uploaded_file = st.file_uploader("Upload Patient Data (Excel Format)", type="xlsx")

    if uploaded_file:
        data = pd.read_excel(uploaded_file, sheet_name='ag-grid')
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
            
        with tab2:
            st.subheader("Detailed Patient Groups")
            for condition, group in segregated_data.items():
                with st.expander(f"{condition} - {len(group)} patients"):
                    st.dataframe(
                        group[['REGNO', 'PATIENTNAME', 'HAEMOGLOBIN', 'PLATELET COUNT']]
                        .style.background_gradient(cmap='Blues', subset=['HAEMOGLOBIN', 'PLATELET COUNT'])
                        .format({'HAEMOGLOBIN': '{:.1f}', 'PLATELET COUNT': '{:.0f}'})
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