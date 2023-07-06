import mysql.connector
def Connect(host,port,user,password,database):
    connection = mysql.connector.connect(host=host,port=port,user=user,password=password,database=database)
    return connection
def is_2d_array(arr):
    if isinstance(arr, list) and all(isinstance(sub_arr, list) for sub_arr in arr):
        return True
    else:
        return False
class DataBase:
    def __init__(this,host,port,user,password,database):
        this.host = host
        this.port = port
        this.user = user
        this.password = password
        this.database = database
    def createTable(this,tableName,values,valuesType):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE {} (martvisSoOpTADADADAWDAWDAWSRNGBIRSHBNGIU VARCHAR(100))".format(tableName,'martvisSoOpTADADADAWDAWDAWSRNGBIRSHBNGIU',valuesType[0]))
        for x,z in zip(values,valuesType):
            cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {x} {z}")
        cursor.execute(f"ALTER TABLE {tableName} DROP COLUMN martvisSoOpTADADADAWDAWDAWSRNGBIRSHBNGIU")
        connection.commit()
        cursor.close()
        connection.close()
    def add(this,values,tableName):
        try: 
            connection = Connect(this.host,this.port,this.user,this.password,this.database)
            cursor = connection.cursor()
            getColumnsNames = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{this.database}' AND TABLE_NAME = '{tableName}' ORDER BY ORDINAL_POSITION"
            cursor.execute(getColumnsNames)
            names = [row[0] for row in cursor.fetchall()]
            column_placeholders = ", ".join(names)
            value_placeholders = ""
            if (is_2d_array(values) is True):
                for x in range(len(values)):
                    if x != len(values)  - 1:
                        value_placeholders += '(' + (', '''.join(i for i in values)) + '),'
                    else:
                        value_placeholders += '(' + (', '''.join(i for i in values)) + ')'
            else:
                value_placeholders = '(' + ', '.join("'" + i + "'" for i in values) + ')'
            print(value_placeholders,column_placeholders)
            add = f"INSERT INTO {tableName} ({column_placeholders}) VALUES {value_placeholders}"
            cursor.execute(add)
            connection.commit()
        except mysql.connector.Error as e:
            print("An Error Happened : ", e)
        finally:
            cursor.close()
            connection.close()
    def remove(this,values,tableName):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()
        try:
            getColumns = f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '{tableName}'"
            cursor.execute(getColumns)
            columns = cursor.fetchone()[0]
            getColumnsNames = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{this.database}' AND TABLE_NAME = '{tableName}' ORDER BY ORDINAL_POSITION"
            cursor.execute(getColumnsNames)
            names = [row[0] for row in cursor.fetchall()]
            values_placeholder = ""
            if (is_2d_array(values) is True):
                for x in range (len(values)):
                    if (x != len(values) - 1):
                        values_placeholder += "(" + (" AND ".join([f"{z} = '{x}'" for x, z in zip(values[x], names)])) + ") OR "
                    else: 
                        values_placeholder += "(" + (" AND ".join([f"{z} = '{x}'" for x, z in zip(values[x], names)])) + ")"
            else: 
                values_placeholder = (" AND ".join([f"{z} = '{x}'" for x, z in zip(values[x], names)]))
            remove = f"DELETE FROM {tableName} WHERE {remove}"
            cursor.execute(remove)
            connection.commit()
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.close()
            connection.close()
    def DropTable(this,tableName):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()        
        try:
            cursor.execute(f"DROP TABLE {tableName}")
            connection.commit()
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.close()
            connection.close()
    def UpdateValue(this,tableName,ValueName,NewType):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()        
        try:
            cursor.execute(f"ALTER TABLE {tableName} CHANGE {ValueName} {ValueName} {NewType}")
            connection.commit()
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.close()
            connection.close()
    def AddColumn(this,tableName,NewvalueName,NewValueType):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()        
        try:
            cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {NewvalueName} {NewValueType}")
            connection.commit()
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.close()
            connection.close()   
    def removeColumn(this,tableName,ColumnName):
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()        
        try:
            cursor.execute(f"ALTER TABLE {tableName} DROP COLUMN {ColumnName};")
            connection.commit()
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.close()
            connection.close()
    def countRows(this,tableName):
        count = 1
        connection = Connect(this.host,this.port,this.user,this.password,this.database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(tableName))
        row = cursor.fetchone()
        count = 1
        while row is not None:
            count += 1
            row = cursor.fetchone()
        cursor.close()
        connection.close()
        return count
    def exists(this, tableName, value, columnName, WHERE):
        try:
            connection = Connect(this.host, this.port, this.user, this.password, this.database)
            cursor = connection.cursor()
            if WHERE is None:
                add_WHERE = ''
            else:
                add_WHERE = f'WHERE {WHERE}'
            cursor.execute(f"SELECT {columnName} FROM {tableName} {add_WHERE}")
            rows = cursor.fetchone()
            cursor.fetchall()
            cursor.close()
            connection.close()
            return rows is not None
        except mysql.connector.Error as e:
            print("An error happened:", e)
    def setDataBase(this,databaseName):
        try:
            connection = Connect(this.host,this.port,this.user,this.password,this.database)
            cursor = connection.cursor()
            cursor.execute(f"use {databaseName}")
            this.database = databaseName
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()                    
    def INNER_JOIN(this,columns,tableName_1,tableName_2,ON,WHERE,ORDER_BY):
        try:
            connection = Connect(this.host,this.port,this.user,this.password,this.database)
            cursor = connection.cursor()
            selected_columns = ", ".join(columns)
            if (WHERE is None):
                add_WHERE = ''
            else:
                add_WHERE = f'WHERE {WHERE}'
            if (ORDER_BY is None):
                add_ORDER_BY = ''
            else:
                add_ORDER_BY = f'ORDER BY {ORDER_BY}'
            cursor.execute(f"SELECT {selected_columns} FROM {tableName_1} INNER JOIN {tableName_2} ON {ON} {add_WHERE} {add_ORDER_BY}")
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()             
    def getValue(this,columnName,tableName,WHERE,ORDER_BY):
        try:
            connection = Connect(this.host,this.port,this.user,this.password,this.database)
            cursor = connection.cursor()
            if (WHERE is None):
                add_WHERE = ''
            else: 
                add_WHERE = f'WHERE {WHERE}'
            if (ORDER_BY is None):
                add_ORDER_BY = ''
            else:
                add_ORDER_BY = f'ORDER BY {ORDER_BY}'
            cursor.execute(f"SELECT {columnName} FROM {tableName} {add_WHERE} {add_ORDER_BY}") 
            print(f"SELECT {columnName} FROM {tableName} {add_WHERE} {add_ORDER_BY}")
            rows = cursor.fetchall()
            for i in range(len(rows)):
                x = str(rows[i])
                x = x.replace(")","")
                x = x.replace("(","")
                x = x.replace("'","")
                x = x.replace(",","")
                rows[i] = x
            return rows  
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:     
            connection.commit()
            cursor.close()
            connection.close() 
    def setValue(this,column,value,tableName,WHERE):
        try:
            connection = Connect(this.host,this.port,this.user,this.password,this.database)
            cursor = connection.cursor()
            if (WHERE is None):
                add_WHERE = ''
            else:
                add_WHERE = f'WHERE {WHERE}'
            cursor.execute(f"UPDATE {tableName} SET {column} = {value} {add_WHERE}")
        except mysql.connector.Error as e:
            print("An error Happened : ",e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()            