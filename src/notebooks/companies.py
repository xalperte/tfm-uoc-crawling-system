# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import pandas as pd


def get_companies(session):

    companies_df = session.execute(
        "select ccvm, company_name, cnpj from bovespa_company;")
    companies_df = pd.DataFrame(
        [{
            "ccvm": int(x.ccvm),
            "company_name": x.company_name,
            "cnpj": x.cnpj}
            for x in list(companies_df)])
    return companies_df


def get_companies_with_tickers_and_fundamentals(session):

    # All the companies in the system
    companies_df = get_companies(session)

    # Companies with fundamentals
    companies_with_fundamentals_df = get_companies_accounts(session)

    # Available tickers
    original_tickers_df = pd.read_csv('tickers.csv', header=None,
                                      names=["ccvm", "ticker", "ticker_type"])

    stock_prices_df = pd.read_csv('stock_prices.csv.gz',
                                  parse_dates=['formatted_date'])

    tickers_df = stock_prices_df.groupby(by=["ticker"]).count()
    tickers_df = tickers_df.reset_index()["ticker"]

    tickers_df = pd.merge(
        left=tickers_df,
        right=original_tickers_df,
        how='left',
        left_on='ticker',
        right_on='ticker')

    # Compute the ticker for each company (CCVM)
    companies_tickers_df = pd.merge(
        left=companies_with_fundamentals_df,
        right=companies_df,
        how='left',
        left_on='ccvm',
        right_on='ccvm')

    companies_tickers_df = pd.merge(left=companies_tickers_df,
                                    right=tickers_df,
                                    how='left',
                                    left_on='ccvm',
                                    right_on='ccvm')

    companies_tickers_df = companies_tickers_df[
        (pd.notnull(companies_tickers_df["ticker"]))]
    companies_tickers_df = companies_tickers_df.\
        sort_values(['ccvm', 'ticker'], ascending=[1, 1])

    return companies_tickers_df


def get_companies_accounts(session):
    """
    This function computes the total number of financial accounts
    informed by company.

    It returns a pandas dataframe with the company id (ccvm)
    and the number of accounts.
    """
    import json

    solr_query = {
        "q": "*:*",
        "facet": {
            "field": "ccvm_exact",
            "limit": 10000
        }
    }

    accounts_per_company_query = \
        f"select * from bovespa_account WHERE " \
        f"solr_query='{json.dumps(solr_query)}'"

    accounts_per_company = session.execute(accounts_per_company_query).one()
    accounts_per_company = json.loads(accounts_per_company.facet_fields)[
        "ccvm_exact"]
    accounts_per_company = pd.DataFrame([{
        "ccvm": int(ccvm),
        "num_accounts": num_accounts}
        for ccvm, num_accounts in accounts_per_company.items()])
    return accounts_per_company
