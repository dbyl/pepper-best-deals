from pepper_app.models import UserRequest
from django.db.models import Q, Count
from pepper_app.populate_database import LoadSuccessfulResponse


class Notifications:

    def __init__(self, item_df):
        self.item_df = item_df


    def check_conditions(self, desired_name_list, request_id, article_name_list):

        matched = all(item in article_name_list for item in desired_name_list)

        if matched:
            LoadSuccessfulResponse()


    def matching_request(self):
        
        LoadSuccessfulResponse()


        # Initialize conditions with a default condition
        conditions = Q()

        for _, row in self.item_df.iterrows():
            #item_id = row["item_id"],
            article_name = row["name"]
            #discount_price = row["discount_price"],
            #percentage_discount = row["percentage_discount"],
            #regular_price = row["regular_price"],
            #date_added = row["date_added"],
            #url = row["url"],
         #   list_of_words_article_name = article_name.split()

            # Create a new condition for each word in the article name
     #   for word in list_of_words_article_name:
      #      conditions &= Q(desired_article__icontains=word)
        
        desired_article = article_name
        # Filter UserRequest objects based on the conditions and order by request_time
        successful_responses = UserRequest.objects.values(article_name).annotate(count=Count('request_id')).filter(count__gt=1)
       # successful_responses = UserRequest.objects.filter(conditions).order_by('-request_time')

    

        return successful_responses

    def populate_successful_response_db(self, successful_responses):

        for successful_response in successful_responses:
            
            pass


    def check_if_item_in_user_requests(self, data) -> bool:
            

            
            
            # check if in database exists item from user's requests

                # if exists then successful response,  delete the user's request, run fuction sending email/sms


        pass


'''
def load_to_db(self) -> None:
        data = self.item
        item_df = pd.DataFrame([data], columns=DATA_HEADER)
        for _, row in item_df.iterrows():
            try:
                pepperarticle_obj, _ = PepperArticle.objects.get_or_create(
                    item_id = row["item_id"],
                    article_name = row["name"],
                    discount_price = self.na_discount_price(row),
                    percentage_discount = self.na_percentage_discount(row),
                    regular_price = self.na_regular_price(row),
                    date_added = row["date_added"],
                    url = row["url"],
                )
            except Exception as e:
                with open("populating_detailstodb_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


 def searching_conditions(self, request):
        """Adding conditions for better data filtering. 
        Necessary to improve the search by name and to include expressions to be ignored."""
        conditions = Q()

        searched_article_list = request.session.get('searched_article').split()
        excluded_terms = request.session.get('excluded_terms')

        if len(excluded_terms) != 0:
            excluded_terms_list = excluded_terms.split(', ')
            for term in excluded_terms_list:
                conditions &= ~Q(article_name__icontains=term)
        
        for word in searched_article_list:
            conditions &= Q(article_name__icontains=word)
        
        return conditions


    def get(self, request):

        conditions = self.searching_conditions(request)  

        results = PepperArticle.objects.filter(conditions).order_by('date_added')[:request.session.get("searched_articles_to_retrieve")][::-1]

        session_variables = {"searched_articles_to_retrieve": False,
                            "searched_article": False,
                            "scrape_data": False,
                            "excluded_terms": False,}
                
        request.session.update(session_variables)

        context = {"results": results}

        return render(request, self.template_name, context)
'''