import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from datetime import datetime, timedelta

# Инициализация приложения
app = dash.Dash(__name__)
server = app.server
