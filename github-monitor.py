import time, sys, json, os
from github import Github
from github import Auth
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class BuildStatus:
    label = ""
    state = ""
    pr_count = 0
    branch_count = 0

def update_repo(repo_name, label):
    repos = git.get_user().get_repos()
    for repo in repos:
        if repo.name == repo_name:
            commit = repo.get_commit("main")
            status = BuildStatus()
            status.label = label
            status.state = commit.get_combined_status().state
            status.pr_count = repo.get_pulls().totalCount
            status.branch_count = repo.get_branches().totalCount
            return status

def render_status(status, row):
    # todo: calc y offset from row
    y_offset = 2
    graphics.DrawText(matrix, font, 2, y_offset, white, status.label)

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

font = font.LoadFont("10x20.bdf")
white = graphics.Color(0, 0, 0)
red = graphics.Color(255, 0, 0)
green = graphics.Color(0, 255, 0)
blue = graphics.Color(0, 0, 255)

with open('.github-secret', 'r') as github_secret_file:
    github_pat = github_secret_file.read()

auth = Auth.Token(github_pat)

git = Github(auth=auth)

try:
    print("Press CTRL-C to stop.")
    while True:
        core = update_repo("pico", "Core")
        graph = update_repo("pico.supergraph", "Graph")
        sdk = update_repo("pico.event.sdk", "SDK")
        web = update_repo("pico.frontend", "Web")
        cms = update_repo("pico.payloadcms", "CMS")

        render_status(core, 1)

        time.sleep(60)
except KeyboardInterrupt:
    sys.exit(0)

