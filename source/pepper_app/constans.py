CSV_COLUMNS=['item_id', 'name', 'discount_price', 'percentage_discount',
            'regular_price', 'date_added', 'url']

DATA_HEADER=['item_id', 'name', 'discount_price',
                'percentage_discount', 'regular_price',
                'date_added', 'url']

STATS_HEADER=['category_type', 'start_page', 'retrieved_articles_quantity',
            'time_of_the_action', 'action_execution_datetime', 'searched_article',
            'to_csv', 'to_database', 'scrap_continuously', 'scrap_choosen_data']

REQUEST_HEADER=['request_id', 'user_id', 'request_time', 'desired_article', 'desired_price']

RESPONSE_HEADER=['response_id', 'request_id', 'response_time', 'item_id']

OLD_DATES_DATA_PATTERN_1=r"[A-Za-z]+\s\d\d\.\s[0-9]+"
OLD_DATES_DATA_PATTERN_2=r"[A-Za-z]+\s\d\.\s[0-9]+"