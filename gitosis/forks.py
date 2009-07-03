import logging
import re
import os
import os.path

log = logging.getLogger('gitosis.forks')

from gitosis import util
from gitosis import repository

repo_sect = re.compile(r'^repo\s+')

def update_forks(config):
    repositories = util.getRepositoryDir(config)

    for sect in config.sections():
        fork = repo_sect.sub('', sect)
        old_repo = ''
        if fork != sect and config.has_option(sect, 'forkof'):
            old_repo = config.get(sect, 'forkof')
        else:
            continue

        fork += '.git'
        fork = os.path.join(repositories, fork)
        old_repo += '.git'
        old_repo = os.path.join(repositories, old_repo)

        if not os.path.exists(old_repo):
            log.warning("original repository %s doesn't exist" % old_repo)
            continue
        
        log.debug("fork %s to %s" % (old_repo, fork))
        repository.fork(old_path=old_repo, new_path=fork)
