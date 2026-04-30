import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows"""
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"✅ Removed {before - after:,} duplicates")
    return df


def filter_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Filter ratings to be between 1 and 5"""
    df = df[df["rating"].between(1, 5)]
    print(f"✅ Ratings filtered: {df.shape[0]:,} rows remaining")
    return df


def filter_active_users(df: pd.DataFrame, min_ratings: int = 5) -> pd.DataFrame:
    """Keep only users with at least min_ratings ratings"""
    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_ratings].index
    df = df[df["user_id"].isin(active_users)]
    print(f"✅ Active users filtered: {df["user_id"].nunique():,} users remaining")
    return df


def filter_popular_products(df: pd.DataFrame, min_ratings: int = 5) -> pd.DataFrame:
    """Keep only products with at least min_ratings ratings"""
    product_counts = df["product_id"].value_counts()
    popular_products = product_counts[product_counts >= min_ratings].index
    df = df[df["product_id"].isin(popular_products)]
    print(f"✅ Popular products filtered: {df["product_id"].nunique():,} products remaining")
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full preprocessing pipeline

    Parameters:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("🔄 Starting preprocessing pipeline...")
    df = remove_duplicates(df)
    df = filter_ratings(df)
    df = filter_active_users(df, min_ratings=5)
    df = filter_popular_products(df, min_ratings=5)
    print(f"✅ Preprocessing complete!")
    print(f"📊 Final Shape: {df.shape}")
    print(f"👥 Final Unique Users: {df["user_id"].nunique():,}")
    print(f"📦 Final Unique Products: {df["product_id"].nunique():,}")
    return df


def save_clean_data(df: pd.DataFrame, path: str) -> None:
    """Save cleaned data to CSV"""
    df.to_csv(path, index=False)
    print(f"✅ Clean data saved to: {path}")


if __name__ == "__main__":
    from ingest import load_ratings
    DATA_PATH = "/content/drive/MyDrive/recommendation-data/Electronics.csv"
    SAVE_PATH = "/content/drive/MyDrive/recommendation-data/ratings_clean.csv"
    df = load_ratings(DATA_PATH)
    df = preprocess(df)
    save_clean_data(df, SAVE_PATH)
