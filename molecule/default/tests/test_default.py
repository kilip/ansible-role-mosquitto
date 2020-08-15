"""Role testing files using testinfra."""

def test_installation(host):
    assert host.package('mosquitto').is_installed


def test_service(host):
    mqtt = host.service('mosquitto')
    port = host.socket('tcp://127.0.0.1:1883')
    tls = host.socket('tcp://0.0.0.0:8883')

    assert mqtt.is_enabled
    assert mqtt.is_running
    assert port.is_listening
    assert tls.is_listening

def test_connection(host):
    """Test Mosquitto password"""
    cmd = host.run('mosquitto_pub -h 127.0.0.1 -p 1883 -t test -m "hello world"')
    assert cmd.stderr.find('not authorised') != -1

    cmd = host.run('mosquitto_pub -d -h 127.0.0.1 -p 1883 -t test -m "hello world" -u "foo" -P "bar"')
    assert cmd.stdout.find('PUBLISH') != -1

