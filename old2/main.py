import streamlit as st


st.title("🏠 Main")

# st.table(
#     {
#         ":material/folder: Project": "**Streamlit** - The fastest way to build data apps",
#         ":material/code: Repository": "[github.com/streamlit/streamlit](https://github.com/streamlit/streamlit)",
#         ":material/new_releases: Version": ":gray-badge[1.45.0]",
#         ":material/license: License": ":green-badge[Apache 2.0]",
#         ":material/group: Maintainers": ":blue-badge[Core Team] :violet-badge[Community]",
#     },
#     border="horizontal",
#     width="content",
# )

MetinA = "Kişisel Sınav Sistemine Hoş Geldiniz."
MetinB = "Bu sistem üzerinden DLA ve REC sistemine hazırlanabilirsiniz."

from v1.utils.text_utils import slow_print
from v1.utils.text_utils import trim_text


from v1.utils.time_utils import wait

wait(1)
slow_print(MetinA,False,0.1)
wait(1)
slow_print(MetinB,False,0.1)
