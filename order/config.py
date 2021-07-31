from collections import defaultdict

URL = "https://9v8upsmsai.execute-api.us-east-1.amazonaws.com/prod/biz/orders"
TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxbWVudSIsInJlc3RhdXJhbnQiOiJ7XCJuYW1lXCI6XCJTaWNodWFuIEdvdXJtZXRcIixcImlkXCI6XCI1OWI1ODZlY2I3YTQ5ZjExMDAwN2JiYTVcIn0ifQ.FdnUPZ-O57qOpeN3ilfLKEVjt9z79IN8Q_V_NIMsn6k"

# db file to write order to
# DB_FILE = "Y:\\new-01-16.mdb"

DB_FILE = "C:\\Users\laosichuan\\Desktop\\new-01-16.mdb"

'''
    menu mapping

    qmenu_menu_id : lsc_menu_id
'''
MENU_ITEM_MAP = {
    # empty id
    "" : "",
    '1-4-1': '21',
    '1-4-2': '23',
    '1-4-3': '24',
    '1-3-1': '75',
    '1-3-2': '76',
    '1-3-3': '77',
    '1-3-4': '78',
    '1-3-7': '81',
    '1-3-5': '82',
    '1-3-8': '83',
    '1-3-6': '85',
    '1-7-1': '86',
    '1-7-3': '87',
    '1-7-4': '88',
    '1-7-6': '89',
    '1-7-7': '92',
    '1-7-5': '100',
    '1-7-8': '101',
    '1-2-2': '112',
    '1-2-4': '113',
    '1-2-3': '114',
    '1-1-6': '115',
    '1-2-1': '116',
    '1-1-1': '120',
    '1-1-4': '121',
    '1-1-6': '122',
    '1-1-7': '123',
    '1-1-8': '124',
    '1-1-9': '125',
    '1-1-10': '126',
    '1-1-5': '127',
    '1-1-11': '128',
    '1-1-12': '130',
    '1-1-13': '131',
    '1-1-2': '213',
    '1-1-1': '214',
    '1-2-5': '241',
    '1-7-2': '267',
    '1-1-3': '277',
    '1-4-4': '390',
    '1-4-5': '391',
    '1611338659848': '440'
}
