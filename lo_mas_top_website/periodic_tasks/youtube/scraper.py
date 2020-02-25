import requests, sys, time, os
import inspect
from background_task import background
from posts.models import Post

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# List of simple to collect features
snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

# Used to identify columns, currently hardcoded order
header = ["video_id"] + ['video_link'] + snippet_features + ["trending_date", 
                                            "view_count",
                                            "likes", 
                                            "dislikes",
                                            "comment_count"]


def setup(api_path, code_path):

    with open(api_path, 'r') as file:
        api_key = file.readline()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes


def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(page_token, country_code, api_key):
    # Builds the URL and requests the JSON from it
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    print(request_url)
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


def get_videos(items):
    lines = []
    for video in items:
        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue

        # A full explanation of all of these features can be found on the GitHub page for this project
        video_id = prepare_feature(video['id'])
        video_link = prepare_feature('https://www.youtube.com/watch?v=' + video['id'])

        # Snippet and statistics are sub-dicts of video, containing the most useful info
        snippet = video['snippet']
        statistics = video['statistics']

        # This list contains all of the features in snippet that are 1 deep and require no special processing
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]

        # The following are special case features which require unique processing, or are not within the snippet dict
        #description = snippet.get("description", "")
        # thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        # tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)

        # This may be unclear, essentially the way the API works is that if a video has comments or ratings disabled
        # then it has no feature for it, thus if they don't exist in the statistics dict we know they are disabled
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comment_count = 0

        # Compiles all of the various bits of info into one consistently formatted line
        line = [video_id] + [video_link] + features + [prepare_feature(x) for x in [trending_date,
                                                                     view_count, 
                                                                     likes, 
                                                                     dislikes,
                                                                     comment_count]]
        lines.append(",".join(line))
    return lines


def get_pages(country_code, api_key, next_page_token="&"):
    country_data = []

    # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
    # more inconvenient to iterate over pages, but that is what is done here.
    while next_page_token is not None:
        # A page of data i.e. a list of videos and all needed data
        print('Scrapping... ', next_page_token)
        video_data_page = api_request(next_page_token, country_code, api_key)

        # Get the next page token and build a string which can be injected into the request with it, unless it's None,
        # then let the whole thing be None so that the loop ends after this cycle
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

        # Get all of the items as a list and let get_videos return the needed features
        items = video_data_page.get('items', [])
        country_data += get_videos(items)

    return country_data


def save(country_data, country_code):
    print(f"Saving {country_code} data to DB...")
    for idx ,row in enumerate(country_data):
        if(idx > 0):
            post_data = row.split(',')
            post = Post()
            post.title = post_data[2].replace('"', '')
            post.link    = post_data[0].replace('"', '')
            post.description = post_data[1].replace('"', '')
            post.source = 'YOUTUBE'

            post.save()

def write_to_file(country_code, country_data, output_dir):
    print(f"Writing {country_code} data to file...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/dataset_youtube_{time.strftime('%y.%d.%m')}_{country_code}.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")

@background(schedule=60)
def get_data():
    print('Starting scraper Youtube trends...')
    print('Getting data...')
    output_dir = os.path.join(BASE_DIR, 'youtube', 'output/')
    api_key_file = os.path.join(BASE_DIR, 'youtube', 'api_key.txt')
    country_codes_file = os.path.join(BASE_DIR, 'youtube', 'country_codes.txt')
    api_key, country_codes = setup(api_key_file , country_codes_file)
    for country_code in country_codes:
        country_data = [",".join(header)] + get_pages(country_code, api_key)
        write_to_file(country_code, country_data, output_dir)
        save(country_data, country_code)