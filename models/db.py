class DataBase:
    db_file = 'db.call'
    SEP_CHAR = '|'
    NEW_LINE_CHAR = '\n'
    pk_field_name = 'ID'
    pk_max_size = 6

    def __init__(self):
        self.pk = None
        self.primary_key_text = 'PrimaryKey'
        self.table = None

        self.read()

    def read(self):
        with open(self.db_file) as file:
            pk_line = file.readline()
            self._get_pk_from_file(pk_line)
            table = file.read()
            if table:
                self.table = table

    def _get_pk_from_file(self, pk_line):
        if not pk_line:
            self.pk = 0
        else:
            self.pk = int(pk_line.split(':')[-1])

    def get_new_pk(self):
        self.pk += 1
        return self.pk

    def write(self, text):
        with open(self.db_file, 'w') as file:
            pk_line = f'{self.primary_key_text}:{self.pk}\n'
            file.write(pk_line)
            file.write(text)

    def get_rows(self):
        rows = self.table.split(self.NEW_LINE_CHAR)
        rows.pop()
        return rows
