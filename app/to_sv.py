from openpyxl.styles import Font
from openpyxl import Workbook
def save_to_excel(users_data, filename='users_test_555.xlsx'):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    # Заголовки
    headers = ['id', 'username', 'first_name', 'last_name','phone','bot']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    # Данные
    for user in users_data:
        ws.append([
            user.get('id', ''),
            user.get('username', ''),
            user.get('first_name', ''),
            user.get('last_name', '')
        ])
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                cell_value = str(cell.value)
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
            except:
                pass
        ws.column_dimensions[column_letter].width = max_length

    wb.save(filename)