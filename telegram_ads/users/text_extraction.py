def parse_file_details(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Initialize an empty dictionary to store key-value pairs
    details = {}

    # Find the index of 'movie' or 'series' to determine the type
    type_index = None
    for i, word in enumerate(words):
        if word.lower() == 'movie' or word.lower() == 'series':
            type_index = i
            details['type'] = word.lower()
            break

    # If the type is not found, return an empty dictionary
    if 'type' not in details:
        return details

    # Extract the name using the type_index
    details['name'] = ' '.join(words[:type_index]).strip()

    # Iterate through the words after the type_index to extract information
    for i in range(type_index + 1, len(words)):
        if words[i].lower() == 'season':
            # If the word is 'season', get the season number
            details['season'] = words[i + 1]
        elif words[i].lower() == 'ep' or words[i].lower() == 'episode':
            # If the word is 'ep' or 'episode', get the episode number
            details['episode'] = words[i + 1]
        elif words[i].lower() in ['360p','720p', '480p', '1080p']:
            # If the word is a resolution, set the quality
            details['quality'] = words[i].lower()
        elif words[i].lower() in ['english', 'tamil', 'malayalam','telumgu','eng','tam','mal','tel']:
            # If the word is a language, set the language
            details['language'] = words[i].lower()
        elif words[i].lower() == 'year':
            # If the word is 'year', get the year
            details['year'] = words[i + 1]

    return details