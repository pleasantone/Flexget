import pytest

from flexget.utils.simple_persistence import SimplePersistence

persist = SimplePersistence('matrix')


@pytest.mark.require_optional_deps
@pytest.mark.online
class TestMatrixNotifier:
    config = """
        templates:
            global:
                mock:
                  - {title: matrix-test}
                accept_all: yes
        tasks:
            use-token-and-room-id:
              notify:
                entries:
                  message: This is a message for testing.
                  via:
                      - matrix:
                          server: https://matrix.org
                          token: mat_1bGYIG9S4j7bbTuVlOyGzbVOZrTWms_g6epP1
                          room_id: '!PVlIjQRbvFpeHCCxGy:matrix.org'
            use-password-and-room-address:
              notify:
                entries:
                  message: This is a message for testing.
                  via:
                      - matrix:
                          server: https://matrix.org
                          user: '@viodi:matrix.org'
                          password: b2!pFpbeP$WuJt$
                          device_name: Notifier by FlexGet LLC
                          room_address: '#flexgettest:matrix.org'
            token-expired:
              notify:
                entries:
                  message: This is a message for testing.
                  via:
                      - matrix:
                          server: https://matrix.org
                          user: '@viodi:matrix.org'
                          password: b2!pFpbeP$WuJt$
                          room_id: '!PVlIjQRbvFpeHCCxGy:matrix.org'
            room-version-upgraded:
              notify:
                entries:
                  message: This is a message for testing.
                  via:
                    - matrix:
                        server: https://matrix.org
                        token: mat_1bGYIG9S4j7bbTuVlOyGzbVOZrTWms_g6epP1
                        room_address: '#flexgettest:matrix.org'
        """

    def test_use_token_and_room_id(self, execute_task):
        execute_task('use-token-and-room-id', options={'test': True})

    def test_use_password_and_room_address(self, execute_task):
        execute_task('use-password-and-room-address', options={'test': True})

    def test_token_expired(self, execute_task):
        persist['@viodi:matrix.org'] = 'mat_BZDW7Rdbkj4KOFNn6LkRh5Y3xC3dtR_0SzXAT'
        execute_task('token-expired', options={'test': True})

    def test_room_version_upgraded(self, execute_task):
        persist['#flexgettest:matrix.org'] = '!dVlujCRbvepeDCCxgG:matrix.org'
        execute_task('room-version-upgraded', options={'test': True})
