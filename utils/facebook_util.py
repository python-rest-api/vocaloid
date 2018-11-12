import facebook


def get_facebook_profile(access_token):
    try:
        graph = facebook.GraphAPI(access_token=access_token, version='2.7')
        args = {
            'fields': 'id, name, email, first_name, last_name, gender, locale,'
                      'hometown, quotes, languages, relationship_status, education,'
                      'political, religion, location, website, link, birthday, about,'
                      'work, interested_in, timezone, picture', }
        profile = graph.get_object('me', **args)
        return profile
    except Exception as ex:
        print(ex)
    return None
