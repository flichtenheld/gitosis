import logging
import re
import os
import os.path

log = logging.getLogger('gitosis.heads')

from gitosis import util
from gitosis import repository

repo_sect = re.compile(r'^repo\s+')

def update_heads(config):
    repositories = util.getRepositoryDir(config)

    for sect in config.sections():
        repo = repo_sect.sub('', sect)
        if repo != sect and config.has_option(sect, 'default_branch'):
            head = config.get(sect, 'default_branch')
        else:
            continue

        repo += '.git'
        repo = os.path.join(repositories, repo)

        log.debug("set HEAD of %s to %s" % (repo, head))
        repository.setHEAD(path=repo,branch=head)
