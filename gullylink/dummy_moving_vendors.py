import asyncio
import websockets
import json
import random

# Gwalior City Centre Coordinates
BASE_LAT = 26.2037
BASE_LNG = 78.1574

async def simulate_vendor(vendor_id, name, icon):
    uri = f"ws://localhost:8000/ws/vendor/{vendor_id}"
    
    # Random start position near City Centre
    lat = BASE_LAT + random.uniform(-0.005, 0.005)
    lng = BASE_LNG + random.uniform(-0.005, 0.005)

    print(f"🚀 {name} ({vendor_id}) started at {lat}, {lng}")

    async with websockets.connect(uri) as websocket:
        # 1. Initialize Vendor Profile (Send once)
        # In a real app, this happens via REST API, but for dummy we just start broadcasting
        
        while True:
            # 2. Move slightly (Random Walk)
            lat += random.uniform(-0.0001, 0.0001) # Move approx 10 meters
            lng += random.uniform(-0.0001, 0.0001)
            
            payload = {
                "type": "location_update",
                "vendor_id": vendor_id,
                "icon": icon, # "veg" or "food"
                "location": {"lat": lat, "lng": lng}
            }
            
            await websocket.send(json.dumps(payload))
            print(f"📡 {name} moved to {lat:.4f}, {lng:.4f}")
            
            # Wait 2 seconds before next move
            await asyncio.sleep(2)

async def main():
    # Run 3 vendors simultaneously
    await asyncio.gather(
        simulate_vendor("v_bot_1", "Raju Veggies", "veg"),
        simulate_vendor("v_bot_2", "Mohan Fruits", "veg"),
        simulate_vendor("v_bot_3", "Gully Green", "veg")
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopped Moving Vendors")
