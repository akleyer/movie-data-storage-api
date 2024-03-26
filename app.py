"""Application entry point"""

import logging.config

logging.config.fileConfig('app/logging.cfg')

from app import app
from app.db import check_and_create_movies_table

if __name__ == '__main__':
    app.logger.info("Starting application...")
    check_and_create_movies_table()
    app.run(debug=True)
