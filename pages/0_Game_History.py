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
from streamlit.hello.utils import show_code


def game_history():
    @st.cache_data
    def get_data():
        URL = "https://github.com/ansonli0521/go/blob/main/elo/game.csv?raw=true"
        df = pd.read_csv(URL)
        return df

    try:
        data = get_data()
        data.index = data.index + 1
        st.write(data)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Game History", page_icon="⏳")
st.markdown("# Game History")
st.sidebar.header("Game History")

game_history()
