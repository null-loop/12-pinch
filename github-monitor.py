import time, sys, json, os
from github import Github
from github import Auth
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFile, ImageDraw, ImageFont, ImageColor

def render_repo_state(repo_name, label, row, draw):
    print("Checking %1".format(label))
    repos = git.get_user().get_repos()
    for repo in repos:
        if repo.name == repo_name:
            commit = repo.get_commit("main")
            state = commit.get_combined_status().state
            pr_count = repo.get_pulls().totalCount
            branch_count = repo.get_branches().totalCount
            row_height = 23
            y_offset = (row * row_height) + 2 + (row * 2)
            build_color = 'Green'
            if state == 'pending':
                build_color = 'Yellow'
            if state == 'failed':
                build_color = 'Red'
            draw.line([2, y_offset + row_height + 2, 125, y_offset + row_height], fill=build_color)
            draw.rectangle([54, y_offset, 64, y_offset + 10], fill=build_color)
            print("Drew %1".format(label))

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 2
options.limit_refresh_rate_hz = 120
options.brightness = 50
options.disable_hardware_pulsing = True
options.drop_privileges = False

matrix = RGBMatrix(options = options)

with open('.github-secret', 'r') as github_secret_file:
    github_pat = github_secret_file.read().rstrip('\n')

auth = Auth.Token(github_pat)

git = Github(auth=auth)

#font = ImageFont.truetype("FreeMono.ttf", 12)

try:
    print("Press CTRL-C to stop.")
    while True:

        outputImage = Image.new('RGB', (128, 128))
        outputImageDraw = ImageDraw.Draw(outputImage)

        render_repo_state("pico", "Core", 0, outputImageDraw)
        render_repo_state("pico.supergraph", "Graph", 1, outputImageDraw)
        render_repo_state("pico.event.sdk", "SDK", 2, outputImageDraw)
        render_repo_state("pico.frontend", "Web", 3, outputImageDraw)
        render_repo_state("pico.payloadcms", "CMS", 4, outputImageDraw)

        top_half = outputImage.crop((0, 0, 128, 64))
        bottom_half = outputImage.crop((0, 64, 128, 128))

        stitched = Image.new('RGB', (256, 64))
        stitched.paste(top_half, (0, 0))
        stitched.paste(bottom_half, (128, 0))

        rgb = stitched.convert('RGB')

        matrix.SetImage(rgb)

        time.sleep(60)
except KeyboardInterrupt:
    sys.exit(0)

