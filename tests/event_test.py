import datetime

from google_nest_sdm_jm.event import EventMessage


def MakeEvent(raw_data: dict) -> EventMessage:
    return EventMessage(raw_data, auth=None)


def test_camera_sound_event():
    event = MakeEvent(
        {
            "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
            "timestamp": "2019-01-01T00:00:01Z",
            "resourceUpdate": {
                "name": "enterprises/project-id/devices/device-id",
                "events": {
                    "sdm.devices.events.CameraSound.Sound": {
                        "eventSessionId": "CjY5Y3VKaTZwR3o4Y19YbTVfMF...",
                        "eventId": "FWWVQVUdGNUlTU2V4MGV2aTNXV...",
                    }
                },
            },
            "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
        }
    )
    assert "0120ecc7-3b57-4eb4-9941-91609f189fb4" == event.event_id
    ts = datetime.datetime(2019, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)

    assert ts == event.timestamp
    assert "enterprises/project-id/devices/device-id" == event.resource_update_name
    events = event.resource_update_events
    assert "sdm.devices.events.CameraSound.Sound" in events
    e = events["sdm.devices.events.CameraSound.Sound"]
    assert "FWWVQVUdGNUlTU2V4MGV2aTNXV..." == e.event_id
    assert "CjY5Y3VKaTZwR3o4Y19YbTVfMF..." == e.event_session_id
    assert ts == e.timestamp
    expire_ts = datetime.datetime(2019, 1, 1, 0, 0, 31, tzinfo=datetime.timezone.utc)
    assert expire_ts == e.expires_at


def test_camera_person_event():
    event = MakeEvent(
        {
            "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
            "timestamp": "2019-01-01T00:00:01Z",
            "resourceUpdate": {
                "name": "enterprises/project-id/devices/device-id",
                "events": {
                    "sdm.devices.events.CameraPerson.Person": {
                        "eventSessionId": "CjY5Y3VKaTZwR3o4Y19YbTVfMF...",
                        "eventId": "FWWVQVUdGNUlTU2V4MGV2aTNXV...",
                    }
                },
            },
            "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
        }
    )
    assert "0120ecc7-3b57-4eb4-9941-91609f189fb4" == event.event_id
    assert (
        datetime.datetime(2019, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        == event.timestamp
    )
    assert "enterprises/project-id/devices/device-id" == event.resource_update_name
    events = event.resource_update_events
    assert "sdm.devices.events.CameraPerson.Person" in events
    e = events["sdm.devices.events.CameraPerson.Person"]
    assert "FWWVQVUdGNUlTU2V4MGV2aTNXV..." == e.event_id
    assert "CjY5Y3VKaTZwR3o4Y19YbTVfMF..." == e.event_session_id


def test_camera_motion_event():
    event = MakeEvent(
        {
            "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
            "timestamp": "2019-01-01T00:00:01Z",
            "resourceUpdate": {
                "name": "enterprises/project-id/devices/device-id",
                "events": {
                    "sdm.devices.events.CameraMotion.Motion": {
                        "eventSessionId": "CjY5Y3VKaTZwR3o4Y19YbTVfMF...",
                        "eventId": "FWWVQVUdGNUlTU2V4MGV2aTNXV...",
                    }
                },
            },
            "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
        }
    )
    assert "0120ecc7-3b57-4eb4-9941-91609f189fb4" == event.event_id
    assert (
        datetime.datetime(2019, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        == event.timestamp
    )
    assert "enterprises/project-id/devices/device-id" == event.resource_update_name
    events = event.resource_update_events
    assert "sdm.devices.events.CameraMotion.Motion" in events
    e = events["sdm.devices.events.CameraMotion.Motion"]
    assert "FWWVQVUdGNUlTU2V4MGV2aTNXV..." == e.event_id
    assert "CjY5Y3VKaTZwR3o4Y19YbTVfMF..." == e.event_session_id


def test_doorbell_chime_event():
    event = MakeEvent(
        {
            "eventId": "0120ecc7-3b57-4eb4-9941-91609f189fb4",
            "timestamp": "2019-01-01T00:00:01Z",
            "resourceUpdate": {
                "name": "enterprises/project-id/devices/device-id",
                "events": {
                    "sdm.devices.events.DoorbellChime.Chime": {
                        "eventSessionId": "CjY5Y3VKaTZwR3o4Y19YbTVfMF...",
                        "eventId": "FWWVQVUdGNUlTU2V4MGV2aTNXV...",
                    }
                },
            },
            "userId": "AVPHwEuBfnPOnTqzVFT4IONX2Qqhu9EJ4ubO-bNnQ-yi",
        }
    )
    assert "0120ecc7-3b57-4eb4-9941-91609f189fb4" == event.event_id
    assert (
        datetime.datetime(2019, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        == event.timestamp
    )
    assert "enterprises/project-id/devices/device-id" == event.resource_update_name
    events = event.resource_update_events
    assert "sdm.devices.events.DoorbellChime.Chime" in events
    e = events["sdm.devices.events.DoorbellChime.Chime"]
    assert "FWWVQVUdGNUlTU2V4MGV2aTNXV..." == e.event_id
    assert "CjY5Y3VKaTZwR3o4Y19YbTVfMF..." == e.event_session_id


def test_relation():
    event = MakeEvent(
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
    assert "0120ecc7-3b57-4eb4-9941-91609f189fb4" == event.event_id
    assert (
        datetime.datetime(2019, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
        == event.timestamp
    )
    assert event.resource_update_name is None
    assert event.resource_update_events is None
    assert event.resource_update_traits is None
    update = event.relation_update
    assert "CREATED" == update.type
    assert "enterprises/project-id/structures/structure-id" == update.subject
    assert "enterprises/project-id/devices/device-id" == update.object
