import pandas as pd
import re

# Allowed values as per rules
ALLOWED_IDENTIFIER_TYPES = {"CUSIP", "ISIN", "SEDOL", "INTERNAL"}
ALLOWED_ACCOUNTING_INTENT = {"AFS", "HTM", "EQ"}
ALLOWED_HEDGE_TYPES = {1, 2}  # 1 = Fair Value Hedge, 2 = Cash Flow Hedge
ALLOWED_HEDGED_RISK = {1, 2, 3, 4}  # Valid risk types
ALLOWED_HEDGE_INTEREST_RATE = {1, 2, 3, 4, 5}
ALLOWED_HEDGED_CASH_FLOW = {1, 2, 3, 4, 5, 6}
ALLOWED_SIDEDNESS = {1, 2}

# Function to check identifier type
def validate_identifier_type(df):
    """Validation Rule: Identifier Type should be one of CUSIP, ISIN, SEDOL, INTERNAL."""
    return df[~df["Identifier Type"].isin(ALLOWED_IDENTIFIER_TYPES)]

# Function to check accounting intent
def validate_accounting_intent(df):
    """Validation Rule: Accounting Intent should be one of AFS, HTM, EQ."""
    return df[~df["Accounting Intent (AFS, HTM, EQ)"].isin(ALLOWED_ACCOUNTING_INTENT)]

# Function to check type of hedge
def validate_type_of_hedge(df):
    """Validation Rule: Type of Hedge should be 1 (Fair Value Hedge) or 2 (Cash Flow Hedge)."""
    return df[~df["Type of Hedge(s)"].isin(ALLOWED_HEDGE_TYPES)]

# Function to check hedged risk
def validate_hedged_risk(df):
    """Validation Rule: Hedged Risk should be between 1-4."""
    return df[~df["Hedged Risk"].isin(ALLOWED_HEDGED_RISK)]

# Function to check hedge interest rate
def validate_hedge_interest_rate(df):
    """Validation Rule: Hedge Interest Rate should be between 1-5."""
    return df[~df["Hedge Interest Rate"].isin(ALLOWED_HEDGE_INTEREST_RATE)]

# Function to check hedge percentage (should be between 0 and 1)
def validate_hedge_percentage(df):
    """Validation Rule: Hedge Percentage should be between 0 and 1."""
    return df[(df["Hedge Percentage"] < 0) | (df["Hedge Percentage"] > 1)]

# Function to check hedge horizon (should be in YYYY-MM-DD format)
def validate_hedge_horizon(df):
    """Validation Rule: Hedge Horizon should be a valid YYYY-MM-DD date."""
    return df[~df["Hedge Horizon"].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$")]

# Function to check hedged cash flow
def validate_hedged_cash_flow(df):
    """Validation Rule: Hedged Cash Flow should be between 1-6."""
    return df[~df["Hedged Cash Flow"].isin(ALLOWED_HEDGED_CASH_FLOW)]

# Function to check sidedness
def validate_sidedness(df):
    """Validation Rule: Sidedness should be 1 (One-sided) or 2 (Not One-sided)."""
    return df[~df["Sidedness"].isin(ALLOWED_SIDEDNESS)]

# Function to check hedging instrument at fair value (should be a valid number)
def validate_hedging_instrument_at_fair_value(df):
    """Validation Rule: Hedging Instrument at Fair Value should be a valid number."""
    return df[pd.to_numeric(df["Hedging Instrument at Fair Value"], errors="coerce").isna()]
