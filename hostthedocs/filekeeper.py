import os
import zipfile

DEFAULT_PROJECT_DESCRIPTION = '<No project description>'


def _get_proj_dict(docfiles_dir, proj_dir, link_root):
    join = lambda *a: os.path.join(docfiles_dir, proj_dir, *a)
    allpaths = os.listdir(join())
    versions = [
        dict(version=p, link='%s/%s/%s/index.html' % (link_root, proj_dir, p))
        for p in allpaths if os.path.isdir(join(p))
    ]
    descr = DEFAULT_PROJECT_DESCRIPTION
    if 'description.txt' in allpaths:
        dpath = join('description.txt')
        with open(dpath) as f:
            descr = f.read().strip()
    return {'name': proj_dir, 'versions': versions, 'description': descr}


def parse_docfiles(docfiles_dir, link_root):
    if not os.path.exists(docfiles_dir):
        return {}

    result = [_get_proj_dict(docfiles_dir, f, link_root)
              for f in os.listdir(docfiles_dir)]

    return result


def unpack_project(zippath, proj_metadata, docfiles_dir):
    projdir = os.path.join(docfiles_dir, proj_metadata['name'])
    verdir = os.path.join(projdir, proj_metadata['version'])

    if not os.path.isdir(verdir):
        os.makedirs(verdir)

    descrpath = os.path.join(projdir, 'description.txt')
    with open(descrpath, 'w') as f:
        f.write(proj_metadata.get('description', DEFAULT_PROJECT_DESCRIPTION))

    zf = zipfile.ZipFile(zippath)
    # This is insecure, we are only accepting things from trusted sources.
    zf.extractall(verdir)
