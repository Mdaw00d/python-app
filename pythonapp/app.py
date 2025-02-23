import streamlit as st
import pandas as pd
import os
from io import BytesIO
from sqlalchemy import create_engine
from fpdf import FPDF
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Transify", layout="wide", page_icon="🚀")

# Custom CSS for a modern and vibrant look
st.markdown(
    """
    <style>
        .main {
            background-color: #f0f4f8;
        }
        .block-container {
            padding: 3rem 2rem;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f77b4;
        }
        .stButton>button {
            border: none;
            border-radius: 8px;
            background-color: #ff7f0e;
            color: white;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .stButton>button:hover {
            background-color: #e6550d;
            cursor: pointer;
        }
        .stDownloadButton>button {
            background-color: #2ca02c;
            color: white;
        }
        .stDownloadButton>button:hover {
            background-color: #1f7a1f;
        }
        .stDataFrame, .stTable {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #ccc;
        }
        .stSelectbox>label, .stCheckbox>label {
            font-weight: bold;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the main app title and introductory text
st.title("Transify")
st.write("Easily convert, clean, and visualize your files with Transify.")

# File uploader - Allow all file types
uploaded_files = st.file_uploader("📁 Drag and Drop or Select Files:", type=None, accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        # Read file
        try:
            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(file)
            elif file_extension == ".json":
                df = pd.read_json(file)
            elif file_extension == ".xml":
                tree = ET.parse(file)
                root = tree.getroot()
                data = [{elem.tag: elem.text for elem in item} for item in root]
                df = pd.DataFrame(data)
            elif file_extension == ".sql":
                st.warning("SQL file reading is not supported. Please use the conversion feature.")
                continue
            elif file_extension == ".pdf":
                reader = PdfReader(file)
                text = "\n".join([page.extract_text() for page in reader.pages])
                df = pd.DataFrame({"PDF_Text": text.splitlines()})
            else:
                st.error(f"Unsupported file type: {file_extension}")
                continue
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
            continue

        # File info
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")

        # Preview data
        st.header("👀 Quick Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.header("🧹 Tidy Up Your Data")
        if st.checkbox(f"Enable Cleaning for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❌ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates successfully removed!")
            with col2:
                if st.button(f"🔄 Fill Missing Data in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled with column averages!")

        # Column Selection
        st.header("🎯 Focus on Key Columns")
        columns = st.multiselect(f"Pick Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.header("📈 Explore Your Data")
        if st.checkbox(f"Visualize {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.header("🔄 Convert & Download")
        conversion_type = st.selectbox(f"Choose Format for {file.name}:", ["CSV", "Excel", "JSON", "XML", "PDF", "SQL"], key=file.name)
        if st.button(f"💾 Save {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "JSON":
                df.to_json(buffer, orient='records', lines=True)
                file_name = file.name.replace(file_extension, ".json")
                mime_type = "application/json"
            elif conversion_type == "XML":
                root = ET.Element("root")
                for _, row in df.iterrows():
                    item = ET.SubElement(root, "item")
                    for col in df.columns:
                        child = ET.SubElement(item, col)
                        child.text = str(row[col])
                tree = ET.ElementTree(root)
                tree.write(buffer, encoding='utf-8', xml_declaration=True)
                file_name = file.name.replace(file_extension, ".xml")
                mime_type = "application/xml"
            elif conversion_type == "PDF":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for i, row in df.iterrows():
                    line = ', '.join([str(item) for item in row])
                    pdf.cell(200, 10, txt=line, ln=1, align='L')
                pdf.output(buffer)
                file_name = file.name.replace(file_extension, ".pdf")
                mime_type = "application/pdf"
            elif conversion_type == "SQL":
                engine = create_engine('sqlite://', echo=False)
                df.to_sql('table', con=engine, index=False)
                sql_script = "".join(engine.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchone())
                buffer.write(sql_script.encode())
                file_name = file.name.replace(file_extension, ".sql")
                mime_type = "application/sql"
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files have been successfully processed!")
