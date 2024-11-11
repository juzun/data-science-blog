# Udacity course - write a data science blog

This repository contains a final project of the first course of Udacity Nanodegree Data Scientist. The task of this project was to choose a dataset, conduct some analysis on it in Jupyter Notebook and then publish the results in a blog, e.g. on Medium.

## Table of Contents

- [Introduction](#introduction)
- [Data](#data)
- [Business Questions](#business-questions)
- [Installation](#installation)

## Introduction

Data from yearly Stackoverflow Survey were used. There are several business questions answered throughout the analysis. The visualisation and deeper explanation of the results can be found on the [Medium blog post](https://medium.com/@zapletalja/stackoverflow-survey-analysis-0aa55b4a9b48).

## Data

As mentioned, Stackoverflow Survey data were used. The range of the years used is 2013 - 2024. Some of the information isn't contained in all the years though, therefore some of the questions were answered by limited subset of the data.

The structure of the project directories is following (only relevant directories and files are mentioned):
- `notebooks`: a directory containing notebooks with separate analyses.
- `notebooks/data`: a directory containing original data of the [Stackoverflow Survey](https://survey.stackoverflow.co/). These are not present in `csv` but archived in ZIP. One must extract the data files and rename them in format `f"{year}.csv"`.
- `notebooks/images`: a directory containing static Plotly graphs showing results of analyses.
- `data_science_blog`: a directory containing core of the project. Since this is project is done in very simple way, it contains only one file with utility functions to support analyses in notebooks.

## Business Questions

The analysis explores the following business questions:

1. **What is the trend in remote work among developers?**
2. **What is the gender distribution among developers throughout the years?**
- In general and in particular in the countries with the highest number of respondents.
3. **What are the most used programming languages based on developers branch (professionals/learners)?**

## Installation

Project uses a Poetry virtual environment.
To run the notebooks in the project it is therefore enough to `poetry install` and the environment will be set.
