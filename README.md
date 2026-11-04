# Steam Game Store Data Analysis

A beginner-friendly Class 12 Informatics Practices project. It reads game records from a CSV file, analyses them with Pandas, and displays or saves graphs through a numbered menu.

## Important note about the data

`data/steam_games.csv` is a small **illustrative sample** for learning how the project works. Its review counts, owner estimates, prices, and playtime values are not verified official Steam statistics. Replace it with a real dataset if your teacher requires authentic data.

## Menu options

1. Project introduction.
2. Dataset information.
3. Show the first ten games.
4. Show the top ten games by estimated owners.
5. Show a genre report.
6. Show the top ten games by positive review percentage.
7. Search for a game by name.
8. Open the graph menu to create one selected graph or all six.
9. Find up to five top-rated games within a budget and optional genre.
0. Exit.

From the graph menu, choose a number to create just that graph, or choose 7 to create all six. Each graph is saved as its own PNG file in `outputs/graphs/`:

1. Top 10 games by estimated owners.
2. Number of games released each year.
3. Number of games by genre.
4. Average game price by genre.
5. Game price compared with positive review percentage.
6. Average playtime by genre.

Option 9 filters games by the maximum price you enter and, if selected, by genre. It ranks the matching games by positive review percentage and saves a comparison chart as `outputs/graphs/07_budget_game_finder.png`.

## CSV columns

| Column | Meaning |
| --- | --- |
| `game_name` | Name of the game |
| `genre` | Main game genre |
| `release_year` | Release year |
| `price_usd` | Price in US dollars; `0` means free to play |
| `positive_reviews` | Number of positive reviews in the sample |
| `negative_reviews` | Number of negative reviews in the sample |
| `average_playtime_hours` | Average playtime in hours |
| `estimated_owners_millions` | Estimated owners, in millions |

When using another CSV, keep these column names or update `required_columns` and the graph code in `analyse_steam.py`.

## Run the project

Install Python 3, then open a terminal in this folder and run:

Windows:

```bash
python -m pip install -r requirements.txt
python analyse_steam.py
```

macOS or Linux:

```bash
python3 -m pip install -r requirements.txt
python3 analyse_steam.py
```

Each graph uses Pandas' `.plot()` method. In IDLE or another graphical Python session, the selected chart opens in a window; close the window to return to the menu. The program also saves every chart as a separate PNG file in `outputs/graphs/`. In a headless terminal, it saves the PNG without opening a window.

## Run from IDLE on Linux

1. Open a terminal in the `steam_game_analysis` folder.
2. Start the Python file in IDLE by running `idle analyse_steam.py` (on some systems, use `idle3 analyse_steam.py`).
3. In the IDLE editor, choose **Run → Run Module** or press **F5**.
4. Use the IDLE Shell to enter menu choices. For option 9, enter a budget and then a genre, or type `all`.

Install the libraries first in the same Python installation that IDLE uses:

```bash
python3 -m pip install -r requirements.txt
```

## Class 12 IP topics used

- Pandas: reading CSV files, DataFrames, selecting columns, cleaning missing values, grouping data, and calculating averages.
- Pandas `.plot()` and Matplotlib: line, bar, horizontal bar, and scatter plots with titles and axis labels; graphs are displayed when a graphical backend is available and also saved as PNG files.
- Real-world problem solving: summarising game prices, genres, reviews, release years, and playtime.
