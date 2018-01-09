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

def post_file(url, auth, bundle, modelObjectsPath):

    if modelObjectsPath == '':
        modelObjectsFile = tempfile.NamedTemporaryFile(
            mode='wb', prefix='tmp_promote_', delete=False)
        modelObjectsPath = modelObjectsFile.name
        modelObjectsFile.close()
    
    # zlib_compress(modelObjects, modelObjectsFile)
    modelObjectsFile = open(modelObjectsPath, 'rb')
    size = sizeof_fmt(os.path.getsize(modelObjectsPath))
    logging.info('compressed model objects size: %s', size)

    files = {
        'model_objects': modelObjectsFile
    }

    try:
        r = requests.post(url=url, files=files, auth=auth, data=bundle)
        if r.status_code != 200:
            r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if r.status_code > 200:
            responseText = r.text
            sys.stderr.write("\nDeployment error: " + responseText)
            cleanupFile(modelObjectsFile)
            return {"status": "error", "message": responseText}
        else:
            sys.stderr.write("\nError in HTTP connection")
            cleanupFile(modelObjectsFile)
            return {"status": "error", "message": "Error in HTTP connection."}
    except Exception as err:
        sys.stderr.write("\nDeployment error: " + str(err))
        cleanupFile(modelObjectsFile)
        return {"status": "error", "message": str(err)}

    cleanupFile(modelObjectsFile)
    rsp = r.text
    return rsp

def cleanupFile(file):
    try:
        file.close()
        os.unlink(file.name)
    except:
        pass

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
