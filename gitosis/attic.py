import logging
import re
import os
import os.path
import shutil

log = logging.getLogger('gitosis.attic')

from gitosis import util

repo_sect = re.compile(r'^repo\s+')
attic_name = re.compile(r'^Attic/\d+/')

def update_attic(config):
    repositories = util.getRepositoryDir(config)

    for sect in config.sections():
        repo = repo_sect.sub('', sect)
        repo += '.git'
        old_repo = attic_name.sub('', repo)
        if old_repo == repo:
            continue

        repo = os.path.join(repositories, repo)
        old_repo = os.path.join(repositories, old_repo)

        if os.path.exists(repo):
            log.debug("repo %s already deleted" % repo)
            continue

        if not os.path.exists(old_repo):
            log.warning("original repository %s doesn't exist" % old_repo)
            continue
        
        log.info("move %s to %s" % (old_repo, repo))
        shutil.move(old_repo, repo)
