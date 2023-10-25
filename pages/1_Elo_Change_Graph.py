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
        if not players:
            st.error("Please select at least one player.")
        else:
            data = df[df.Player.isin(players)]

            lines = (
                alt.Chart(data, title="Elo Change of Players")
                .mark_line()
                .encode(
                    x="Date",
                    y="New Elo",
                    color="Player",
                )
            )

            st.altair_chart(lines.interactive(), use_container_width=True)
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
