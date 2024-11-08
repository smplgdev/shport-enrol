## Šport UP enrollment tracker
This is a simple script that tracks the enrollment status of the Šport UP events and notifies the user when the event is open for enrollment.

### How to run:
1. python -m venv venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. fill in the .env file
5. run telegram bot with command: `python main.py`
6. In the neighboring window run the command: `./run_celery.sh`

TODO:
- [x] Add tracking system
- [x] Add Telegram bot for notifications
- [x] Add database for storing events
- [x] Tracking events with Celery
- [ ] Multiple users support
- [ ] Extended management of events through Telegram bot