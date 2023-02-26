def generate_image(latex, name):
    latex_file = name + ".tex"
    dvi_file = name + ".dvi"
    png_file = name + "1.png"

    with open(LATEX_TEMPLATE) as tex_template_file:
        tex_template = tex_template_file.read()

        with open(latex_file, "w") as tex:
            background_colour = self.settings["latex"]["background-colour"]
            text_colour = self.settings["latex"]["text-colour"]
            latex = (
                tex_template.replace("__DATA__", latex)
                .replace("__BGCOLOUR__", background_colour)
                .replace("__TEXTCOLOUR__", text_colour)
            )

            tex.write(latex)
            tex.flush()
            tex.close()

    image_dpi = self.settings["latex"]["dpi"]
    exit_code = os.system("latex -quiet -interaction=nonstopmode " + latex_file)
    if exit_code == 0:
        os.system("dvipng -q* -D {0} -T tight ".format(image_dpi) + dvi_file)
        return png_file
    else:
        return ""


def generate_image_online(latex, client_session):
    url = "http://frog.isima.fr/cgi-bin/bruno/tex2png--10.cgi?"
    url += urllib.parse.quote(latex, safe="")
    file_name = str(random.randint(0, 2 ** 31)) + ".png"
    urllib.request.urlretrieve(url, file_name)
    return file_name


def cleanup_output_files(outputnum):
    try:
        os.remove(outputnum + ".tex")
        os.remove(outputnum + ".dvi")
        os.remove(outputnum + ".aux")
        os.remove(outputnum + ".log")
        os.remove(outputnum + "1.png")
    except OSError:
        pass
