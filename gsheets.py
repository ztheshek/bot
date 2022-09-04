from oauth2client.service_account import ServiceAccountCredentials
from secret import G_CREDS, G_SHEETS_ID, G_SCOPE
import gspread



def get_auth(sheet_list):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(G_CREDS, G_SCOPE)
    gc = gspread.authorize(credentials)
    sht1 = gc.open_by_key(G_SHEETS_ID)
    return sht1.worksheet(sheet_list)


def append_row_gsheets(msg_id, value, text, category, state, date, author):
    worksheet = get_auth('data')
    row = []
    row.append(msg_id)
    row.append(value)
    row.append(' '.join(text))
    row.append(category)
    row.append(state)
    row.append(date.strftime("%Y.%m.%d %H:%M:%S"))
    row.append(author)
    print(row)
    worksheet.append_row(row, value_input_option="USER_ENTERED")


def update_row_gsheets(row_id, msg_id, value, text, category, state, date, author):
    worksheet = get_auth('data')
    row = []
    row.append(msg_id)
    row.append(value)
    row.append(' '.join(text))
    row.append(category)
    row.append(state)
    row.append(date.strftime("%Y.%m.%d %H:%M:%S"))
    row.append(author)
    print(row)
    worksheet.update('A{id}:G{id}'.format(id=row_id), [row])


def delete_row_gsheets(msg_id):
    worksheet = get_auth('data')
    edited_id = worksheet.find(query=str(msg_id), in_column=1)
    worksheet.batch_clear(['A{id}:G{id}'.format(id=edited_id.row)])


def get_categories():
    worksheet = get_auth('meta')
    categories = worksheet.col_values(col=1)
    return categories

def get_plan_fact():
    worksheet = get_auth('main')
    return worksheet.batch_get(['B1:B25', 'E1:E25'])

def find_category(category_name):
    worksheet = get_auth('meta')
    return worksheet.find(query=category_name, in_column=1)


def get_category_alias(category_name):
    worksheet = get_auth('meta')
    category = find_category(category_name)
    return worksheet.row_values(category.row)[1:]


def insert_category_alias(category_name, value):
    worksheet = get_auth('meta')
    category = find_category(category_name)
    col = len(get_category_alias(category_name)) + 2
    worksheet.update_cell(row=category.row, col=col, value=' '.join(value))


def set_category_msg(text):
    categories = get_categories()



def find_category_msg(text):
    text = ' '.join(text)
    worksheet = get_auth('meta')
    all_values = worksheet.get_all_values()
    for category in all_values:
        for alias in category[1:]:
            if alias == text:
                return category[0]
    # Поместить в категорию + поместить text  в alias
    # Создать новую категорию и поместить в alias
    print(f'Нет алиаса для: {text}')
    return None


def get_state_category(msg_id):
    worksheet = get_auth('data')
    row = worksheet.find(query=str(msg_id), in_column=1)
    category, state = worksheet.row_values(row.row)[3:5]
    return category, state


def get_cell_row(msg_id):
    worksheet = get_auth('data')
    cell = worksheet.find(query=str(msg_id))
    return cell.row


def add_chosen_category(category_name, msg_id):
    worksheet = get_auth('data')
    cell = worksheet.find(query=str(msg_id), in_column=1)
    print(cell)
    worksheet.update_cell(row=cell.row, col=4, value=category_name)
