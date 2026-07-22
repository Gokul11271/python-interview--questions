import praw
import time

# ----------------------------
# Reddit Credentials
# ----------------------------
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    user_agent="Subreddit Joiner by YOUR_USERNAME"
)

# ----------------------------
# List of Subreddits
# ----------------------------
subreddits = [
    "freelance_forhire",
    "DigitalIncomePath",
    "WFHJobs",
    "parttimejobs",
    "Collaboration",
    "hiring",
    "freelancing",
    "remoteworking",
    "RemoteJobs",
    "slavelabour",
    "LookingforJob",
    "B2BForHire",
    "sideJobs",
    "forhire",
    "RecruitmentHub",
    "freelancerguide",
    "hireforgigs",
    "PaidOnlineJobs"
]

# ----------------------------
# Join Subreddits
# ----------------------------
print("Starting...\n")

for name in subreddits:
    try:
        reddit.subreddit(name).subscribe()
        print(f"✓ Joined r/{name}")
        time.sleep(2)   # Avoid hitting API rate limits
    except Exception as e:
        print(f"✗ Failed r/{name}")
        print(e)

print("\nDone!")