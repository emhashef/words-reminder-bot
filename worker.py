from jobs.remind import start_reminding
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:

    start_reminding()
except KeyboardInterrupt:
    pass