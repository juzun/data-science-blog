from typing import Dict, List

import numpy as np
import pandas as pd
from plotly import graph_objects as po


def search_for_columns_with_keyword(
    data: Dict[str, pd.DataFrame], keywords: List[str]
) -> Dict[int, List[str]]:
    """
    Searches for columns in data frames within the provided dictionary that contain any of the specified keywords.

    Attributes:
        data (Dict[str, pd.DataFrame]): A dictionary where keys are identifiers and values are data frames to search within.
        keywords (List[str]): A list of keywords to search for in column names.

    Returns:
        Dict[int, List[str]]: A dictionary mapping each key in 'data' to a list of column names containing any of the keywords.
    """
    return {
        key: [
            col
            for col in data[key].columns
            if any(keyword in col.lower() for keyword in keywords)
        ]
        for key in data
        if any(
            keyword in col.lower() for col in data[key].columns for keyword in keywords
        )
    }


def categorize_gender(value: str) -> str:
    """
    Categorizes a given gender string into 'Male', 'Female' and 'Queer/Non-binary'. The one with 'Other' is jsut formal, not used in the code later.

    Attributes:
        value (str): The gender description to categorize.

    Returns:
        str: The standardized gender category ('Male', 'Female', 'Queer/Non-binary', or 'Other').
    """
    value = value.lower()
    if (
        "non-binary" in value
        or "genderqueer" in value
        or "gender non-conforming" in value
        or "queer" in value
    ):
        return "Queer/Non-binary"
    elif "woman" in value or "female" in value:
        return "Female"
    elif ("man" in value and "woman" not in value) or (
        "male" in value and "female" not in value
    ):
        return "Male"
    else:
        return "Other"


def prepare_remote_work_data(
    data: pd.DataFrame, column_map: Dict[int, str], category_map: Dict[str, str]
) -> pd.DataFrame:
    """
    Prepares remote work data by standardizing and calculating yearly remote work proportions.

    Attributes:
        data (pd.DataFrame): The survey data containing remote work information across years.
        column_map (Dict[int, str]): A dictionary mapping years to the column names with remote work data for that year.
        category_map (Dict[str, str]): A dictionary mapping raw categories to standardized remote work categories.

    Returns:
        pd.DataFrame: A dataframe with columns 'Year', 'State', 'Count', 'Yearly total', and 'Proportional',
                      showing the proportion of each remote work category by year.
    """
    work_remote_data = []
    for year, column in column_map.items():
        counts = data[year][column].value_counts()

        for category, count in counts.items():
            if category in category_map:
                standardized_category = category_map.get(category, category)
                work_remote_data.append(
                    {"Year": year, "State": standardized_category, "Count": count}
                )

    work_remote_data = (
        pd.DataFrame(work_remote_data).groupby(by=["Year", "State"]).sum().reset_index()
    )
    work_remote_data["Yearly total"] = work_remote_data.groupby(by=["Year"])[
        "Count"
    ].transform("sum")
    work_remote_data["Proportional"] = (
        work_remote_data["Count"] / work_remote_data["Yearly total"]
    )
    return work_remote_data


def prepare_gender_dist_data(
    data: pd.DataFrame, column_map: Dict[int, str]
) -> pd.DataFrame:
    """
    Prepares gender distribution data, categorizing and calculating proportions all categories.

    Attributes:
        data (pd.DataFrame): The survey data containing gender information across years.
        column_map (Dict[int, str]): A dictionary mapping years to the column names with gender data for that year.

    Returns:
        pd.DataFrame: A dataframe with columns 'Year', 'Gender', 'Count', 'Total', and 'Proportional',
                      showing the proportion of each gender category by year.
    """
    gender_data = []
    for year, column in column_map.items():
        counts = data[year][column].value_counts()

        for category, count in counts.items():
            standardized_category = categorize_gender(category)
            if standardized_category == "Other":
                continue
            gender_data.append(
                {"Year": year, "Gender": standardized_category, "Count": count}
            )

    gender_data = (
        pd.DataFrame(gender_data).groupby(by=["Year", "Gender"]).sum().reset_index()
    )
    gender_data["Total"] = gender_data.groupby(by=["Year"])["Count"].transform("sum")
    gender_data["Proportional"] = gender_data["Count"] / gender_data["Total"]

    return gender_data


def prepare_gender_dist_data_per_country(
    data: pd.DataFrame,
    year: int,
    gender_column_map: Dict[int, str],
    country_column_map: Dict[int, str],
) -> pd.DataFrame:
    """
    Prepares gender distribution data by country, categorizing and calculating proportions for all categories.

    Attributes:
        data (pd.DataFrame): The survey data containing gender and country information.
        year (int): The specific year of data to process.
        gender_column_map (Dict[int, str]): A dictionary mapping years to the column names with gender data.
        country_column_map (Dict[int, str]): A dictionary mapping years to the column names with country data.

    Returns:
        pd.DataFrame: A dataframe with columns 'Country', 'Gender', 'Count', 'Total', and 'Proportional',
                      showing the proportion of each gender category within each country.
    """
    data_selection = data[year][
        [gender_column_map[year], country_column_map[year]]
    ].dropna()
    data_selection.rename(
        columns={
            country_column_map[year]: "Country",
            gender_column_map[year]: "Gender",
        },
        inplace=True,
    )
    data_selection["Gender"] = data_selection["Gender"].apply(categorize_gender)
    data_selection = data_selection[data_selection["Gender"] != "Other"]
    country_gender_data = (
        data_selection.groupby(by=["Country"])["Gender"]
        .value_counts()
        .reset_index(name="Count")
    )
    country_gender_data["Total"] = country_gender_data.groupby(by=["Country"])[
        "Count"
    ].transform("sum")
    country_gender_data["Proportional"] = (
        country_gender_data["Count"] / country_gender_data["Total"]
    )

    return country_gender_data


