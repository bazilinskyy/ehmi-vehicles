# by Pavlo Bazilinskyy <p.bazilinskyy@tue.nl>
"""Run the analysis: optionally export the data from MongoDB, then build tables and figures."""
import os
import subprocess

import art as ar

ar.logs(show_level=ar.common.get_configs('logger_level'), show_color=True)
logger = ar.CustomLogger(__name__)  # use custom logger


if __name__ == '__main__':
    path_data = ar.common.get_configs('path_data')
    files_heroku = ar.common.get_configs('files_heroku')
    if ar.common.get_configs('download_data'):
        # export the collection into the first data file; the connection string stays in the secret file
        out = os.path.join(path_data, files_heroku[0])
        logger.info('Exporting data from MongoDB to {}.', out)
        subprocess.run(['mongoexport', '--uri', ar.common.get_secrets('mongodb_uri'), '--collection', 'entries',
                        '--type', 'json', '--out', out], check=True)
    ar.analysis.main(path_data, files_heroku)
