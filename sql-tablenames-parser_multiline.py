# Date: Thur June 27, 2019
# Filename: sql-tablenames-parser.py
# Short Discription: Extract Table/View Names
# Remarks:
#   1. Read a SQL SCRIPT in a STRING.
#   2. Prase and retrive TABLE/VIEWS used from the string.
#   3. Display the retrived Table/ View names.

import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False

def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                raise StopIteration
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True

def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value

def extract_tables(sql):
    stream = extract_from_part(sqlparse.parse(sql)[0])
    return list(extract_table_identifiers(stream))

# Main
def main():
    # Title
    print('\n\tSQL TABLES/VIEWS RETRIVAL PROGRAM v1.0\n')
    print('\t      Please Enter \'q\' to QUIT!\n')
    print('    ***MULTI-LINE/SINGLE-LINE SQL STATEMENTS***\n')
    
    raw = '7'
    print('\n\t-- Enter SQL Statement/Script(s): --')
    while (raw != 'q'):
        # Get SQL Query
        lines = []
        while True:
            line = input('> ')
            if line:
                lines.append(line)
            else:
                break
        
        sql_str = [x.lstrip(' ') for x in lines]    # Remove Trailing Whitespaces
        raw = ' '.join(sql_str)     # Join the lines and add one whitespace

        # Checking if the Join and split worked!
        # print(raw)
        
        if (raw == 'q'):
            print('\n\tThank you for using SQL Parser!')
            quit()
        
        # Testing
        # raw = "select * from spriden where spriden_change_ind is null;"
        # raw = """
        # Select max(SARADAP_APPL_NO) from SARADAP
        #    where SARADAP_PIDM = SPRIDEN_PIDM
        #      and SARADAP_APPL_NO = (select max(b.sarappd_appl_no) 
        #    from sarappd b
        #    where b.sarappd_pidm = spriden_pidm
        #      and saradap_appl_no = b.sarappd_appl_no));
        # """
        
        print('\n\t-- Displaying Tables/Views: --')
        tables = ', '.join(extract_tables(raw))
        print('Tables: {0}'.format(tables))


if __name__ == "__main__":
    main()

# End of Script!