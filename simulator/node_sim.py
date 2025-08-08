import asyncio
import json
import random
import time
import redis.asyncio as redis

# Redis settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379
STREAM_KEY = "hpc:telemetry"

# Simulated HPC nodes
NODE_COUNT = 10
SLEEP_INTERVAL = 1  # seconds between readings

# Function to generate fake HPC telemetry
def generate_telemetry(node_id):
    return {
        "node_id": f"node-{node_id}",
        "timestamp": time.time(),
        "cpu_usage": round(random.uniform(10, 95), 2),
        "memory_usage": round(random.uniform(1000, 64000), 2),  # in MB
        "temperature": round(random.uniform(30, 90), 2),        # Celsius
        "net_io": round(random.uniform(10, 1000), 2)            # MB/s
    }

async def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")

    try:
        while True:
            tasks = []
            for node_id in range(1, NODE_COUNT + 1):
                telemetry = generate_telemetry(node_id)
                tasks.append(
                    r.xadd(STREAM_KEY, telemetry)
                )
            await asyncio.gather(*tasks)
            print(f"Published telemetry for {NODE_COUNT} nodes.")
            await asyncio.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        await r.close()

if __name__ == "__main__":
    asyncio.run(main())
