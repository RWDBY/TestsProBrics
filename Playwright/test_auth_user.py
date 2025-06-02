from playwright.sync_api import Page, expect

def test_auth_user(page: Page):
    email = "quqisocy@gmail.com"
    password = "12345678aA!"

    print("\n[ТЕСТ] Авторизация пользователя")

    print("[ШАГ 1] Открываем страницу авторизации пользователя...")
    page.goto("https://account.pro-brics.com")
    print("[ОТЧЁТ] Страница авторизации открыта.")

    print("[ШАГ 2] Вводим логин и пароль пользователя...")
    page.fill('id=username', email)
    page.fill('id=password', password)
    print(f"[ОТЧЁТ] Введены данные:\n  Email: {email}\n  Пароль: {password}")

    print("[ШАГ 3] Отправляем форму авторизации...")
    page.get_by_role("button", name="Войти").click()
    print("[ОТЧЁТ] Форма авторизации отправлена.")

    print("[ШАГ 4] Ожидаем редиректа на страницу товаров...")
    try:
        page.wait_for_url("https://account.pro-brics.com/products", timeout=5000)
        print("[ОТЧЁТ] Успешный редирект на страницу товаров.")
    except Exception:
        print("[ОШИБКА] Редирект на страницу товаров не произошёл.")
        raise AssertionError("[ОШИБКА] Редирект на https://account.pro-brics.com/products не выполнен")

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
