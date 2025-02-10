from io import BytesIO

import cairosvg
from PIL import Image, ImageDraw, ImageFont
from github import Auth
from github import Github
from github.Repository import Repository


class BuildStatus:
    label = ""
    state = list()
    pr_count = 0
    branch_count = 0

class GitScreen:
    update_interval_seconds=60
    label = "GitHub"
    render_as_image = True
    def __init__(self):
        with open('../secrets/.github-secret', 'r') as github_secret_file:
            github_pat = github_secret_file.read().rstrip('\n')
        auth = Auth.Token(github_pat)
        self.__git = Github(auth=auth)
        self.__big_font = ImageFont.truetype("../assets/NotoSans-Regular.ttf", 23)
        self.__small_font = ImageFont.truetype("../assets/NotoSans-Regular.ttf", 12)

        pr_out = BytesIO()
        cairosvg.svg2png(url='../assets/git-pull-request.svg', write_to=pr_out)
        self.__pr_icon = Image.open(pr_out)

        branch_out = BytesIO()
        cairosvg.svg2png(url='../assets/git-branch.svg', write_to=branch_out)
        self.__branch_icon = Image.open(branch_out)

    def render(self) -> Image:

        output_image = Image.new('RGB', (128, 128))
        output_image_draw = ImageDraw.Draw(output_image)

        user = self.__git.get_user()
        all_repos = user.get_repos()

        core = self.__get_repo_status(all_repos, "pico", "Core",["Core API - Deploy to Production and Reference","Core Services - Analyse"])
        graph = self.__get_repo_status(all_repos, "pico.supergraph", "Graph",["Deploy Main"])
        sdk = self.__get_repo_status(all_repos, "pico.event.sdk", "SDK",["Publish NuGet Package", "Publish Avro Schema to Eventhub Schema Registry"])
        web = self.__get_repo_status(all_repos, "pico.frontend", "Web",["Build and deploy to Cloudflare Pages"])
        cms = self.__get_repo_status(all_repos, "pico.payloadcms", "CMS",[])

        self.__render_repo_status(cms, 4, output_image_draw)
        self.__render_repo_status(web, 3, output_image_draw)
        self.__render_repo_status(sdk, 2, output_image_draw)
        self.__render_repo_status(graph, 1, output_image_draw)
        self.__render_repo_status(core, 0, output_image_draw)

        return output_image

    def __render_repo_status(self, info: BuildStatus, row, draw):

        row_height = 23
        y_offset = (row * row_height) + 1 + (row * 2)
        overall_status = 'success'

        if len(info.state) > 0:
            current_x = 74

            status_height = 4
            if len(info.state) == 1: status_height = 16
            if len(info.state) == 2: status_height = 8
            if len(info.state) == 3: status_height = 4

            current_y = y_offset + row_height - 3

            for builds in info.state:
                # look at the latest build for the overall_status
                latest_build = builds[0]
                if latest_build == 'pending': overall_status = 'pending'
                if latest_build == 'failure' or latest_build == 'startup_failure': overall_status = 'failure'
                if latest_build == 'cancelled': overall_status = 'cancelled'
                states = builds.copy()
                states.reverse()
                for state in states:
                    run_color = 'DarkBlue'
                    if state == 'success': run_color = 'DarkGreen'
                    if state == 'failure' or state == 'startup_failure': run_color = 'DarkRed'
                    if state == 'cancelled': run_color = 'DarkGrey'
                    draw.rectangle([current_x, current_y - status_height, current_x + 2, current_y], fill=run_color)
                    current_x = current_x + 3
                current_y = current_y - status_height - 1
                current_x = 74

            current_y = y_offset + row_height - 3
            draw.line([74, current_y - 17, 94, current_y - 17], fill='DimGrey')
            draw.line([74, current_y + 1, 94, current_y + 1], fill='DimGrey')

        summary_color = 'DarkBlue'
        if overall_status == 'success': summary_color = 'DarkGreen'
        if overall_status == 'failure' or overall_status == 'startup_failure': summary_color = 'DarkRed'

        draw.line([2, y_offset + row_height + 1, 125, y_offset + row_height + 1], fill='DimGrey')
        draw.text([2, y_offset - 2], info.label, font=self.__big_font, fill=summary_color)

        draw.bitmap([98, y_offset], self.__pr_icon, fill='DimGrey')
        draw.bitmap([98, y_offset + 12], self.__branch_icon, fill='DimGrey')

        draw.text([112, y_offset - 2], "{0}".format(info.pr_count), font=self.__small_font, fill='DimGrey')
        draw.text([112, y_offset + 10], "{0}".format(info.branch_count), font=self.__small_font, fill='DimGrey')

    def __get_repo_status(self, repos, repo_name, label, workflows_to_report) -> BuildStatus:
        for repo in repos:
            if repo.name == repo_name:
                status = BuildStatus()
                status.state = list()
                status.label = label
                status.pr_count = repo.get_pulls().totalCount
                status.branch_count = repo.get_branches().totalCount
                self.__update_status(repo, workflows_to_report, status)

                return status

    def __update_status(self, repo: Repository, workflows_to_report, status):
        workflows = repo.get_workflows()
        for workflow in workflows:
            if workflow.name in workflows_to_report:
                build_statuses = list()
                workflow_runs = workflow.get_runs(branch="main")
                day = 0
                last_date = ""
                for run in workflow_runs:
                    if day > 6:
                        break
                    if run.updated_at.date() != last_date:
                        last_date = run.updated_at.date()
                        build_statuses.append(run.conclusion)
                        day = day + 1
                status.state.append(build_statuses)