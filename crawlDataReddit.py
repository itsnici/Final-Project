import praw
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

def setup_reddit():
    """setup reddit api connection"""
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    return reddit

def get_politician_info(keyword, politicians_info):
    """Get party and gender information for a politician"""
    return politicians_info.get(keyword, {})

def collect_comments_for_politicians(politicians_dict, politicians_info, limit=10):
    """
    collect comments data for multiple politicians
    politicians_dict: dictionary, containing keywords and full names of politicians
    politicians_info: dictionary containing party and gender information
    """
    reddit = setup_reddit()
    all_comments_data = []
    
    for keyword, full_name in tqdm(politicians_dict.items(), desc="Collecting data for politicians"):
        print(f"\nCollecting data for {full_name}...")
        politician_info = get_politician_info(keyword, politicians_info)
        
        try:
            for submission in reddit.subreddit('all').search(f'"{full_name}"', limit=limit):
                print(f"Processing post: {submission.title[:50]}...")
                
                submission.comments.replace_more(limit=0)
                
                for comment in submission.comments.list():
                    comment_data = {
                        'politician': full_name,
                        'search_keyword': keyword,
                        'party': politician_info.get('party', 'Unknown'),
                        'gender': politician_info.get('gender', 'Unknown'),
                        'post_title': submission.title,
                        'post_id': submission.id,
                        'post_url': f"https://reddit.com{submission.permalink}",
                        'comment_body': comment.body,
                        'comment_score': comment.score,
                        'comment_created': datetime.fromtimestamp(comment.created_utc),
                        'comment_id': comment.id
                    }
                    all_comments_data.append(comment_data)
                
                time.sleep(1)
                
        except Exception as e:
            print(f"Error collecting data for {full_name}: {e}")
            continue
    
    return pd.DataFrame(all_comments_data)

def save_to_csv(df, filename):
    """save data to csv file"""
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")

def main():
    # define politicians to study with their full names
    politicians = {
        # Democratic Women
        'Harris': 'Kamala Harris',
        'AOC': 'Alexandria Ocasio-Cortez',
        'Pelosi': 'Nancy Pelosi',
        
        # Republican Women
        'Haley': 'Nikki Haley',
        'Greene': 'Marjorie Taylor Greene',
        'Cheney': 'Liz Cheney',
        
        # Democratic Men
        'Biden': 'Joe Biden',
        'Sanders': 'Bernie Sanders',
        
        # Republican Men
        'Trump': 'Donald Trump',
        'DeSantis': 'Ron DeSantis'
    }
    
    # define additional information for each politician
    politicians_info = {
        'Harris': {'party': 'Democratic', 'gender': 'Female'},
        'AOC': {'party': 'Democratic', 'gender': 'Female'},
        'Pelosi': {'party': 'Democratic', 'gender': 'Female'},
        'Haley': {'party': 'Republican', 'gender': 'Female'},
        'Greene': {'party': 'Republican', 'gender': 'Female'},
        'Cheney': {'party': 'Republican', 'gender': 'Female'},
        'Biden': {'party': 'Democratic', 'gender': 'Male'},
        'Sanders': {'party': 'Democratic', 'gender': 'Male'},
        'Trump': {'party': 'Republican', 'gender': 'Male'},
        'DeSantis': {'party': 'Republican', 'gender': 'Male'}
    }
    
    print("Starting data collection...")
    df = collect_comments_for_politicians(politicians, politicians_info, limit=10)
    
    print("\nCollection Complete!")
    print(f"Total comments collected: {len(df)}")
    
    print("\nComments per politician:")
    print(df['politician'].value_counts())
    
    print("\nComments by party:")
    print(df['party'].value_counts())
    
    print("\nComments by gender:")
    print(df['gender'].value_counts())
    
    filename = f"politicians_comments_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    save_to_csv(df, filename)
    
    print("\nSample of collected data:")
    print(df.head())

if __name__ == "__main__":
    main()