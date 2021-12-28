import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
from auth import google_api_json


URL =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

class Interrogator():
    """
    Класс для взаимодействия с google sheets. Использует библиотеку gspread.
    При инициализации экземпляра создаются необходимые worksheet таблиц.
    """

    def __init__(self,credentials:dict):
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, URL)
        self.__client = gspread.authorize(self.__credentials)

        self__sheets_contracts_service = self.__client.open('Договора.Н')
        self__sheets_income_expenses_today = self.__client.open('Расходы.Н')

        self.__worksheet_contracts_service = self__sheets_contracts_service.worksheet("Договоры.Служебная")
        self.__worksheet_income_expenses_today = self__sheets_income_expenses_today.worksheet("Доходы.Расходы.Сегодня")
        self.__authorization = self__sheets_income_expenses_today.worksheet("Авторизация")

    def __check_cell_for_surcharge(self,cells):
        """
        Метод для выбора клеток из нужных столбцов.
        На вход метода передается массив, всех найденых клеток.
        С помощью генератора, на выход передается новых масив, подходящий под правило.
        """
        return [cell for cell in cells if self.__worksheet_contracts_service.cell(1, cell.col).value in ["Дата 1","Дата 2","Дата 3","Дата 4"]]

    def __check_cell_for_days_contract(self,cells):
        """
        Метод для выбора клеток из нужных столбцов.
        На вход метода передается массив, всех найденых клеток.
        С помощью генератора, на выход передается новых масив, подходящий под правило.
        """        
        return [cell for cell in cells if self.__worksheet_contracts_service.cell(1, cell.col).value == "Дата"]

    def __get_row_list(self, cell_list):
        """
        Метод для получения массива строк, по клеткам.
        На вход передается массив из клеток, из клетки получается значение строки и запрашивается 
        """
        return [self.__worksheet_contracts_service.row_values(cell.row) for cell in cell_list]

    def __pass_null_cell_in_row(self, row_list):
        """
        Метод для удаления пустых мест в строке
        """
        return [[val for val in row if val] for row in row_list]

    def __row_formatter_for_surcharge(self,day,rows_list):
        """
        Метод для формирования данных,для функции «Доплаты».
        """
        final_dict = {}
        final_list = [
            {
                'Клиент': f'{row[1]}({row[-3]})',
                'Сумма доплаты': row[row.index(day)-1],
                'Юристы': row[-1],
            }
            for row in rows_list
        ]
        final_dict["Количество доплат"] = len(final_list)
        final_dict["Сумма"]= sum([float(row['Сумма доплаты']) for row in final_list])
        final_dict["Дата"] = day
        final_dict["Данные"] = final_list
        return final_dict

    def __row_formatter_days_contract(self,day,rows_list):
        """
        Метод для формирования данных,для функции «Договоры».
        """
        final_dict = {}
        final_list = [
            {
                'Клиент': f'{row[1]}({row[-3]})',
                'Юристы': row[-1],
            }
            for row in rows_list
        ]
        final_dict["Дата"] = day
        final_dict["Данные"] = final_list
        return final_dict


    def get_surcharge(self,day_relatively_today=0):
        """
        Метод для получения доплат,для функции «Доплаты».
        day_relatively_today это смещение в днях, далее оно переводится в дату.
        """        
        day = datetime.strftime(
            datetime.now() +\
                timedelta(days=day_relatively_today),"%d.%m.%Y")
        cell_list = self.__check_cell_for_surcharge(
            self.__worksheet_contracts_service.findall(day))
        row_list = self.__pass_null_cell_in_row(
            self.__get_row_list(cell_list))
        return self.__row_formatter_for_surcharge(day,row_list)

    def get_income_expenses(self):
        """
        Метод для получения расходов/доходов,для функции «Доходы».
        """        
        list_rows = self.__worksheet_income_expenses_today.get("A:F")
        income = float()
        expenditure = float()
        total = float()
        list_dicts = tuple()
        for row in list_rows[1:]:
            _dict = dict(zip(list_rows[0],row))
            if _dict['Тип операции'] == 'Расход':
                _dict['Сумма'] = -(float(_dict['Сумма']))
                expenditure += _dict['Сумма']
            else:
                _dict['Сумма'] = float(_dict['Сумма'])
                income += _dict['Сумма']
            _ = (*list_dicts, _dict)
            list_dicts = _
        total = income + expenditure
        return {
            'Данные': list_dicts, 
            "Дата": datetime.strftime(datetime.now() ,"%d.%m.%Y"),
            "Доход за день": income, 
            "Расход за день": expenditure,
            "Итог за день": total
            }

    def twenty_days_contract(self,day_relatively_today=0):
        """
        Метод для получения договоров у которых 20ый день с заключения,для функции «Договоры».
        day_relatively_today это смещение в днях, далее оно переводится в дату.
        """        
        day_for_print = datetime.strftime(
            datetime.now() +\
                timedelta(days=day_relatively_today),"%d.%m.%Y")
        day_days_ago = datetime.strftime(
            datetime.now() +\
                timedelta(days=day_relatively_today) -\
                    timedelta(days=20),"%d.%m.%Y")
        cell_list = self.__check_cell_for_days_contract(
            self.__worksheet_contracts_service.findall(day_days_ago))
        row_list = self.__pass_null_cell_in_row(
            self.__get_row_list(cell_list))
        return self.__row_formatter_days_contract(day_for_print,row_list)
     
    def forty_days_contract(self,day_relatively_today=0):
        """
        Метод для получения договоров у которых 40ой день с заключения,для функции «Договоры».
        day_relatively_today это смещение в днях, далее оно переводится в дату.
        """      
        day_for_print = datetime.strftime(
            datetime.now() +\
                timedelta(days=day_relatively_today),"%d.%m.%Y")
        day_days_ago = datetime.strftime(
            datetime.now() +\
                timedelta(days=day_relatively_today) -\
                    timedelta(days=40),"%d.%m.%Y")
        cell_list = self.__check_cell_for_days_contract(
            self.__worksheet_contracts_service.findall(day_days_ago))
        row_list = self.__pass_null_cell_in_row(
            self.__get_row_list(cell_list))
        return self.__row_formatter_days_contract(day_for_print,row_list)
    
    def get_append_id(self):
        """
        Метод для получения id, которым разрешен доступ к боту.
        """   
        list_rows = [row[0] for row in self.__authorization.get("B3:B")]
        return list_rows

    def admin_list(self,telegram_id):
        """
        Метод для проверки id, на права admin.
        """   
        cell = self.__authorization.findall(telegram_id)[0]
        return True if self.__authorization.cell(cell.row, 3).value == "admin" else False

    def add_user(self,data):
        """
        Метод для добавления id, в таблицу разрешенных.
        """ 
        self.__authorization.append_row((*data,'user'))

    def remove_user(self,id):
        """
        Метод для удаления id, из таблицы разрешенных.
        """ 
        cell = self.__authorization.findall(id)[0]
        self.__authorization.delete_row(cell.row)

    def add_admin_rights(self,id):
        """
        Метод для добавления id, прав admin.
        """ 
        cell = self.__authorization.findall(id)[0]
        self.__authorization.update_cell(cell.row,3,'admin')

    def remove_admin_rights(self,id):
        """
        Метод для удаления id, прав admin.
        """ 
        cell = self.__authorization.findall(id)[0]
        self.__authorization.update_cell(cell.row,3,'user')


s = Interrogator(google_api_json)