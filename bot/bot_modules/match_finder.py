"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   11/28/2016
Version:            v2.0
==========================================
"""

from utils.subscription import Subscription


class MatchFinder:

    @staticmethod
    def is_match(subscription, submission):
        result = True
        mismatched_keys = []
        for key in subscription.data.keys():
            if key == Subscription.TITLE:
                title_match = False
                # Empty title_list is automatically 'True' because it has no effect on result
                if len(subscription.data[key]) == 0:
                    title_match = True
                for title_list in subscription.data[key]:
                    title_list_match = True
                    for item in title_list:
                        if item.lower() not in submission.title.lower():
                            title_list_match = False
                    title_match = title_match or title_list_match
                if not title_match:
                    mismatched_keys.append(key)
                result = result and title_match
            if key == Subscription.BODY:
                body_match = False
                # Empty body_list is automatically 'True' because it has no effect on result
                if len(subscription.data[key]) == 0:
                    body_match = True
                for body_list in subscription.data[key]:
                    body_list_match = True
                    for item in body_list:
                        body_content = submission.selftext.lower() if submission.is_self else submission.url.lower()
                        if item.lower() not in body_content:
                            body_list_match = False
                    body_match = body_match or body_list_match
                if not body_match:
                    mismatched_keys.append(key)
                result = result and body_match
            elif key == Subscription.REDDITORS:
                redditor_match = False
                if len(subscription.data[key]) == 0:
                    redditor_match = True
                for redditor in subscription.data[key]:
                    if redditor.lower() == str(submission.author).lower():
                        redditor_match = True
                if not redditor_match:
                    mismatched_keys.append(key)
                result = result and redditor_match
            elif key == Subscription.IGNORE_TITLE:
                ignore_title_match = True
                for item in subscription.data[key]:
                    if item.lower() in submission.title.lower():
                        ignore_title_match = False
                        mismatched_keys.append(key)
                result = result and ignore_title_match
            elif key == Subscription.IGNORE_BODY:
                ignore_body_match = True
                for item in subscription.data[key]:
                    body_content = submission.selftext.lower() if submission.is_self else submission.url.lower()
                    if item.lower() in body_content:
                        ignore_body_match = False
                        mismatched_keys.append(key)
                result = result and ignore_body_match
            elif key == Subscription.IGNORE_REDDITORS:
                ignore_redditors_match = True
                for redditor in subscription.data[key]:
                    if redditor.lower() == str(submission.author).lower():
                        ignore_redditors_match = False
                        mismatched_keys.append(key)
                result = result and ignore_redditors_match
            elif key == Subscription.NSFW:
                if submission.over_18 and not subscription.data[key]:
                    result = result and False
                    mismatched_keys.append(key)
        return result, sorted(set(mismatched_keys))

    @staticmethod
    def find_matches(subscriptions, reddit, database):
        subreddits = {}
        matches = []
        for subscription in subscriptions:
            subreds = subscription.data[Subscription.SUBREDDITS]
            for subreddit in subreds:
                if subreddit.lower() not in [k.lower() for k in subreddits.keys()]:
                    print(subreddit.lower())
                    submissions = reddit.get_submissions(subreddit.lower())
                    temp = []
                    for sub in submissions:
                        temp.append(sub)
                    subreddits[subreddit.lower()] = temp
                submissions = subreddits[subreddit.lower()]
                # submissions = reddit.get_submissions(subreddit)
                num = 0
                for submission in submissions:
                    num += 1
                    is_match, mismatched_keys = MatchFinder.is_match(subscription, submission)
                    if is_match:
                        already_exists = database.check_if_match_exists(subscription.username,
                                                                        subscription.to_string(),
                                                                        submission.permalink)
                        if not already_exists:
                            matches.append((subscription, submission))
        return matches
