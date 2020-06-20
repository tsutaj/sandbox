import argparse
import logging
import pandas as pd
import pathlib
import requests

diff_info = ("https://kenkoooo.com/atcoder/resources/problem-models.json", "./difficulty.json")
prob_info = ("https://kenkoooo.com/atcoder/resources/problems.json", "./problems.json")
result_json_info = ("hoge", "./result.json")
result_csv_info = ("hoge", "./result.csv")


def set_jsonfile(json_info, orient_index=True):
    orient_option = "columns"
    if orient_index:
        orient_option = "index"
        
    if pathlib.Path(json_info[1]).exists():
        df = pd.read_json(json_info[1])
    else:
        logging.warning("{} does not exist. fetching file from '{}' ...".format(json_info[1], json_info[0]))
        df = pd.DataFrame.from_dict(
            requests.get(json_info[0]).json(),
            orient=orient_option,
        )
    return df


def save_jsonfile(df, json_info):
    if not pathlib.Path(json_info[1]).exists():
        df.to_json(json_info[1])
    else:
        logging.warning("{} already exists. do nothing ...".format(json_info[1]))


def save_csvfile(df, csv_info):
    if not pathlib.Path(csv_info[1]).exists():
        df.to_csv(csv_info[1])
    else:
        logging.warning("{} already exists. do nothing ...".format(csv_info[1]))


def create_problem_url(contest_id, problem_id):
    return "https://atcoder.jp/contests/" + contest_id + "/tasks/" + problem_id
        

def main(min_difficulty, max_difficulty):
    """Find problems whose difficulty are in [min_difficulty, max_difficulty)."""
    diff_df = set_jsonfile(diff_info, True)
    prob_df = set_jsonfile(prob_info, False)
    save_jsonfile(diff_df, diff_info)
    save_jsonfile(prob_df, prob_info)

    # difficulty が NaN のものは除外
    diff_df = diff_df.dropna(subset=["difficulty"])
    # 指定した範囲の difficulty を持つもののみ残す
    diff_df = diff_df[ (diff_df["difficulty"] >= min_difficulty) \
              & (diff_df["difficulty"] < max_difficulty) ]
    # 不要な列を消す
    diff_df = diff_df.drop(columns=[
        "slope",
        "intercept",
        "variance",
        "discrimination",
        "irt_loglikelihood",
        "irt_users"
    ])

    # カラムを追加
    diff_df["title"] = "unknown"
    diff_df["contest_id"] = "unknown"
    diff_df["url"] = "unknown"
    # 問題名を入れる
    prob_df = prob_df.set_index("id")
    for prob_id in list(diff_df.index.values):
        diff_df.at[prob_id, "title"] = prob_df.at[prob_id, "title"]

        contest_id = prob_df.at[prob_id, "contest_id"]
        problem_url = create_problem_url(contest_id, prob_id)
        diff_df.at[prob_id, "url"] = problem_url
        
    # 列を入れ替える
    columns_diff = ["title", "url", "difficulty", "is_experimental"]
    diff_df = diff_df.reindex(columns=columns_diff)
    print(diff_df)
    
    save_jsonfile(diff_df, result_json_info)
    save_csvfile(diff_df, result_csv_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-min", "--min-difficulty", default=1600, type=int)
    parser.add_argument("-max", "--max-difficulty", default=2400, type=int)

    args = parser.parse_args()
    print(args)
    main(args.min_difficulty, args.max_difficulty)
