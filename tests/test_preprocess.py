import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "data")))

from preprocess import (
    remove_duplicates,
    filter_ratings,
    filter_active_users,
    filter_popular_products,
    preprocess
)

def get_sample_data():
    return pd.DataFrame({
        "user_id":    ["u1", "u1", "u1", "u1", "u1", "u2", "u2", "u2", "u2", "u2", "u1"],
        "product_id": ["p1", "p2", "p3", "p4", "p5", "p1", "p2", "p3", "p4", "p5", "p1"],
        "rating":     [5,    4,    3,    2,    1,    4,    3,    2,    1,    5,    5  ],
        "date":       pd.to_datetime(["2021-01-01"] * 11)
    })

def test_remove_duplicates():
    df = get_sample_data()
    result = remove_duplicates(df)
    assert result.duplicated().sum() == 0
    print("✅ test_remove_duplicates passed!")

def test_filter_ratings():
    df = get_sample_data()
    df.loc[0, "rating"] = 6
    df.loc[1, "rating"] = 0
    result = filter_ratings(df)
    assert result["rating"].between(1, 5).all()
    print("✅ test_filter_ratings passed!")

def test_filter_active_users():
    df = get_sample_data()
    df = remove_duplicates(df)
    result = filter_active_users(df, min_ratings=5)
    user_counts = result["user_id"].value_counts()
    assert (user_counts >= 5).all()
    print("✅ test_filter_active_users passed!")

def test_filter_popular_products():
    df = get_sample_data()
    df = remove_duplicates(df)
    result = filter_popular_products(df, min_ratings=2)
    product_counts = result["product_id"].value_counts()
    assert (product_counts >= 2).all()
    print("✅ test_filter_popular_products passed!")

def test_preprocess():
    df = get_sample_data()
    result = preprocess(df)
    assert result.duplicated().sum() == 0
    assert result["rating"].between(1, 5).all()
    assert result.isnull().sum().sum() == 0
    print("✅ test_preprocess passed!")

if __name__ == "__main__":
    print("🔄 Running all tests...\n")
    test_remove_duplicates()
    test_filter_ratings()
    test_filter_active_users()
    test_filter_popular_products()
    test_preprocess()
    print("\n🎉 All tests passed!")
