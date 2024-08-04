
from unittest import TestCase
from unittest.mock import MagicMock

from src.modules.events.handlers import EventStatusHandler
from src.modules.events.enums import EventStatus
from src.modules.events.models import Event
from src.modules.events.exceptions import EventStatusSetError


class TestEventStatusHandler(TestCase):
    def setUp(self):
        self.mock_event = MagicMock(spec=Event)

        self.mock_event.configure_mock(**{
            'status': EventStatus.FIRST_TEAM_WIN,
            'open_statuses': [EventStatus.OPEN],
            'is_ended.return_value': True,
        })

    def test_update_event_close_status(self):
        """Test event status update"""

        self.mock_event.is_ended.return_value = False

        EventStatusHandler(self.mock_event).set_status(EventStatus.FIRST_TEAM_WIN)

        self.mock_event.is_ended.assert_not_called()
        self.assertEqual(self.mock_event.status, EventStatus.FIRST_TEAM_WIN)

    def test_update_event_open_status(self):
        """Test event open status update"""

        self.mock_event.status = EventStatus.FIRST_TEAM_WIN
        self.mock_event.is_ended.return_value = False

        EventStatusHandler(self.mock_event).set_status(EventStatus.OPEN)

        self.mock_event.is_ended.assert_called_once()
        self.assertEqual(self.mock_event.status, EventStatus.OPEN)

    def test_update_event_error_status(self):
        """Test event error status update"""

        self.mock_event.status = EventStatus.FIRST_TEAM_WIN
        self.mock_event.is_ended.return_value = True

        # NOTE: cannot set OPEN status if event outdated
        with self.assertRaises(EventStatusSetError):
            EventStatusHandler(self.mock_event).set_status(EventStatus.OPEN)

            self.mock_event.is_ended.assert_called_once()
