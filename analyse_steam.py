"""Menu-based analysis of Steam game data stored in a CSV file."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_FOLDER = Path(__file__).resolve().parent
CSV_FILE = PROJECT_FOLDER / "data" / "steam_games.csv"
OUTPUT_FOLDER = PROJECT_FOLDER / "outputs" / "graphs"


def load_game_data():
    """Read, check, and prepare the CSV data."""
    games = pd.read_csv(CSV_FILE)
    required_columns = [
        "game_name",
        "genre",
        "release_year",
        "price_usd",
        "positive_reviews",
        "negative_reviews",
        "average_playtime_hours",
        "estimated_owners_millions",
    ]

    missing_columns = [column for column in required_columns if column not in games.columns]
    if missing_columns:
        raise ValueError("CSV is missing these columns: " + ", ".join(missing_columns))

    games = games.dropna(subset=required_columns).copy()
    number_columns = required_columns[2:]
    for column in number_columns:
        games[column] = pd.to_numeric(games[column], errors="coerce")
    games = games.dropna(subset=number_columns)

    total_reviews = games["positive_reviews"] + games["negative_reviews"]
    review_percent = games["positive_reviews"].div(total_reviews.where(total_reviews != 0)) * 100
    games["positive_review_percent"] = review_percent.fillna(0)
    return games


def save_graph(file_name):
    """Save the graph and display it when a graphical backend is available."""
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    graph_path = OUTPUT_FOLDER / file_name
    plt.tight_layout()
    plt.savefig(graph_path)
    # IDLE normally uses a graphical backend, so the selected graph opens in a window.
    # The Agg backend is used in headless terminals and can only save the image.
    if plt.get_backend().lower() != "agg":
        plt.show()
    plt.close()
    print("Graph saved:", graph_path)


def make_owners_graph(games):
    top_games = games.nlargest(10, "estimated_owners_millions").sort_values(
        "estimated_owners_millions"
    )
    chart = top_games.set_index("game_name")["estimated_owners_millions"]
    axes = chart.plot(kind="barh", figsize=(10, 6), color="steelblue")
    axes.set_title("Top 10 Games by Estimated Owners")
    axes.set_xlabel("Estimated owners (millions)")
    axes.set_ylabel("Game")
    save_graph("01_top_games_by_owners.png")


def make_releases_graph(games):
    releases_by_year = games.groupby("release_year")["game_name"].count().sort_index()
    axes = releases_by_year.plot(
        kind="line", figsize=(10, 5), marker="o", color="darkorange"
    )
    axes.set_title("Number of Games Released Each Year")
    axes.set_xlabel("Release year")
    axes.set_ylabel("Games in this dataset")
    axes.grid(True, linestyle="--", alpha=0.4)
    save_graph("02_releases_by_year.png")


def make_genre_count_graph(games):
    genre_counts = games.groupby("genre").size().sort_values(ascending=False)
    axes = genre_counts.plot(kind="bar", figsize=(10, 6), color="mediumseagreen")
    axes.set_title("Number of Games by Genre")
    axes.set_xlabel("Genre")
    axes.set_ylabel("Number of games")
    axes.tick_params(axis="x", labelrotation=35)
    save_graph("03_games_by_genre.png")


def make_average_price_graph(games):
    average_prices = (
        games.groupby("genre")["price_usd"].mean().round(2)
        .sort_values(ascending=False)
    )
    axes = average_prices.plot(kind="bar", figsize=(10, 6), color="mediumpurple")
    axes.set_title("Average Game Price by Genre")
    axes.set_xlabel("Genre")
    axes.set_ylabel("Average price (USD)")
    axes.tick_params(axis="x", labelrotation=35)
    save_graph("04_average_price_by_genre.png")


def make_price_reviews_graph(games):
    axes = games.plot(
        kind="scatter",
        x="price_usd",
        y="positive_review_percent",
        figsize=(9, 6),
        color="crimson",
        alpha=0.7,
    )
    axes.set_title("Game Price and Positive Review Percentage")
    axes.set_xlabel("Price (USD)")
    axes.set_ylabel("Positive reviews (%)")
    plt.ylim(0, 105)
    axes.grid(True, linestyle="--", alpha=0.35)
    save_graph("05_price_vs_reviews.png")


def make_playtime_graph(games):
    playtime_by_genre = games.groupby("genre")["average_playtime_hours"].mean().sort_values()
    axes = playtime_by_genre.plot(kind="barh", figsize=(10, 6), color="teal")
    axes.set_title("Average Playtime by Genre")
    axes.set_xlabel("Average playtime (hours)")
    axes.set_ylabel("Genre")
    save_graph("06_average_playtime_by_genre.png")


def make_graphs(games):
    """Create all six graphs."""
    make_owners_graph(games)
    make_releases_graph(games)
    make_genre_count_graph(games)
    make_average_price_graph(games)
    make_price_reviews_graph(games)
    make_playtime_graph(games)


def show_intro():
    print("\nSTEAM GAME STORE DATA ANALYSIS")
    print("This project studies Steam game information stored in a CSV file.")
    print("It uses Pandas to analyse data and Matplotlib to create six graphs.")
    print("You can explore prices, genres, releases, reviews, and playtime.")


def show_data_info(games):
    print("\nDATASET INFORMATION")
    print("Number of games:", len(games))
    print("Number of genres:", games["genre"].nunique())
    print("Release years:", int(games["release_year"].min()), "to", int(games["release_year"].max()))
    print("Free games:", int((games["price_usd"] == 0).sum()))
    print("Paid games:", int((games["price_usd"] > 0).sum()))
    print("Columns:", ", ".join(games.columns))


def show_sample_games(games):
    columns = ["game_name", "genre", "release_year", "price_usd", "positive_review_percent"]
    print("\nFIRST 10 GAMES")
    print(games[columns].head(10).to_string(index=False))


def show_top_games(games):
    columns = ["game_name", "genre", "estimated_owners_millions"]
    top_games = games.nlargest(10, "estimated_owners_millions")[columns]
    print("\nTOP 10 GAMES BY ESTIMATED OWNERS (MILLIONS)")
    print(top_games.to_string(index=False))


def show_genre_report(games):
    genre_report = (
        games.groupby("genre")
        .agg(game_count=("game_name", "count"), average_price=("price_usd", "mean"))
        .round(2)
        .sort_values("game_count", ascending=False)
    )
    print("\nGENRE REPORT")
    print(genre_report.to_string())


def show_best_reviewed(games):
    columns = ["game_name", "positive_review_percent", "positive_reviews", "negative_reviews"]
    best_games = games.nlargest(10, "positive_review_percent")[columns]
    print("\nTOP 10 GAMES BY POSITIVE REVIEW PERCENTAGE")
    print(best_games.to_string(
        index=False,
        formatters={"positive_review_percent": "{:.1f}%".format},
    ))


def search_game(games):
    search_text = input("Enter a game name or part of a name: ").strip()
    if not search_text:
        print("Please enter a game name to search.")
        return

    matches = games[games["game_name"].str.contains(search_text, case=False, na=False)]
    if matches.empty:
        print("No matching games were found.")
    else:
        columns = ["game_name", "genre", "release_year", "price_usd", "positive_review_percent"]
        print(matches[columns].to_string(index=False))


def budget_game_finder(games):
    """Recommend games under a budget, with an optional genre filter."""
    try:
        maximum_price = float(input("Enter your maximum budget in USD: "))
    except ValueError:
        print("Please enter the budget as a number, such as 20 or 14.99.")
        return

    if maximum_price < 0:
        print("Budget cannot be negative.")
        return

    preferred_genre = input("Enter a genre, or type all: ").strip()
    matches = games[games["price_usd"] <= maximum_price].copy()

    if preferred_genre and preferred_genre.lower() != "all":
        matches = matches[matches["genre"].str.lower() == preferred_genre.lower()]

    if matches.empty:
        print("No games matched that budget and genre. Try a higher budget or another genre.")
        return

    recommendations = matches.nlargest(5, "positive_review_percent")
    columns = ["game_name", "genre", "price_usd", "positive_review_percent"]
    print("\nTOP PICKS WITHIN YOUR BUDGET")
    print(recommendations[columns].to_string(
        index=False,
        formatters={"positive_review_percent": "{:.1f}%".format},
    ))

    # Plot the positive review percentage of the recommended games.
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    axes = recommendations.plot(
        kind="bar",
        x="game_name",
        y="positive_review_percent",
        figsize=(9, 5),
        legend=False,
        color="cornflowerblue",
    )
    axes.set_title("Top Game Picks Under ${:.2f}".format(maximum_price))
    axes.set_xlabel("Game")
    axes.set_ylabel("Positive reviews (%)")
    axes.tick_params(axis="x", labelrotation=30)
    plt.ylim(0, 100)
    recommendation_chart = OUTPUT_FOLDER / "07_budget_game_finder.png"
    plt.savefig(recommendation_chart)
    plt.close()
    print("Recommendation chart saved to:", recommendation_chart)


def generate_graphs(games):
    make_graphs(games)
    print("\nAll six graphs have been saved in:", OUTPUT_FOLDER)


def show_graph_menu(games):
    """Let the user create one selected graph or all six graphs."""
    while True:
        print("\nGRAPH MENU")
        print("1. Top 10 games by estimated owners")
        print("2. Number of games released each year")
        print("3. Number of games by genre")
        print("4. Average game price by genre")
        print("5. Price and positive reviews")
        print("6. Average playtime by genre")
        print("7. Generate all six graphs")
        print("0. Return to the main menu")
        choice = input("Choose a graph: ").strip()

        if choice == "1":
            make_owners_graph(games)
        elif choice == "2":
            make_releases_graph(games)
        elif choice == "3":
            make_genre_count_graph(games)
        elif choice == "4":
            make_average_price_graph(games)
        elif choice == "5":
            make_price_reviews_graph(games)
        elif choice == "6":
            make_playtime_graph(games)
        elif choice == "7":
            generate_graphs(games)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select a number from the graph menu.")


def show_menu():
    print("\n" + "=" * 42)
    print("STEAM GAME STORE DATA ANALYSIS")
    print("=" * 42)
    print("1. Project introduction")
    print("2. Dataset information")
    print("3. Show first 10 games")
    print("4. Show top 10 games by estimated owners")
    print("5. Show genre report")
    print("6. Show top 10 games by positive reviews")
    print("7. Search for a game")
    print("8. Open the graph menu")
    print("9. Find top-rated games within a budget")
    print("0. Exit")


def main():
    try:
        games = load_game_data()
    except FileNotFoundError:
        print("Could not find the CSV file:", CSV_FILE)
        print("Make sure data/steam_games.csv is in the project folder.")
        return
    except ValueError as error:
        print(error)
        return

    if games.empty:
        print("There are no complete game records to analyse.")
        return

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            show_intro()
        elif choice == "2":
            show_data_info(games)
        elif choice == "3":
            show_sample_games(games)
        elif choice == "4":
            show_top_games(games)
        elif choice == "5":
            show_genre_report(games)
        elif choice == "6":
            show_best_reviewed(games)
        elif choice == "7":
            search_game(games)
        elif choice == "8":
            show_graph_menu(games)
        elif choice == "9":
            budget_game_finder(games)
        elif choice == "0":
            print("Thank you for using the project.")
            break
        else:
            print("Invalid choice. Please select a number from the menu.")


if __name__ == "__main__":
    main()
