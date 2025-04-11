import streamlit as st
from typing import List
import random


# === Page Setup ===
st.set_page_config(page_title="Contains Duplicate Visualizer", layout="wide")
st.title("🔎 Contains Duplicate Visualizer")
st.header("🧠 Problem: Contains Duplicate")


# === Session State ===
def_state = {
    'step': 0,
    'iter': 0,
    'seen': set(),
    'msg': '',
    'done': False,
    'current': None,
    'skip_return_true': False
}

def init_session_state():
    for k, v in def_state.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if 'nums' not in st.session_state:
        st.session_state.nums = [1, 2, 3, 3]

init_session_state()


def reset_all():
    for k, v in def_state.items():
        st.session_state[k] = v
    st.session_state.nums = [1, 2, 3, 3]  # reset array


def reset_partial():
    st.session_state.step = 0
    st.session_state.iter = 0
    st.session_state.seen = set()
    st.session_state.current = None
    st.session_state.msg = ''
    st.session_state.done = False

# === Execution Logic ===

def step_logic():
    step = st.session_state.step
    nums_list = st.session_state.nums
    iter_idx = st.session_state.iter

    if step == 0:
        st.session_state.msg = "Starting function..."
        st.session_state.step += 1

    elif step == 1:
        st.session_state.seen = set()
        st.session_state.msg = "Initialized empty set."
        st.session_state.step += 1

    elif step == 2:
        if iter_idx >= len(nums_list):
            st.session_state.msg = "Loop finished. Going to return False."
            st.session_state.step = 6
        else:
            st.session_state.current = nums_list[iter_idx]
            st.session_state.msg = f"num = {st.session_state.current}"
            st.session_state.step += 1

    elif step == 3:
        if st.session_state.current in st.session_state.seen:
            st.session_state.msg = f"{st.session_state.current} found in seen. Will return True."
            st.session_state.step = 4
            st.session_state.skip_return_true = False
        else:
            st.session_state.msg = f"{st.session_state.current} not in seen."
            st.session_state.skip_return_true = True
            st.session_state.step = 5

    elif step == 4:
        if not st.session_state.skip_return_true:
            st.session_state.msg = "Returning :green[True] (duplicate found)."
            st.session_state.done = True
        else:
            st.session_state.msg = "Skipping return True."
            st.session_state.step += 1

    elif step == 5:
        st.session_state.seen.add(st.session_state.current)
        st.session_state.iter += 1
        st.session_state.msg = f"Added {st.session_state.current} to seen."
        st.session_state.step = 2

    elif step == 6:
        st.session_state.msg = "Returning False (no duplicates)."
        st.session_state.done = True




# === Problem Description ===
with st.container():
    st.markdown("""
    :green[**Description:**] Given an integer array `nums`, return :green[True] if it appears more than once in the array, otherwise return :red[False].

    **Example 1:**
    ```python
    Input : nums = [1,2,3,3]
    Output: True
    ```

    **Example 2:**
    ```python
    Input : nums = [1,2,3,4]
    Output: False
    ```
    """)

# === Code Definition ===
code_lines = [
    "def hasDuplicate(nums: List[int]) -> bool:",
    "    seen = set()",
    "    for num in nums:",
    "        if num in seen:",
    "            return True",
    "        seen.add(num)",
    "    return False"
]




# === Code Visualization ===
st.subheader("💻 Code Execution - Hash Set Solution", divider='gray')

# === Input Form ===
# nums = [1, 2, 3, 3]
with st.form("array_form"):
    st.subheader("🎛️ Generate Random Input")
    col1, col2, col3 = st.columns(3)
    with col1:
        array_len = st.number_input(
            "Length", min_value=1, max_value=100, value=5, step=1, key="len")
    with col2:
        min_val = st.number_input("Min Value", value=1, step=1, key="min")
    with col3:
        max_val = st.number_input("Max Value", value=10, step=1, key="max")

    submitted = st.form_submit_button("🎲 Generate Array")


if submitted:
    if min_val > max_val:
        st.warning("⚠️ Min value must be ≤ max value.")
    else:
        st.session_state.nums = [random.randint(
            min_val, max_val) for _ in range(array_len)]
        reset_partial()
# nums = st.session_state.nums

# === Display Generated Array ===
st.subheader(f"🔢 **Current Array**: `{st.session_state.nums}`")

# === Code Visualization Layout ===
with st.container():
    arrowed_code_block = ""
    for idx, line in enumerate(code_lines):
        arrow = "\t⬅️" if idx == st.session_state.step and not st.session_state.done else "   "
        arrowed_code_block += f"{line}{arrow}\n"

    code_col, info_col = st.columns([10, 5])
    code_col.code(arrowed_code_block, language="python")

    # info on the side

    seen_display = (
        "set()" if len(st.session_state.seen) == 0
        else "{" + ", ".join(map(str, sorted(st.session_state.seen))) + "}"
    )
    info_col.markdown(f"**Seen Set**: `{seen_display}`")
    info_col.markdown(f"**Current num**: `{st.session_state.current}`")
    info_col.markdown(f"**Message**: {st.session_state.msg}")

    # Hardcode but yea
    if st.session_state.done:
        if st.session_state.step == 4:
            info_col.success("✅ Returned `True` — duplicate found.")
        elif st.session_state.step == 6:
            info_col.info("❎ Returned `False` — no duplicates.")


# # === State Display ===
# st.markdown(f"**Seen Set**: `{sorted(list(st.session_state.seen))}`")
# st.markdown(f"**Current num**: `{st.session_state.current}`")
# st.markdown(f"**Message**: {st.session_state.msg}")

# === Buttons ===
done = st.session_state.done
left, right = st.columns(2)
left.button("▶️ Next Step", on_click=step_logic,
            disabled=done, use_container_width=True)
right.button("🔄 Reset", on_click=reset_all, use_container_width=True)

# === Debug info ===
with st.expander("🛠 Debug Info"):
    st.write(st.session_state)

# === Footer ===
st.markdown("---")
st.caption("Made with ❤️ by Wilfred Djumin")
