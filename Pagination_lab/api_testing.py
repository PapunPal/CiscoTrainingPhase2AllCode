
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Devices API Testing Lab")

# Temporary storage
devices = []
next_id = 1


# Device request model
class Device(BaseModel):
    name: str
    device_type: str
    brand: str
    status: str


# Home endpoint
@app.get("/")
def home():
    return {"message": "Devices API is running"}


# CREATE DEVICE
@app.post("/devices", status_code=201)
def create_device(device: Device):
    global next_id

    new_device = {
        "id": next_id,
        "name": device.name,
        "device_type": device.device_type,
        "brand": device.brand,
        "status": device.status
    }

    devices.append(new_device)
    next_id += 1

    return new_device


# GET ALL DEVICES
@app.get("/devices")
def get_devices():
    return devices


# GET DEVICE BY ID
@app.get("/devices/{device_id}")
def get_device(device_id: int):

    for device in devices:
        if device["id"] == device_id:
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# UPDATE DEVICE
@app.put("/devices/{device_id}")
def update_device(device_id: int, updated_device: Device):

    for device in devices:
        if device["id"] == device_id:

            device["name"] = updated_device.name
            device["device_type"] = updated_device.device_type
            device["brand"] = updated_device.brand
            device["status"] = updated_device.status

            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


# DELETE DEVICE
@app.delete("/devices/{device_id}")
def delete_device(device_id: int):

    for index, device in enumerate(devices):
        if device["id"] == device_id:

            deleted_device = devices.pop(index)

            return {
                "message": "Device deleted successfully",
                "device": deleted_device
            }

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )