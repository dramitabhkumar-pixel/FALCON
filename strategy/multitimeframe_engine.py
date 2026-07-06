"""
===========================================================
PROJECT FALCON
Multi Timeframe Engine
===========================================================

Synchronizes:

15 Minute  <-- Base Timeframe
1 Hour
4 Hour
Daily

Uses merge_asof() to eliminate look-ahead bias.

Author : Project FALCON
"""

from __future__ import annotations

import logging
from typing import Dict, Any

import pandas as pd


logger = logging.getLogger(__name__)


class MultiTimeframeEngine:
    """
    Multi Timeframe Synchronization Engine.

    Responsibilities
    ----------------
    1. Validate OHLC data
    2. Normalize columns
    3. Synchronize higher timeframes
    4. Prevent look-ahead bias
    5. Supply context to Strategy Layer
    """

    DATETIME_ALIASES = [
        "Datetime",
        "Date",
        "date",
        "DATE",
        "datetime",
        "timestamp",
        "Timestamp",
    ]

    PRICE_COLUMNS = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    def __init__(
        self,
        df_15m: pd.DataFrame,
        df_1h: pd.DataFrame,
        df_4h: pd.DataFrame,
        df_daily: pd.DataFrame,
    ):

        self.df_15m = df_15m.copy()

        self.df_1h = df_1h.copy()

        self.df_4h = df_4h.copy()

        self.df_daily = df_daily.copy()

        self.merged_df: pd.DataFrame | None = None

    # =====================================================
    # DATA VALIDATION
    # =====================================================

    def validate_data(self):

        datasets = {
            "15m": self.df_15m,
            "1H": self.df_1h,
            "4H": self.df_4h,
            "Daily": self.df_daily,
        }

        for timeframe, df in datasets.items():

            self._normalize_dataframe(df, timeframe)

        logger.info("All timeframes validated.")

    # =====================================================

    def _normalize_dataframe(
        self,
        df: pd.DataFrame,
        timeframe: str,
    ):

        if df.empty:

            raise ValueError(
                f"{timeframe} dataframe is empty."
            )

        datetime_column = None

        for candidate in self.DATETIME_ALIASES:

            if candidate in df.columns:

                datetime_column = candidate

                break

        if datetime_column is None:

            raise ValueError(
                f"{timeframe} has no datetime column."
            )

        if datetime_column != "Datetime":

            df.rename(
                columns={
                    datetime_column: "Datetime"
                },
                inplace=True,
            )

        required = [
            "Open",
            "High",
            "Low",
            "Close",
        ]

        for column in required:

            if column not in df.columns:

                raise ValueError(
                    f"{timeframe} missing column '{column}'"
                )

        df["Datetime"] = pd.to_datetime(
            df["Datetime"],
            errors="coerce",
        )

        if df["Datetime"].isnull().any():

            raise ValueError(
                f"{timeframe} contains invalid datetime values."
            )

        for column in required:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

        if "Volume" in df.columns:

            df["Volume"] = pd.to_numeric(
                df["Volume"],
                errors="coerce",
            )

        df.sort_values(
            "Datetime",
            inplace=True,
        )

        df.drop_duplicates(
            subset="Datetime",
            inplace=True,
        )

        df.reset_index(
            drop=True,
            inplace=True,
        )

        logger.info(
            "%s normalized (%d rows)",
            timeframe,
            len(df),
        )

    # =====================================================

    def _prefix_columns(
        self,
        df: pd.DataFrame,
        prefix: str,
    ) -> pd.DataFrame:

        renamed = {}

        for column in df.columns:

            if column == "Datetime":
                continue

            renamed[column] = f"{prefix}_{column}"

        return df.rename(columns=renamed)
    # =====================================================
    # TIMEFRAME SYNCHRONIZATION
    # =====================================================

    def align_timeframes(self) -> pd.DataFrame:
        """
        Synchronize all higher timeframes to the 15-minute timeframe.

        Uses backward merge_asof() to ensure that only completed
        higher-timeframe candles are visible to the strategy.
        """

        base = self.df_15m.copy()

        h1 = self._prefix_columns(self.df_1h.copy(), "1H")
        h4 = self._prefix_columns(self.df_4h.copy(), "4H")
        daily = self._prefix_columns(self.df_daily.copy(), "D")

        # Safety: merge_asof requires sorted data
        base = base.sort_values("Datetime")
        h1 = h1.sort_values("Datetime")
        h4 = h4.sort_values("Datetime")
        daily = daily.sort_values("Datetime")

        merged = pd.merge_asof(
            base,
            h1,
            on="Datetime",
            direction="backward",
            allow_exact_matches=True,
        )

        merged = pd.merge_asof(
            merged,
            h4,
            on="Datetime",
            direction="backward",
            allow_exact_matches=True,
        )

        merged = pd.merge_asof(
            merged,
            daily,
            on="Datetime",
            direction="backward",
            allow_exact_matches=True,
        )

        self.merged_df = merged

        logger.info(
            "Synchronization completed. %d rows created.",
            len(self.merged_df),
        )

        return self.merged_df

    # =====================================================
    # ACCESSORS
    # =====================================================

    def get_dataframe(self) -> pd.DataFrame:

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() first."
            )

        return self.merged_df

    # =====================================================

    def get_context(
        self,
        index: int,
    ) -> Dict[str, Any]:

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() first."
            )

        if index < 0 or index >= len(self.merged_df):
            raise IndexError(
                "Context index out of range."
            )

        row = self.merged_df.iloc[index]

        context = {
            "timestamp": row["Datetime"],
            "15m": {},
            "1H": {},
            "4H": {},
            "Daily": {},
        }

        for column in self.merged_df.columns:

            if column == "Datetime":
                continue

            if column.startswith("1H_"):

                context["1H"][
                    column.replace("1H_", "")
                ] = row[column]

            elif column.startswith("4H_"):

                context["4H"][
                    column.replace("4H_", "")
                ] = row[column]

            elif column.startswith("D_"):

                context["Daily"][
                    column.replace("D_", "")
                ] = row[column]

            else:

                context["15m"][column] = row[column]

        return context

    # =====================================================

    def print_summary(self):

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() first."
            )

        print("\n========== MULTI TIMEFRAME SUMMARY ==========")
        print(f"Rows    : {len(self.merged_df)}")
        print(f"Columns : {len(self.merged_df.columns)}")
        print("\nColumns:")
        print(list(self.merged_df.columns))
        print("=============================================\n")
        
    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_alignment(self) -> bool:
        """
        Validate the merged multi-timeframe dataset.
        """

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() before validation."
            )

        df = self.merged_df

        # Datetime checks
        if df["Datetime"].isnull().any():
            raise ValueError("Merged dataframe contains null timestamps.")

        if not df["Datetime"].is_monotonic_increasing:
            raise ValueError("Merged dataframe is not chronologically sorted.")

        if df["Datetime"].duplicated().any():
            raise ValueError("Duplicate timestamps detected.")

        # Higher timeframe timestamps should never be in the future
        for prefix in ["1H", "4H", "D"]:

            ts_col = f"{prefix}_Datetime"

            if ts_col not in df.columns:
                continue

            invalid = df[df[ts_col] > df["Datetime"]]

            if not invalid.empty:
                raise ValueError(
                    f"Look-ahead bias detected in {prefix} alignment."
                )

        logger.info("Alignment validation passed.")

        return True

    # =====================================================
    # INFORMATION
    # =====================================================

    def info(self):

        if self.merged_df is None:
            print("Merged dataframe not created.")
            return

        print("\n========== MULTI TIMEFRAME ENGINE ==========")
        print(f"Rows          : {len(self.merged_df)}")
        print(f"Columns       : {len(self.merged_df.columns)}")
        print(f"Start         : {self.merged_df['Datetime'].min()}")
        print(f"End           : {self.merged_df['Datetime'].max()}")
        print("============================================\n")

    # =====================================================

    def head(self, rows: int = 5):

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() first."
            )

        return self.merged_df.head(rows)

    # =====================================================

    def tail(self, rows: int = 5):

        if self.merged_df is None:
            raise ValueError(
                "Run align_timeframes() first."
            )

        return self.merged_df.tail(rows)

    # =====================================================

    def __len__(self):

        if self.merged_df is None:
            return 0

        return len(self.merged_df)

    # =====================================================

    def __repr__(self):

        if self.merged_df is None:
            return "MultiTimeframeEngine(Not Initialized)"

        return (
            f"MultiTimeframeEngine("
            f"rows={len(self.merged_df)}, "
            f"columns={len(self.merged_df.columns)})"
        )