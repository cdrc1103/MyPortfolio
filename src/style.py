def streamlit_style() -> str:
    """Configure visibility of streamlit elements"""
    return """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        footer:after {
            content:'Developed by Cedric Issel';
            visibility: visible;
            display: block;
            position: relative;
            text-align: center;
        }
        </style>
    """


def max_page_width(max_width: int) -> str:
    """Configure max width of main page in pixels"""
    return f"""
        <style>
        .appview-container .main .block-container{{
            max-width: {max_width}px;
            padding-top: 1rem;
        }}
        </style>
    """
