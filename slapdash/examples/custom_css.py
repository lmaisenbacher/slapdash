import slapdash
import os


class CustomCSS:
    number = 0.0
    button = False


if __name__ == '__main__':
    custom_css = CustomCSS()
    print(__file__)

    parent_dir_path = os.path.dirname(os.path.realpath(__file__))
    css = os.path.join(parent_dir_path, 'custom_css.css')
    slapdash.run(custom_css, css=css)
