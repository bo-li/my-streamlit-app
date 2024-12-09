import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
import pandas as pd
import io
import base64
import plotly.express as px
from streamlit_plotly_events import plotly_events

df = pd.read_csv('./all_2_ener.csv')

# Function to convert SMILES to base64-encoded PNG
def smiles_to_base64(smiles, size=(200, 200)):
    mol = Chem.MolFromSmiles(smiles)
    img = Draw.MolToImage(mol, size=size)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Add the image column
df['ImageBase64'] = df['SMILES-carbanions'].apply(smiles_to_base64)

# Create a scatter plot with Plotly
fig = px.scatter(df, x='dE_COO', y='dE_COOH', hover_data=['Index'])
fig.update_layout(
        xaxis_title="dE_COO(kcal/mol)",
        yaxis_title="dE_COOH(kcal/mol)",
        title='Click on a point to see the molecule',
        )

x_min=min(df['dE_COO'].min(), df['dE_COOH'].min())
x_max=max(df['dE_COO'].max(), df['dE_COOH'].max())
fig.add_shape(type="line", x0=x_min, y0=x_min, x1=x_max, y1=x_max,
        line=dict(color="red", width=2, dash="dash"))

st.title("Molecule Visualization App")

# Use plotly_events to capture clicks
selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    key="plot"
)

st.write("Click on a point above to display the corresponding molecule structure:")

# If a point is clicked, display the corresponding molecule
if selected_points:
    clicked_point = selected_points[0]
    idx = clicked_point['pointIndex']
    img_data = df.iloc[idx]['ImageBase64']
    st.image(base64.b64decode(img_data), caption=df.iloc[idx]['SMILES-carbanions'])
