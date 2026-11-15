# Missed Choice --- Understanding Why Customers Don't Buy

## 1. The idea

Imagine running a local clothing shop for one month.

Most shops naturally keep track of what they sell: which products
customers purchase, how much revenue they generate, and which items are
popular. But there is another side of the customer experience that can
be just as useful: **the customers who walk into the shop, look around,
and leave without buying anything.**

Missed Choice is a simple retail insights application built around that
idea.

It helps a clothing shop understand why a potential customer did not
make a purchase. For example, a customer may leave because: - The price
is higher than their budget. - Their preferred size is unavailable. -
The colour or design they wanted is not in stock. - They are unsure
which product to choose. - They have another reason for not purchasing.

Instead of treating these visits as lost opportunities that go
unexplained, the shop can politely ask customers whether they are
willing to share why they did not buy, record the response, and look for
recurring patterns.

The goal is to use those observations to make better-informed decisions
about stock, pricing, and the customer experience.

## 2. The problem

Businesses often focus on completed transactions because sales are easy
to count. However, customers who leave without purchasing can also
provide useful information about unmet demand.

For example: - Several customers may ask for the same size that is
unavailable. - Customers may repeatedly look for a particular style or
colour. - A product may attract interest, but its price may be outside
the budget of many visitors. - Some customers may need more information
or time before deciding.

Without a simple way to record these reasons, the shop may miss patterns
that could help it improve.

## 3. The proposed solution

Missed Choice provides a straightforward way to record non-purchase
observations and review them over time.

The process is intentionally simple:

1.  **Ask politely:** Invite a customer who did not purchase to share
    the reason, making it clear that answering is optional.
2.  **Record the observation:** Capture the reason, product category,
    approximate price range, and relevant preferences such as size,
    colour, or style.
3.  **Review patterns weekly:** Identify which reasons and product
    requests appear repeatedly.
4.  **Consider a small change:** For example, review stock availability,
    explore a small quantity of a frequently requested style, or
    reassess whether the price range matches customer demand.
5.  **Compare results:** At the end of the month, review the
    observations and available sales records to see whether the changes
    appear to have helped.

The application is intended to support decisions, not make automatic
stock or pricing decisions on behalf of the shop owner.

## 4. What the application includes

### Overview dashboard

-   Total recorded missed-choice observations.
-   Observations from the last seven days.
-   Most frequently recorded reason for not purchasing.
-   Most requested product category.
-   Charts showing reasons and requested categories.

### Record a missed sale

-   Visit date.
-   Reason for not purchasing.
-   Product category.
-   Approximate budget or price range.
-   Preferred size and colour, where relevant.
-   Optional style and non-identifying notes.

### Sales log

-   Record a sale date, product category, and sale amount.
-   Use the sales records as additional context when reviewing trends.

### Insights and actions

-   Filter observations by date range.
-   Compare common reasons and requested categories.
-   View possible next steps based on recurring observations.
-   Review recorded sales by category when sales data is available.

### View and export records

-   Review recorded observations and sales.
-   Download the data as CSV files for further analysis.

## 5. Example use case

Suppose a clothing shop records customer feedback over a week and
notices that several visitors wanted kurtis in a particular size, but
that size was unavailable.

The shop owner could:

1.  Review the number of observations and the dates they were recorded.
2.  Check whether the same size request appears repeatedly.
3.  Compare the pattern with existing stock and sales information.
4.  Consider a small stock adjustment rather than making a large
    purchase immediately.
5.  Review customer observations and sales again after the change.

This is an example of how a shop could use customer feedback to
investigate missed demand. A repeated request is a useful signal, but a
small sample alone does not prove that a larger stock order will be
profitable.

## 6. Technology stack

-   **Python** --- application logic.
-   **Streamlit** --- interactive web application.
-   **SQLite** --- local data storage.
-   **Pandas** --- data handling and analysis.
-   **Plotly** --- interactive charts and visualisations.

## 7. Run the application locally

### Requirements

-   Python 3.10 or later.
-   pip.

### Setup

Clone the repository or download the project files, then open a terminal
in the project directory.

Create and activate a virtual environment (optional but recommended):

``` bash
python -m venv .venv
```

On Windows:

``` bash
.venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Start the application:

``` bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

``` text
http://localhost:8501
```

## 8. Try the demo

Use **Load sample data** in the sidebar to explore the dashboard with
synthetic example records.

You can then: - Review the overview charts. - Record a new missed-sale
observation. - Add sample sales. - Explore the date-filtered insights. -
Export the records as CSV.

The sample records are fictional and are provided only to demonstrate
the application.

## 9. Possible next improvements

-   Weekly and monthly comparison reports.
-   A clearer comparison of customer requests before and after a stock
    change.
-   Product-level demand tracking.
-   A simple action log to record what change the shop tried and when.
-   User authentication and separate shop accounts.
-   A hosted database for reliable persistent storage.
-   Automated tests for form validation and data workflows.

## 10. Data, privacy, and limitations

-   Ask customers politely and make participation optional.
-   Do not collect names, phone numbers, or sensitive personal
    information for this demonstration.
-   Keep free-text notes short and non-identifying.
-   Use synthetic data for public demos.
-   The current starter version stores data in a local SQLite database.
    A local database file on Streamlit Community Cloud is not guaranteed
    to persist across restarts or redeployments. For real ongoing use,
    the application should be connected to a hosted database.
-   The dashboard describes the observations entered into the app. It
    does not automatically know how many people entered the shop, how
    many declined to respond, or the true conversion rate unless those
    figures are also collected.
-   Suggestions are prompts for the shop owner to investigate. They are
    not proof of customer demand or guaranteed sales improvements.

## 11. Why this project?

The central thought behind Missed Choice is simple:

> Businesses learn from what customers buy. They can also learn from
> what customers wanted but could not find, afford, or decide on.

This project explores how a small local clothing shop could capture that
overlooked feedback and use it to make more informed decisions.

------------------------------------------------------------------------

**Project status:** Portfolio / demonstration application\
**Built with:** Python, Streamlit, SQLite, Pandas, and Plotly
