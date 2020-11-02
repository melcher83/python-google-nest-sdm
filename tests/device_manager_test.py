from google_nest_sdm_jm.device import Device
from google_nest_sdm_jm.device_manager import DeviceManager
from google_nest_sdm_jm.event import EventCallback, EventMessage
from google_nest_sdm_jm.structure import Structure


def MakeDevice(raw_data: dict) -> Device:
    return Device.MakeDevice(raw_data, auth=None)


def MakeStructure(raw_data: dict) -> Device:
    return Structure.MakeStructure(raw_data)


def MakeEvent(raw_data: dict) -> EventMessage:
    return EventMessage(raw_data, auth=None)


def test_add_device():
    mgr = DeviceManager()
    mgr.add_device(
        MakeDevice(
            {
                "name": "my/device/name1",
                "type": "sdm.devices.types.SomeDeviceType",
            }
        )
    )
    assert 1 == len(mgr.devices)
    mgr.add_device(
        MakeDevice(
            {
                "name": "my/device/name2",
                "type": "sdm.devices.types.SomeDeviceType",
            }
        )
    )
    assert 2 == len(mgr.devices)


def test_duplicate_device():
    mgr = DeviceManager()
    mgr.add_device(
        MakeDevice(
            {
                "name": "my/device/name1",
                "type": "sdm.devices.types.SomeDeviceType",
            }
        )
    )
    assert 1 == len(mgr.devices)
    mgr.add_device(
        MakeDevice(
            {
                "name": "my/device/name1",
                "type": "sdm.devices.types.SomeDeviceType",
            }
        )
    )
    assert 1 == len(mgr.devices)


def test_update_traits():
    mgr = DeviceManager()
    mgr.add_device(
        MakeDevice(
            {
                "name": "my/device/name1",
                "type": "sdm.devices.types.SomeDeviceType",
                "traits": {
                    "sdm.devices.traits.Connectivity": {
                        "status": "OFFLINE",
                    },
                },
            }
        )
    )
    assert 1 == len(mgr.devices)
    device = mgr.devices["my/device/name1"]
    assert "sdm.devices.traits.Connectivity" in device.traits
    trait = device.traits["sdm.devices.traits.Connectivity"]
    assert "OFFLINE" == trait.status
    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "resourceUpdate": {
                    "name": "my/device/name1",
                    "traits": {
                        "sdm.devices.traits.Connectivity": {
                            "status": "ONLINE",
                        }
                    },
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    device = mgr.devices["my/device/name1"]
    assert "sdm.devices.traits.Connectivity" in device.traits
    trait = device.traits["sdm.devices.traits.Connectivity"]
    assert "ONLINE" == trait.status


def test_device_created_in_structure():
    mgr = DeviceManager()
    mgr.add_device(
        MakeDevice(
            {
                "name": "enterprises/project-id/devices/device-id",
                "type": "sdm.devices.types.SomeDeviceType",
                "parentRelations": [],
            }
        )
    )
    assert 1 == len(mgr.devices)
    device = mgr.devices["enterprises/project-id/devices/device-id"]
    assert 0 == len(device.parent_relations)

    mgr.add_structure(
        MakeStructure(
            {
                "name": "enterprises/project-id/structures/structure-id",
                "traits": {
                    "sdm.structures.traits.Info": {
                        "customName": "Structure Name",
                    },
                },
            }
        )
    )
    assert 1 == len(mgr.structures)
    structure = mgr.structures["enterprises/project-id/structures/structure-id"]
    assert "sdm.structures.traits.Info" in structure.traits
    trait = structure.traits["sdm.structures.traits.Info"]
    assert "Structure Name" == trait.custom_name

    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "relationUpdate": {
                    "type": "CREATED",
                    "subject": "enterprises/project-id/structures/structure-id",
                    "object": "enterprises/project-id/devices/device-id",
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    device = mgr.devices["enterprises/project-id/devices/device-id"]
    assert {
        "enterprises/project-id/structures/structure-id": "Structure Name",
    } == device.parent_relations

    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "relationUpdate": {
                    "type": "DELETED",
                    "subject": "enterprises/project-id/structures/structure-id",
                    "object": "enterprises/project-id/devices/device-id",
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    device = mgr.devices["enterprises/project-id/devices/device-id"]
    assert 0 == len(device.parent_relations)


def test_device_event_callback():
    device = MakeDevice(
        {
            "name": "my/device/name1",
            "type": "sdm.devices.types.SomeDeviceType",
            "traits": {
                "sdm.devices.traits.Connectivity": {
                    "status": "OFFLINE",
                },
            },
        }
    )
    mgr = DeviceManager()
    mgr.add_device(device)
    assert 1 == len(mgr.devices)
    device = mgr.devices["my/device/name1"]
    assert "sdm.devices.traits.Connectivity" in device.traits
    trait = device.traits["sdm.devices.traits.Connectivity"]
    assert "OFFLINE" == trait.status

    class MyCallback(EventCallback):
        invoked = False

        def handle_event(self, event_message: EventMessage):
            self.invoked = True

    callback = MyCallback()
    unregister = device.add_event_callback(callback)
    assert not callback.invoked

    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "resourceUpdate": {
                    "name": "my/device/name1",
                    "traits": {
                        "sdm.devices.traits.Connectivity": {
                            "status": "ONLINE",
                        }
                    },
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    device = mgr.devices["my/device/name1"]
    assert "sdm.devices.traits.Connectivity" in device.traits
    trait = device.traits["sdm.devices.traits.Connectivity"]
    assert "ONLINE" == trait.status
    assert callback.invoked

    # Test event not for this device
    callback.invoked = False
    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "resourceUpdate": {
                    "name": "some-device-id",
                    "traits": {
                        "sdm.devices.traits.Connectivity": {
                            "status": "ONLINE",
                        }
                    },
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    assert not callback.invoked

    # Unregister the callback.  The event is still processed, but the callback
    # is not invoked
    unregister()
    mgr.handle_event(
        MakeEvent(
            {
                "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
                "timestamp": "2019-01-01T00:00:01Z",
                "resourceUpdate": {
                    "name": "my/device/name1",
                    "traits": {
                        "sdm.devices.traits.Connectivity": {
                            "status": "OFFLINE",
                        }
                    },
                },
                "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
            }
        )
    )
    device = mgr.devices["my/device/name1"]
    assert "sdm.devices.traits.Connectivity" in device.traits
    trait = device.traits["sdm.devices.traits.Connectivity"]
    assert "OFFLINE" == trait.status
    assert not callback.invoked
