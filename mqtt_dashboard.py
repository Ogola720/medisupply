import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import paho.mqtt.client as mqtt
import json
from collections import deque
import threading
import datetime
import traceback

# --- Thread-safe shared state ---
state_lock = threading.Lock()
dispatched = 0
received = 0
last_event = "None"
event_time = "N/A"
temperature_data = deque(maxlen=50)
humidity_data = deque(maxlen=50)
time_data = deque(maxlen=50)
log_buffer = deque(maxlen=50)

# --- MQTT Configuration ---
broker = "broker.hivemq.com"
topics = [
    ("medical/supply/event", 0),
    ("medical/supply/monitor", 0),
    ("medical/supply/summary", 0),
]

def log(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with state_lock:
        log_buffer.appendleft(entry)

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    log(f"✅ MQTT connected (rc={rc})")
    client.subscribe(topics)

def on_message(client, userdata, msg):
    global dispatched, received, last_event, event_time
    payload = msg.payload.decode()
    topic = msg.topic

    log(f"📨 Topic: {topic} | Payload: {payload}")

    try:
        data = json.loads(payload)

        with state_lock:
            if topic == "medical/supply/event":
                if data.get("event") == "arrival":
                    received += 1
                    last_event = "Item Received"
                elif data.get("event") == "dispatch":
                    dispatched += 1
                    last_event = "Item Dispatched"
                event_time = datetime.datetime.now().strftime("%H:%M:%S")

            elif topic == "medical/supply/summary":
                received = data.get("summary", {}).get("received", received)
                dispatched = data.get("summary", {}).get("dispatched", dispatched)

            elif topic == "medical/supply/monitor":
                temp = data.get("temperature")
                hum = data.get("humidity")
                if temp is not None and hum is not None:
                    temperature_data.append(temp)
                    humidity_data.append(hum)
                    time_data.append(datetime.datetime.now().strftime("%H:%M:%S"))
    except Exception as e:
        log(f"⚠️ Error in on_message: {e}")
        log(traceback.format_exc())

# --- MQTT Background Thread ---
def mqtt_thread():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker, 1883, 60)
        client.loop_forever()
    except Exception as e:
        log(f"❌ MQTT Error: {e}")
        log(traceback.format_exc())

threading.Thread(target=mqtt_thread, daemon=True).start()

# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.title = "Medical Supply Dashboard"

app.layout = dbc.Container([
    html.H2("📦 Medical Supply Dashboard", className="text-center my-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            html.H5("🟢 Last Event", className="card-title"),
            html.H4(id="event-status", className="text-primary"),
            html.P(id="event-time", className="text-muted mb-0")
        ], body=True, color="light"), md=4),

        dbc.Col(dbc.Card([
            html.H5("📥 Received", className="card-title text-success"),
            html.H2(id="received-counter", className="display-5")
        ], body=True, color="light"), md=4),

        dbc.Col(dbc.Card([
            html.H5("📤 Dispatched", className="card-title text-danger"),
            html.H2(id="dispatched-counter", className="display-5")
        ], body=True, color="light"), md=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            html.H5("📊 Stock Status", className="card-title"),
            html.Div(id="stock-status", className="mt-2")
        ], body=True, color="light"), md=6),

        dbc.Col(dbc.Card([
            html.H5("🧾 Debug Logs", className="card-title"),
            html.Pre(id="debug-logs", style={"height": "200px", "overflowY": "auto", "fontSize": "0.85rem"})
        ], body=True, color="dark", inverse=True), md=6)
    ], className="mb-4"),

    dbc.Card([
        dbc.CardHeader("📈 Environmental Monitoring"),
        dbc.CardBody(dcc.Graph(id="temp-humidity-chart"))
    ]),

    dcc.Interval(id="interval-update", interval=2000, n_intervals=0)
], fluid=True)

@app.callback(
    Output("received-counter", "children"),
    Output("dispatched-counter", "children"),
    Output("stock-status", "children"),
    Output("temp-humidity-chart", "figure"),
    Output("debug-logs", "children"),
    Output("event-status", "children"),
    Output("event-time", "children"),
    Input("interval-update", "n_intervals")
)
def update_dashboard(n):
    with state_lock:
        rec = received
        disp = dispatched
        logs = list(log_buffer)
        event = last_event
        timestamp = event_time
        temp = list(temperature_data)
        hum = list(humidity_data)
        times = list(time_data)

    stock_level = rec - disp
    badge_color = "success" if stock_level > 0 else "danger"
    badge = dbc.Badge(f"Available: {stock_level}", color=badge_color, className="p-2")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=temp, mode='lines+markers', name='Temp (°C)', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=times, y=hum, mode='lines+markers', name='Humidity (%)', line=dict(color='blue')))
    fig.update_layout(
        title="Real-Time Environment Data",
        xaxis_title="Time",
        yaxis_title="Value",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return str(rec), str(disp), badge, fig, "\n".join(logs), event, f"Last update: {timestamp}"

if __name__ == "__main__":
    app.run(debug=True)
