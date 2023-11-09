import click
import requests
from requests.auth import HTTPBasicAuth


@click.command()
@click.option('--project', default="", help='Project name.')
def jira_migration(project):
    # 你的 Jira 实例的 URL
    jira_url = "http://192.168.35.155:8080"

    # 你的用户名和密码
    username = "sai.yuan"
    password = "123456"

    # API 的路径
    api_path = "/rest/api/2/search?jql=project="+project
    print(jira_url + api_path)
    # 发送 GET 请求
    response = requests.get(
        jira_url + api_path,
        auth=HTTPBasicAuth(username, password)
    )

    # 打印响应的 JSON 内容
    print(response.json())
