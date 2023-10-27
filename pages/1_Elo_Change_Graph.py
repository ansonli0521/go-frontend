# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from datetime import datetime


def elo_change_history():
    @st.cache_data
    def get_data():
        URL = "https://github.com/ansonli0521/go/blob/main/elo/history.csv?raw=true"
        df = pd.read_csv(URL)
        return df
    
    @st.cache_data
    def get_player():
        URL = "https://github.com/ansonli0521/go/blob/main/elo/elo.csv?raw=true"
        df = pd.read_csv(URL)
        return df.set_index('Player')


    try:
        df = get_data()
        df.index = df.index + 1
        player_df = get_player()
        players = st.multiselect(
            "Choose Players", list(player_df.index), list(player_df.index)
        )
        date_range = st.slider(
            "Date Range:",
            min_value=datetime.strptime(df.iloc[df.Date.idxmin(), 0], "%Y-%m-%d").date(),
            max_value=datetime.strptime(df.iloc[df.Date.idxmax(), 0], "%Y-%m-%d").date(),
            value=(datetime.strptime(df.iloc[df.Date.idxmin(), 0], "%Y-%m-%d").date(), datetime.strptime(df.iloc[df.Date.idxmax(), 0], "%Y-%m-%d").date())
        )
        if not players:
            st.error("Please select at least one player.")
        else:
            df = df[df.Player.isin(players)]
            data = df[df.Date.between(str(date_range[0]), str(date_range[1]))]

            lines = (
                alt.Chart(data, title="Elo Change of Players")
                .mark_line()
                .encode(
                    x="Date",
                    y="Elo",
                    color="Player",
                )
            )

            hover = alt.selection_single(
                fields=["Date"],
                nearest=True,
                on="mouseover",
                empty="none",
            )

            points = lines.transform_filter(hover).mark_circle(size=65)

            # Draw a rule at the location of the selection
            tooltips = (
                alt.Chart(data)
                .mark_rule()
                .encode(
                    x="Date",
                    y="Elo",
                    opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                    tooltip=[
                        alt.Tooltip("Date", title="Date"),
                        alt.Tooltip("Player", title="Player"),
                        alt.Tooltip("Elo", title="Elo"),
                    ],
                )
                .add_selection(hover)
            ).properties(height=800)

            st.altair_chart((lines+points+tooltips).interactive(), use_container_width=True)

            st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
             unsafe_allow_html=True)

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Elo Change Graph", page_icon="📈")
st.markdown("# Elo Change Graph 📈")
st.sidebar.header("Elo Change Graph")

elo_change_history()
