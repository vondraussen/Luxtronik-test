import pytest
from unittest.mock import patch
from Luxtronik.luxtronik import Luxtronik



def test_login():
    password = "my_password"
    expected_message = f"LOGIN;{password}"

    with patch('websocket.WebSocket.connect', autospec=True):
        luxtronik = Luxtronik("127.0.0.1", 8214, password)

    # Act and Assert
    with patch('websocket.WebSocket.send', autospec=True) as mock_send:
        luxtronik.login()
        mock_send.assert_called_once_with(luxtronik.ws, expected_message)

def test_login_default_pw():
    expected_message = f"LOGIN;999999"
    with patch('websocket.WebSocket.connect', autospec=True):
        luxtronik = Luxtronik("127.0.0.1")

    # Act and Assert
    with patch('websocket.WebSocket.send', autospec=True) as mock_send:
        luxtronik.login()
        mock_send.assert_called_once_with(luxtronik.ws, expected_message)

def test_refresh():
    with patch('websocket.WebSocket.connect', autospec=True):
        luxtronik = Luxtronik("127.0.0.1")

    # Act and Assert
    with patch('websocket.WebSocket.send', autospec=True) as mock_send, \
            patch('websocket.WebSocket.recv', autospec=True) as mock_recv:
        with open('tests/refresh_data.xml', 'r') as file:
            refresh_result = file.read().strip()
            mock_recv.return_value = refresh_result
        refresh_data = luxtronik.refresh()
        mock_send.assert_called_once_with(luxtronik.ws, 'REFRESH')
        assert refresh_data == refresh_result

def test_parse_refresh_data():
    with patch('websocket.WebSocket.connect', autospec=True):
        luxtronik = Luxtronik("127.0.0.1")

    with open('tests/refresh_data.xml', 'r') as file:
        refresh_result = file.read().strip()

    # Act and Assert
    with patch('websocket.WebSocket.send', autospec=True), \
            patch('websocket.WebSocket.recv', autospec=True) as mock_recv:
        mock_recv.return_value = refresh_result
        luxtronik.refresh()
        result = luxtronik.parse_refresh_data(refresh_result)

    assert result == []