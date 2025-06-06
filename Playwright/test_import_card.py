from playwright.sync_api import Page, expect
import random
import re

def test_import_card(page: Page):
    print("\n[ТЕСТ] Создание карточки импорта")
    email = "quqisocy@gmail.com"
    password = "12345678aA!"
    password = "12345678aA!"

    print("[ШАГ 1] Переход на страницу авторизации...")
    page.goto("https://account.pro-brics.com")
    print("[ОТЧЁТ] Страница авторизации открыта.")

    print("[ШАГ 2] Вводим логин и пароль...")
    page.fill('id=username', email)
    page.fill('id=password', password)
    print("[ОТЧЁТ] Логин и пароль введены.")

    print("[ШАГ 3] Нажимаем кнопку 'Войти'...")
    page.get_by_role("button", name="Войти").click()
    print("[ОТЧЁТ] Кнопка входа нажата.")

    print("[ШАГ 4] Ожидание перехода на страницу товаров...")
    try:
        page.wait_for_url("https://account.pro-brics.com/products", timeout=5000)
        print("[ОТЧЁТ] Успешно перешли на страницу товаров.")
    except Exception:
        print("[ОШИБКА] Не удалось перейти на страницу товаров!")
        raise

    print("[ШАГ 5] Проверка наличия уведомлений об ошибке...")
    push_notifications = page.locator(".ant-notification-notice-description:visible")
    notification_count = push_notifications.count()

    if notification_count > 0:
        error_messages = []
        for i in range(notification_count):
            message = push_notifications.nth(i).inner_text().strip()
            error_messages.append(message)

        full_error_text = "\n".join(error_messages)
        print("[ОШИБКА] Обнаружены уведомления после входа:\n" + full_error_text)
        raise AssertionError("Уведомления после входа:\n" + full_error_text)
    else:
        print("[ОТЧЁТ] Уведомлений об ошибке не найдено.")

    print("[ШАГ 6] Переходим в раздел 'Мои товары'...")
    page.locator('span.ant-menu-title-content >> a[data-discover="true"]', has_text="Мои товары").click()
    print("[ОТЧЁТ] Клик по 'Мои товары' выполнен.")

    print("[ШАГ 7] Нажимаем кнопку 'Добавить товар'...")
    page.get_by_role("button", name="Добавить товар").click()
    print("[ОТЧЁТ] Кнопка 'Добавить товар' нажата.")

    print("[ШАГ 8] Ожидание формы 'Создание товара'...")
    expect(page.locator('h2.ant-typography', has_text="Создание товара")).to_be_visible(timeout=5000)
    print("[ОТЧЁТ] Форма создания товара отображается.")

    print("[ШАГ 9] Заполняем карточку товара...")
    page.fill('id=category', "0601101000")
    print("[ОТЧЁТ] Код категории введён.")
    page.locator('button.ant-btn.css-vdczu1.css-var-r1.ant-btn-default.ant-btn-color-default.ant-btn-variant-outlined.ant-btn-icon-only.ant-input-search-button').click()
    print("[ОТЧЁТ] Кнопка поиска категории нажата.")

    random_code = random.randint(10000, 99999)
    product_name = f"TEST_PRODUCT_{random_code}"
    page.fill('id=name', product_name)
    print(f"[ОТЧЁТ] Название товара введено: {product_name}")
    page.fill('id=description', product_name)
    print(f"[ОТЧЁТ] Описание товара введено: {product_name}")

    page.evaluate("document.getElementById('location').value = 'Россия'")
    print("[ОТЧЁТ] Местоположение указано: Россия")

    page.fill('id=StockQuantity', "50000")
    print(f"[ОТЧЁТ] Количество на складе: 50000")

    page.fill('id=MounthSupply', "5000")
    print(f"[ОТЧЁТ] Месячный объём поставки: 5000")

    page.fill('id=Price', "152652.5")
    print(f"[ОТЧЁТ] Цена: 152652.5")

    # Проверка, что поле PriceCNY заполнилось
    print("[ШАГ 9.1] Проверяем, что поле PriceCNY заполнилось...")
    page.wait_for_timeout(1000)  # Подождать, если пересчет происходит асинхронно
    price_cny_value = page.eval_on_selector('#PriceCNY', 'el => el.value')
    print(f"[ОТЧЁТ] Значение PriceCNY: '{price_cny_value}'")
    assert price_cny_value, "[ОШИБКА] Поле PriceCNY не заполнилось!"

    random_day = random.randint(1, 13)
    page.fill('id=MinimalmDeliveryDays', str(random_day))
    print(f"[ОТЧЁТ] Минимальный срок поставки: {random_day}")

    page.fill('id=MaximalDeliveryDays', str(random_day+14))
    print(f"[ОТЧЁТ] Максимальный срок поставки: {random_day+14}")

    print("[ШАГ 10] Карточка товара успешно заполнена.")

    print("[ШАГ 11] Кликаем по кнопке 'Сохранить' с нужным классом...")
    save_button_selector = (
        "button.ant-btn.css-vdczu1.css-var-r1.ant-btn-round.ant-btn-primary."
        "ant-btn-color-primary.ant-btn-variant-solid"
    )
    page.locator(save_button_selector, has_text="Сохранить").click()
    print("[ОТЧЁТ] Кнопка 'Сохранить' нажата.")

    print("[ШАГ 12] Ожидание перехода на страницу успешного создания товара...")
    page.wait_for_url(re.compile(
        r"https://account\.pro-brics\.com/company-products/[0-9a-fA-F\-]+/create-success"
    ), timeout=10000)
    current_url = page.url
    print(f"[ОТЧЁТ] Перешли по адресу: {current_url}")

    pattern = r"^https://account\.pro-brics\.com/company-products/[0-9a-fA-F\-]+/create-success$"
    assert re.match(pattern, current_url), (
        f"[ОШИБКА] URL после создания товара не соответствует ожидаемому шаблону!\nТекущий URL: {current_url}"
    )

    print("[ОТЧЁТ] Успешно получили ссылку создания товара!")