def prepare_language_data(
    data: pd.DataFrame,
    year: int,
    language_column_map: Dict[int, str],
    branch_category_map: Dict[str, str],
    top_5_languages: List[str],
) -> pd.DataFrame:
    """
    Prepares language usage data by filtering and calculating the proportion of top languages used by professional and learning/hobby developers.

    Attributes:
        data (pd.DataFrame): The survey data containing language and branch information.
        year (int): The specific year of data to process.
        language_column_map (Dict[int, str]): A dictionary mapping years to the column names with language data.
        branch_category_map (Dict[str, str]): A dictionary mapping raw branch categories to standardized categories.
        top_5_languages (List[str]): A list of the top 5 languages to filter by.

    Returns:
        pd.DataFrame: A dataframe with columns 'Branch', 'Language', 'Count', 'Total', 'Proportion', and 'Year',
                      showing the proportion of each language used by branch.
    """
    language_data = data[year][[language_column_map[year], "MainBranch"]].dropna()
    language_data.rename(
        columns={
            language_column_map[year]: "Language",
            "MainBranch": "Branch",
        },
        inplace=True,
    )
    language_data["Branch"] = language_data["Branch"].replace(branch_category_map)
    language_data = language_data[
        (language_data["Branch"] == "Professional developer")
        | (language_data["Branch"] == "Learning/Hobby")
    ]
    language_data["Language"] = language_data["Language"].str.split(";")
    language_data = language_data.explode("Language").reset_index(drop=True)
    language_data = (
        language_data.groupby(by=["Branch", "Language"])
        .size()
        .reset_index(name="Count")
    )
    language_data["Total"] = language_data.groupby(by=["Branch"])["Count"].transform(
        "sum"
    )
    language_data["Proportion"] = language_data["Count"] / language_data["Total"]

    language_data = language_data[language_data["Language"].isin(top_5_languages)]

    language_data["Year"] = year

    return language_data


def create_plot_gender_dist(gender_data: pd.DataFrame) -> po.Figure:
    """
    Creates a bar plot visualizing the gender distribution of developers over the years.

    Attributes:
        gender_data (pd.DataFrame): A data frame containing gender proportions by year.
                                    Expected columns include 'Year', 'Gender', and 'Proportional'.

    Returns:
        po.Figure: A Plotly figure object representing the bar plot of gender distribution over time.
    """
    colors = {"Male": "#58508d ", "Female": "#ff6361", "Queer/Non-binary": "#ffa600"}

    fig = po.Figure()

    for gender in gender_data["Gender"].unique():
        gender_df = gender_data[gender_data["Gender"] == gender]
        fig.add_trace(
            po.Bar(
                x=gender_df["Year"],
                y=gender_df["Proportional"],
                name=gender,
                marker_color=colors[gender],
            )
        )

    fig.update_layout(
        title="Developers gender distribution throughout years",
        xaxis_title="Year",
        yaxis_title="Proportion of developers",
    )

    return fig


def create_plot_gender_dist_per_country(
    country_gender_data: pd.DataFrame, rename_country: Dict[str, str], year: int
) -> po.Figure:
    """
    Creates a stacked bar plot visualizing gender distribution by country for a given year.

    Attributes:
        country_gender_data (pd.DataFrame): The data frame containing gender proportions by country.
        rename_country (Dict[str, str]): A dictionary mapping country codes or names to readable country names.
        year (int): The year of data being plotted.

    Returns:
        po.Figure: A Plotly figure object representing the stacked bar plot of gender distribution by country.
    """
    colors = {"Male": "#ff6361", "Female": "#58508d", "Queer/Non-binary": "#ffa600"}

    fig = po.Figure()

    country_gender_data_high_perc = country_gender_data[
        country_gender_data["Total"]
        >= np.partition(country_gender_data["Total"].unique(), -5)[-5]
    ]
    for gender in country_gender_data_high_perc["Gender"].unique():
        gender_df = country_gender_data_high_perc[
            country_gender_data_high_perc["Gender"] == gender
        ]
        fig.add_trace(
            po.Bar(
                x=gender_df["Country"].replace(rename_country),
                y=gender_df["Proportional"],
                name=gender,
                marker_color=colors[gender],
            )
        )

    fig.update_layout(
        title=f"Gender Distribution by Country for {year}",
        xaxis_title="Country",
        yaxis_title="Proportion of developers",
        barmode="stack",
    )

    return fig


def create_plot_language(
    all_language_data: pd.DataFrame, top_5_languages: List[str], branch: str
) -> po.Figure:
    """
    Creates a line plot visualizing the trend of top programming languages used by a specified branch.

    Attributes:
        all_language_data (pd.DataFrame): The data frame containing language usage proportions by branch and year.
        top_5_languages (List[str]): A list of the top 5 languages to display in the plot.
        branch (str): The developer branch (e.g., 'Professional developer') to filter data for the plot.

    Returns:
        po.Figure: A Plotly figure object representing the line plot of language usage trends by year.
    """
    fig = po.Figure()

    for language in top_5_languages:
        language_data = all_language_data[all_language_data["Branch"] == branch][
            all_language_data[all_language_data["Branch"] == branch]["Language"]
            == language
        ]
        fig.add_trace(
            po.Scatter(
                x=language_data["Year"],
                y=language_data["Proportion"],
                mode="lines+markers",
                name=language,
                text=language_data["Language"],
            )
        )

    fig.update_layout(
        title=f"Trend of Programming Languages Used by {branch}",
        xaxis_title="Year",
        yaxis_title="Proportion",
        legend_title="Languages",
    )

    return fig
