from playwright.sync_api import Page, expect

def test_auth_admin(page: Page):
    print("\n[ТЕСТ] Авторизация администратора")

    print("[ШАГ 1] Открываем страницу авторизации администратора...")
    page.goto("https://admin.pro-brics.com")
    print("[ОТЧЁТ] Страница авторизации открыта.")

    print("[ШАГ 2] Вводим логин и пароль администратора...")
    username = 'probrics@solutionfactory.ru'
    password = 'LcR-G9R-ebG-CvR'
    page.fill('id=username', username)
    page.fill('id=password', password)
    print(f"[ОТЧЁТ] Введены данные:\n  Логин: {username}\n  Пароль: {password}")

    print("[ШАГ 3] Отправляем форму авторизации...")
    page.get_by_role("button", name="Войти").click()
    print("[ОТЧЁТ] Форма авторизации отправлена.")

    print("[ШАГ 4] Проверяем наличие элемента 'Иностранные компании'...")
    try:
        element = page.locator("a", has_text="Иностранные компании")
        expect(element).to_be_visible(timeout=5000)
        print("[ОТЧЁТ] Успешный вход: элемент 'Иностранные компании' найден.")
    except Exception:
        print("[ОШИБКА] Элемент 'Иностранные компании' не найден.")
        raise

    print("[ШАГ 5] Проверяем уведомления об ошибках...")
    push_notifications = page.locator(".ant-notification-notice-description:visible")
    notification_count = push_notifications.count()

    if notification_count > 0:
        error_messages = []
        for i in range(notification_count):
            message = push_notifications.nth(i).inner_text().strip()
            error_messages.append(message)
        full_error_text = "\n".join(error_messages)
        print("[ОТЧЁТ] Найдены уведомления об ошибках:")
        print(full_error_text)
        raise AssertionError("[ОШИБКА] Уведомления после входа:\n" + full_error_text)
    else:
        print("[ОТЧЁТ] Ошибочных уведомлений не обнаружено.")
