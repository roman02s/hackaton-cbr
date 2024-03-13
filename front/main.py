import streamlit as st
import os

def save_uploaded_file(uploaded_file):
    try:
        # Определение пути к директории текущего скрипта
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        # Путь к директории для сохранения файлов
        upload_dir = os.path.join(current_script_dir, "uploaded_files")

        # Проверка существования папки и создание, если она не существует
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Сохранение файла
        with open(os.path.join(upload_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        print(e)
        return False

def main():
    st.title("Загрузка и сохранение файлов")

    # Создание виджета для загрузки файлов
    uploaded_files = st.file_uploader("Перетащите файлы сюда или нажмите для выбора", 
                                      accept_multiple_files=True)

    # Отображение выбранных файлов и кнопка для их сохранения
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write("Выбранный файл:", uploaded_file.name)
        
        # Кнопка для сохранения файлов
        if st.button("Сохранить файлы"):
            success = True
            for uploaded_file in uploaded_files:
                if not save_uploaded_file(uploaded_file):
                    success = False
                    st.error(f"Ошибка при сохранении файла {uploaded_file.name}")
            if success:
                st.success("Все файлы успешно сохранены")

if __name__ == "__main__":
    main()
