from flask import request, Blueprint

from controllers import commits_controller as controller

commits = Blueprint("commits", __name__)


@commits.route('/commit', methods=["POST"])
def add_commit():
    return controller.add_commit(request)


@commits.route('/commits', methods=['GET'])
def get_commits():
    return controller.get_all_commits(request)


@commits.route('/commit/<commit_id>', methods=['GET'])
def get_commit_by_id(commit_id):
    return controller.get_commit(request, commit_id)


@commits.route('/commit/<commit_id>', methods=['GET'])
def get_commits_by_repo_id(repo_id):
    return controller.get_commits_by_repo_id(request, repo_id)


@commits.route('/commit/<commit_id>', methods=["PATCH"])
def update_commit(commit_id):
    return controller.update_commit(request, commit_id)


@commits.route('/commit/<commit_id>', methods=["DELETE"])
def delete_commit(commit_id):
    return controller.delete_commit(request, commit_id)
