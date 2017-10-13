import zlib
import tempfile
import json
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoderMonitor, MultipartEncoder
import sys
import logging


def zlib_compress(data, to):
    step = 4 << 20  # 4MiB
    c = zlib.compressobj()
    data = bytes(data, "utf-8")
    for i in range(0, len(data), step):
        to.write(c.compress(data[i:i + step]))

    to.write(c.flush())

def post_file(url, auth, json_string):
    f = tempfile.NamedTemporaryFile(mode='wb', prefix='tmp_promote_', delete=False)
    zlib_compress(json_string, f)
    logging.info('compressed bundle size: %s', sizeof_fmt(os.path.getsize(f.name)))
    f.close()

    files = {
        'bundle': open(f.name, 'rb')
    }

    try:
        # TODO: could do this?
        # r = requests.post(url=url, files=files, auth=auth, params={'language': 'python' })
        r = requests.post(url=url, files=files, auth=auth)
        if r.status_code != 200:
            r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if r.status_code > 200:
            responseText = r.text
            sys.stderr.write("\nDeployment error: " + responseText)
            return {"status": "error", "message": responseText}
        else:
            sys.stderr.write("\nError in HTTP connection")
            return {"status": "error", "message": "Error in HTTP connection."}
    except Exception as err:
        sys.stderr.write("\nDeployment error: " + str(err))
        return {"status": "error", "message": str(err)}
    rsp = r.text
    # clean up after we're done
    f.close()
    try:
        os.unlink(f.name)
    except:
        pass

    return rsp

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)