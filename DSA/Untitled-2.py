import time
import requests

def evaluate_agent_navigation(agent_url, query):
    start = time.time()
    # Find closest intent
    response = requests.post(agent_url, json={"input": query})
    latency = time.time() - start
    # Compute steering to next dialogue point
    return response.json(), latency

# Simulation loop for multi-turn tracking
for i in range(10):
    res, lat = evaluate_agent_navigation("https://api.agent.ai/v1", "Track context")
    print(f"Latency: {lat}s | Path: {res['status']}")