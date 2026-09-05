from IPython.display import HTML, display
def show_img(path, html_caption):
    html_str = f"""
    <figure style="text-align:center; margin:1.5rem auto; max-width:32rem; font-family:sans-serif;">
      <img src="{path}" style="width:100%; border-radius:0.5rem; box-shadow:0 0.25rem 0.5rem rgba(0,0,0,0.1);">
      <figcaption style="font-style:italic; color:#555; font-size:0.9em; margin-top:0.5em;">
        {html_caption}
      </figcaption>
    </figure>
    """
    display(HTML(html_str))

