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

def add_to_database(data):
    # Здесь должен быть ваш код для добавления данных в базу знаний
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
                        st.success(f"Файл {uploaded_file.name} успешно обработан")
                    else:
                        st.error(f"Ошибка при сохранении файла {uploaded_file.name}")

            if st.button("Добавить файлы в базу знаний"):
                for uploaded_file in uploaded_files:
                    # Добавьте логику для добавления файлов в базу знаний
                    pass
                st.success("Файлы добавлены в базу знаний")

    # Дополнительное поле ввода
    if choice == 'Дополнительное поле ввода':
        additional_input = st.text_area("Введите дополнительный текст", height=300)
        if st.button("Добавить текст в базу знаний"):
            add_to_database(additional_input)
            st.success("Текст добавлен в базу знаний")

    # Поисковая строка и кнопка отправки запроса находятся в самом низу страницы
    query = st.text_input("Введите запрос для поиска", key="search_query")
    if st.button("Найти"):
        if query:
            st.write(f"Результаты поиска для запроса: {query}")

if __name__ == "__main__":
    main()
