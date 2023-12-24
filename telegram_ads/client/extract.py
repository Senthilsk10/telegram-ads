import re

def extract_content(file_info):
    # Define regular expressions for each field
    file_name_pattern = re.compile(r'File name: (.+)')
    series_movie_pattern = re.compile(r'series/movie: (.+)')
    part_pattern = re.compile(r'part: (.+)')
    season_pattern = re.compile(r'season: (.+)')
    episode_pattern = re.compile(r'episode: (.+)')
    language_pattern = re.compile(r'language: (.+)')
    quality_pattern = re.compile(r'quality: (.+)')

    # Initialize dictionary to store extracted values
    extracted_content = {
        'file_name': None,
        'series_movie': None,
        'part': None,
        'season': None,
        'episode': None,
        'language': None,
        'quality': None
    }

    # Split lines based on newline character
    lines = file_info.split('\n')

    # Check if the template has the expected structure
    if len(lines) != 7:
        raise ValueError("Error: Invalid template structure. Please check the template.")

    # Extract values using regular expressions
    match = file_name_pattern.search(lines[0])
    if match:
        extracted_content['file_name'] = match.group(1)
    

    match = series_movie_pattern.search(lines[1])
    if match:
        extracted_content['series_movie'] = match.group(1)
    
    match = part_pattern.search(lines[2])
    if match:
        extracted_content['part'] = match.group(1)
    
    match = season_pattern.search(lines[3])
    if match:
        extracted_content['season'] = match.group(1)
    

    match = episode_pattern.search(lines[4])
    if match:
        extracted_content['episode'] = match.group(1)
    

    match = language_pattern.search(lines[5])
    if match:
        extracted_content['language'] = match.group(1)
   

    match = quality_pattern.search(lines[6])
    if match:
        extracted_content['quality'] = match.group(1)

    return extracted_content
