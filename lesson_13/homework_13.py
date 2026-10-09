"""
Ваша команда та ви розробляєте систему входу для веб-додатка,
і вам потрібно реалізувати тести на функцію для логування подій в системі входу.
Дано функцію, напишіть набір тестів для неї.
"""
import unittest
import logging

def log_event(username: str, status: str):
    """
    Логує подію входу в систему.

    username: Ім'я користувача, яке входить в систему.

    status: Статус події входу:

    * success - успішний, логується на рівні інфо
    * expired - пароль застаріває і його слід замінити, логується на рівні warning
    * failed  - пароль невірний, логується на рівні error
    """
    log_message = f"Login event - Username: {username}, Status: {status}"

    # Створення та налаштування логера
    logging.basicConfig(
        filename='login_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
        )
    logger = logging.getLogger("log_event")

    # Логування події
    if status == "success":
        logger.info(log_message)
    elif status == "expired":
        logger.warning(log_message)
    else:
        logger.error(log_message)




class Test(unittest.TestCase):
    def test_success_log_event(self):
        test_login = ('test_username', 'success')
        expected_result = f"Login event - Username: {test_login[0]}, Status: {test_login[1]}"

        with self.assertLogs("log_event", level="INFO") as cm:
            log_event("test_username", "success")
        self.assertEqual(cm.records[0].getMessage(), expected_result)
        self.assertEqual(cm.records[0].levelname, "INFO")
    def test_expired_log_event(self):
        test_login = ('test_username', 'expired')
        expected_result = f"Login event - Username: {test_login[0]}, Status: {test_login[1]}"

        with self.assertLogs("log_event", level="INFO") as cm:
            log_event("test_username", "expired")
        self.assertEqual(cm.records[0].getMessage(), expected_result)
        self.assertEqual(cm.records[0].levelname, "WARNING")

    def test_failed_log_event(self):
        test_login = ('test_username', 'failed')
        expected_result = f"Login event - Username: {test_login[0]}, Status: {test_login[1]}"

        with self.assertLogs("log_event", level="INFO") as cm:
            log_event("test_username", "failed")
        self.assertEqual(cm.records[0].getMessage(), expected_result)
        self.assertEqual(cm.records[0].levelname, "ERROR")
if __name__ == '__main__':
    unittest.main()