from playwright.sync_api import Page, expect
import random
import string

def test_registration(page: Page):
    print("\n[ТЕСТ] Регистрация пользователя")

    print("[ШАГ 1] Открываем страницу регистрации...")
    page.goto("https://account.pro-brics.com/register")
    print("[ОТЧЁТ] Страница регистрации открыта.")

    print("[ШАГ 2] Вводим данные пользователя...")
    random_part = ''.join(random.choices(string.digits, k=3))
    email = f"quqisocy+{random_part}@gmail.com"
    password = '12345678aA!'
    page.fill('id=email', email)
    page.fill('id=pass', password)
    page.fill('id=repeat', password)
    print(f"[ОТЧЁТ] Данные пользователя введены:\n  Email: {email}\n  Пароль: {password}")

    print("[ШАГ 2.5] Отмечаем чекбоксы согласий...")
    # Первый чекбокс
    page.locator('input.ant-checkbox-input').nth(0).click()
    # Второй чекбокс
    page.locator('input.ant-checkbox-input').nth(1).click()
    print("[ОТЧЁТ] Чекбоксы отмечены.")

    print("[ШАГ 3] Отправляем форму регистрации...")
    page.get_by_role("button", name="Зарегистрироваться").click()
    print("[ОТЧЁТ] Форма регистрации отправлена.")

    print("[ШАГ 4] Ожидаем редиректа на страницу успешной регистрации...")
    try:
        page.wait_for_url("**/register-success", timeout=15000)
        print(f"[ОТЧЁТ] Успешный редирект на {page.url}")
    except Exception:
        print("[ОШИБКА] Редирект не произошёл. Проверяем наличие модального окна с ошибкой...")
        if page.locator('.ant-modal-wrap').is_visible():
            modal_text = page.locator('.ant-modal-wrap').inner_text()
            print("[ОТЧЁТ] Модальное окно с ошибкой обнаружено:")
            print(modal_text)
        raise AssertionError("[ОШИБКА] Регистрация неуспешна – редирект не выполнен")
