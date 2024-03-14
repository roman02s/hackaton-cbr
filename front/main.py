import streamlit as st
import os
import requests

def save_uploaded_file(uploaded_file):
    try:
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        upload_dir = os.path.join(current_script_dir, "uploaded_files")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        print(e)
        return None

def call_api_with_file(file_path):
    # Здесь должен быть ваш код для вызова API с файлом
    pass

def add_to_database(text):
    try:
        # Ваш код для добавления текста в базу знаний

        # Отправка текста на эндпоинт
        response = send_text_to_endpoint(text)
        return response
    except Exception as e:
        print(e)
        return None

def send_query(query):
    url = "http://10.0.101.102:8000/query/"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"text": query}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def send_paths_to_endpoint(paths):
    url = "http://10.0.101.102:8000/drag_n_drop/"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"texts": paths}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def send_text_to_endpoint(text):
    url = "http://10.0.101.102:8000/load_text/"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    st.title("Выбор функции, загрузка файлов и поиск")

    # Выбор между загрузкой файлов и дополнительным полем ввода
    choice = st.radio("Выберите функцию:", ('Загрузка файлов', 'Дополнительное поле ввода'))

    uploaded_files_paths = []

    # Загрузка файлов
    if choice == 'Загрузка файлов':
        uploaded_files = st.file_uploader("Перетащите файлы сюда или нажмите для выбора", 
                                          accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.write("Выбранный файл:", uploaded_file.name)

            if st.button("Обработать файлы и добавить в базу"):
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    if file_path:
                        call_api_with_file(file_path)
                        uploaded_files_paths.append(file_path)
                        st.success(f"Файл {uploaded_file.name} успешно обработан и добавлен в базу")
                        if uploaded_files_paths:
                            print([f"/nfs/home/rodobesku/hackaton_front_cbr/uploaded_files/{path.split('/')[-1]}" for path in uploaded_files_paths])
                            response = send_paths_to_endpoint([f"/nfs/home/rodobesku/hackaton_front_cbr/uploaded_files/{path.split('/')[-1]}" for path in uploaded_files_paths])
                            st.write("Ответ от сервера:")
                            st.write(response)
                    else:
                        st.error(f"Ошибка при сохранении файла {uploaded_file.name}")


    # Дополнительное поле ввода
    if choice == 'Дополнительное поле ввода':
        additional_input = st.text_area("Введите дополнительный текст", height=300)
        if st.button("Добавить текст в базу знаний"):
            if additional_input:
                response = add_to_database(additional_input)
                if response:
                    st.success("Текст успешно добавлен в базу знаний и отправлен на сервер")
                else:
                    st.error("Ошибка при добавлении текста в базу знаний и отправке на сервер")
            else:
                st.warning("Введите текст перед добавлением в базу знаний")


if __name__ == "__main__":
    main()

# Поисковая строка и кнопка отправки запроса находятся в самом низу страницы
query = st.text_input("Введите запрос для поиска", key="search_query")
if st.button("Найти"):
    if query:
        search_result = send_query(query)
        st.write(f"Результаты поиска для запроса: {query}")
        # Выведите результаты поиска
        st.write(search_result)
