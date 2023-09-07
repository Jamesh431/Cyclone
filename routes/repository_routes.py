from flask import request, Blueprint

from controllers import repository_controller as controller

repos = Blueprint("repositories", __name__)


@repos.route('/repo', methods=["POST"])
def add_repo():
    return controller.add_repository(request)


@repos.route('/repo/<repo_id>', methods=['GET'])
def get_repo_by_id(repo_id):
    return controller.get_repository(request, repo_id)


@repos.route('/repo/search', methods=['GET'])
def get_repo_by_search():
    return controller.get_repository_by_search(request)


@repos.route('/repo/sender/<sender_id>', methods=['GET'])
def get_repos_by_sender_id(sender_id):
    return controller.get_repositories_by_senders_github_username(request, sender_id)


@repos.route('/repos', methods=['GET'])
def get_all_repos():
    return controller.get_all_repositories(request)


@repos.route('/repos/active', methods=['GET'])
def get_active_repos():
    return controller.get_active_repositories(request)


@repos.route('/repo/<repo_id>', methods=["PATCH"])
def update_repo(repo_id):
    return controller.update_repository(request, repo_id)


@repos.route('/repo/status/<repo_id>', methods=["PATCH"])
def repo_activity(repo_id):
    return controller.repository_activity(request, repo_id)


@repos.route('/repo/<repo_id>', methods=["DELETE"])
def delete_repo(repo_id):
    return controller.delete_repository(request, repo_id)
