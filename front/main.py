import streamlit as st
import os

def save_uploaded_file(uploaded_file):
    try:
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        upload_dir = os.path.join(current_script_dir, "uploaded_files")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        with open(os.path.join(upload_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        print(e)
        return False

def call_api_with_file(file_path):
    # Здесь должен быть ваш код для вызова API с файлом
    pass

def main():
    st.title("Выбор функции, загрузка файлов и поиск")

    # Выбор между загрузкой файлов и дополнительным полем ввода
    choice = st.radio("Выберите функцию:", ('Загрузка файлов', 'Дополнительное поле ввода'))

    # Загрузка файлов
    if choice == 'Загрузка файлов':
        uploaded_files = st.file_uploader("Перетащите файлы сюда или нажмите для выбора", 
                                          accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.write("Выбранный файл:", uploaded_file.name)
            
            if st.button("Обработать файлы"):
                for uploaded_file in uploaded_files:
                    if save_uploaded_file(uploaded_file):
                        file_path = os.path.join("uploaded_files", uploaded_file.name)
                        call_api_with_file(file_path)
                        st.success(f"Файл {uploaded_file.name} обработан")
                    else:
                        st.error(f"Ошибка при сохранении файла {uploaded_file.name}")

    # Дополнительное поле ввода
    elif choice == 'Дополнительное поле ввода':
        additional_input = st.text_area("Введите дополнительный текст")

    # Поисковая строка
    query = st.text_input("Введите запрос для поиска", key="search_query")

    # Кнопка отправки запроса
    if st.button("Отправить запрос", key="send_query"):
        # Обработка запроса (простая заглушка, здесь должна быть ваша логика поиска)
        if query:
            st.write(f"Результаты поиска для запроса: {query}")

if __name__ == "__main__":
    main()
